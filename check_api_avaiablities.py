from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

print("--- Checking Available Models ---")

try:
    for m in client.models.list():
        print(f"\nModel: {m.name}")
        if hasattr(m, 'supported_actions'):
             print(f"   Supported Actions: {m.supported_actions}")
        

        try:
            print(f"   Details: {m.model_dump_json(exclude_none=True)}")
        except:
            pass

except Exception as e:
    print(f"Error: {e}")