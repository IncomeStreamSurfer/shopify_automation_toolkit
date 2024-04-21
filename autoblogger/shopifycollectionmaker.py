import os
import csv
import requests
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Set up Anthropic API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic.api_key = anthropic_api_key

# Shopify store data
shopify_store_url = os.getenv("SHOPIFY_STORE_URL")
shopify_access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

# Function to generate text using Claude API
def generate_text(prompt):
    try:
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=150,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(f"Claude API Response: {response}")
        return response.content[0].text.strip()
    except Exception as e:
        print(f"Error generating text: {str(e)}")
        return None

# Function to create a smart collection using Shopify API
def create_smart_collection(title, handle, body_html, rules):
    url = f"{shopify_store_url}/admin/api/2024-01/smart_collections.json"
    headers = {
        "X-Shopify-Access-Token": shopify_access_token,
        "Content-Type": "application/json"
    }
    data = {
        "smart_collection": {
            "title": title,
            "handle": handle,
            "body_html": body_html,
            "rules": rules
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Shopify API Response: {response.text}")
    if response.status_code == 201:
        print(f"Smart collection created: {title}")
    else:
        print(f"Error creating smart collection: {response.status_code}")

# Main function to process keywords, generate content, and create smart collections
def process_keywords(input_csv, output_csv):
    print(f"Processing input CSV: {input_csv}")
    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        keywords = next(reader)  # Assumes the first row contains the keywords

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Keyword', 'Title', 'Handle', 'Body (HTML)', 'Rules'])

        for keyword in keywords:
            print(f"Processing keyword: {keyword}")
            title_prompt = f"Create one single SEO-Optimized meta title for {keyword}. This is for a business selling blacksmithing supplies. Use words like cheap, affordable, and buy at least once. Just add some words to it that people may search. Do not write anything else."
            title = generate_text(title_prompt)
            print(f"Generated Title: {title}")

            handle_prompt = f"Generate a handle for a smart collection based on the keyword: {keyword}. This is for a business selling blacksmithing supplies. Just put hyphens between the words and replace special letters with hyphens. Do not do anything else."
            handle = generate_text(handle_prompt)
            print(f"Generated Handle: {handle}")

            body_prompt = f"Generate a brief HTML description for a smart collection based on the keyword: {keyword}. This is for a business selling blacksmithing supplies. Just write 300 characters of a <p> description. Do not write anything else."
            body_html = generate_text(body_prompt)
            print(f"Generated Body (HTML): {body_html}")

            rules = [{"column": "tag", "relation": "equals", "condition": keyword}]

            writer.writerow([keyword, title, handle, body_html, str(rules)])

            # Create the smart collection using Shopify API
            create_smart_collection(title, handle, body_html, rules)

    print(f"Content generated and saved to output CSV: {output_csv}")
    print("Smart collections created.")

# Example usage
if __name__ == "__main__":
    input_csv = 'tags.csv'  # Input CSV file containing keywords
    output_csv = 'output.csv'  # Output CSV file to store generated content

    process_keywords(input_csv, output_csv)