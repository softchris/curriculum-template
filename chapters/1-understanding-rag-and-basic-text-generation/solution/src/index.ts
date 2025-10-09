import dotenv from 'dotenv';
import { OllamaTextGenerator } from './services/OllamaTextGenerator.js';
import { OllamaConfig } from './types/index.js';

// Load environment variables
dotenv.config();

/**
 * Main application entry point demonstrating basic RAG text generation
 * This example shows the "Generation" part of RAG using Ollama
 */
async function main(): Promise<void> {
  console.log('🚀 Starting RAG Text Generation Demo');
  
  try {
    // Configure Ollama connection
    const config: OllamaConfig = {
      baseUrl: process.env.OLLAMA_BASE_URL || 'http://localhost:11434',
      model: process.env.OLLAMA_MODEL || 'llama3.2',
      timeout: 30000
    };
    
    console.log(`📡 Connecting to Ollama at ${config.baseUrl}`);
    console.log(`🤖 Using model: ${config.model}`);
    
    // Initialize the text generator
    const generator = new OllamaTextGenerator(config);
    
    // Test basic text generation
    await demonstrateBasicGeneration(generator);
    
    // Test context-aware generation (preview of RAG)
    await demonstrateContextAwareGeneration(generator);
    
    console.log('✅ Demo completed successfully!');
    
  } catch (error) {
    console.error('❌ Demo failed:', error);
    process.exit(1);
  }
}

/**
 * Demonstrates basic text generation without context
 */
async function demonstrateBasicGeneration(generator: OllamaTextGenerator): Promise<void> {
  console.log('\n📝 Testing Basic Text Generation...');
  
  const prompt = "Explain what artificial intelligence is in simple terms.";
  console.log(`Question: ${prompt}`);
  
  const response = await generator.generate(prompt, {
    maxTokens: 200,
    temperature: 0.7,
    systemPrompt: "You are a helpful assistant that explains complex topics clearly."
  });
  
  console.log(`\nResponse (${response.metadata.tokensGenerated} tokens, ${response.metadata.generationTime}ms):`);
  console.log(response.content);
}

/**
 * Demonstrates context-aware generation (basic RAG preview)
 */
async function demonstrateContextAwareGeneration(generator: OllamaTextGenerator): Promise<void> {
  console.log('\n🧠 Testing Context-Aware Generation (RAG Preview)...');
  
  // Simulate retrieved context (this would come from document retrieval)
  const context = `
  Retrieval Augmented Generation (RAG) is a technique that combines information retrieval 
  with text generation. It works by first retrieving relevant information from a knowledge 
  base or document collection, then using that information to generate more accurate and 
  contextual responses. RAG systems typically have three components: retrieval (finding 
  relevant information), augmentation (adding context to the prompt), and generation 
  (producing the final response).
  `;
  
  const question = "What are the three main components of RAG?";
  const contextualPrompt = `
Context: ${context.trim()}

Question: ${question}

Please answer the question based on the provided context.
  `;
  
  console.log(`Question: ${question}`);
  console.log('Using retrieved context to enhance the response...');
  
  const response = await generator.generate(contextualPrompt, {
    maxTokens: 150,
    temperature: 0.3,
    systemPrompt: "Answer questions based on the provided context. Be concise and accurate."
  });
  
  console.log(`\nContextual Response (${response.metadata.tokensGenerated} tokens, ${response.metadata.generationTime}ms):`);
  console.log(response.content);
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  process.exit(1);
});

// Run the main function
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}