import { EmbeddingResponse, RetrievalError } from '../types';
import { validateSearchQuery } from '../utils/validation';

export class EmbeddingService {
  private readonly baseUrl: string;
  private readonly model: string;
  private readonly timeout: number;
  
  constructor(
    baseUrl: string = 'http://localhost:11434',
    model: string = 'nomic-embed-text',
    timeout: number = 30000
  ) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.model = model;
    this.timeout = timeout;
  }
  
  async generateEmbedding(text: string): Promise<EmbeddingResponse> {
    try {
      validateSearchQuery(text);
      
      const startTime = Date.now();
      
      // Note: This is a simplified implementation
      // In a real scenario, you would make an HTTP request to Ollama
      const response = await this.makeEmbeddingRequest(text);
      
      const processingTime = Date.now() - startTime;
      
      return {
        embedding: response.embedding,
        model: this.model,
        metadata: {
          dimension: response.embedding.length,
          processingTime
        }
      };
      
    } catch (error) {
      throw {
        type: 'EMBEDDING_ERROR',
        message: 'Failed to generate embedding',
        details: error
      } as RetrievalError;
    }
  }
  
  async generateBatchEmbeddings(texts: string[]): Promise<EmbeddingResponse[]> {
    try {
      if (!Array.isArray(texts) || texts.length === 0) {
        throw {
          type: 'EMBEDDING_ERROR',
          message: 'Texts must be a non-empty array',
          details: { texts }
        } as RetrievalError;
      }
      
      const embeddings: EmbeddingResponse[] = [];
      
      // Process embeddings in batches to avoid overwhelming the service
      const batchSize = 10;
      for (let i = 0; i < texts.length; i += batchSize) {
        const batch = texts.slice(i, i + batchSize);
        const batchPromises = batch.map(text => this.generateEmbedding(text));
        const batchResults = await Promise.all(batchPromises);
        embeddings.push(...batchResults);
      }
      
      return embeddings;
      
    } catch (error) {
      throw {
        type: 'EMBEDDING_ERROR',
        message: 'Failed to generate batch embeddings',
        details: error
      } as RetrievalError;
    }
  }
  
  private async makeEmbeddingRequest(text: string): Promise<{ embedding: number[] }> {
    // Simplified mock implementation for demonstration
    // In production, this would make an actual HTTP request to Ollama
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Generate a mock embedding based on text characteristics
    const mockEmbedding = this.generateMockEmbedding(text);
    
    return { embedding: mockEmbedding };
  }
  
  private generateMockEmbedding(text: string): number[] {
    // Create a deterministic mock embedding based on text content
    // This is for demonstration purposes only
    const dimension = 384; // Common embedding dimension
    const embedding: number[] = [];
    
    // Use text characteristics to generate consistent embeddings
    const chars = text.toLowerCase().split('');
    const charCodes = chars.map(char => char.charCodeAt(0));
    
    for (let i = 0; i < dimension; i++) {
      // Create pseudo-random but deterministic values
      const seed = (charCodes[i % charCodes.length] || 97) * (i + 1);
      const value = (Math.sin(seed) + Math.cos(seed * 0.7)) / 2;
      embedding.push(value);
    }
    
    // Normalize the embedding
    const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
    return embedding.map(val => val / magnitude);
  }
  
  validateEmbeddingDimensions(embedding: number[], expectedDimension: number): boolean {
    if (embedding.length !== expectedDimension) {
      throw {
        type: 'EMBEDDING_ERROR',
        message: `Embedding dimension mismatch. Expected ${expectedDimension}, got ${embedding.length}`,
        details: { expected: expectedDimension, actual: embedding.length }
      } as RetrievalError;
    }
    
    return true;
  }
  
  async isServiceAvailable(): Promise<boolean> {
    try {
      // In a real implementation, this would ping the Ollama service
      // For now, we'll simulate service availability
      return true;
    } catch {
      return false;
    }
  }
}