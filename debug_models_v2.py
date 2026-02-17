
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

models_to_test = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-001',
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro',
    'gemini-1.0-pro',
    'gemini-2.0-flash-exp',
]

api_versions = ['v1beta', 'v1']

with open('model_test_results.txt', 'w') as f:
    for version in api_versions:
        f.write(f"Testing API version: {version}\n")
        try:
            client = genai.Client(api_key=api_key, http_options={'api_version': version})
        except Exception as e:
            f.write(f"  Failed to init client: {e}\n")
            continue
            
        for model in models_to_test:
            f.write(f"  Testing model: {model}\n")
            try:
                response = client.models.generate_content(
                    model=model,
                    contents='Hello'
                )
                f.write(f"    SUCCESS! Response: {response.text[:50]}...\n")
                f.write(f"    WORKING CONFIG: Model={model}, Version={version}\n")
            except Exception as e:
                f.write(f"    Failed: {e}\n")
