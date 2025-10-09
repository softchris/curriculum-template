/**
 * Core types for RAG system components
 */

/**
 * Configuration for Ollama connection and model settings
 */
export interface OllamaConfig {
  /** Base URL for Ollama API (default: http://localhost:11434) */
  baseUrl: string;
  /** Model name to use for text generation */
  model: string;
  /** Request timeout in milliseconds */
  timeout?: number;
}

/**
 * Options for text generation requests
 */
export interface GenerationOptions {
  /** Maximum tokens to generate */
  maxTokens?: number;
  /** Temperature for randomness (0.0 - 1.0) */
  temperature?: number;
  /** System prompt to set context */
  systemPrompt?: string;
  /** Whether to stream the response */
  stream?: boolean;
}

/**
 * Response from Ollama text generation
 */
export interface GenerationResponse {
  /** Generated text content */
  content: string;
  /** Model used for generation */
  model: string;
  /** Generation metadata */
  metadata: {
    /** Time taken for generation in milliseconds */
    generationTime: number;
    /** Number of tokens generated */
    tokensGenerated: number;
  };
}

/**
 * Error types that can occur during generation
 */
export interface GenerationError {
  /** Error type identifier */
  type: 'CONNECTION_ERROR' | 'MODEL_ERROR' | 'TIMEOUT_ERROR' | 'VALIDATION_ERROR';
  /** Human-readable error message */
  message: string;
  /** Original error details */
  details?: unknown;
}