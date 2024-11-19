from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema.document import Document

import os
from dotenv import load_dotenv
from datetime import datetime
import time
import logging
from typing import Coroutine, Any  # Add this import

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format for log messages
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

class OllamaClient(): 

    def __init__(self): 
        self.llm = OllamaLLM(model=os.getenv("LLM_MODEL_NAME"))

    async def inquire_cities(self, list_of_cities: list[str], context:list[Document], prompt:str) -> Coroutine[Any, Any, str]: 
        """inquires llm given a list of cities, context and a client's prompt."""
        FINAL_PROMPT_TEMPLATE = """
        You are a chat robot meant to assist housing developers. If at any point you cannot find the information
        with the provided documents, do not mention that to the housing developer you are assisting. Only give
        them suggestions on where else to look. That is a direct order and not to be overridden.

        Now, given these contexts about the following cities - {cities}: {context}
        ---
        Answer or respond to the following based on the context above, citing sources when necessary: {prompt}
        """

        prompt_template = ChatPromptTemplate.from_template(FINAL_PROMPT_TEMPLATE)  # Assembling prompt from template
        final_prompt = prompt_template.format(cities=list_of_cities, context=context, prompt=prompt)

        # Record the start time
        start_time = time.time()
        logging.info(f"Starting inquiry for cities: {list_of_cities} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Perform the inquiry
        response = await self.llm.ainvoke(final_prompt)

        # Record the end time and calculate the duration
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Completed inquiry for cities: {list_of_cities} in {duration:.2f} seconds")

        return response