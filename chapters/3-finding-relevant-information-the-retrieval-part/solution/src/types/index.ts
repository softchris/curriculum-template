export interface DocumentChunk {
  id: string;
  content: string;
  source: string;
  metadata: ChunkMetadata;
  embedding?: number[];
}

export interface ChunkMetadata {
  position: number;
  wordCount: number;
  characterCount: number;
  chunkIndex: number;
  keywords?: string[];
  tfIdfScores?: Map<string, number>;
}

export interface SearchQuery {
  text: string;
  filters?: SearchFilters;
  options?: SearchOptions;
}

export interface SearchFilters {
  source?: string;
  minWordCount?: number;
  maxWordCount?: number;
  keywords?: string[];
}

export interface SearchOptions {
  maxResults?: number;
  similarityThreshold?: number;
  includeEmbeddings?: boolean;
  algorithm?: SimilarityAlgorithm;
}

export interface SearchResult {
  chunk: DocumentChunk;
  score: number;
  similarity: SimilarityScore;
  highlights?: string[];
  explanation?: string;
}

export interface SimilarityScore {
  overall: number;
  keyword: number;
  semantic?: number;
  algorithm: SimilarityAlgorithm;
}

export interface RetrievalConfig {
  similarityThreshold: number;
  maxResults: number;
  embeddingModel?: string;
  ollamaBaseUrl?: string;
}

export interface EmbeddingResponse {
  embedding: number[];
  model: string;
  metadata: {
    dimension: number;
    processingTime: number;
  };
}

export interface TextAnalysis {
  wordCount: number;
  uniqueWords: number;
  keywords: string[];
  termFrequency: Map<string, number>;
  tfIdfScores: Map<string, number>;
}

export type SimilarityAlgorithm = 'cosine' | 'jaccard' | 'tfidf' | 'hybrid';

export interface RetrievalError {
  type: 'SIMILARITY_ERROR' | 'EMBEDDING_ERROR' | 'SEARCH_ERROR' | 'VALIDATION_ERROR';
  message: string;
  details?: unknown;
}