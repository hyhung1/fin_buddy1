import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import multer from "multer";
import path from "path";
import fs from "fs";
import axios from "axios";
import FormData from "form-data";
import { spawn } from "child_process";
import express from "express";

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB limit
  fileFilter: (req, file, cb) => {
    // Allow only CSV files now
    const allowedExtensions = ['.csv', '.xlsx', '.xls'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedExtensions.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Only CSV, XLSX, and XLS files are allowed'));
    }
  }
});

// Python FastAPI backend URL - Corrected Port
const PYTHON_API_URL = "http://127.0.0.1:5000"; // Use localhost and port 5000

export async function registerRoutes(app: Express): Promise<Server> {
  const httpServer = createServer(app);

  // Start the Python backend
  startPythonBackend();

  // Serve generated files (visualizations)
  const generatedFilesDir = path.resolve(process.cwd(), 'gen_scripts_csv_arti_v2_4');
  app.use('/generated-files', express.static(generatedFilesDir));
  
  // Log all requests to /generated-files for debugging
  app.use('/generated-files', (req, res, next) => {
    console.log(`[STATIC] Serving: ${req.path}`);
    next();
  });

  // --- NEW PROXY LOGIC for ADK Backend ---

  // Proxy /api/upload to Python backend
  // Handles both file and session_id form data
  app.post('/api/upload', upload.single('file'), async (req, res, next) => {
    try {
      if (!req.file) {
        return res.status(400).json({ message: 'No file uploaded' });
      }

      const formData = new FormData();
      formData.append('file', req.file.buffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype,
      });

      // Append session_id if present in the request body (from Form data)
      if (req.body.session_id) {
          formData.append('session_id', req.body.session_id);
      }

      const pythonResponse = await axios.post(`${PYTHON_API_URL}/api/upload`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });
      res.status(pythonResponse.status).json(pythonResponse.data);
    } catch (error: unknown) {
      console.error('[PROXY ERROR /api/upload]:', error);
       const axiosError = error as any; // Type assertion for potential Axios error
      if (axiosError.response) {
        // Forward error from Python backend if possible
        res.status(axiosError.response.status).json(axiosError.response.data);
      } else {
        // Generic server error if Python backend is unreachable or other error
        res.status(500).json({ message: 'Failed to process upload request.', detail: axiosError.message });
      }
    }
  });

  // Proxy /api/upload_v1 to Python backend
  app.post('/api/upload_v1', upload.single('file'), async (req, res, next) => {
    try {
      console.log('[API] Upload_v1 request received');
      
      if (!req.file) {
        return res.status(400).json({ message: 'No file uploaded' });
      }

      const formData = new FormData();
      formData.append('file', req.file.buffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype,
      });

      // Append session_id if present in the request body
      if (req.body.session_id) {
        formData.append('session_id', req.body.session_id);
      }

      console.log('[API] Forwarding upload_v1 request to Python backend (smart)');
      const pythonResponse = await axios.post(`${PYTHON_API_URL}/api/upload_v1`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });

      console.log('[API] Upload_v1 successful');
      res.status(pythonResponse.status).json(pythonResponse.data);
    } catch (error) {
      console.error('[PROXY ERROR /api/upload_v1]:', error);
      const axiosError = error as any;
      if (axiosError.response) {
        res.status(axiosError.response.status).json(axiosError.response.data);
      } else {
        res.status(500).json({ 
          message: 'Failed to process upload_v1 request.', 
          detail: axiosError.message 
        });
      }
    }
  });

  // Proxy /api/chat to Python backend
  // Expects JSON body: { message: string, session_id?: string }
  app.post('/api/chat', express.json(), async (req, res, next) => {
    try {
      console.log('[API] Chat request with session_id:', req.body.session_id);
      
      const pythonResponse = await axios.post(`${PYTHON_API_URL}/api/chat`, req.body, { // Forward JSON body
        headers: { 'Content-Type': 'application/json' }
      });

      return res.json(pythonResponse.data);
    } catch (error) {
      console.error('[PROXY ERROR /api/chat]:', error);
      const axiosError = error as any;
      if (axiosError.response) {
        res.status(axiosError.response.status).json(axiosError.response.data);
      } else {
        res.status(500).json({ message: 'Failed to process chat request.', detail: axiosError.message });
      }
    }
  });


  // Proxy /api/chat_v1 to Python backend
  // Expects JSON body: { message: string, session_id?: string }
  app.post('/api/chat_v1', express.json(), async (req, res, next) => {
    try {
      console.log('[API] Chat request with session_id:', req.body.session_id);
      
      const pythonResponse = await axios.post(`${PYTHON_API_URL}/api/chat_v1`, req.body, { // Forward JSON body
        headers: { 'Content-Type': 'application/json' }
      });

      return res.json(pythonResponse.data);
    } catch (error) {
      console.error('[PROXY ERROR /api/chat_v1]:', error);
      const axiosError = error as any;
      if (axiosError.response) {
        res.status(axiosError.response.status).json(axiosError.response.data);
      } else {
        res.status(500).json({ message: 'Failed to process chat request.', detail: axiosError.message });
      }
    }
  });

  // Add route to serve dashboard HTML files
  app.get('/dashboard/:filename', async (req, res) => {
    try {
      const { filename } = req.params;
      console.log(`[API] Serving dashboard file: ${filename}`);
      
      // Forward request to Python backend
      const pythonResponse = await axios.get(`${PYTHON_API_URL}/dashboard/${filename}`);
      
      // Set content type to HTML
      res.setHeader('Content-Type', 'text/html');
      res.send(pythonResponse.data);
    } catch (error) {
      console.error('[PROXY ERROR /dashboard]:', error);
      const axiosError = error as any;
      if (axiosError.response) {
        res.status(axiosError.response.status).json(axiosError.response.data);
      } else {
        res.status(500).json({ message: 'Failed to serve dashboard.', detail: axiosError.message });
      }
    }
  });

  // Proxy /api/upload_smart to Python backend
  app.post('/api/upload_smart', upload.single('file'), async (req, res, next) => {
    try {
      console.log('[API] Upload_smart request received');

      if (!req.file) {
        return res.status(400).json({ message: 'No file uploaded' });
      }

      const formData = new FormData();
      formData.append('file', req.file.buffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype,
      });

      console.log('[API] Forwarding upload_smart request to Python backend');
      const pythonResponse = await axios.post(`${PYTHON_API_URL}/api/upload_smart`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });

      console.log('[API] Upload_smart successful');
      res.status(pythonResponse.status).json(pythonResponse.data);
    } catch (error) {
      console.error('[PROXY ERROR /api/upload_smart]:', error);
      const axiosError = error as any;
      if (axiosError.response) {
        res.status(axiosError.response.status).json(axiosError.response.data);
      } else {
        res.status(500).json({ 
          message: 'Failed to process upload_smart request.', 
          detail: axiosError.message 
        });
      }
    }
  });

  // Optional: Proxy for fetching messages (if backend implements it)
  // app.get('/api/chat/messages/:sessionId', async (req, res) => {
  //   try {
  //     const { sessionId } = req.params;
  //     const pythonResponse = await axios.get(`${PYTHON_API_URL}/api/chat/messages/${sessionId}`);
  //     res.status(pythonResponse.status).json(pythonResponse.data);
  //   } catch (error: unknown) {
  //      console.error('[PROXY ERROR /api/chat/messages]:', error);
  //      const axiosError = error as any;
  //      // ... error handling ...
  //   }
  // });

  return httpServer;
}

// Function to start the Python backend
function startPythonBackend() {
  console.log('Starting Python FastAPI backend...');
  
  // Start the Python process - execute Python script directly
  const pythonProcess = spawn('python', ['python_backend/main.py']);
  
  // Log Python process output
  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python backend: ${data}`);
  });
  
  pythonProcess.stderr.on('data', (data) => {
    const output = data.toString();
    // Filter out LLM request guidelines
    if (output.includes('LLM Request:') || output.includes('System Instruction:') || 
        output.includes('FINANCIAL-PANDAS-EXPERT') || output.includes('Guidelines:')) {
      // Don't log these lines
      return;
    }
    
    // Check if the message is an INFO log rather than an actual error
    if (output.includes('INFO:')) {
      console.log(`Python backend: ${data}`);
    } else {
      console.error(`Python backend error: ${data}`);
    }
  });
  
  pythonProcess.on('close', (code) => {
    console.log(`Python backend process exited with code ${code}`);
  });
  
  // Handle Node.js process exit
  process.on('exit', () => {
    pythonProcess.kill();
  });
}
