import { DocumentChunk, SimilarityAlgorithm, SimilarityScore, RetrievalError } from '../types';
import { 
  extractKeywords, 
  calculateTermFrequency, 
  normalizeVector, 
  dotProduct,
  analyzeText
} from '../utils/textProcessing';
import { validateSearchQuery } from '../utils/validation';

export class SimilarityService {
  
  calculateCosineSimilarity(textA: string, textB: string): number {
    try {
      validateSearchQuery(textA);
      validateSearchQuery(textB);
      
      const tokensA = extractKeywords(textA);
      const tokensB = extractKeywords(textB);
      
      if (tokensA.length === 0 || tokensB.length === 0) {
        return 0;
      }
      
      // Create vocabulary from both texts
      const vocabulary = Array.from(new Set([...tokensA, ...tokensB]));
      
      // Create frequency vectors
      const freqA = calculateTermFrequency(tokensA);
      const freqB = calculateTermFrequency(tokensB);
      
      // Convert to vectors based on vocabulary
      const vectorA = vocabulary.map(term => freqA.get(term) || 0);
      const vectorB = vocabulary.map(term => freqB.get(term) || 0);
      
      // Normalize vectors
      const normalizedA = normalizeVector(vectorA);
      const normalizedB = normalizeVector(vectorB);
      
      // Calculate cosine similarity
      return dotProduct(normalizedA, normalizedB);
      
    } catch (error) {
      throw {
        type: 'SIMILARITY_ERROR',
        message: 'Failed to calculate cosine similarity',
        details: error
      } as RetrievalError;
    }
  }
  
  calculateJaccardSimilarity(textA: string, textB: string): number {
    try {
      validateSearchQuery(textA);
      validateSearchQuery(textB);
      
      const tokensA = new Set(extractKeywords(textA));
      const tokensB = new Set(extractKeywords(textB));
      
      if (tokensA.size === 0 && tokensB.size === 0) {
        return 1;
      }
      
      const intersection = new Set([...tokensA].filter(token => tokensB.has(token)));
      const union = new Set([...tokensA, ...tokensB]);
      
      return intersection.size / union.size;
      
    } catch (error) {
      throw {
        type: 'SIMILARITY_ERROR',
        message: 'Failed to calculate Jaccard similarity',
        details: error
      } as RetrievalError;
    }
  }
  
  calculateTfIdfSimilarity(
    textA: string, 
    textB: string, 
    documentCollection: string[] = []
  ): number {
    try {
      validateSearchQuery(textA);
      validateSearchQuery(textB);
      
      const allDocuments = [textA, textB, ...documentCollection];
      const analysisA = analyzeText(textA, allDocuments.length);
      const analysisB = analyzeText(textB, allDocuments.length);
      
      // Get all unique terms
      const allTerms = new Set([
        ...analysisA.tfIdfScores.keys(),
        ...analysisB.tfIdfScores.keys()
      ]);
      
      if (allTerms.size === 0) {
        return 0;
      }
      
      // Create TF-IDF vectors
      const vectorA = Array.from(allTerms).map(term => 
        analysisA.tfIdfScores.get(term) || 0
      );
      const vectorB = Array.from(allTerms).map(term => 
        analysisB.tfIdfScores.get(term) || 0
      );
      
      // Normalize and calculate cosine similarity
      const normalizedA = normalizeVector(vectorA);
      const normalizedB = normalizeVector(vectorB);
      
      return dotProduct(normalizedA, normalizedB);
      
    } catch (error) {
      throw {
        type: 'SIMILARITY_ERROR',
        message: 'Failed to calculate TF-IDF similarity',
        details: error
      } as RetrievalError;
    }
  }
  
  calculateEmbeddingSimilarity(embeddingA: number[], embeddingB: number[]): number {
    try {
      if (!embeddingA || !embeddingB) {
        throw {
          type: 'SIMILARITY_ERROR',
          message: 'Both embeddings must be provided',
          details: { embeddingA: !!embeddingA, embeddingB: !!embeddingB }
        } as RetrievalError;
      }
      
      if (embeddingA.length !== embeddingB.length) {
        throw {
          type: 'SIMILARITY_ERROR',
          message: 'Embeddings must have the same dimensions',
          details: { dimA: embeddingA.length, dimB: embeddingB.length }
        } as RetrievalError;
      }
      
      const normalizedA = normalizeVector(embeddingA);
      const normalizedB = normalizeVector(embeddingB);
      
      return dotProduct(normalizedA, normalizedB);
      
    } catch (error) {
      throw {
        type: 'SIMILARITY_ERROR',
        message: 'Failed to calculate embedding similarity',
        details: error
      } as RetrievalError;
    }
  }
  
  calculateHybridSimilarity(
    query: string,
    chunk: DocumentChunk,
    documentCollection: string[] = []
  ): SimilarityScore {
    try {
      const cosineScore = this.calculateCosineSimilarity(query, chunk.content);
      const jaccardScore = this.calculateJaccardSimilarity(query, chunk.content);
      const tfIdfScore = this.calculateTfIdfSimilarity(query, chunk.content, documentCollection);
      
      let semanticScore: number | undefined;
      
      // Calculate semantic similarity if embeddings are available
      if (chunk.embedding) {
        // Note: This would require generating an embedding for the query
        // For now, we'll use the TF-IDF score as a proxy
        semanticScore = tfIdfScore;
      }
      
      // Weighted combination of different similarity measures
      const keywordScore = (cosineScore * 0.4) + (jaccardScore * 0.3) + (tfIdfScore * 0.3);
      const overallScore = semanticScore 
        ? (keywordScore * 0.6) + (semanticScore * 0.4)
        : keywordScore;
      
      return {
        overall: Math.max(0, Math.min(1, overallScore)),
        keyword: Math.max(0, Math.min(1, keywordScore)),
        semantic: semanticScore ? Math.max(0, Math.min(1, semanticScore)) : undefined,
        algorithm: 'hybrid' as SimilarityAlgorithm
      };
      
    } catch (error) {
      throw {
        type: 'SIMILARITY_ERROR',
        message: 'Failed to calculate hybrid similarity',
        details: error
      } as RetrievalError;
    }
  }
  
  getBestSimilarityAlgorithm(
    query: string,
    chunks: DocumentChunk[]
  ): SimilarityAlgorithm {
    // Simple heuristic for algorithm selection
    const queryLength = extractKeywords(query).length;
    const hasEmbeddings = chunks.some(chunk => chunk.embedding && chunk.embedding.length > 0);
    
    if (hasEmbeddings && queryLength > 3) {
      return 'hybrid';
    } else if (queryLength > 5) {
      return 'tfidf';
    } else if (queryLength > 2) {
      return 'cosine';
    } else {
      return 'jaccard';
    }
  }
}