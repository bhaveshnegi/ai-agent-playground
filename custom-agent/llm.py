import requests
import json
import re

def clean_json_output(output):
    # Remove ```json and ```
    output = re.sub(r"```json", "", output)
    output = re.sub(r"```", "", output)
    return output.strip()

def safe_parse_json(text):
    try:
        return json.loads(text)
    except:
        # try extracting JSON manually
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
    return None

def call_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3.5:2b",
                "prompt": prompt,
                "stream": False
            }
        )

        raw_output = response.json().get("response", "")

        if not raw_output.strip():
            print("⚠️ EMPTY LLM RESPONSE")
            return None

        print("🔍 RAW LLM OUTPUT:", raw_output)

        cleaned = clean_json_output(raw_output)
        print("CLEANED:", repr(cleaned))

        parsed = safe_parse_json(cleaned)
        print("PARSED:", parsed)

        if parsed is None:
            print("⚠️ JSON parsing failed")
            return None

        return parsed   # ✅ THIS IS CRITICAL

    except Exception as e:
        print("❌ ERROR:", e)
        return None