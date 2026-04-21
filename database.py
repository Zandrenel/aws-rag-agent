import chromadb

class ChromaInstance:
    def __init__(self):
        # self.chroma_client = chromadb.Client()
        self.chroma_client = chromadb.PersistentClient(path="/data/chromadb/aws_rag/")
        self.collection = self.chroma_client.get_collection(name="aws_raw")
        
    def add(self, id_, document):
        self.collection.upsert(
            ids=[id_],
            documents=[document]            
        )
        print(f"Document Added: {id_}")

    def query(self, query):
        results = self.collection.query(query_texts=[query], n_results=1)
        return results
