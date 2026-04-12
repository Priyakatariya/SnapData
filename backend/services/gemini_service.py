from groq import Groq
import os
import re
from dotenv import load_dotenv

# Load env variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_sql(prompt, schema):
    full_prompt = f"""
You are a SQLite SQL expert.

STRICT RULES:
- Use ONLY SQLite syntax
- DO NOT use: EXTRACT, YEAR, MONTH, DATE_PART, WEEKOFYEAR
- Use STRFTIME for date operations:
    STRFTIME('%Y', date)
    STRFTIME('%m', date)
    STRFTIME('%W', date)

- Use ONLY these tables and columns:

employees(id, name, department, salary, hire_date)
products(id, name, category, price, stock)
sales(id, product_id, quantity, total_amount, sale_date)

- DO NOT invent tables
- DO NOT invent columns
- DO NOT guess relationships
- Return ONLY ONE SELECT query
- NO markdown
- NO explanation
- NO multiple queries

Examples:

Question: monthly sales
SQL:
SELECT STRFTIME('%m', sale_date), SUM(total_amount)
FROM sales
GROUP BY STRFTIME('%m', sale_date);

Question: top products by revenue
SQL:
SELECT product_id, SUM(total_amount)
FROM sales
GROUP BY product_id
ORDER BY SUM(total_amount) DESC
LIMIT 5;

User question:
{prompt}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a SQL expert."},
            {"role": "user", "content": full_prompt}
        ]
    )

    sql = response.choices[0].message.content.strip()

    # ✅ CLEAN SQL (correct indentation)
    sql = re.sub(r"```sql|```", "", sql).strip()
    sql = sql.split(";")[0] + ";"

    print("Generated SQL:", sql)

    return sql