from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from config import GIGACHAT_CREDENTIALS, MODEL_NAME, VERIFY_SSL
from langchain_gigachat.chat_models import GigaChat

# Функция для загрузки и индексирования текстовых документов

def load_rag_documents(text_path: str):
    loader = TextLoader(text_path, encoding='utf-8')  # или попробуй 'cp1251'
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    emb = HuggingFaceEmbeddings(model_name="cointegrated/rubert-tiny")
    return FAISS.from_documents(chunks, emb)

# Инициализация модели и RAG-цепочки
model = GigaChat(
    credentials=GIGACHAT_CREDENTIALS,
    scope="GIGACHAT_API_PERS",
    model=MODEL_NAME,
    verify_ssl_certs=VERIFY_SSL,
)
vectorstore = load_rag_documents("deposits_context.txt")  # файл с контекстом
rag_qa = RetrievalQA.from_chain_type(
    llm=model,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
)