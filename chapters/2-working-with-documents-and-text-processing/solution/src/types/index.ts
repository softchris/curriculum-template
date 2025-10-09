export interface DocumentChunk {
  id: string;
  content: string;
  source: string;
  metadata: ChunkMetadata;
}

export interface ChunkMetadata {
  position: number;
  wordCount: number;
  characterCount: number;
  chunkIndex: number;
  overlap?: {
    previousChunk?: string;
    nextChunk?: string;
  };
}

export interface ProcessingConfig {
  chunkSize: number;
  chunkOverlap: number;
  maxFileSize: number;
  supportedExtensions: string[];
}

export interface DocumentCollection {
  chunks: DocumentChunk[];
  metadata: CollectionMetadata;
}

export interface CollectionMetadata {
  totalChunks: number;
  totalDocuments: number;
  averageChunkSize: number;
  createdAt: Date;
  lastUpdated: Date;
}

export interface SearchResult {
  chunk: DocumentChunk;
  score: number;
  highlights?: string[];
}

export interface ProcessingError {
  type: 'FILE_NOT_FOUND' | 'INVALID_FORMAT' | 'SIZE_EXCEEDED' | 'PROCESSING_ERROR';
  message: string;
  details?: unknown;
}

export interface FileInfo {
  path: string;
  size: number;
  extension: string;
  name: string;
}