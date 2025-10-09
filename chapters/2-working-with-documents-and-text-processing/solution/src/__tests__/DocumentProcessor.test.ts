import { DocumentProcessor } from '../services/DocumentProcessor';
import { ProcessingConfig } from '../types';

describe('DocumentProcessor', () => {
  let processor: DocumentProcessor;
  let config: ProcessingConfig;

  beforeEach(() => {
    config = {
      chunkSize: 300,
      chunkOverlap: 50,
      maxFileSize: 10 * 1024 * 1024,
      supportedExtensions: ['.txt', '.md']
    };
    processor = new DocumentProcessor(config);
  });

  describe('Text Processing', () => {
    it('should process simple text into chunks', async () => {
      const text = 'This is a test sentence. This is another sentence. And one more for good measure.';
      const chunks = await processor.processText(text, 'test.txt');

      expect(chunks).toHaveLength(1);
      expect(chunks[0]).toHaveProperty('content');
      expect(chunks[0]).toHaveProperty('id');
      expect(chunks[0]).toHaveProperty('source', 'test.txt');
      expect(chunks[0]).toHaveProperty('metadata');
    });

    it('should split long text into multiple chunks', async () => {
      const longText = 'This is a sentence. '.repeat(50);
      const chunks = await processor.processText(longText, 'long-test.txt');

      expect(chunks.length).toBeGreaterThan(1);
      
      for (const chunk of chunks) {
        expect(chunk.content.length).toBeLessThanOrEqual(config.chunkSize);
        expect(chunk.metadata.wordCount).toBeGreaterThan(0);
        expect(chunk.metadata.characterCount).toBe(chunk.content.length);
      }
    });

    it('should handle empty text gracefully', async () => {
      await expect(processor.processText('', 'empty.txt')).rejects.toThrow();
    });

    it('should sanitize text properly', async () => {
      const messyText = 'This  has   multiple    spaces.\r\nAnd\tsome\ttabs.\r\n\r\nMultiple newlines.';
      const chunks = await processor.processText(messyText, 'messy.txt');

      expect(chunks[0].content).not.toContain('\r');
      expect(chunks[0].content).not.toContain('\t');
      expect(chunks[0].content).not.toMatch(/  +/);
    });
  });

  describe('Search Functionality', () => {
    let testChunks: any[];

    beforeEach(async () => {
      const text1 = 'Machine learning algorithms enable computers to learn patterns from data automatically.';
      const text2 = 'Natural language processing helps computers understand human language effectively.';
      const text3 = 'Deep learning neural networks require large amounts of training data for optimal performance.';
      
      const chunks1 = await processor.processText(text1, 'ml.txt');
      const chunks2 = await processor.processText(text2, 'nlp.txt');
      const chunks3 = await processor.processText(text3, 'dl.txt');
      
      testChunks = [...chunks1, ...chunks2, ...chunks3];
    });

    it('should find relevant chunks for search queries', () => {
      const results = processor.searchChunks('machine learning', testChunks);

      expect(results.length).toBeGreaterThan(0);
      expect(results[0]).toHaveProperty('chunk');
      expect(results[0]).toHaveProperty('score');
      expect(results[0].score).toBeGreaterThan(0);
    });

    it('should return results sorted by relevance score', () => {
      const results = processor.searchChunks('learning data', testChunks);

      for (let i = 1; i < results.length; i++) {
        expect(results[i - 1].score).toBeGreaterThanOrEqual(results[i].score);
      }
    });

    it('should return empty results for non-matching queries', () => {
      const results = processor.searchChunks('quantum computing', testChunks);
      expect(results).toHaveLength(0);
    });

    it('should handle empty search queries', () => {
      expect(() => processor.searchChunks('', testChunks)).toThrow();
    });
  });

  describe('Configuration Validation', () => {
    it('should throw error for invalid chunk size', () => {
      const invalidConfig = { ...config, chunkSize: -1 };
      expect(() => new DocumentProcessor(invalidConfig)).toThrow();
    });

    it('should throw error for invalid overlap configuration', () => {
      const invalidConfig = { ...config, chunkOverlap: config.chunkSize };
      expect(() => new DocumentProcessor(invalidConfig)).toThrow();
    });

    it('should throw error for invalid max file size', () => {
      const invalidConfig = { ...config, maxFileSize: -1 };
      expect(() => new DocumentProcessor(invalidConfig)).toThrow();
    });
  });

  describe('Chunk Metadata', () => {
    it('should include proper metadata for each chunk', async () => {
      const text = 'This is a test sentence with several words to count properly.';
      const chunks = await processor.processText(text, 'metadata-test.txt');

      const chunk = chunks[0];
      expect(chunk.metadata).toHaveProperty('wordCount');
      expect(chunk.metadata).toHaveProperty('characterCount');
      expect(chunk.metadata).toHaveProperty('position');
      expect(chunk.metadata).toHaveProperty('chunkIndex');
      
      expect(chunk.metadata.wordCount).toBe(text.split(/\s+/).length);
      expect(chunk.metadata.characterCount).toBe(chunk.content.length);
      expect(chunk.metadata.chunkIndex).toBe(0);
    });

    it('should include overlap information for multiple chunks', async () => {
      const longText = 'Sentence one. Sentence two. Sentence three. '.repeat(20);
      const chunks = await processor.processText(longText, 'overlap-test.txt');

      if (chunks.length > 1) {
        expect(chunks[0].metadata.overlap?.nextChunk).toBeDefined();
        expect(chunks[0].metadata.overlap?.previousChunk).toBeUndefined();
        
        expect(chunks[chunks.length - 1].metadata.overlap?.previousChunk).toBeDefined();
        expect(chunks[chunks.length - 1].metadata.overlap?.nextChunk).toBeUndefined();
      }
    });
  });
});