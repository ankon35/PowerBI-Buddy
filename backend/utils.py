import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_dataset(headers):
    prompt = f"""
You are a data expert. A user has uploaded a CSV file with the following column headers:
{headers}

1. Categorize the dataset (e.g., Banking, E-commerce, Healthcare, etc.).
2. Suggest up to 3 dashboard pages (names).
3. Recommend what each dashboard should display.
4. Suggest key business metrics based on dataset category.
5. Provide 3 useful slicers/filters (e.g., Date, Region).
6. Recommend ideal Power BI visuals for each dashboard.
7. Suggest DAX formulas for extracting the key metrics.

Respond ONLY in this valid JSON format (no extra text):

{{
  "category": "...",
  "recommended_pages": [
    {{
      "name": "...",
      "description": "...",
      "visuals": ["...", "..."]
    }}
  ],
  "key_metrics": ["...", "..."],
  "suggested_filters": ["...", "..."],
  "dax_formulas": [
    {{
      "metric": "...",
      "dax": "..."
    }}
  ]
}}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Extract the first full JSON block using regex
        json_str = re.search(r'{[\s\S]+}', text).group()

        data = json.loads(json_str)
        return data

    except Exception as e:
        print("Gemini error:", e)
        return {
            "category": "Unknown",
            "recommended_pages": [],
            "key_metrics": [],
            "suggested_filters": [],
            "dax_formulas": []
        }
