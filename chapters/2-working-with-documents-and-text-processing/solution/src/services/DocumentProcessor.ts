import * as fs from 'fs';
import * as path from 'path';
import { DocumentChunk, ProcessingConfig, SearchResult, ProcessingError, ChunkMetadata } from '../types';
import { validateNonEmptyString, validateChunkSize, sanitizeText } from '../utils/validation';

export class DocumentProcessor {
  private readonly config: ProcessingConfig;

  constructor(config: ProcessingConfig) {
    this.validateConfig(config);
    this.config = { ...config };
  }

  private validateConfig(config: ProcessingConfig): void {
    validateChunkSize(config.chunkSize);
    
    if (config.chunkOverlap < 0 || config.chunkOverlap >= config.chunkSize) {
      throw {
        type: 'PROCESSING_ERROR',
        message: 'Chunk overlap must be non-negative and less than chunk size',
        details: { chunkOverlap: config.chunkOverlap, chunkSize: config.chunkSize }
      } as ProcessingError;
    }

    if (config.maxFileSize <= 0) {
      throw {
        type: 'PROCESSING_ERROR',
        message: 'Maximum file size must be positive',
        details: { maxFileSize: config.maxFileSize }
      } as ProcessingError;
    }
  }

  async processFile(filePath: string): Promise<DocumentChunk[]> {
    try {
      if (!fs.existsSync(filePath)) {
        throw {
          type: 'FILE_NOT_FOUND',
          message: `File not found: ${filePath}`,
          details: { filePath }
        } as ProcessingError;
      }

      const stats = fs.statSync(filePath);
      
      if (stats.size > this.config.maxFileSize) {
        throw {
          type: 'SIZE_EXCEEDED',
          message: `File size ${stats.size} exceeds maximum allowed size ${this.config.maxFileSize}`,
          details: { fileSize: stats.size, maxSize: this.config.maxFileSize }
        } as ProcessingError;
      }

      const extension = path.extname(filePath).toLowerCase();
      if (!this.config.supportedExtensions.includes(extension)) {
        throw {
          type: 'INVALID_FORMAT',
          message: `Unsupported file extension: ${extension}`,
          details: { extension, supportedExtensions: this.config.supportedExtensions }
        } as ProcessingError;
      }

      const content = fs.readFileSync(filePath, 'utf-8');
      return this.processText(content, filePath);
    } catch (error) {
      if ((error as ProcessingError).type) {
        throw error;
      }
      
      throw {
        type: 'PROCESSING_ERROR',
        message: `Failed to process file: ${filePath}`,
        details: error
      } as ProcessingError;
    }
  }

  async processText(text: string, source: string): Promise<DocumentChunk[]> {
    validateNonEmptyString(text, 'text');
    validateNonEmptyString(source, 'source');

    const sanitizedText = sanitizeText(text);
    const sentences = this.splitIntoSentences(sanitizedText);
    const chunks = this.createChunks(sentences, source);

    return chunks;
  }

  private splitIntoSentences(text: string): string[] {
    const sentences = text
      .split(/[.!?]+/)
      .map(sentence => sentence.trim())
      .filter(sentence => sentence.length > 0);

    return sentences;
  }

  private createChunks(sentences: string[], source: string): DocumentChunk[] {
    const chunks: DocumentChunk[] = [];
    let currentChunk = '';
    let position = 0;

    for (let i = 0; i < sentences.length; i++) {
      const sentence = sentences[i];
      const proposedChunk = currentChunk + (currentChunk ? '. ' : '') + sentence;

      if (proposedChunk.length <= this.config.chunkSize) {
        currentChunk = proposedChunk;
      } else {
        if (currentChunk) {
          chunks.push(this.createChunkObject(currentChunk, source, position, chunks.length));
          position += currentChunk.length;
        }
        
        if (sentence.length > this.config.chunkSize) {
          const subChunks = this.splitLongSentence(sentence);
          for (const subChunk of subChunks) {
            chunks.push(this.createChunkObject(subChunk, source, position, chunks.length));
            position += subChunk.length;
          }
          currentChunk = '';
        } else {
          currentChunk = sentence;
        }
      }
    }

    if (currentChunk) {
      chunks.push(this.createChunkObject(currentChunk, source, position, chunks.length));
    }

    return this.addOverlapInfo(chunks);
  }

  private splitLongSentence(sentence: string): string[] {
    const words = sentence.split(' ');
    const chunks: string[] = [];
    let currentChunk = '';

    for (const word of words) {
      const proposedChunk = currentChunk + (currentChunk ? ' ' : '') + word;
      
      if (proposedChunk.length <= this.config.chunkSize) {
        currentChunk = proposedChunk;
      } else {
        if (currentChunk) {
          chunks.push(currentChunk);
        }
        currentChunk = word;
      }
    }

    if (currentChunk) {
      chunks.push(currentChunk);
    }

    return chunks;
  }

  private createChunkObject(content: string, source: string, position: number, chunkIndex: number): DocumentChunk {
    const wordCount = content.split(/\s+/).length;
    const characterCount = content.length;

    const metadata: ChunkMetadata = {
      position,
      wordCount,
      characterCount,
      chunkIndex
    };

    return {
      id: this.generateChunkId(source, chunkIndex),
      content: content.trim(),
      source,
      metadata
    };
  }

  private generateChunkId(source: string, chunkIndex: number): string {
    const sourceName = path.basename(source, path.extname(source));
    const timestamp = Date.now();
    return `${sourceName}_chunk_${chunkIndex}_${timestamp}`;
  }

  private addOverlapInfo(chunks: DocumentChunk[]): DocumentChunk[] {
    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      chunk.metadata.overlap = {};

      if (i > 0) {
        chunk.metadata.overlap.previousChunk = chunks[i - 1].id;
      }

      if (i < chunks.length - 1) {
        chunk.metadata.overlap.nextChunk = chunks[i + 1].id;
      }
    }

    return chunks;
  }

  searchChunks(query: string, chunks: DocumentChunk[]): SearchResult[] {
    validateNonEmptyString(query, 'query');

    const queryTerms = query.toLowerCase().split(/\s+/);
    const results: SearchResult[] = [];

    for (const chunk of chunks) {
      const score = this.calculateRelevanceScore(queryTerms, chunk);
      
      if (score > 0) {
        results.push({
          chunk,
          score,
          highlights: this.getHighlights(queryTerms, chunk.content)
        });
      }
    }

    return results.sort((a, b) => b.score - a.score);
  }

  private calculateRelevanceScore(queryTerms: string[], chunk: DocumentChunk): number {
    const content = chunk.content.toLowerCase();
    let score = 0;

    for (const term of queryTerms) {
      const termCount = (content.match(new RegExp(term, 'g')) || []).length;
      score += termCount;
    }

    return score / chunk.metadata.wordCount;
  }

  private getHighlights(queryTerms: string[], content: string): string[] {
    const highlights: string[] = [];
    const words = content.split(/\s+/);

    for (let i = 0; i < words.length; i++) {
      const word = words[i].toLowerCase();
      
      if (queryTerms.some(term => word.includes(term))) {
        const start = Math.max(0, i - 5);
        const end = Math.min(words.length, i + 6);
        const context = words.slice(start, end).join(' ');
        highlights.push(context);
      }
    }

    return highlights.slice(0, 3);
  }
}