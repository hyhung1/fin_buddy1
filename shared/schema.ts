import { pgTable, text, serial, integer, boolean, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

// Excel file related schemas
export const excelFiles = pgTable("excel_files", {
  id: serial("id").primaryKey(),
  filename: text("filename").notNull(),
  originalName: text("original_name").notNull(),
  fileSize: integer("file_size").notNull(),
  userId: integer("user_id"),
  uploadedAt: text("uploaded_at").notNull().default("CURRENT_TIMESTAMP"),
  metadata: jsonb("metadata")
});

export const insertExcelFileSchema = createInsertSchema(excelFiles).pick({
  filename: true,
  originalName: true,
  fileSize: true,
  userId: true,
  metadata: true
});

export type InsertExcelFile = z.infer<typeof insertExcelFileSchema>;
export type ExcelFile = typeof excelFiles.$inferSelect;

// Chat messages related schemas
export const chatMessages = pgTable("chat_messages", {
  id: serial("id").primaryKey(),
  fileId: integer("file_id").notNull(),
  role: text("role").notNull(), // "user" or "assistant"
  content: text("content").notNull(),
  timestamp: text("timestamp").notNull().default("CURRENT_TIMESTAMP")
});

export const insertChatMessageSchema = createInsertSchema(chatMessages).pick({
  fileId: true,
  role: true,
  content: true
});

export type InsertChatMessage = z.infer<typeof insertChatMessageSchema>;
export type ChatMessage = typeof chatMessages.$inferSelect;

// File analysis schema for Gemini AI interactions
export const FileAnalysisSchema = z.object({
  fileId: z.string().optional(),
  fileName: z.string().optional(),
  fileSize: z.number().optional(),
  sheets: z.array(z.object({
    name: z.string(),
    rowCount: z.number(),
    columnCount: z.number(),
    headers: z.array(z.string()).optional(),
    sampleData: z.record(z.string(), z.array(z.any())).optional()
  })),
  sheetNames: z.array(z.string()).optional(),
  activeSheet: z.string().optional(),
  summary: z.string().optional(),
  insights: z.array(z.string()).optional(),
  suggestedQuestions: z.array(z.string()).optional()
});

export type FileAnalysis = z.infer<typeof FileAnalysisSchema>;
