import { RetrievalError, TextAnalysis } from '../types';

export function validateSearchQuery(query: string): boolean {
  if (!query || typeof query !== 'string') {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Search query must be a non-empty string',
      details: { query }
    } as RetrievalError;
  }

  if (query.trim().length === 0) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Search query cannot be empty or only whitespace',
      details: { query }
    } as RetrievalError;
  }

  if (query.length < 2) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Search query must be at least 2 characters long',
      details: { query, length: query.length }
    } as RetrievalError;
  }

  return true;
}

export function validateSimilarityThreshold(threshold: number): boolean {
  if (typeof threshold !== 'number' || isNaN(threshold)) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Similarity threshold must be a valid number',
      details: { threshold }
    } as RetrievalError;
  }

  if (threshold < 0 || threshold > 1) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Similarity threshold must be between 0 and 1',
      details: { threshold }
    } as RetrievalError;
  }

  return true;
}

export function validateMaxResults(maxResults: number): boolean {
  if (typeof maxResults !== 'number' || !Number.isInteger(maxResults)) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Max results must be a positive integer',
      details: { maxResults }
    } as RetrievalError;
  }

  if (maxResults <= 0) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Max results must be greater than 0',
      details: { maxResults }
    } as RetrievalError;
  }

  if (maxResults > 1000) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Max results cannot exceed 1000 for performance reasons',
      details: { maxResults }
    } as RetrievalError;
  }

  return true;
}

export function validateEmbedding(embedding: number[]): boolean {
  if (!Array.isArray(embedding)) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Embedding must be an array of numbers',
      details: { embedding }
    } as RetrievalError;
  }

  if (embedding.length === 0) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Embedding cannot be empty',
      details: { length: embedding.length }
    } as RetrievalError;
  }

  if (!embedding.every(value => typeof value === 'number' && !isNaN(value))) {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'All embedding values must be valid numbers',
      details: { embedding }
    } as RetrievalError;
  }

  return true;
}