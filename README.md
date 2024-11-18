# HackSocial HouseJedi

This project is designed to assist housing developers by providing relevant information from a database of documents. The application uses a language model to answer questions based on the context of the documents.

## Prerequisites

- Python 3.8 or higher
- Virtual environment tool (e.g., `venv` or `virtualenv`)
- Access to the internet for downloading dependencies

## Setup Instructions

1. **Clone the Repository**

   Clone this repository to your local machine using:

   ```bash
   git clone <repository-url>
   cd HackSocial_HouseJedi
   ```

2. **Create and Activate a Virtual Environment**

   Create a virtual environment to manage dependencies:

   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**

   Install the required Python packages using the appropriate `requirements.txt` file for your operating system:

   - **For Windows**: You need to install Visual Studio Build Tools to compile some of the dependencies, such as `chromadb`. You can download it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

     ```bash
     pip install -r windows_requirements.txt
     ```

   - **For macOS**:

     ```bash
     pip install -r macos_requirements.txt
     ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project and add the following environment variables:

   ```plaintext
   OPEN_AI_EMBED_MODEL=<your_openai_embed_model>
   OPEN_AI_API_KEY=<your_openai_api_key>
   LLM_MODEL_NAME=<your_llm_model_name>
   ```

   Replace `<your_openai_embed_model>`, `<your_openai_api_key>`, and `<your_llm_model_name>` with your actual OpenAI model and API key details.

5. **Prepare the Data Directory**

   Ensure that the `data` directory contains the `.docx` files you want to process. The script will load these documents to initialize the database.

6. **Run the Script**

   Execute the `rag.py` script to start the application:

   ```bash
   python src/rag.py
   ```

   Follow the on-screen instructions to enter a list of cities and ask questions.

## Usage

- Enter a list of cities when prompted. The application will search for relevant documents in the database.
- Ask questions related to the cities you entered. The language model will provide answers based on the context of the documents.

## Troubleshooting

- Ensure all dependencies are installed correctly.
- Verify that the `.env` file contains the correct API keys and model names.
- Check that the `data` directory is not empty and contains valid `.docx` files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.