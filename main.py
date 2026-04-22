# Popular Usecases RAG
# Enhanced Content Creation
# Customer feedback analysis
# Market Intelligence
# Personalized Reccomendations
# Dialogue Systems and Chatbots


from aws_crawler import AWSProductCrawler
from database import ChromaInstance
from aws_scraper import AWSScraper
from llm_factory import LLMFactory

import requests, json, os
from dotenv import load_dotenv
load_dotenv()

chromaDB = ChromaInstance()
aws_scraper = AWSScraper()
aws_crawler = AWSProductCrawler(chromaDB, aws_scraper)
factory = LLMFactory()

agent = factory.gemini()

# aws_crawler.populateIndex()

query = "How should I Deploy server-side rendered Apps"
result = chromaDB.query("How should I Deploy server-side rendered Apps")["documents"][0]


agentResponse = agent.query(query=query, context=result)

print(agentResponse)
