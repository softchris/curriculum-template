import { GenerationError } from '../types/index.js';

/**
 * Validates that a string is not empty and contains meaningful content
 * @param value - The string to validate
 * @param fieldName - Name of the field for error messages
 * @returns true if valid
 * @throws GenerationError if validation fails
 */
export function validateNonEmptyString(value: string, fieldName: string): boolean {
  if (!value || typeof value !== 'string') {
    throw {
      type: 'VALIDATION_ERROR',
      message: `${fieldName} must be a non-empty string`,
      details: { value, fieldName }
    } as GenerationError;
  }
  
  if (value.trim().length === 0) {
    throw {
      type: 'VALIDATION_ERROR',
      message: `${fieldName} cannot be empty or only whitespace`,
      details: { value, fieldName }
    } as GenerationError;
  }
  
  return true;
}

/**
 * Validates URL format for Ollama endpoints
 * @param url - The URL to validate
 * @returns true if valid
 * @throws GenerationError if validation fails
 */
export function validateUrl(url: string): boolean {
  validateNonEmptyString(url, 'URL');
  
  try {
    new (globalThis as any).URL(url);
    return true;
  } catch {
    throw {
      type: 'VALIDATION_ERROR',
      message: 'Invalid URL format',
      details: { url }
    } as GenerationError;
  }
}

/**
 * Validates numeric ranges for generation parameters
 * @param value - The number to validate
 * @param min - Minimum allowed value
 * @param max - Maximum allowed value
 * @param fieldName - Name of the field for error messages
 * @returns true if valid
 * @throws GenerationError if validation fails
 */
export function validateNumericRange(
  value: number, 
  min: number, 
  max: number, 
  fieldName: string
): boolean {
  if (typeof value !== 'number' || isNaN(value)) {
    throw {
      type: 'VALIDATION_ERROR',
      message: `${fieldName} must be a valid number`,
      details: { value, fieldName }
    } as GenerationError;
  }
  
  if (value < min || value > max) {
    throw {
      type: 'VALIDATION_ERROR',
      message: `${fieldName} must be between ${min} and ${max}`,
      details: { value, min, max, fieldName }
    } as GenerationError;
  }
  
  return true;
}