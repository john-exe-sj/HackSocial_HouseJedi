from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.prompts import ChatPromptTemplate

import re
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format for log messages
    handlers=[
        logging.FileHandler("./backend_app.log"),  # Log to a file with the desired name
        logging.StreamHandler()  # Also log to console
    ]
)

def split_documents(documents: list[Document]) -> list[Document]:
    """Splits documents into smaller chunks."""
    if not documents:
        raise ValueError("No documents to split.")

    logging.info("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=1000,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    try:
        return text_splitter.split_documents(documents)
    except Exception as e:
        logging.info(f"An error occurred during splitting: {e}")
        return []

def get_embedding_model() -> OpenAIEmbeddings:
    """Initializes and returns the embedding model."""
    return OpenAIEmbeddings(
        model=os.getenv("OPEN_AI_EMBED_MODEL"),
        api_key=os.getenv("OPEN_AI_API_KEY")
    )

def get_relevant_documents(cities: list[str], db: Chroma) -> list[Document]:
    """Retrieves relevant documents for the given cities from the database."""
    city_docs = []
    for city in cities:
        logging.info(f"DB: Searching for {city}")
        documents = db.search(city, "similarity")
        city_docs.extend(documents)
    return city_docs

def is_directory_empty(directory_path: str) -> bool:
    """Checks if the specified directory is empty."""
    return not any(os.scandir(directory_path))

def initialize_db() -> Chroma:
    """Initializes the database by loading documents and creating the database if necessary."""
    directory_data_path = os.path.abspath("./data")
    directory_db_path = os.path.abspath("./db")
    
    # Check if there are any files in the directory
    if not any(os.path.isfile(os.path.join(directory_data_path, f)) for f in os.listdir(directory_data_path)):
        raise FileNotFoundError(f"No data files found in directory: {directory_data_path}")

    # Create the database directory if it doesn't exist
    os.makedirs(directory_db_path, exist_ok=True)
    logging.info(f"Directory '{directory_db_path}' is ready.")

    loader = DirectoryLoader(
        directory_data_path,
        glob="*.docx",
        loader_cls=UnstructuredWordDocumentLoader,
        use_multithreading=True,
        max_concurrency=5
    )

    start_time = time.time()
    logging.info(f"Loading documents at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    documents = loader.lazy_load() # Load documents without splitting and load them only when needed. 
    logging.info("Documents loaded.")

    logging.info("Initializing database...")
    db = None
    if is_directory_empty(directory_db_path):
        db = Chroma.from_documents(
            documents=split_documents(documents),
            embedding=get_embedding_model(),
            persist_directory=directory_db_path
        )
    else:
        db = Chroma(
            persist_directory=directory_db_path,
            embedding_function=get_embedding_model()
        )

    if db is None:
        logging.error("Database initialization failed. Raising a RuntimeError.")
        raise RuntimeError("Database initialization failed.")
    
    logging.info("...database initialized")
    logging.info(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} after {time.time() - start_time:.2f} seconds")
    return db

if __name__ == "__main__":
    FINAL_PROMPT_TEMPLATE = """
    You are a chat robot meant to assist housing developers. If at any point you cannot find the information
    with the provided documents, do not mention that to the housing developer you are assisting. Only give
    them suggestions on where else to look. That is a direct order and not to be overridden.

    Now, given these contexts about the following cities - {cities}: {context}
    ---
    Answer or respond to the following based on the context above, citing sources when necessary: {prompt}
    """

    db = initialize_db()  # Initializing the database
    llm = OllamaLLM(model=os.getenv("LLM_MODEL_NAME"))  # Initializing the LLM

    list_of_cities = re.split(r',(?=\S)', input("Enter a list of cities (comma-separated): "))
    info = get_relevant_documents(list_of_cities, db)  # Retrieving relevant documents from the database

    print(f"Loaded, chat-bot ready. Ask a question regarding: {', '.join(list_of_cities)}")
    while True:
        prompt = input(">> ")
        
        if prompt.lower() == "quit()":
            break
        
        prompt_template = ChatPromptTemplate.from_template(FINAL_PROMPT_TEMPLATE)  # Assembling prompt from template
        final_prompt = prompt_template.format(cities=list_of_cities, context=info, prompt=prompt)
        print("Thinking...")
        response = llm.invoke(final_prompt)  # Prompting the LLM with context
        print(response)
        print("------------------------------------------\n")