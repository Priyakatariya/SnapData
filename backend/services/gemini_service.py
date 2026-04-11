from groq import Groq
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_sql(prompt, schema):
    full_prompt = f"""
You are a SQL expert.

STRICT RULES:
- Use ONLY tables and columns from the schema below
- DO NOT invent column names
- DO NOT guess relationships
- Use simple queries when possible
- Avoid subqueries unless necessary
- If unsure, return a basic SELECT query

Database schema:
{schema}

User question:
{prompt}

Return ONLY valid SQL query. No explanation.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a SQL expert."},
            {"role": "user", "content": full_prompt}
        ]
    )

    sql = response.choices[0].message.content.strip()

    print("Generated SQL:", sql)  # 🔍 Debug

    return sql