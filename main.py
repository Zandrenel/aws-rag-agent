# Popular Usecases RAG
# Enhanced Content Creation
# Customer feedback analysis
# Market Intelligence
# Personalized Reccomendations
# Dialogue Systems and Chatbots

from crawler.aws_crawler import AWSProductCrawler
from db.database import ChromaInstance
from crawler.aws_scraper import AWSScraper
from llm.llm_factory import LLMFactory

import requests, json, os
from dotenv import load_dotenv
load_dotenv()

chromaDB = ChromaInstance()
aws_scraper = AWSScraper()
aws_crawler = AWSProductCrawler(chromaDB, aws_scraper)
factory = LLMFactory()

# agent = factory.gemini()
agent = factory.ollama()



def chatLoop():
    print("Hello, how may I help you today\nh for help")
    print("$- ")
    userInput = input()
    userInput = userInput.strip()
    
    while not userInput == "q":
        if userInput == "h":
            printHelp()
        elif userInput == "q":
            break
        elif userInput == "":
            print("You can't have an empty question")
        else:
            context = RAGContext(userInput)
            agentResponse = agent.query(query=userInput, context=context)
            print(agentResponse)
        print("$- ")
        userInput = input()

def printHelp():
    print("h: Help\nq: Quit\nOtherwise type any information in and watch the agent return relevant responses")
            
def RAGContext(query):
    return chromaDB.query(query)["documents"][0]


if __name__ == '__main__':
    # chatLoop()
    aws_crawler.populateIndex()
