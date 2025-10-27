#!/usr/bin/env python3
# Script to switch between OpenAI and Hugging Face engines

import os

def switch_to_huggingface():
    """Switch to using Hugging Face models"""
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    # Remove any existing USE_HUGGINGFACE line
    lines = [line for line in lines if not line.startswith('USE_HUGGINGFACE=')]
    
    # Add the new line
    lines.append('USE_HUGGINGFACE=true\n')
    
    with open('.env', 'w') as f:
        f.writelines(lines)
    
    print("Switched to Hugging Face models")
    print("Note: Hugging Face models may be slower and have different capabilities")

def switch_to_openai():
    """Switch back to using OpenAI models"""
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    # Remove any existing USE_HUGGINGFACE line
    lines = [line for line in lines if not line.startswith('USE_HUGGINGFACE=')]
    
    # Add the new line
    lines.append('USE_HUGGINGFACE=false\n')
    
    with open('.env', 'w') as f:
        f.writelines(lines)
    
    print("Switched to OpenAI models")

if __name__ == "__main__":
    print("AI Engine Switcher")
    print("1. Switch to Hugging Face (no payment required)")
    print("2. Switch to OpenAI (requires API key with quota)")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        switch_to_huggingface()
    elif choice == "2":
        switch_to_openai()
    else:
        print("Invalid choice")