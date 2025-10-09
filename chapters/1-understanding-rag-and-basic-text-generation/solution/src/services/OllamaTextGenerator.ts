import { OllamaConfig, GenerationOptions, GenerationResponse, GenerationError } from '../types/index.js';
import { validateNonEmptyString, validateUrl, validateNumericRange } from '../utils/validation.js';

/**
 * Service class for interacting with Ollama API for text generation
 * Implements the "Generation" component of RAG systems
 */
export class OllamaTextGenerator {
  private readonly config: OllamaConfig;
  
  constructor(config: OllamaConfig) {
    this.validateConfig(config);
    this.config = { ...config };
  }
  
  /**
   * Generates text using Ollama based on the provided prompt
   * @param prompt - The input prompt for text generation
   * @param options - Optional generation parameters
   * @returns Promise containing the generated response
   */
  async generate(prompt: string, options: GenerationOptions = {}): Promise<GenerationResponse> {
    const startTime = Date.now();
    
    try {
      // Validate inputs
      validateNonEmptyString(prompt, 'prompt');
      this.validateGenerationOptions(options);
      
      // Prepare the request payload
      const payload = this.buildRequestPayload(prompt, options);
      
      // Make the API request
      const response = await this.makeRequest(payload);
      
      // Process and return the response
      return this.processResponse(response, startTime);
      
    } catch (error) {
      throw this.handleError(error);
    }
  }
  
  /**
   * Validates the Ollama configuration
   */
  private validateConfig(config: OllamaConfig): void {
    validateUrl(config.baseUrl);
    validateNonEmptyString(config.model, 'model');
    
    if (config.timeout && config.timeout <= 0) {
      throw {
        type: 'VALIDATION_ERROR',
        message: 'Timeout must be a positive number',
        details: { timeout: config.timeout }
      } as GenerationError;
    }
  }
  
  /**
   * Validates generation options
   */
  private validateGenerationOptions(options: GenerationOptions): void {
    if (options.maxTokens !== undefined) {
      validateNumericRange(options.maxTokens, 1, 4096, 'maxTokens');
    }
    
    if (options.temperature !== undefined) {
      validateNumericRange(options.temperature, 0.0, 2.0, 'temperature');
    }
  }
  
  /**
   * Builds the request payload for Ollama API
   */
  private buildRequestPayload(prompt: string, options: GenerationOptions): object {
    const systemPrompt = options.systemPrompt || 'You are a helpful assistant.';
    const fullPrompt = systemPrompt + '\n\nUser: ' + prompt + '\n\nAssistant:';
    
    return {
      model: this.config.model,
      prompt: fullPrompt,
      stream: options.stream || false,
      options: {
        num_predict: options.maxTokens || 500,
        temperature: options.temperature || 0.7,
        top_p: 0.9,
        top_k: 40
      }
    };
  }
  
  /**
   * Makes the HTTP request to Ollama API
   */
  private async makeRequest(payload: object): Promise<any> {
    const url = `${this.config.baseUrl}/api/generate`;
    const timeout = this.config.timeout || 30000;
    
    // Create a timeout promise
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => {
        reject({
          type: 'TIMEOUT_ERROR',
          message: `Request timed out after ${timeout}ms`,
          details: { timeout }
        } as GenerationError);
      }, timeout);
    });
    
    // Create the fetch promise (simplified for example)
    const fetchPromise = this.simulateHttpRequest(url, payload);
    
    // Race between fetch and timeout
    return Promise.race([fetchPromise, timeoutPromise]);
  }
  
  /**
   * Simulates HTTP request (in real implementation, use fetch or axios)
   */
  private async simulateHttpRequest(url: string, payload: object): Promise<any> {
    // This is a simulation for the example
    // In real implementation, use fetch or axios
    console.log(`Making request to ${url} with payload:`, JSON.stringify(payload, null, 2));
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 200));
    
    // Simulate different responses based on the prompt
    const promptText = (payload as any).prompt.toLowerCase();
    let response = '';
    
    if (promptText.includes('artificial intelligence')) {
      response = 'Artificial intelligence (AI) refers to computer systems that can perform tasks typically requiring human intelligence, such as learning, reasoning, and problem-solving.';
    } else if (promptText.includes('rag') || promptText.includes('retrieval augmented generation')) {
      response = 'The three main components of RAG are: 1) Retrieval - finding relevant information from a knowledge base, 2) Augmentation - adding the retrieved context to the prompt, and 3) Generation - producing the final response using the enhanced prompt.';
    } else {
      response = 'This is a simulated response from the Ollama service. In a real implementation, this would be the actual AI-generated text.';
    }
    
    return {
      response,
      done: true,
      total_duration: 150000000, // nanoseconds
      prompt_eval_count: 50,
      eval_count: response.split(' ').length
    };
  }
  
  /**
   * Processes the API response into our standard format
   */
  private processResponse(response: any, startTime: number): GenerationResponse {
    const endTime = Date.now();
    const generationTime = endTime - startTime;
    
    return {
      content: response.response.trim(),
      model: this.config.model,
      metadata: {
        generationTime,
        tokensGenerated: response.eval_count || 0
      }
    };
  }
  
  /**
   * Handles and standardizes errors
   */
  private handleError(error: any): GenerationError {
    if (error.type && error.message) {
      // Already a GenerationError
      return error as GenerationError;
    }
    
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      return {
        type: 'CONNECTION_ERROR',
        message: 'Cannot connect to Ollama service. Make sure Ollama is running.',
        details: error
      };
    }
    
    return {
      type: 'MODEL_ERROR',
      message: error.message || 'Unknown error occurred during text generation',
      details: error
    };
  }
}