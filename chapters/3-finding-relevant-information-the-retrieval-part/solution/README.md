# Retrieval System Solution

This solution demonstrates document retrieval and similarity search capabilities for RAG systems using TypeScript.

## Features

- **Text Similarity**: Multiple algorithms for measuring text similarity including cosine similarity and Jaccard index
- **Keyword Search**: Enhanced keyword-based search with TF-IDF scoring and relevance ranking
- **Embedding Generation**: Integration with Ollama for generating semantic embeddings
- **Semantic Search**: Vector-based similarity search using embeddings for better context understanding
- **Production Ready**: Comprehensive error handling, validation, and performance optimization
- **Testing**: Full test suite covering all similarity algorithms and search functionality

## Project Structure

```
src/
├── index.ts                    # Main demonstration application
├── types/                      # TypeScript interface definitions
│   └── index.ts
├── services/                   # Core business logic
│   ├── RetrievalService.ts     # Main retrieval orchestration
│   ├── SimilarityService.ts    # Text similarity algorithms
│   └── EmbeddingService.ts     # Ollama embedding integration
├── utils/                      # Utility functions
│   ├── textProcessing.ts       # Text preprocessing and analysis
│   └── validation.ts           # Input validation
└── __tests__/                  # Test files
    ├── SimilarityService.test.ts
    └── RetrievalService.test.ts
```

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

3. **Start Ollama (for embedding functionality)**:
   ```bash
   ollama serve
   ollama pull nomic-embed-text
   ```

4. **Run the demonstration**:
   ```bash
   npm run dev
   ```

5. **Run tests**:
   ```bash
   npm test
   ```

## Key Concepts Demonstrated

- **Text Similarity Algorithms**: Cosine similarity, Jaccard index, and TF-IDF scoring
- **Keyword Processing**: Stemming, stop word removal, and term frequency analysis
- **Embedding Generation**: Converting text to numerical vectors for semantic analysis
- **Similarity Search**: Finding relevant documents using both keyword and semantic approaches
- **Performance Optimization**: Efficient algorithms and caching strategies

## Configuration Options

- `SIMILARITY_THRESHOLD`: Minimum similarity score for results (0.0-1.0)
- `MAX_RESULTS`: Maximum number of search results to return
- `EMBEDDING_MODEL`: Ollama model for generating embeddings
- `SEARCH_TIMEOUT`: Timeout for search operations in milliseconds

## Next Steps

This retrieval foundation enables advanced RAG features:
- Vector database integration for large-scale deployments
- Hybrid search combining keyword and semantic approaches
- Query expansion and refinement techniques
- Real-time indexing and incremental updates