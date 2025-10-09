# Retrieval Augmented Generation in TypeScript: Building Intelligent Applications with RAG and Ollama

## Course Overview

This beginner-friendly course teaches you to build a simple but functional Retrieval Augmented Generation (RAG) system using TypeScript and Ollama. Each lesson introduces one core concept, and by the end, you'll have a complete working RAG application.

**Target Audience**: Beginner to intermediate TypeScript developers interested in AI applications  
**Prerequisites**: Basic TypeScript knowledge and familiarity with Node.js  
**Course Duration**: 4 lessons (4-6 hours total)  
**Tools Used**: TypeScript, Node.js, Ollama

---

## Lesson 1: Understanding RAG and Basic Text Generation

**Problem Statement**: AI models have limitations - they can't access new information or your specific documents. How can we make AI responses more relevant and up-to-date by giving them access to external knowledge?

**Learning Objectives**:
- Understand what RAG is and why it's useful for AI applications
- Set up Ollama for local AI text generation
- Create a simple TypeScript project with basic AI text generation
- Learn the three parts of RAG: Retrieval, Augmentation, and Generation

**Key Concepts**:
- What is RAG and why do we need it
- Setting up Ollama and generating text responses
- The basic RAG workflow and components

**Exercises**:
- Install and set up Ollama with a simple model
- Create a TypeScript project that generates text using Ollama

**Quiz Question**: What does RAG stand for?
- A) Rapid Application Generation
- B) Retrieval Augmented Generation ✓
- C) Random Access Generator

**Major Assignment**: Build a simple TypeScript application that can generate text responses using Ollama, demonstrating basic AI integration and understanding of the generation component of RAG.

---

## Lesson 2: Working with Documents and Text Processing

**Problem Statement**: To make AI responses relevant to your specific content, you need to process and prepare your documents. How do we take a document and break it into manageable pieces that an AI can work with?

**Learning Objectives**:
- Learn how to read and process text documents in TypeScript
- Understand why we need to split documents into smaller chunks
- Implement simple document chunking (splitting text into pieces)
- Create a basic document collection that can store multiple text pieces

**Key Concepts**:
- Reading files and processing text content
- Document chunking: breaking text into smaller, manageable pieces
- Storing processed documents in memory

**Exercises**:
- Create a function to read text files and split them into chunks
- Build a simple document store that can hold multiple text pieces

**Quiz Question**: Why do we split documents into smaller chunks for RAG?
- A) To save memory
- B) To make it easier for AI to find relevant information ✓
- C) To make files load faster

**Major Assignment**: Build a document processor that can read text files, split them into logical chunks of around 200-300 words, and store them in a simple array-based collection with basic search functionality.

---

## Lesson 3: Finding Relevant Information (The Retrieval Part)

**Problem Statement**: When a user asks a question, how do we find the most relevant pieces of information from our document collection? We need a way to search through our chunks and find the ones that best match the user's question.

**Learning Objectives**:
- Understand how to compare text similarity using simple methods
- Implement basic keyword-based search in document chunks
- Learn about embeddings and how they represent text meaning
- Create a simple retrieval system that finds relevant document pieces

**Key Concepts**:
- Text similarity and how to measure it
- Keyword search vs. semantic search basics
- Simple embedding generation with Ollama

**Exercises**:
- Build a keyword-based search function for document chunks
- Create a simple similarity scoring system

**Quiz Question**: What is the main goal of the retrieval step in RAG?
- A) To generate new text
- B) To find the most relevant documents for a user's question ✓
- C) To store documents efficiently

**Major Assignment**: Create a retrieval system that can take a user question, search through your document collection, and return the most relevant chunks using both keyword matching and basic similarity scoring.

---

## Lesson 4: Putting It All Together - Complete RAG System

**Problem Statement**: Now that we understand generation, document processing, and retrieval, how do we combine them into a working RAG system that can answer questions using information from our documents?

**Learning Objectives**:
- Combine document processing, retrieval, and generation into one system
- Learn how to create effective prompts that include retrieved context
- Build a simple chat interface that uses your RAG system
- Understand how to improve responses by providing relevant context

**Key Concepts**:
- Integrating all RAG components into a single workflow
- Prompt engineering: how to include retrieved context in AI prompts
- Creating a simple user interface for your RAG system

**Exercises**:
- Connect your retrieval system to Ollama for context-aware generation
- Build a simple command-line chat interface

**Quiz Question**: In a RAG system, what happens right before the AI generates a response?
- A) Documents are processed and stored
- B) Relevant context is retrieved and added to the prompt ✓
- C) The user interface is updated

**Major Assignment**: Create a complete RAG application that combines your document processor, retrieval system, and Ollama generation into a working chat system where users can ask questions and get answers based on your document collection.

---

## Course Completion Outcomes

By completing this course, you will have:

- **Built a working RAG system** using TypeScript and Ollama that can answer questions based on your documents
- **Understood the core concepts** of document processing, retrieval, and AI generation
- **Created a practical application** that demonstrates how AI can be enhanced with external knowledge
- **Gained foundational skills** in AI application development using accessible tools and techniques

**Next Steps**: Once comfortable with these basics, explore advanced topics like vector databases, embedding optimization, and production deployment strategies.

**Portfolio Project**: Your completed RAG application serves as a solid foundation for more complex AI projects and demonstrates practical understanding of how modern AI systems work with external knowledge sources.