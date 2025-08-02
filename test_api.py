import os
import google.generativeai as genai
from dotenv import load_dotenv

print("Attempting to test the Google Gemini API...")

try:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    print("API configured successfully. Sending a test prompt...")
    response = model.generate_content("Tell me a short, one-sentence joke.")

    print("\nSUCCESS! The API key works.")
    print("Response:", response.text.strip())

except Exception as e:
    print("\nFAILED! There is a problem with your API key or connection.")
    print("Error Details:", e)