import OpenAI from "openai";
import { FileAnalysis } from "@shared/schema";

// Initialize OpenAI client with API key from environment variables
const openai = new OpenAI({ 
  apiKey: process.env.OPENAI_API_KEY 
});

// the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
const MODEL = "gpt-4o";

/**
 * Analyze Excel data to provide insights
 */
export async function analyzeData(fileAnalysis: FileAnalysis): Promise<any> {
  try {
    const sheetsInfo = fileAnalysis.sheets.map(sheet => {
      return {
        name: sheet.name,
        rowCount: sheet.rowCount,
        columnCount: sheet.columnCount,
        headers: sheet.headers,
        sampleData: sheet.sampleData
      };
    });

    const prompt = `
      I have an Excel file with the following sheets:
      ${JSON.stringify(sheetsInfo, null, 2)}
      
      Please analyze this data and provide a brief summary of what kind of data this is, 
      what insights can be drawn from it, and what kinds of questions would be valuable to ask about it.
      Format your response as JSON with the following structure: 
      { "summary": "...", "dataType": "...", "possibleInsights": ["...", "..."], "suggestedQuestions": ["...", "..."] }
    `;

    const response = await openai.chat.completions.create({
      model: MODEL,
      messages: [
        {
          role: "system",
          content: "You are an Excel data analysis expert. Analyze the Excel file data and provide insights."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      response_format: { type: "json_object" }
    });

    const result = JSON.parse(response.choices[0].message.content);
    return result;
  } catch (error) {
    console.error("OpenAI analysis error:", error);
    throw new Error("Failed to analyze Excel data");
  }
}

/**
 * Generate a response to a user query about the Excel data
 */
export async function generateResponse(
  userQuery: string, 
  fileAnalysis: FileAnalysis
): Promise<{ content: string; analysis?: any }> {
  try {
    const sheetsInfo = fileAnalysis.sheets.map(sheet => {
      return {
        name: sheet.name,
        rowCount: sheet.rowCount,
        columnCount: sheet.columnCount,
        headers: sheet.headers,
        sampleData: sheet.sampleData
      };
    });

    const prompt = `
      I have an Excel file with the following sheets:
      ${JSON.stringify(sheetsInfo, null, 2)}
      
      User question: "${userQuery}"
      
      Please answer the question based on the data available. If the information needed to answer 
      the question is not available in the data provided, please explain why and suggest what information 
      would be needed.
      
      If your answer includes calculations or data from specific columns, please format it as a table 
      when appropriate. 
      
      Return your response in JSON format with the following structure:
      {
        "answer": "Your detailed answer to the user's question",
        "tableData": {
          "headers": ["Column 1", "Column 2", ...],
          "rows": [
            ["Value 1", "Value 2", ...],
            ...
          ]
        }
      }
      
      If no table is needed, you can omit the tableData field.
    `;

    const response = await openai.chat.completions.create({
      model: MODEL,
      messages: [
        {
          role: "system",
          content: "You are an Excel data analysis expert. Answer questions about Excel data clearly and concisely."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      response_format: { type: "json_object" }
    });

    const result = JSON.parse(response.choices[0].message.content);
    
    return {
      content: result.answer,
      analysis: result.tableData ? { tableData: result.tableData } : undefined
    };
  } catch (error) {
    console.error("OpenAI response generation error:", error);
    throw new Error("Failed to generate response to your question");
  }
}
