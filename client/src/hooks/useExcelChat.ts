import { useState, useCallback, useRef, useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { FileAnalysis } from "@shared/schema";
import { apiRequest } from "@/lib/queryClient";
import { useQuery, useMutation, useQueryClient, UseMutationResult } from "@tanstack/react-query";

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  link?: string | null;
  fileAnalysis?: any;
  images?: string[];
}

// Define structure for backend responses
interface UploadResponse {
  session_id: string;
  file_id: string;
  file_name: string;
  headers: string[];
  message: string;
  analysis?: FileAnalysis | null;
}

interface ChatResponse {
  session_id: string;
  response: string;
  events?: any[];
  analysis?: FileAnalysis | null;
}

interface ChatResponseV1 {
  session_id: string;
  response: MessageV1;
  events?: any[];
  analysis?: FileAnalysis | null;
  images?: string[];
}

interface MessageV1 {
  content: string;
  is_link: boolean;
  link?: string;
  images?: string[];
}

// Define structure for mutation variables if needed
interface SelectSheetVariables {
  fileId: string;
  sheetName: string;
}

interface SendMessageVariables {
  message: string;
}

export function useExcelChat() {
  const [file, setFile] = useState<File | null>(null);
  const [fileMetadata, setFileMetadata] = useState<FileAnalysis | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isProcessingFile, setIsProcessingFile] = useState(false);

  // Each browser reload starts with a fresh sessionId (no persistence)
  const [sessionId, setSessionId] = useState<string | null>(null);

  const { toast } = useToast();
  const queryClient = useQueryClient();

  // Query to fetch messages - Use sessionId as key
  // Note: Backend needs a GET /api/chat/messages/{session_id} endpoint
  // For now, this query might not work as intended without backend changes.
  const { isLoading: isLoadingMessages } = useQuery({
    queryKey: ['/api/chat/messages', sessionId],
    enabled: !!sessionId,
    queryFn: async (): Promise<{ messages: ChatMessage[] }> => {
      console.warn("GET /api/chat/messages needs backend implementation for sessions");
      // Replace with actual fetch when backend endpoint exists
      // const response = await apiRequest('GET', `/api/chat/messages/${sessionId}`);
      // return response.json();
      return { messages: [] }; // Return empty for now
    },
    // Optional: Refetch on window focus or interval if needed
  });

  // Mutation to upload a file
  const uploadFileMutation: UseMutationResult<UploadResponse, Error, FormData> = useMutation<UploadResponse, Error, FormData>({
    mutationFn: async (formData: FormData): Promise<UploadResponse> => {
      if (sessionId) {
        console.log('[UPLOAD] Including existing session_id:', sessionId);
        formData.append('session_id', sessionId);
      } else {
        console.log('[UPLOAD] No existing session_id');
      }

      const response = await apiRequest('POST', '/api/upload_v1', formData);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Upload failed with non-JSON response' }));
        throw new Error(errorData.message || 'Upload failed');
      }

      const data = await response.json();
      console.log('[UPLOAD] Received session_id:', data.session_id);
      return data;
    },
    onSuccess: (data: UploadResponse): void => {
      console.log('[UPLOAD] Setting session_id:', data.session_id);
      setSessionId(data.session_id);
      setFileMetadata(data.analysis || null);
      setIsProcessingFile(false);

      const welcomeMessage = data.message || `Successfully processed ${data.file_name}.`;
      // Make sure the object structure matches ChatMessage
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: welcomeMessage,
        fileAnalysis: data.analysis // Pass analysis for potential display
      };
      setMessages((prev) => [...prev, assistantMessage]); // Start new message list

      // Invalidate based on session_id - might not be needed if GET isn't used
      // queryClient.invalidateQueries({ queryKey: ['/api/chat/messages', data.session_id] });
      toast({
        title: "File ready",
        description: `You can now ask questions about ${data.file_name}.`,
      });
    },
    onError: (error: Error): void => {
      setIsProcessingFile(false);
      toast({
        variant: "destructive",
        title: "Error uploading file",
        description: error.message || "Failed to upload CSV file",
      });
    }
  });

  // Mutation to select a specific sheet
  // WARNING: Backend needs verification for this functionality with ADK sessions
  const selectSheetMutation: UseMutationResult<any, Error, SelectSheetVariables> = useMutation<any, Error, SelectSheetVariables>({
    mutationFn: async ({ fileId, sheetName }: SelectSheetVariables): Promise<any> => {
      console.warn("selectSheetMutation needs backend verification with ADK sessions");
      // Assuming backend needs session_id and potentially fileId if multiple files per session allowed
      const formData = new FormData();
      formData.append('fileId', fileId); // Backend needs to interpret this within the session
      formData.append('sheetName', sheetName);
      if (sessionId) formData.append('session_id', sessionId);

      // Replace with actual API call if backend supports it
      // const response = await apiRequest('POST', '/api/excel/select-sheet', formData);
      // if (!response.ok) throw new Error('Failed to select sheet');
      // return response.json();
      return Promise.resolve({ success: false, message: "Sheet selection not implemented with current backend" });
    },
    onSuccess: (data: any): void => {
      if (!data.success) {
        toast({ variant: "destructive", title: "Sheet Selection Error", description: data.message });
        return;
      }
      // Update active sheet state if applicable
      // setFileMetadata(prev => prev ? { ...prev, activeSheet: data.sheetName } : null);
      toast({
        title: "Sheet Selected (If Implemented)",
        description: `Now analyzing sheet: ${data.sheetName}`,
      });
    },
    onError: (error: Error): void => {
      toast({
        variant: "destructive",
        title: "Error selecting sheet",
        description: error.message || "Failed to select sheet",
      });
    }
  });

  // Mutation to send a message
  const sendMessageMutation: UseMutationResult<ChatResponseV1, Error, SendMessageVariables> = useMutation<ChatResponseV1, Error, SendMessageVariables>({
    mutationFn: async ({ message }: SendMessageVariables): Promise<ChatResponseV1> => {
      const payload = {
        message: message,
        session_id: sessionId // Send the current session ID (can be null)
      };

      console.log('[CHAT] Sending message with session_id:', payload.session_id);

      const response = await apiRequest('POST', '/api/chat_v1', payload);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Failed to send message with non-JSON response' }));
        throw new Error(errorData.message || 'Failed to send message');
      }
      const data = await response.json();
      console.log('[CHAT] Received response with session_id:', data.session_id);
      return data;
    },
    onSuccess: (data: ChatResponseV1): void => {
      console.log('[CHAT] Updating session_id from:', sessionId, 'to:', data.session_id);
      setSessionId(data.session_id); // Always update session ID from response
      
      // Create assistant message with content, link, images and analysis
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: data.response.content,
        link: data.response.link,
        images: data.response.images || data.images, // Get images from either location
        fileAnalysis: data.analysis
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      setInputMessage('');
      // queryClient.invalidateQueries({ queryKey: ['/api/chat/messages', data.session_id] });
    },
    onError: (error: Error): void => {
      toast({
        variant: "destructive",
        title: "Error sending message",
        description: error.message || "Failed to get a response",
      });
    }
  });

  // Callbacks

  const handleFileUpload = useCallback((selectedFile: File): void => {
    setFile(selectedFile);
    setIsProcessingFile(true);
    // Keep existing messages unless requirement is to clear them
    // setMessages([]);
    setFileMetadata(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    uploadFileMutation.mutate(formData);
  }, [sessionId, uploadFileMutation]);

  const handleRemoveFile = useCallback((): void => {
    setFile(null);
    setFileMetadata(null);
    // Keep messages, let user continue chat without file context
    // setMessages([]);
    setInputMessage('');
    toast({ title: "File context removed", description: "You can continue chatting generally." });
    // Inform backend? Maybe not needed for InMemorySessionService
    // If backend needs update: call a mutation here
  }, [sessionId]);

  const handleSendMessage = useCallback((): void => {
    const trimmedMessage = inputMessage.trim();
    if (!trimmedMessage) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: trimmedMessage
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage(''); // Clear input immediately

    sendMessageMutation.mutate({ message: trimmedMessage });

  }, [inputMessage, sessionId, sendMessageMutation]);

  const handleExampleQuery = useCallback((query: string): void => {
    setInputMessage(query);
  }, []);

  const handleSelectSheet = useCallback((sheetName: string): void => {
    console.warn("handleSelectSheet needs adaptation for ADK backend");
    // Requires knowing the fileId associated with the current session or a way
    // for the backend to know which file context to use within the session.
    // This needs backend design confirmation.
    // if (sessionId && fileMetadata?.fileId) { // Assuming fileMetadata stores the relevant fileId
    //   selectSheetMutation.mutate({ fileId: fileMetadata.fileId, sheetName });
    // }
  }, [sessionId, fileMetadata, selectSheetMutation]);

  return {
    file,
    fileMetadata,
    messages,
    isLoading: uploadFileMutation.isPending || sendMessageMutation.isPending || selectSheetMutation.isPending || isProcessingFile || isLoadingMessages,
    inputMessage,
    setInputMessage,
    handleFileUpload,
    handleRemoveFile,
    handleSendMessage,
    handleExampleQuery,
    handleSelectSheet,
    isProcessingFile,
    // Determine fileUploaded status based on whether fileMetadata exists
    fileUploaded: !!fileMetadata
  };
}
