# Popular Usecases RAG
# Enhanced Content Creation
# Customer feedback analysis
# Market Intelligence
# Personalized Reccomendations
# Dialogue Systems and Chatbots


from aws_crawler import AWSProductCrawler
from database import ChromaInstance
from aws_scraper import AWSScraper
import requests, json, os
from dotenv import load_dotenv
load_dotenv()

chromaDB = ChromaInstance()
aws_scraper = AWSScraper()
aws_crawler = AWSProductCrawler(chromaDB, aws_scraper)

geminiAPIKey = os.getenv("GEMINI_API_KEY")

# aws_crawler.populateIndex()
query = "How should I Deploy server-side rendered Apps"
result = chromaDB.query("How should I Deploy server-side rendered Apps")["documents"][0]

headers = {
    'x-goog-api-key':geminiAPIKey,
    'Content-Type': 'application/json'
}

data = {
    "contents":[
        {"parts":[
            {"text":f"context:{result}\n rules: Don't directly mention the context, give short responses\n query:{query}"}
        ]}
    ]
}

postreq = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent', data=json.dumps(data), headers=headers)


print(postreq.text)
