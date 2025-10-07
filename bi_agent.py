# bi_agent.py

from logic import get_gemini_vision_pro_model
from google.cloud import bigquery
import os

def generate_bigquery_query(prompt: str):
    """
    Generates a BigQuery query from a natural language prompt.
    """
    # AI Prompt tailored for BigQuery generation
    full_prompt = f"""
    Based on the following prompt, generate a BigQuery SQL query that answers the user's question.
    The data is stored in a table called `printify_data.orders`.
    The table has the following columns: `id`, `status`, `total_price`, `created_at`.
    The `created_at` column is a timestamp.
    
    Prompt: "{prompt}"
    
    Return the response as a JSON object with a "query" key.
    """

    try:
        model = get_gemini_vision_pro_model()
        response = model.generate_content([full_prompt])
        
        # Extracting and parsing the JSON from the response
        import json
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        query = json.loads(clean_response)
        
        return query
    except Exception as e:
        print(f"An error occurred while generating BigQuery query: {e}")
        return {"error": f"Failed to generate BigQuery query. Raw response: {str(e)}"}

def run_bigquery_query(query: str):
    """
    Runs a BigQuery query and returns the results.
    """
    try:
        client = bigquery.Client()
        query_job = client.query(query)
        results = query_job.result()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"An error occurred while running BigQuery query: {e}")
        return {"error": str(e)}
