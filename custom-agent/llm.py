import requests
import json
import re

def clean_json_output(output):
    # Remove ```json and ```
    output = re.sub(r"```json", "", output)
    output = re.sub(r"```", "", output)
    return output.strip()

def call_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3.5:0.8b",
                "prompt": prompt,
                "stream": False
            }
        )

        raw_output = response.json()["response"]

        print("🔍 RAW LLM OUTPUT:", raw_output)

        cleaned_output = clean_json_output(raw_output)

        print("🧹 CLEANED OUTPUT:", cleaned_output)

        return json.loads(cleaned_output)

    except Exception as e:
        print("❌ LLM ERROR:", e)
        return None