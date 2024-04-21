import csv
import anthropic
import openai
from time import sleep
import requests

# Set up Anthropic API key
anthropic_api_key = "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"
anthropic.api_key = anthropic_api_key

# Set up OpenAI API key
openai.api_key = "sk-proj-m50BQ0JAB2PWVO84kr1MT3BlbkFJA8tvey0dcbG7zbWx94KP"

# Function to generate guest post using Claude AI
def generate_guest_post(topic, keywords, word_count):
    prompt = f"Respond in markdown. Can Please write a comprehensive guest post about {topic}, focusing on the following keywords: {keywords}. Ensure that you use a lot of formatting such as tables and correcet heading tags, with only the first header being h1. Use h2 and h3 tags throughout the article. Make the post as detailed as possible, with 30 paragraphs."
    
    try:
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        guest_post_text = response.content[0].text
        print(f"Generated guest post:\n{guest_post_text}\n")
        return guest_post_text
    except Exception as e:
        print(f"Error generating guest post: {str(e)}")
        return None

# Function to generate image using DALL-E API
def generate_image(keywords):
    prompt = f"A general image representing the following keywords: {keywords}"
    
    for _ in range(15):
        try:
            response = openai.Image.create(
                model = "dall-e-3",
                prompt=prompt,
                n=1,
                size="1792x1024"
            )
            return response['data'][0]['url']
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            sleep(5)  # Wait for 5 seconds before retrying
    
    return None

# Read CSV file
with open('Content Request - Content - April Month (1)[1].csv', 'r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Create output CSV file
with open('output.csv', 'w', newline='') as file:
    fieldnames = ['Guest Post', 'Image URL']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    
    image_count = 1
    
    for row in rows:
        topic = row['Topics']
        keywords = row['Target Keywords']
        word_count = row['Word Count']
        
        # Generate guest post
        guest_post = generate_guest_post(topic, keywords, word_count)
        
        if guest_post:
            # Generate image based on niche keywords
            image_url = generate_image(keywords)
            
            if image_url:
                # Download and save the image
                image_filename = f"{image_count}.jpg"
                response = requests.get(image_url)
                with open(image_filename, 'wb') as image_file:
                    image_file.write(response.content)
                
                image_count += 1
            else:
                image_url = "N/A"
            
            # Write guest post and image URL to output CSV
            writer.writerow({'Guest Post': guest_post, 'Image URL': image_url})
        else:
            print(f"Failed to generate guest post for topic: {topic}")

print("Guest posts and images generated successfully.")