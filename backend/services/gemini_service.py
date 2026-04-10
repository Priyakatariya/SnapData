import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def build_prompt(question: str, schema: str) -> str:
    return f"""
You are an expert SQL assistant for a data analytics tool called Talk2Data AI.

Given the following database schema:
{schema}

Convert this natural language question into a valid SQL query:
"{question}"

Rules:
- Only return SELECT statements. Never return INSERT, UPDATE, DELETE, DROP, or DDL.
- Use proper SQL syntax compatible with SQLite.
- Do not use markdown code blocks in the SQL output.
- Return a JSON object with exactly these fields:
  {{
    "sql": "<the SQL query>",
    "explanation": "<one paragraph plain-english explanation of what the query does and what the result means>",
    "confidence": <a float between 0.0 and 1.0 representing your confidence this SQL answers the question correctly>
  }}
"""


async def generate_sql(question: str, schema: str) -> dict:
    """
    Calls Gemini API to convert a natural language question into SQL.
    Returns dict with keys: sql, explanation, confidence
    """
    prompt = build_prompt(question, schema)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
    )
    raw = response.text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    parsed = json.loads(raw.strip())

    return {
        "sql": parsed.get("sql", ""),
        "explanation": parsed.get("explanation", ""),
        "confidence": float(parsed.get("confidence", 0.5)),
    }
