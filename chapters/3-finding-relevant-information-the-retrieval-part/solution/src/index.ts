import { RetrievalService } from './services/RetrievalService';
import { SimilarityService } from './services/SimilarityService';
import { DocumentChunk, SearchQuery, RetrievalConfig } from './types';

async function demonstrateRetrievalSystem(): Promise<void> {
  console.log('Starting Retrieval System Demonstration...\n');
  
  // Configuration for the retrieval system
  const config: RetrievalConfig = {
    similarityThreshold: 0.1,
    maxResults: 5,
    embeddingModel: 'nomic-embed-text',
    ollamaBaseUrl: 'http://localhost:11434'
  };
  
  const retrievalService = new RetrievalService(config);
  const similarityService = new SimilarityService();
  
  // Sample document chunks for demonstration
  const sampleChunks: DocumentChunk[] = [
    {
      id: 'chunk_1',
      content: 'Retrieval Augmented Generation (RAG) combines information retrieval with text generation. It allows AI models to access external knowledge sources and provide more accurate, contextual responses.',
      source: 'rag-overview.txt',
      metadata: {
        position: 0,
        wordCount: 24,
        characterCount: 176,
        chunkIndex: 0,
        keywords: ['retrieval', 'augmented', 'generation', 'information', 'models', 'knowledge']
      }
    },
    {
      id: 'chunk_2',
      content: 'Text similarity algorithms measure how similar two pieces of text are. Common approaches include cosine similarity, which uses vector representations, and Jaccard similarity, which compares sets of words.',
      source: 'similarity-methods.txt',
      metadata: {
        position: 200,
        wordCount: 28,
        characterCount: 201,
        chunkIndex: 1,
        keywords: ['similarity', 'algorithms', 'cosine', 'jaccard', 'vector', 'words']
      }
    },
    {
      id: 'chunk_3',
      content: 'Embeddings are numerical representations of text that capture semantic meaning. They enable computers to understand that words like "car" and "automobile" are related, even if they don\'t share letters.',
      source: 'embeddings-explained.txt',
      metadata: {
        position: 150,
        wordCount: 26,
        characterCount: 189,
        chunkIndex: 2,
        keywords: ['embeddings', 'numerical', 'semantic', 'meaning', 'computers', 'related']
      }
    },
    {
      id: 'chunk_4',
      content: 'Vector databases store and index high-dimensional vectors efficiently. They enable fast similarity search across millions of embeddings, making them essential for large-scale RAG applications.',
      source: 'vector-databases.txt',
      metadata: {
        position: 300,
        wordCount: 22,
        characterCount: 170,
        chunkIndex: 3,
        keywords: ['vector', 'databases', 'dimensional', 'similarity', 'embeddings', 'applications']
      }
    },
    {
      id: 'chunk_5',
      content: 'Keyword search looks for exact matches of specific words or phrases in documents. While simple and fast, it can miss semantically related content that uses different terminology.',
      source: 'search-methods.txt',
      metadata: {
        position: 100,
        wordCount: 25,
        characterCount: 168,
        chunkIndex: 4,
        keywords: ['keyword', 'search', 'matches', 'documents', 'semantically', 'terminology']
      }
    }
  ];
  
  console.log(`Loaded ${sampleChunks.length} sample document chunks\n`);
  
  // Demonstrate different similarity algorithms
  await demonstrateSimilarityAlgorithms(similarityService, sampleChunks);
  
  // Demonstrate retrieval with different queries
  await demonstrateRetrievalQueries(retrievalService, sampleChunks);
  
  // Show retrieval statistics
  await demonstrateRetrievalStatistics(retrievalService, sampleChunks);
}

async function demonstrateSimilarityAlgorithms(
  similarityService: SimilarityService,
  chunks: DocumentChunk[]
): Promise<void> {
  console.log('=== Similarity Algorithm Comparison ===\n');
  
  const query = 'How do vector representations work?';
  const testChunk = chunks[1]; // Text similarity chunk
  
  console.log(`Query: "${query}"`);
  console.log(`Comparing against: "${testChunk.content.substring(0, 80)}..."\n`);
  
  // Test different similarity algorithms
  const cosineScore = similarityService.calculateCosineSimilarity(query, testChunk.content);
  const jaccardScore = similarityService.calculateJaccardSimilarity(query, testChunk.content);
  const tfidfScore = similarityService.calculateTfIdfSimilarity(
    query, 
    testChunk.content, 
    chunks.map(c => c.content)
  );
  
  console.log(`Cosine Similarity: ${(cosineScore * 100).toFixed(2)}%`);
  console.log(`Jaccard Similarity: ${(jaccardScore * 100).toFixed(2)}%`);
  console.log(`TF-IDF Similarity: ${(tfidfScore * 100).toFixed(2)}%\n`);
  
  // Show best algorithm recommendation
  const bestAlgorithm = similarityService.getBestSimilarityAlgorithm(query, chunks);
  console.log(`Recommended algorithm for this query: ${bestAlgorithm}\n`);
}

async function demonstrateRetrievalQueries(
  retrievalService: RetrievalService,
  chunks: DocumentChunk[]
): Promise<void> {
  console.log('=== Retrieval Query Demonstrations ===\n');
  
  const queries = [
    'What is RAG and how does it work?',
    'Explain vector similarity search',
    'How do embeddings capture meaning?'
  ];
  
  for (const queryText of queries) {
    console.log(`Query: "${queryText}"`);
    
    const query: SearchQuery = {
      text: queryText,
      options: {
        maxResults: 3,
        similarityThreshold: 0.05,
        algorithm: 'hybrid'
      }
    };
    
    try {
      const results = await retrievalService.searchSimilarChunks(query, chunks);
      
      if (results.length === 0) {
        console.log('No relevant chunks found.\n');
        continue;
      }
      
      console.log(`Found ${results.length} relevant chunks:\n`);
      
      results.forEach((result, index) => {
        console.log(`  ${index + 1}. Score: ${(result.score * 100).toFixed(1)}%`);
        console.log(`     Source: ${result.chunk.source}`);
        console.log(`     Content: ${result.chunk.content.substring(0, 120)}...`);
        console.log(`     Explanation: ${result.explanation}`);
        
        if (result.highlights && result.highlights.length > 0) {
          console.log(`     Highlights: "${result.highlights[0]}"`);
        }
        console.log('');
      });
      
    } catch (error) {
      console.error(`Error processing query: ${error}`);
    }
    
    console.log('---\n');
  }
}

async function demonstrateRetrievalStatistics(
  retrievalService: RetrievalService,
  chunks: DocumentChunk[]
): Promise<void> {
  console.log('=== Retrieval Statistics ===\n');
  
  const query: SearchQuery = {
    text: 'similarity search algorithms',
    options: {
      maxResults: 10,
      similarityThreshold: 0.01,
      algorithm: 'hybrid'
    }
  };
  
  try {
    const results = await retrievalService.searchSimilarChunks(query, chunks);
    const stats = retrievalService.getRetrievalStatistics(results);
    
    console.log(`Total Results: ${stats.totalResults}`);
    console.log(`Average Score: ${(stats.averageScore * 100).toFixed(2)}%`);
    
    console.log('\nScore Distribution:');
    console.log(`  High (70%+): ${stats.scoreDistribution.high} chunks`);
    console.log(`  Medium (30-70%): ${stats.scoreDistribution.medium} chunks`);
    console.log(`  Low (<30%): ${stats.scoreDistribution.low} chunks`);
    
    console.log('\nAlgorithm Usage:');
    for (const [algorithm, count] of stats.algorithmDistribution.entries()) {
      console.log(`  ${algorithm}: ${count} results`);
    }
    
  } catch (error) {
    console.error(`Error generating statistics: ${error}`);
  }
}

// Run the demonstration if this file is executed directly
if (require.main === module) {
  demonstrateRetrievalSystem()
    .then(() => console.log('\nRetrieval system demonstration completed.'))
    .catch(console.error);
}