import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from .base_faq import INITIAL_FAQS

# 初始化向量库（单例）
class KnowledgeBase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            embeddings = OpenAIEmbeddings()
            cls._instance.vectorstore = Chroma(embedding_function=embeddings)
            # 插入初始FAQ
            documents = [Document(page_content=faq) for faq in INITIAL_FAQS]
            splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
            docs = splitter.split_documents(documents)
            cls._instance.vectorstore.add_documents(docs)
        return cls._instance

    def search(self, query: str, k=3):
        return self.vectorstore.similarity_search(query, k=k)

    def add(self, text: str):
        self.vectorstore.add_documents([Document(page_content=text)])