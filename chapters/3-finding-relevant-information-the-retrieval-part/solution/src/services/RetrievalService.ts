import { 
  DocumentChunk, 
  SearchQuery, 
  SearchResult, 
  RetrievalConfig, 
  SimilarityAlgorithm,
  RetrievalError
} from '../types';
import { SimilarityService } from './SimilarityService';
import { EmbeddingService } from './EmbeddingService';
import { 
  validateSearchQuery, 
  validateSimilarityThreshold, 
  validateMaxResults 
} from '../utils/validation';
import { extractKeywords } from '../utils/textProcessing';

export class RetrievalService {
  private readonly config: RetrievalConfig;
  private readonly similarityService: SimilarityService;
  private readonly embeddingService: EmbeddingService;
  
  constructor(config: RetrievalConfig) {
    this.validateConfig(config);
    this.config = { ...config };
    this.similarityService = new SimilarityService();
    this.embeddingService = new EmbeddingService(
      config.ollamaBaseUrl,
      config.embeddingModel
    );
  }
  
  private validateConfig(config: RetrievalConfig): void {
    validateSimilarityThreshold(config.similarityThreshold);
    validateMaxResults(config.maxResults);
  }
  
  async searchSimilarChunks(
    query: SearchQuery,
    chunks: DocumentChunk[]
  ): Promise<SearchResult[]> {
    try {
      validateSearchQuery(query.text);
      
      if (!Array.isArray(chunks) || chunks.length === 0) {
        return [];
      }
      
      const algorithm = query.options?.algorithm || 
        this.similarityService.getBestSimilarityAlgorithm(query.text, chunks);
      
      const results: SearchResult[] = [];
      
      for (const chunk of chunks) {
        if (this.shouldSkipChunk(chunk, query)) {
          continue;
        }
        
        const similarity = await this.calculateSimilarity(
          query.text,
          chunk,
          algorithm,
          chunks.map(c => c.content)
        );
        
        if (similarity.overall >= this.config.similarityThreshold) {
          const highlights = this.generateHighlights(query.text, chunk.content);
          const explanation = this.generateExplanation(similarity, algorithm);
          
          results.push({
            chunk,
            score: similarity.overall,
            similarity,
            highlights,
            explanation
          });
        }
      }
      
      // Sort by relevance score and limit results
      const maxResults = query.options?.maxResults || this.config.maxResults;
      return results
        .sort((a, b) => b.score - a.score)
        .slice(0, maxResults);
        
    } catch (error) {
      throw {
        type: 'SEARCH_ERROR',
        message: 'Failed to search similar chunks',
        details: error
      } as RetrievalError;
    }
  }
  
  private shouldSkipChunk(chunk: DocumentChunk, query: SearchQuery): boolean {
    const filters = query.filters;
    if (!filters) return false;
    
    if (filters.source && chunk.source !== filters.source) {
      return true;
    }
    
    if (filters.minWordCount && chunk.metadata.wordCount < filters.minWordCount) {
      return true;
    }
    
    if (filters.maxWordCount && chunk.metadata.wordCount > filters.maxWordCount) {
      return true;
    }
    
    if (filters.keywords && filters.keywords.length > 0) {
      const chunkKeywords = extractKeywords(chunk.content);
      const hasRequiredKeywords = filters.keywords.some(keyword =>
        chunkKeywords.includes(keyword.toLowerCase())
      );
      if (!hasRequiredKeywords) {
        return true;
      }
    }
    
    return false;
  }
  
  private async calculateSimilarity(
    query: string,
    chunk: DocumentChunk,
    algorithm: SimilarityAlgorithm,
    documentCollection: string[]
  ) {
    switch (algorithm) {
      case 'cosine':
        const cosineScore = this.similarityService.calculateCosineSimilarity(query, chunk.content);
        return {
          overall: cosineScore,
          keyword: cosineScore,
          algorithm
        };
        
      case 'jaccard':
        const jaccardScore = this.similarityService.calculateJaccardSimilarity(query, chunk.content);
        return {
          overall: jaccardScore,
          keyword: jaccardScore,
          algorithm
        };
        
      case 'tfidf':
        const tfidfScore = this.similarityService.calculateTfIdfSimilarity(
          query, 
          chunk.content, 
          documentCollection
        );
        return {
          overall: tfidfScore,
          keyword: tfidfScore,
          algorithm
        };
        
      case 'hybrid':
        return this.similarityService.calculateHybridSimilarity(
          query,
          chunk,
          documentCollection
        );
        
      default:
        throw {
          type: 'SEARCH_ERROR',
          message: `Unknown similarity algorithm: ${algorithm}`,
          details: { algorithm }
        } as RetrievalError;
    }
  }
  
  private generateHighlights(query: string, content: string): string[] {
    const queryTerms = extractKeywords(query);
    const highlights: string[] = [];
    const words = content.split(/\s+/);
    
    for (let i = 0; i < words.length; i++) {
      const word = words[i].toLowerCase().replace(/[^\w]/g, '');
      
      if (queryTerms.some(term => word.includes(term))) {
        const start = Math.max(0, i - 6);
        const end = Math.min(words.length, i + 7);
        const context = words.slice(start, end).join(' ');
        
        // Avoid duplicate highlights
        if (!highlights.some(h => h.includes(context.substring(10, -10)))) {
          highlights.push(context);
        }
      }
    }
    
    return highlights.slice(0, 3);
  }
  
  private generateExplanation(similarity: any, algorithm: SimilarityAlgorithm): string {
    const score = (similarity.overall * 100).toFixed(1);
    
    switch (algorithm) {
      case 'cosine':
        return `Cosine similarity: ${score}% based on term frequency and vector angle`;
      case 'jaccard':
        return `Jaccard similarity: ${score}% based on shared keywords ratio`;
      case 'tfidf':
        return `TF-IDF similarity: ${score}% based on term importance and frequency`;
      case 'hybrid':
        const keywordScore = (similarity.keyword * 100).toFixed(1);
        const semanticScore = similarity.semantic ? (similarity.semantic * 100).toFixed(1) : 'N/A';
        return `Hybrid similarity: ${score}% (keyword: ${keywordScore}%, semantic: ${semanticScore}%)`;
      default:
        return `Similarity: ${score}%`;
    }
  }
  
  async enhanceChunksWithEmbeddings(chunks: DocumentChunk[]): Promise<DocumentChunk[]> {
    try {
      if (!await this.embeddingService.isServiceAvailable()) {
        console.warn('Embedding service not available, skipping embedding enhancement');
        return chunks;
      }
      
      const enhancedChunks: DocumentChunk[] = [];
      
      for (const chunk of chunks) {
        if (chunk.embedding && chunk.embedding.length > 0) {
          // Chunk already has embedding
          enhancedChunks.push(chunk);
          continue;
        }
        
        try {
          const embeddingResponse = await this.embeddingService.generateEmbedding(chunk.content);
          const enhancedChunk: DocumentChunk = {
            ...chunk,
            embedding: embeddingResponse.embedding
          };
          enhancedChunks.push(enhancedChunk);
        } catch (error) {
          console.warn(`Failed to generate embedding for chunk ${chunk.id}:`, error);
          enhancedChunks.push(chunk);
        }
      }
      
      return enhancedChunks;
      
    } catch (error) {
      throw {
        type: 'EMBEDDING_ERROR',
        message: 'Failed to enhance chunks with embeddings',
        details: error
      } as RetrievalError;
    }
  }
  
  getRetrievalStatistics(results: SearchResult[]): {
    totalResults: number;
    averageScore: number;
    algorithmDistribution: Map<SimilarityAlgorithm, number>;
    scoreDistribution: { low: number; medium: number; high: number };
  } {
    if (results.length === 0) {
      return {
        totalResults: 0,
        averageScore: 0,
        algorithmDistribution: new Map(),
        scoreDistribution: { low: 0, medium: 0, high: 0 }
      };
    }
    
    const totalScore = results.reduce((sum, result) => sum + result.score, 0);
    const averageScore = totalScore / results.length;
    
    const algorithmDistribution = new Map<SimilarityAlgorithm, number>();
    const scoreDistribution = { low: 0, medium: 0, high: 0 };
    
    for (const result of results) {
      // Algorithm distribution
      const algorithm = result.similarity.algorithm;
      algorithmDistribution.set(algorithm, (algorithmDistribution.get(algorithm) || 0) + 1);
      
      // Score distribution
      if (result.score < 0.3) {
        scoreDistribution.low++;
      } else if (result.score < 0.7) {
        scoreDistribution.medium++;
      } else {
        scoreDistribution.high++;
      }
    }
    
    return {
      totalResults: results.length,
      averageScore,
      algorithmDistribution,
      scoreDistribution
    };
  }
}