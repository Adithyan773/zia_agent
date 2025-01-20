from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain.docstore.document import Document


tl= TextLoader('C:/Users/adith/Documents/zoople_bot/zoople_scrap.txt', encoding="utf-8")
data = tl.load()
page_content = [doc.page_content for doc in data]
page =''.join(page_content)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)
text_chunk = text_splitter.split_text(page)
docs = [Document(page_content = chunk)for chunk in text_chunk]
embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")
vector_db = Chroma.from_documents(docs, embeddings)

