from crawler.aws_crawler import AWSProductCrawler
from db.database import ChromaInstance
from crawler.aws_scraper import AWSScraper
from llm.llm_factory import LLMFactory

import requests, json, os, time
from dotenv import load_dotenv
load_dotenv()

chromaDB = ChromaInstance()
aws_scraper = AWSScraper()
aws_crawler = AWSProductCrawler(chromaDB, aws_scraper)
factory = LLMFactory()

# agent = factory.gemini()
LLMBackend = "ollama"
if LLMBackend == "ollama":
    agent = factory.ollama()
    
def startBenchmarking():
    
    
    benchmarkingFile = "benchmark_questions.json"
    with open(benchmarkingFile, "r") as question_file:
        questions = json.load(question_file)["questions"]

        limit = 10
        filename = f"benchmarking-{limit}Q-{time.time()}-report.txt"
        logFile = f"benchmarking-{limit}Q-{time.time()}-log.txt"
        with open(f"benchmarking/{filename}", "w") as f:
            with open(f"benchmarking/{logFile}", "w") as logs:
                f.write(f"---- Benchmarking Test ----\nDate:{time.asctime()}\n")
                f.write(f"Agent:{LLMBackend}\n")
                f.write(f"Questions:{benchmarkingFile}\n")
                f.write(f"Tested:{limit}\n")
                i = 0
                correct = 0
                wrong = 0                
                
                for question in questions[:limit]:                
                    context = RAGContext(question["question"])
                    query = f"What is the correct answer. Answer the question with exact responses only. The answer must come from the options provided and it can't have any varying letters. You will not return any explanation, only the response. Options:\n{question['options']}"
                    agentResponse = agent.query(query=query, context=context)
                    isCorrect = (agentResponse == question["answer"])
                    f.write(f"Question {i}: {isCorrect}\n")
                    timestamp = time.strftime("%H:%M:S")
                    logs.write(f"{timestamp}:question:{question['question']}\n")

                    if isCorrect:
                        correct = correct + 1
                        logs.write(f"{agentResponse} == {question['answer']}\n")
                    else:
                        wrong = wrong + 1
                        logs.write(f"{agentResponse} != {question['answer']}")
                    i = i + 1                    
                    
                f.write(f"Score:{correct}/{correct+wrong}\nPercent:{(correct/(correct+wrong))*100}%")

def RAGContext(query):
    return chromaDB.query(query)["documents"][0]

            
if __name__ == '__main__':
    startBenchmarking()
