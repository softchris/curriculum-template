import * as fs from 'fs';
import * as path from 'path';
import { FileInfo, ProcessingError } from '../types';

export function validateFile(filePath: string): FileInfo {
  if (!filePath || typeof filePath !== 'string') {
    throw {
      type: 'PROCESSING_ERROR',
      message: 'File path must be a non-empty string',
      details: { filePath }
    } as ProcessingError;
  }

  if (!fs.existsSync(filePath)) {
    throw {
      type: 'FILE_NOT_FOUND',
      message: `File not found: ${filePath}`,
      details: { filePath }
    } as ProcessingError;
  }

  const stats = fs.statSync(filePath);
  const extension = path.extname(filePath).toLowerCase();
  const name = path.basename(filePath);

  return {
    path: filePath,
    size: stats.size,
    extension,
    name
  };
}

export function validateNonEmptyString(value: string, fieldName: string): boolean {
  if (!value || typeof value !== 'string') {
    throw {
      type: 'PROCESSING_ERROR',
      message: `${fieldName} must be a non-empty string`,
      details: { value, fieldName }
    } as ProcessingError;
  }

  if (value.trim().length === 0) {
    throw {
      type: 'PROCESSING_ERROR',
      message: `${fieldName} cannot be empty or only whitespace`,
      details: { value, fieldName }
    } as ProcessingError;
  }

  return true;
}

export function validateChunkSize(chunkSize: number): boolean {
  if (typeof chunkSize !== 'number' || chunkSize <= 0) {
    throw {
      type: 'PROCESSING_ERROR',
      message: 'Chunk size must be a positive number',
      details: { chunkSize }
    } as ProcessingError;
  }

  if (chunkSize < 50) {
    throw {
      type: 'PROCESSING_ERROR',
      message: 'Chunk size must be at least 50 characters',
      details: { chunkSize }
    } as ProcessingError;
  }

  return true;
}

export function sanitizeText(text: string): string {
  return text
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .replace(/\t/g, ' ')
    .replace(/[ ]{2,}/g, ' ')
    .trim();
}