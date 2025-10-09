# Document Processing Solution

This solution demonstrates document processing and text chunking capabilities for RAG systems using TypeScript.

## Features

- **Document Processing**: Read and process text files with proper validation
- **Text Chunking**: Split documents into manageable chunks with configurable size and overlap
- **Search Functionality**: Basic keyword-based search through document chunks
- **Type Safety**: Full TypeScript implementation with comprehensive interfaces
- **Error Handling**: Robust error handling for various failure scenarios
- **Testing**: Comprehensive test suite covering core functionality

## Project Structure

```
src/
├── index.ts                 # Main demonstration application
├── types/                   # TypeScript interface definitions
│   └── index.ts
├── services/                # Core business logic
│   └── DocumentProcessor.ts # Document processing service
├── utils/                   # Utility functions
│   └── validation.ts        # Input validation and sanitization
└── __tests__/              # Test files
    └── DocumentProcessor.test.ts
```

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Run the demonstration**:
   ```bash
   npm run dev
   ```

3. **Run tests**:
   ```bash
   npm test
   ```

## Configuration

The application supports configuration through environment variables:

- `CHUNK_SIZE`: Maximum size for text chunks (default: 300)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `MAX_FILE_SIZE_MB`: Maximum file size in MB (default: 10)
- `SUPPORTED_EXTENSIONS`: Comma-separated list of file extensions (default: .txt,.md)

## Key Concepts Demonstrated

- **Text Sanitization**: Cleaning and normalizing text for processing
- **Intelligent Chunking**: Breaking text at sentence boundaries when possible
- **Metadata Tracking**: Recording chunk position, word count, and relationships
- **Search Implementation**: Basic relevance scoring for text search
- **Error Categorization**: Different error types for appropriate handling

## Next Steps

This foundation prepares for more advanced RAG features:
- Vector embeddings for semantic search
- Database storage for large document collections
- Advanced chunking strategies
- Integration with retrieval systems