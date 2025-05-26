# Financial Analysis Buddy 📊

A powerful AI-driven financial data analysis tool that combines the intelligence of Google's Gemini AI with pandas data processing to provide comprehensive financial insights from your CSV and Excel files.

## 🌟 Features

- **Smart File Upload**: Support for both CSV and Excel files with automatic header detection
- **AI-Powered Analysis**: Uses Google Gemini AI to understand and analyze financial data
- **Interactive Chat Interface**: Ask questions about your data in natural language
- **Automated Visualization**: Generates matplotlib charts and graphs automatically
- **Two-Phase Processing**: 
  - Phase 1: Data analysis with pandas
  - Phase 2: Automatic visualization generation
- **Business Rules Engine**: Customizable business logic for financial calculations
- **Real-time Results**: Fast processing with live chat interface
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS

## 🏗️ Architecture

This application uses a hybrid architecture:

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend API**: Node.js + Express + TypeScript
- **AI Processing**: Python + FastAPI + Google Gemini AI
- **Data Processing**: Pandas + Matplotlib
- **Database**: Drizzle ORM with PostgreSQL support

## 📋 Prerequisites

Before running this application, ensure you have:

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **npm** or **yarn**
- **Google AI API Key** (for Gemini AI integration)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fin_buddy
```

### 2. Environment Setup

Create a `.env` file in the root directory and add your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

**⚠️ Important**: You must obtain a Google AI API key from [Google AI Studio](https://aistudio.google.com/) and add it to your `.env` file as `GOOGLE_API_KEY=your_key_here`.

### 3. Install Dependencies

#### Install Node.js Dependencies
```bash
npm install
```

#### Install Python Dependencies
```bash
# Using uv (recommended - uses pyproject.toml)
uv sync

# Or using pip (uses requirements.txt)
pip install -r requirements.txt
```

### 4. Start the Development Server

#### Option 1: Using the Batch Script (Windows)
```bash
./start_dev.bat
```

#### Option 2: Manual Start
```bash
# Terminal 1: Start Python Backend
cd python_backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Start Node.js Server (in project root)
npm run dev
```

### 5. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
fin_buddy/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Main application pages
│   │   ├── hooks/          # Custom React hooks
│   │   └── lib/            # Utility libraries
│   └── index.html
├── server/                 # Node.js Express server
│   ├── routes.ts           # API routes
│   ├── index.ts            # Server entry point
│   └── services/           # Server services
├── python_backend/         # Python FastAPI backend
│   ├── main.py             # FastAPI application
│   ├── financial_data_analysis_app.py  # Core AI analysis
│   ├── services/           # Python services
│   └── uploads/            # File upload directory
├── shared/                 # Shared utilities
├── gen_scripts_csv_arti_v2_4/  # Generated analysis scripts
├── package.json            # Node.js dependencies
├── pyproject.toml          # Python dependencies
└── .env                    # Environment variables (create this)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required: Google AI API Key
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Database configuration (if using PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Optional: Development settings
NODE_ENV=development
```

### Business Rules

The application includes a customizable business rules engine. Default rules include:

- **Parent Equity Calculation**: `Parent Equity = Owner Equity - Minority Interests`
- Custom financial formulas and definitions can be added through the UI

## 📊 Usage

### 1. Upload Your Data

- Click "Upload File" in the sidebar
- Select a CSV or Excel file containing financial data
- The system will automatically detect headers and process the file

### 2. Ask Questions

Use natural language to query your data:

- "What is the net profit for 2023?"
- "Show me the top 5 companies by revenue"
- "Compare quarterly performance across sectors"
- "What are the profit margins by company?"

### 3. View Results

The system provides:
- **Text Analysis**: Detailed numerical results
- **Visualizations**: Automatically generated charts and graphs
- **Interactive Chat**: Follow-up questions and clarifications

## 🛠️ Development

### Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server

# Database
npm run db:push      # Push database schema changes

# Type Checking
npm run check        # Run TypeScript type checking
```

### Python Backend Scripts

```bash
# Start FastAPI server
cd python_backend
uvicorn main:app --reload --port 8000

# Run standalone analysis
python csv_artifact_v4_2_phases.py
```

## 🔍 API Endpoints

### File Upload
- `POST /api/upload_v1` - Upload and process CSV/Excel files

### Chat Interface
- `POST /api/chat_v1` - Send analysis questions and receive AI responses

### Static Files
- `GET /static/*` - Serve generated analysis scripts and visualizations
- `GET /images/*/*` - Serve generated chart images

## 🧪 Example Queries

The application excels at financial data analysis. Try these example queries:

1. **Profitability Analysis**
   - "What is the net profit margin for each company?"
   - "Which sectors have the highest profitability?"

2. **Trend Analysis**
   - "Show revenue growth from 2020 to 2023"
   - "Compare quarterly performance trends"

3. **Comparative Analysis**
   - "Rank companies by total assets"
   - "Which company has the best debt-to-equity ratio?"

4. **Custom Calculations**
   - "Calculate parent equity for all companies"
   - "Show return on equity by sector"

## 🔒 Security Notes

- API keys are stored in environment variables
- File uploads are processed securely
- Generated scripts are sandboxed
- No sensitive data is logged

## 🐛 Troubleshooting

### Common Issues

1. **Missing Google API Key**
   ```
   Error: API key not found
   Solution: Add GOOGLE_API_KEY to your .env file
   ```

2. **Python Dependencies**
   ```
   Error: Module not found
   Solution: Run `uv sync` or `pip install -r requirements.txt`
   ```

3. **Port Conflicts**
   ```
   Error: Port already in use
   Solution: Check if ports 5000 or 8000 are available
   ```

### Debug Mode

Enable debug logging by setting:
```env
LOG_LEVEL=debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language understanding
- **Pandas** for robust data processing
- **Matplotlib** for visualization capabilities
- **React** and **TypeScript** for the modern frontend
- **FastAPI** for the efficient Python backend

## 📞 Support

For support and questions:
- Check the troubleshooting section above
- Review the example queries
- Ensure your `.env` file contains the required `GOOGLE_API_KEY`

---

**Note**: This application requires a valid Google AI API key to function. Please ensure you have obtained one from [Google AI Studio](https://aistudio.google.com/) and added it to your `.env` file as `GOOGLE_API_KEY=your_key_here` before running the application. 