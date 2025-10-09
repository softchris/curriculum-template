# Chapter 1 Solution: Understanding RAG and Basic Text Generation

This directory contains the complete working solution for Chapter 1, demonstrating basic text generation using Ollama as the foundation for understanding RAG systems.

## 🚀 Quick Start

### Prerequisites

1. **Node.js** (v18 or higher)
2. **Ollama** installed and running locally
3. **Basic TypeScript knowledge**

### Installation

1. Clone or download this chapter solution
2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```

4. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

5. Pull a model (if not already available):
   ```bash
   ollama pull llama3.2
   ```

### Running the Solution

```bash
# Development mode (with TypeScript compilation)
npm run dev

# Build and run production version
npm run build
npm start

# Run tests
npm test
```

## 📁 Project Structure

```
src/
├── index.ts                 # Main application entry point
├── types/                   # TypeScript type definitions
│   └── index.ts            # Core interfaces and types
├── services/               # Business logic services
│   └── OllamaTextGenerator.ts  # Ollama integration service
├── utils/                  # Utility functions
│   └── validation.ts       # Input validation helpers
└── __tests__/              # Test files
    └── OllamaTextGenerator.test.ts  # Service tests
```

## 🧠 Key Concepts Demonstrated

### 1. Ollama Integration
The solution shows how to:
- Configure connection to local Ollama instance
- Send text generation requests
- Handle responses and errors properly
- Implement proper TypeScript types

### 2. Production-Ready Code Structure
- **Type Safety**: Comprehensive TypeScript interfaces
- **Error Handling**: Robust error handling with custom error types
- **Validation**: Input validation for all user inputs
- **Testing**: Unit tests for core functionality
- **Configuration**: Environment-based configuration

### 3. RAG Foundation
While this chapter focuses on the "Generation" component, the code structure prepares for:
- **Modular Design**: Easy to extend with retrieval and augmentation
- **Context Handling**: System prompts and context preparation
- **Response Processing**: Structured response handling

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.2` | Model to use for generation |
| `APP_PORT` | `3000` | Application port (future use) |
| `LOG_LEVEL` | `info` | Logging level |

### Generation Options

The `OllamaTextGenerator` supports these options:

```typescript
interface GenerationOptions {
  maxTokens?: number;      // Maximum tokens to generate (1-4096)
  temperature?: number;    // Randomness level (0.0-2.0)
  systemPrompt?: string;   // System context for the AI
  stream?: boolean;        // Stream response (future feature)
}
```

## 📖 How It Works

### 1. Basic Text Generation
```typescript
const generator = new OllamaTextGenerator(config);
const response = await generator.generate("Your question here");
console.log(response.content);
```

### 2. Context-Aware Generation (RAG Preview)
```typescript
const context = "Your retrieved document content...";
const question = "What does the document say about...?";
const prompt = `Context: ${context}\n\nQuestion: ${question}`;

const response = await generator.generate(prompt, {
  systemPrompt: "Answer based on the provided context."
});
```

## 🧪 Testing

Run the test suite to verify functionality:

```bash
npm test
```

Tests cover:
- Configuration validation
- Text generation functionality
- Error handling scenarios
- Response format verification

## 🔍 Understanding the Output

When you run the solution, you'll see:

1. **Basic Generation**: Simple AI responses without specific context
2. **Context-Aware Generation**: Responses that use provided context (simulating RAG)
3. **Response Metadata**: Information about generation time and token usage
4. **Error Handling**: Graceful handling of connection issues

## 🎯 Learning Outcomes

After running this solution, you should understand:

- How to integrate TypeScript applications with Ollama
- The importance of proper error handling in AI applications
- How to structure code for production readiness
- The foundation for building more complex RAG systems
- The difference between basic and context-aware text generation

## 🔄 Next Steps

This solution prepares you for Chapter 2, where you'll learn:
- Document processing and chunking
- Building a document store
- Preparing for the "Retrieval" component of RAG

## 🐛 Troubleshooting

### Common Issues

1. **"Cannot connect to Ollama"**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is available: `ollama list`
   - Verify the URL in your `.env` file

2. **"Model not found"**
   - Pull the model: `ollama pull llama3.2`
   - Or change the model in `.env` to one you have

3. **TypeScript Errors**
   - Install dependencies: `npm install`
   - Check TypeScript version: `npx tsc --version`

4. **Port Already in Use**
   - Change the port in `.env`
   - Or stop other applications using the port

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [RAG Architecture Patterns](https://docs.llamaindex.ai/en/stable/getting_started/concepts.html)