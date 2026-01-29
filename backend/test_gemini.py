"""
Script to test Gemini API and list available models
"""
import google.generativeai as genai
import os

# Configure API
api_key = "AIzaSyAmv1ESjsIAJ8_Nbi2hPhZJIZ4fE7wm3mU"
genai.configure(api_key=api_key)

print("=== Available Gemini Models ===\n")

try:
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"Model: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Supported: {model.supported_generation_methods}")
            print()
except Exception as e:
    print(f"Error listing models: {e}")

print("\n=== Testing model names ===\n")

# Test different model names
test_models = [
    'gemini-pro',
    'gemini-1.5-pro',
    'gemini-1.5-flash',
    'gemini-1.5-pro-latest',
    'gemini-1.5-flash-latest',
]

for model_name in test_models:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello'")
        print(f"✅ {model_name}: SUCCESS - {response.text[:50]}")
    except Exception as e:
        print(f"❌ {model_name}: FAILED - {str(e)[:100]}")
