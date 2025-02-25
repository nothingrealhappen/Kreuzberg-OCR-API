#!/usr/bin/env python3
"""
Test script for the Kreuzberg OCR API.
This script demonstrates how to use the API to extract text from a PDF file.
"""

import requests
import argparse
import os
import json
import mimetypes

def extract_text(file_path, api_url="http://localhost:8000/extract_text", language=None):
    """
    Extract text from a file using the OCR API.
    
    Args:
        file_path (str): Path to the PDF or image file
        api_url (str): URL of the OCR API endpoint
        language (str, optional): Language code for OCR
        
    Returns:
        dict: API response containing the extracted text
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    
    # Check if file type is supported
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif']:
        print(f"Error: Unsupported file type '{file_ext}'. Only PDF and image files are supported.")
        return None
    
    # Prepare the file for upload
    files = {"file": open(file_path, "rb")}
    
    # Prepare parameters
    data = {}
    if language:
        data["language"] = language
    
    # Make the API request
    try:
        response = requests.post(api_url, files=files, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None
    finally:
        files["file"].close()

def main():
    parser = argparse.ArgumentParser(description="Test the Kreuzberg OCR API")
    parser.add_argument("file", help="Path to the PDF or image file to process")
    parser.add_argument("--url", default="http://localhost:8000/extract_text", 
                        help="URL of the OCR API endpoint (default: http://localhost:8000/extract_text)")
    parser.add_argument("--language", help="Language code for OCR (e.g., eng, deu, fra, spa)")
    parser.add_argument("--output", help="Path to save the extracted text (optional)")
    
    args = parser.parse_args()
    
    print(f"Extracting text from '{args.file}'...")
    result = extract_text(args.file, args.url, args.language)
    
    if result:
        print("\nExtracted Text:")
        print("-" * 40)
        print(result["text"])
        print("-" * 40)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"\nText saved to '{args.output}'")
            
        # Also save the full JSON response
        json_output = f"{os.path.splitext(args.output)[0] if args.output else 'output'}.json"
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Full response saved to '{json_output}'")

if __name__ == "__main__":
    main() 