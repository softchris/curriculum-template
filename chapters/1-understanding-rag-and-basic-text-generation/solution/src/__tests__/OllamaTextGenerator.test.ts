import { OllamaTextGenerator } from '../services/OllamaTextGenerator';
import { OllamaConfig } from '../types';

describe('OllamaTextGenerator', () => {
  let generator: OllamaTextGenerator;
  
  beforeEach(() => {
    const config: OllamaConfig = {
      baseUrl: 'http://localhost:11434',
      model: 'llama3.2',
      timeout: 5000
    };
    generator = new OllamaTextGenerator(config);
  });
  
  describe('constructor', () => {
    it('should create instance with valid config', () => {
      expect(generator).toBeInstanceOf(OllamaTextGenerator);
    });
    
    it('should throw error with invalid URL', () => {
      expect(() => {
        new OllamaTextGenerator({
          baseUrl: 'invalid-url',
          model: 'test-model'
        });
      }).toThrow('Invalid URL format');
    });
    
    it('should throw error with empty model', () => {
      expect(() => {
        new OllamaTextGenerator({
          baseUrl: 'http://localhost:11434',
          model: ''
        });
      }).toThrow('model cannot be empty or only whitespace');
    });
  });
  
  describe('generate', () => {
    it('should generate text successfully', async () => {
      const response = await generator.generate('Test prompt');
      
      expect(response).toHaveProperty('content');
      expect(response).toHaveProperty('model');
      expect(response).toHaveProperty('metadata');
      expect(response.metadata).toHaveProperty('generationTime');
      expect(response.metadata).toHaveProperty('tokensGenerated');
      expect(typeof response.content).toBe('string');
      expect(response.content.length).toBeGreaterThan(0);
    });
    
    it('should throw error with empty prompt', async () => {
      await expect(generator.generate('')).rejects.toThrow('prompt cannot be empty or only whitespace');
    });
    
    it('should respect generation options', async () => {
      const response = await generator.generate('Test prompt', {
        maxTokens: 100,
        temperature: 0.5,
        systemPrompt: 'You are a test assistant.'
      });
      
      expect(response.content).toBeTruthy();
      expect(response.model).toBe('llama3.2');
    });
  });
});