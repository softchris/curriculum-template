import { TextAnalysis, RetrievalError } from '../types';

const STOP_WORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
  'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
  'to', 'was', 'will', 'with', 'have', 'had', 'been', 'would', 'could',
  'should', 'may', 'might', 'can', 'must', 'shall', 'this', 'these',
  'those', 'they', 'them', 'their', 'there', 'where', 'when', 'why',
  'how', 'what', 'which', 'who', 'whom', 'whose'
]);

export function preprocessText(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function tokenizeText(text: string): string[] {
  const preprocessed = preprocessText(text);
  return preprocessed
    .split(/\s+/)
    .filter(token => token.length > 0);
}

export function removeStopWords(tokens: string[]): string[] {
  return tokens.filter(token => !STOP_WORDS.has(token));
}

export function extractKeywords(text: string, minLength: number = 3): string[] {
  const tokens = tokenizeText(text);
  const filtered = removeStopWords(tokens);
  const keywords = filtered.filter(token => token.length >= minLength);
  
  // Remove duplicates and return sorted
  return Array.from(new Set(keywords)).sort();
}

export function calculateTermFrequency(tokens: string[]): Map<string, number> {
  const frequency = new Map<string, number>();
  
  for (const token of tokens) {
    frequency.set(token, (frequency.get(token) || 0) + 1);
  }
  
  return frequency;
}

export function calculateTfIdf(
  termFreq: Map<string, number>,
  documentCount: number,
  documentFrequencies: Map<string, number>
): Map<string, number> {
  const tfIdf = new Map<string, number>();
  const totalTerms = Array.from(termFreq.values()).reduce((sum, freq) => sum + freq, 0);
  
  for (const [term, freq] of termFreq.entries()) {
    const tf = freq / totalTerms;
    const df = documentFrequencies.get(term) || 1;
    const idf = Math.log(documentCount / df);
    tfIdf.set(term, tf * idf);
  }
  
  return tfIdf;
}

export function analyzeText(
  text: string,
  documentCount: number = 1,
  documentFrequencies: Map<string, number> = new Map()
): TextAnalysis {
  try {
    const tokens = tokenizeText(text);
    const keywords = extractKeywords(text);
    const termFrequency = calculateTermFrequency(tokens);
    const tfIdfScores = calculateTfIdf(termFrequency, documentCount, documentFrequencies);
    
    return {
      wordCount: tokens.length,
      uniqueWords: termFrequency.size,
      keywords,
      termFrequency,
      tfIdfScores
    };
  } catch (error) {
    throw {
      type: 'SEARCH_ERROR',
      message: 'Failed to analyze text',
      details: error
    } as RetrievalError;
  }
}

export function buildDocumentFrequencies(documents: string[]): Map<string, number> {
  const docFreq = new Map<string, number>();
  
  for (const doc of documents) {
    const uniqueTerms = new Set(extractKeywords(doc));
    
    for (const term of uniqueTerms) {
      docFreq.set(term, (docFreq.get(term) || 0) + 1);
    }
  }
  
  return docFreq;
}

export function normalizeVector(vector: number[]): number[] {
  const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));
  
  if (magnitude === 0) {
    return new Array(vector.length).fill(0);
  }
  
  return vector.map(val => val / magnitude);
}

export function dotProduct(vectorA: number[], vectorB: number[]): number {
  if (vectorA.length !== vectorB.length) {
    throw {
      type: 'SIMILARITY_ERROR',
      message: 'Vectors must have the same length for dot product calculation',
      details: { lengthA: vectorA.length, lengthB: vectorB.length }
    } as RetrievalError;
  }
  
  return vectorA.reduce((sum, val, index) => sum + val * vectorB[index], 0);
}