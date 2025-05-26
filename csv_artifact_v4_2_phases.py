from __future__ import annotations

import asyncio
import datetime
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple, Dict, Any

import pandas as pd  # noqa: F401
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import google.genai.types as types

# -----------------------------------------------------------------------------
# System prompt used by the financial data analysis agent (LLM)
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are **FINANCIAL-PANDAS-EXPERT**, an expert financial data analyst. Please follow the guidelines to answer the user's question.

Guidelines:
1. A CSV dataset will be supplied at runtime and has already been loaded into a pandas DataFrame called `df`.
2. **STRICTLY FORBIDDEN:** **Do NOT** write or suggest any SQL or SQL-like syntax (e.g., `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `INSERT`, `UPDATE`, `DELETE`, etc.). Every task must be solved exclusively with pandas. If a solution somehow seems to require SQL, explicitly state that you cannot use SQL rather than writing any SQL snippet.
3. The dataset is already fully loaded into an in-memory pandas DataFrame (`df`). There is **NO** SQL engine or database connection available, so any SQL would be meaningless and will fail.
4. Work **directly** with the in-memory DataFrame (`df`) supplied at runtime.
   • **NEVER** call any data-loading utilities (`pd.read_csv`, `pd.read_excel`, `pd.read_parquet`, `io.StringIO`, etc.).
   • **NEVER** hard-code a file path or reference the CSV on disk.
   • **NEVER** reassign or overwrite `df`—assume it already exists.
   Use only pandas operations on this existing DataFrame.
5. Pay close attention to the **column names** of the DataFrame – they may contain newline characters and/or extra spaces. **Cell values, however, are already clean**: they have **no leading or trailing whitespace or newline characters**. Therefore, when filtering or comparing by value (e.g., sector names ), use the plain string **without** any extra whitespace.
6. **ABSOLUTELY FORBIDDEN:** Never embed or reproduce any portion of the CSV data (raw rows, sample rows, or header text) inside the answer.  
   • Do **NOT** create multi-line strings or variables that contain CSV text.  
   • Do **NOT** construct a DataFrame manually with hard-coded data.  
   • Do **NOT** use `import io` / `io.StringIO` to wrap inline CSV snippets.  
   Always start from the already-loaded in-memory DataFrame `df`.
7. Respond with **one and only one** fenced Python code block containing the solution.
8. Treat each question **independently**:
   - Assume no variables or results from previous questions exist.
   - Never reuse variable names from prior answers.
9. Do **NOT** rename, duplicate, or otherwise alter `df.columns`:
   • No `.str.strip()`, `.str.replace()`, `.rename()`, or similar methods.
   • Do **NOT** create duplicate "alias" columns with cleaned names.
   Always reference each column exactly as it appears in the original dataset.
10. End your code with one or more `print()` statements that output the final answer. 
   - If the answer is a scalar value, simply `print(value)`.
   - If the answer is a Series or DataFrame, print the relevant identifier(s) together with their numeric value(s), rounding **all numeric outputs** to two decimal places. For example:
      • Regular number: `print(f"{result.index[0]}: {result.iloc[0]:.2f}")`
      • Percentage: `print(f"{result.index[0]}: {result.iloc[0]:.2f}%")`
      Loop over multiple rows when necessary.
11. For any ranking-style questions (*highest*, *lowest*, *maximum*, *minimum*, *top N* etc.), your printed output **must** include both the key identifier (e.g., company, sector, year, category) **and** the corresponding metric value(s).
12. If a question specifies a time period (e.g., 'from Year to Year' or 'between Year1 and Year2'), ensure your output includes the requested metric for *each year* within that period. For example, if asked for 'Net Profit of Company X from 2019 to 2021', the output should show the Net Profit for Company X for 2019, 2020, and 2021 separately.
13. For questions involving multiple calculation steps or conditions, structure your code by breaking the problem into clear, sequential pandas operations. Use intermediate variables to store results of these steps before producing the final output.
14. Refer to the Business Rules and Definitions section below for how to decompose and answer multi-step queries.
15. When iterating over rows, **do NOT** use `DataFrame.itertuples()` (or the named/unnamed variant). Instead, use `iterrows()` or other pandas-safe approaches that preserve column names to avoid tuple-index errors.
16. Understand the difference between a **DataFrame** and a **Series**:
    • `iterrows()` is valid **only for DataFrames**.
    • If you need to loop over a Series (e.g., after `groupby(...).sum()`), use `.items()` (or its alias `.iteritems()`) , **never** `.iterrows()`.
17. Keep any **helper or derived columns** you create (for rankings, aggregations, intermediate calculations, etc.) in the DataFrame **through every step that relies on them**:
   • If you later sort, filter, or group by such a column, make sure it is still present (include it in any column subsets like `df[cols]`).
   • Only drop or exclude helper columns after **all** dependent operations are complete to avoid `KeyError` problems.
   • When creating column subsets or temporary DataFrames, ensure those helper columns stay included while they are needed.
   • Drop helper columns only after all downstream operations referencing them are done to avoid missing-column errors.
18. For "top-N per group" tasks, avoid patterns that trigger `DeprecationWarning` or duplicate columns:
      • Prefer `df.groupby(key, group_keys=False).apply(lambda g: g.nlargest(N, metric))` **without** an extra `reset_index` call.
      • Or sort within each group and use `groupby.head(N)`.
      • If you must call `reset_index`, pass `drop=True` **and** ensure the column you are resetting is **not** still present in the DataFrame (to avoid `ValueError: cannot insert … already exists`).
19. Do **not** pass unsupported keyword arguments (e.g., `skipna`) to `GroupBy.sum()`/`mean()`/`agg()`. The default behaviour already skips `NaN`s.

Business Rules and Definitions:
• For complex, multi-step questions (e.g., nested rankings, calculations that depend on intermediate results), solve them by sequentially computing intermediate DataFrame(s) and reuse them in later steps. Comment each step and store outputs in descriptive variables (e.g., `step1_result`, `filtered_df`, `final_ranking`).
• The dataset **does not include** a ready-made "Parent Equity" column:
   - Value in Parent Equity = Value in column Owner Equity - Value in column Minority Interests.
• When a question refers to a specific company by its ticker, always filter rows using the **'Ticker\n'** column—not by company name.

"""

# -----------------------------------------------------------------------------
# Instruction suffix appended to phase-2 LLM prompts (plotting request)
# -----------------------------------------------------------------------------
PHASE2_INSTRUCTION = f"""
Write a **stand-alone** Python script that uses *matplotlib* to visualise the data shown above.

Inside the script:
• Define the data explicitly (e.g., Python lists or a small DataFrame)—**do NOT** load any external files or reference *df*.
• After creating the plot, always add subtle horizontal grid lines for readability using the pattern:
    `plt.grid(True, axis='y', linestyle='--', alpha=0.8)`
• Make the chart title, both axis labels, **and x-axis tick labels** bold. Use a slightly larger font size (e.g., `fontsize=12`) for all of them to improve readability.
• If the data contains multiple series (e.g., several sectors, companies, or years), plot **all of them in the *same* figure**—use grouped bars, multiple lines, or another appropriate single-chart visual; do **not** generate separate figures for each series.
• If the question targets **all companies**, treat each company as its own series and include **every company** in that single plot.
• If the question involves **multiple distinct metrics or trends**, generate **one separate figure for each metric/trend** (do not combine them into subplots). Save each figure as its own PNG image file.
• Do **NOT** annotate the chart with the underlying numeric values; the visual alone is sufficient.

The script must perform these steps in order:
1) import the required libraries,
2) build the data structure,
3) generate the plot(s) with bold title, bold axis labels, and bold x-tick labels using a larger font size, following the multi-series and multi-metric rules above,
4) add the grid lines as specified above to every plot,
5) save **each** figure as a separate PNG image.

Return the complete script inside **one** Python code block only.
"""

class FinancialDataAnalysisApp:
    """Async-ready, pandas-only data analysis app with auto-code export."""

    APP_NAME = "data_visualization_dashboard"
    CSV_FILE = "excel_files/sample_2023Q4_v2.csv"
    MODEL_ID = "gemini-2.5-flash-preview-04-17"
    
    _SQL_PATTERN = re.compile(r"\b(SELECT|FROM|JOIN|INSERT|UPDATE|DELETE)\b", re.I)
    _PY_BLOCK = re.compile(r"```(?:python)?\s*(.*?)```", re.S | re.I)

    DEFAULT_IMPORTS_AND_SETUP = (
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "from pathlib import Path\n"
        "df = pd.read_csv(r\"{csv_full_path}\")\n"
        "# Make cleaned aliases for columns (whitespace variants) so any reference works\n"
        "orig_cols = df.columns.tolist()\n"
        "strip_cols = pd.Series(orig_cols).str.strip().tolist()\n"
        "collapsed_cols = (pd.Series(orig_cols)\n"
        "                 .str.replace(r\"\\s+\", \" \", regex=True)\n"
        "                 .str.strip()\n"
        "                 .tolist())\n"
        "for orig, s, c in zip(orig_cols, strip_cols, collapsed_cols):\n"
        "    if s not in orig_cols and s not in df.columns:\n"
        "        df[s] = df[orig]\n"
        "    if c not in orig_cols and c not in df.columns:\n"
        "        df[c] = df[orig]\n"
        "# Remove duplicate columns if any\n"
        "df = df.loc[:, ~df.columns.duplicated()]\n"
        "pd.set_option('display.float_format', '{{:,.0f}}'.format)\n\n"
    )

    def __init__(self) -> None:
        load_dotenv()
        self._artifact_service = InMemoryArtifactService()
        self._session_service = InMemorySessionService()

        # Generate random IDs
        random_suffix = f"{random.randint(0, 999999):06d}"
        self.user_id = f"user_{random_suffix}"
        self.session_id = random_suffix # Session ID is just the 6 random digits

        self._session_service.create_session(
            app_name=self.APP_NAME,
            user_id=self.user_id, # Use instance attribute
            session_id=self.session_id, # Use instance attribute
        )
        self._agent = Agent(
            name="financial_data_analysis_agent",
            model=self.MODEL_ID,
            description="Pandas-only analyst. Absolutely no SQL allowed.",
            instruction=SYSTEM_PROMPT,
        )
        self._runner = Runner(
            agent=self._agent,
            app_name=self.APP_NAME,
            session_service=self._session_service,
            artifact_service=self._artifact_service,
        )

    @classmethod
    def _contains_sql(cls, text: str) -> bool:
        return bool(cls._SQL_PATTERN.search(text))

    @classmethod
    def _extract_python_block(cls, text: str) -> str | None:
        match = cls._PY_BLOCK.search(text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _slugify(text: str) -> str:
        return re.sub(r"[^0-9a-zA-Z]+", "_", text.lower()).strip("_")[:60]

    def _callback_context(self) -> CallbackContext:
        return CallbackContext(
            InvocationContext(
                invocation_id="invoke-id",
                session=self._session_service.get_session(
                    app_name=self.APP_NAME,
                    user_id=self.user_id, # Use instance attribute
                    session_id=self.session_id, # Use instance attribute
                ),
                agent=self._agent,
                session_service=self._session_service,
                artifact_service=self._artifact_service,
            )
        )

    def _upload_csv(self, ctx: CallbackContext, path: Path) -> Tuple[float, List[str]]:
        start_time = time.perf_counter()
        df = pd.read_csv(path, nrows=2)
        data = df.to_csv(index=False).encode('utf-8')
        part = types.Part(inline_data=types.Blob(data=data, mime_type="text/csv"))
        ctx.save_artifact(filename=path.name, artifact=part)
        elapsed = time.perf_counter() - start_time
        self._log(f"Uploaded first 2 rows of CSV: {path.name} in {elapsed:.2f}s")
        return elapsed, df.columns.tolist()

    def _prime_agent(self, ctx: CallbackContext) -> None:
        # The artifact was saved with only the base filename (Path.name),
        # so we must look it up the same way even if CSV_FILE contains folders.
        artifact = ctx.load_artifact(filename=Path(self.CSV_FILE).name)
        if not artifact or not artifact.inline_data:
            raise FileNotFoundError(self.CSV_FILE)

        msg = types.Content(
            role="user",
            parts=[
                types.Part(text="Here is the dataset. Please load it into a pandas DataFrame (in python) called df."),
                types.Part(inline_data=artifact.inline_data),
            ],
        )
        events = self._runner.run(
            user_id=self.user_id, # Use instance attribute
            session_id=self.session_id, # Use instance attribute
            new_message=msg,
        )
        for e in events:
            if e.is_final_response():
                break

    async def _ask(self, question: str) -> str:
        msg = types.Content(role="user", parts=[types.Part(text=question)])
        events = self._runner.run(
            user_id=self.user_id, # Use instance attribute
            session_id=self.session_id, # Use instance attribute
            new_message=msg,
        )
        for e in events:
            if e.is_final_response():
                return e.content.parts[0].text
        return "(no response)"

    async def _handle_questions(self, questions: List[str], csv_full_path: Path, columns_list: List[str]) -> Dict[str, Any]:
        """Two-phase workflow.

        Phase 1 – Ask LLM for pandas analysis code (NO plots) that prints the
        answer.  The script is generated, saved, and executed immediately so we
        can capture the printed output.

        Phase 2 – Feed the captured *output* (NOT the analysis code) back to the
        LLM and ask for a standalone matplotlib script that visualises the data
        contained in the output.  The visualisation script is saved in its own
        folder (e.g. *ques_1_phase_2*).  Only these phase-2 scripts are returned
        for downstream execution (the phase-1 scripts have already run).
        """
        overall_start = time.perf_counter()

        # ------------------------------------------------------------------
        # Create one root folder for this run
        # ------------------------------------------------------------------
        ts = datetime.datetime.now()
        run_root = Path("gen_scripts_csv_arti_v2_4") / ts.strftime("generated_%Y%m%d_%H%M%S")
        run_root.mkdir(parents=True, exist_ok=True)
        self._log(f"Run artifacts will be saved to: {run_root.resolve()}")

        # For bookkeeping
        llm_call_details: List[Dict[str, Any]] = []
        total_llm_time = 0.0
        phase2_scripts: List[Tuple[Path, str]] = []  # (folder, filename)

        # Iterate over questions ------------------------------------------------
        for q_idx, question in enumerate(questions, start=1):
            q_prefix = f"ques_{q_idx}"
            self._log(f"\n============= Processing {q_prefix} =============")

            # ------------------------------ PHASE 1 -----------------------------
            phase1_prompt = (
                f"The available columns in the DataFrame are: {columns_list}.\n"
                f"{question}\n"
                "Use only these columns for your analysis. If you need to select a company (e.g., 'FPT'), "
                "filter on the 'Ticker\n' column. Produce pandas code that answers the question and *prints* the result. "
                "Do NOT include any plotting code."
            )
            t0 = time.perf_counter()
            answer = await self._ask(phase1_prompt)
            t_llm = time.perf_counter() - t0
            total_llm_time += t_llm
            llm_call_details.append({"q": question, "phase": "analysis", "sec": t_llm})

            # Enforce pandas-only (no SQL) -------------------------------------------------
            if self._contains_sql(answer):
                self._log("SQL detected – requesting rewrite…")
                t0 = time.perf_counter()
                answer = await self._ask(
                    "Rewrite using pandas only (NO SQL). Ensure the code prints the final answer."
                )
                t_llm = time.perf_counter() - t0
                total_llm_time += t_llm
                llm_call_details.append({"q": question, "phase": "rewrite_no_sql", "sec": t_llm})

            phase1_code = self._extract_python_block(answer) or answer.strip()
            if not phase1_code:
                self._log(f"[PHASE-1] LLM returned empty code for {q_prefix}. Skipping.")
                continue

            # Save PHASE-1 script ----------------------------------------------------------
            phase1_script_name = f"{q_prefix}_phase_1.py"
            phase1_script = run_root / phase1_script_name
            phase1_script.write_text(
                self.DEFAULT_IMPORTS_AND_SETUP.format(csv_full_path=csv_full_path)
                + phase1_code + "\n",
                encoding="utf-8",
            )
            self._log(f"[PHASE-1] Saved analysis script: {phase1_script.name}")

            # Execute PHASE-1 script to capture stdout ------------------------------------
            try:
                proc = subprocess.run(
                    [sys.executable, phase1_script.name],
                    cwd=run_root,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                analysis_output = proc.stdout.strip()
                self._log(f"[PHASE-1] Output:\n{analysis_output}")
            except subprocess.CalledProcessError as e:
                self._log(f"[PHASE-1] Script error (return-code={e.returncode}). Skipping this question.")
                analysis_output = (e.stdout or "") + "\n" + (e.stderr or "")
                continue  # Cannot proceed to phase-2 without clean output

            # ------------------------------ PHASE 2 -----------------------------
            # To keep the prompt lightweight, feed the model ONLY the plain text
            # output from phase-1 (no code, no extra context).  If the output is
            # extremely long, truncate to avoid hitting context limits.
            max_chars = 4000
            trimmed_output = (analysis_output[:max_chars] + "…") if len(analysis_output) > max_chars else analysis_output

            phase2_prompt = f"{trimmed_output}\n\n" + PHASE2_INSTRUCTION
            t0 = time.perf_counter()
            phase2_answer = await self._ask(phase2_prompt)
            t_llm = time.perf_counter() - t0
            total_llm_time += t_llm
            llm_call_details.append({"q": question, "phase": "plot_script", "sec": t_llm})

            phase2_code = self._extract_python_block(phase2_answer) or phase2_answer.strip()
            if not phase2_code:
                self._log(f"[PHASE-2] LLM returned empty code for {q_prefix}. Skipping plot script.")
                continue

            # Save PHASE-2 script in its own folder ---------------------------------------
            phase2_folder = run_root / f"{q_prefix}_phase_2"
            phase2_folder.mkdir(parents=True, exist_ok=True)
            phase2_script_name = "plot.py"
            (phase2_folder / phase2_script_name).write_text(phase2_code + "\n", encoding="utf-8")
            self._log(f"[PHASE-2] Saved plot script to {phase2_folder / phase2_script_name}")

            phase2_scripts.append((phase2_folder, phase2_script_name))

        # ------------------------------------------------------------------
        elapsed_total = time.perf_counter() - overall_start
        self._log(f"Completed two-phase generation in {elapsed_total:.1f}s ({elapsed_total/60:.1f} min)")

        return {
            "scripts_to_run": phase2_scripts,
            "script_gen_and_processing_time": elapsed_total,
            "total_llm_time": total_llm_time,
            "llm_calls_details": llm_call_details,
            "output_folder_name": str(run_root),
        }

    def run_flow(self, questions: List[str]) -> Dict[str, Any]:
        overall_start_time = time.perf_counter()
        self._log(f"Starting financial data analysis flow for user: {self.user_id}, session: {self.session_id}")

        csv_full_path = Path(self.CSV_FILE).expanduser().resolve()
        if not csv_full_path.exists():
            raise FileNotFoundError(f"CSV file not found at resolved path: {csv_full_path}")

        ctx = self._callback_context()
        
        upload_duration, columns_list = self._upload_csv(ctx, csv_full_path)

        prime_start_time = time.perf_counter()
        self._prime_agent(ctx)
        prime_duration = time.perf_counter() - prime_start_time
        self._log(f"Agent priming took {prime_duration:.2f}s")
        
        self._log(f"Starting to handle {len(questions)} questions and generate scripts...")
        handle_questions_results = asyncio.run(
            self._handle_questions(questions, csv_full_path=csv_full_path, columns_list=columns_list)
        )
        
        scripts_to_run = handle_questions_results["scripts_to_run"]
        output_folder_name = handle_questions_results["output_folder_name"]

        if scripts_to_run:
            self._log(f"Executing {len(scripts_to_run)} plot script(s) from '{output_folder_name}' …")
            for idx, (folder_path, script_name) in enumerate(scripts_to_run, start=1):
                script_path = folder_path / script_name
                self._log(f"  [{idx}/{len(scripts_to_run)}] Running {script_path.relative_to(folder_path.parent)}")
                try:
                    proc = subprocess.run(
                        [sys.executable, script_name],
                        cwd=folder_path,
                        text=True,
                        capture_output=True,
                        check=True,
                    )
                    if proc.stdout:
                        self._log(proc.stdout.strip())
                    if proc.stderr:
                        self._log(f"    [stderr] {proc.stderr.strip()}")
                except subprocess.CalledProcessError as e:
                    self._log(f"    Error (return code {e.returncode}) while executing {script_name}")
                    if e.stdout:
                        self._log(e.stdout.strip())
                    if e.stderr:
                        self._log(e.stderr.strip())
        else:
            self._log("No plot scripts were generated.")

        overall_duration = time.perf_counter() - overall_start_time
        self._log(f"Total financial data analysis flow completed in {overall_duration:.2f}s ({overall_duration/60:.2f} min)")
        
        return {
            "overall_duration": overall_duration,
            "upload_duration": upload_duration,
            "prime_duration": prime_duration,
            "script_gen_and_processing_time": handle_questions_results["script_gen_and_processing_time"],
            "total_llm_time": handle_questions_results["total_llm_time"],
            "llm_calls_details": handle_questions_results["llm_calls_details"],
            "output_folder_name": output_folder_name,
            "user_id": self.user_id,
            "session_id": self.session_id
        }

    # ---------------------------------------------------------------------
    # Utility logging helper
    # ---------------------------------------------------------------------

    @staticmethod
    def _log(message: str) -> None:
        """Print a message prefixed with the current HH:M:S timestamp."""
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] {message}")


if __name__ == "__main__":
    FinancialDataAnalysisApp().run_flow([
        "What are top 3 sectors that has good net profit from 2019 to 2023",
        "Find top 3 companies in each sector with highest net profit, after that give me their net profit and Parent Equity from 2019 to 2023",
        # "What is the Parent Equity of HPG, KBC, LHG, FPT, MSN, NVL from 2019 to 2023?",
        # "How about their net profit from 2019 to 2023?",
        # "Give me top 5 sectors with highest net profit from 2019 to 2023?",
        # "Within Oil & Gas, which are the top 5 companies by total net profit from 2019 to 2023?"

        # "What is net profit of VCB in 2019?",
        # "What is the net sales for year 2019 to 2023 of FPT?",
    ])