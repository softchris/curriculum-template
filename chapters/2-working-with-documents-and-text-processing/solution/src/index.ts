import { DocumentProcessor } from './services/DocumentProcessor';
import { DocumentChunk, ProcessingConfig } from './types';
import { validateFile } from './utils/validation';

async function demonstrateDocumentProcessing(): Promise<void> {
  console.log('Starting Document Processing Demonstration...\n');
  
  const config: ProcessingConfig = {
    chunkSize: 300,
    chunkOverlap: 50,
    maxFileSize: 10 * 1024 * 1024, // 10MB
    supportedExtensions: ['.txt', '.md']
  };
  
  const processor = new DocumentProcessor(config);
  
  // Create a sample document for processing
  const sampleText = `
Artificial Intelligence has revolutionized how we interact with technology and process information. Machine learning algorithms enable computers to learn patterns from data without explicit programming for every scenario. This capability has transformed industries from healthcare to finance, creating new possibilities for automation and decision-making.

Natural Language Processing represents a crucial subset of AI that focuses on enabling computers to understand, interpret, and generate human language. Through sophisticated algorithms, NLP systems can analyze text sentiment, extract key information, translate between languages, and even engage in conversational interactions that feel increasingly natural.

The development of large language models has marked a significant milestone in AI advancement. These models, trained on vast amounts of text data, demonstrate remarkable abilities to understand context, generate coherent responses, and perform complex reasoning tasks. However, they also present challenges related to accuracy, bias, and the need for current information.

Retrieval Augmented Generation addresses some of these limitations by combining the power of language models with dynamic information retrieval. Instead of relying solely on training data, RAG systems can access external knowledge sources to provide more accurate, current, and contextually relevant responses. This approach represents a practical solution for creating AI applications that need to work with specific, up-to-date information.
  `;
  
  try {
    console.log('Processing sample document...');
    const chunks = await processor.processText(sampleText, 'sample-ai-overview.txt');
    
    console.log(`Successfully created ${chunks.length} chunks\n`);
    
    chunks.forEach((chunk, index) => {
      console.log(`--- Chunk ${index + 1} ---`);
      console.log(`ID: ${chunk.id}`);
      console.log(`Source: ${chunk.source}`);
      console.log(`Size: ${chunk.content.length} characters`);
      console.log(`Content: ${chunk.content.substring(0, 100)}...`);
      console.log(`Metadata: Words=${chunk.metadata.wordCount}, Position=${chunk.metadata.position}\n`);
    });
    
    // Demonstrate search functionality
    console.log('Testing simple search functionality...');
    const searchResults = processor.searchChunks('language models', chunks);
    console.log(`Found ${searchResults.length} relevant chunks for "language models"\n`);
    
    searchResults.forEach((result, index) => {
      console.log(`Search Result ${index + 1}:`);
      console.log(`Score: ${result.score.toFixed(3)}`);
      console.log(`Content: ${result.chunk.content.substring(0, 150)}...\n`);
    });
    
  } catch (error) {
    console.error('Error during document processing:', error);
  }
}

// Run the demonstration if this file is executed directly
if (require.main === module) {
  demonstrateDocumentProcessing()
    .then(() => console.log('Document processing demonstration completed.'))
    .catch(console.error);
}