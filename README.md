# HackSocial HouseJedi

This project is designed to assist housing developers by providing relevant information from a database of documents. The application uses a language model to answer questions based on the context of the documents. For more information regarding this event, visit: https://pages.pagesuite.com/8/a/8aa600ba-1bca-4098-913d-93b6aa7ab300/page.pdf

## Prerequisites

### Backend
- Python 3.8 or higher
- Virtual environment tool (e.g., `venv` or `virtualenv`)
- Access to the internet for downloading dependencies

### Frontend
- Node.js 16.x or higher
- npm or yarn package manager
- Modern web browser

## Setup Instructions

### Backend Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd HackSocial_HouseJedi
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Backend Dependencies**

   ```bash
   # For Windows (requires Visual Studio Build Tools)
   pip install -r windows_requirements.txt

   # For macOS
   pip install -r macos_requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add:

   ```plaintext
   OPEN_AI_EMBED_MODEL=<your_openai_embed_model>
   OPEN_AI_API_KEY=<your_openai_api_key>
   LLM_MODEL_NAME=<your_llm_model_name>
   ```

5. **Prepare the Data Directory**

   Ensure that the `data` directory contains the `.docx` files you want to process.

### Frontend Setup

1. **Navigate to Frontend Directory**

   ```bash
   cd frontend
   ```

2. **Install Frontend Dependencies**

   ```bash
   # Using npm
   npm install

   # Using yarn
   yarn install
   ```

3. **Set Up Frontend Environment Variables**

   Create a `.env` file in the frontend directory and add:

   ```plaintext
   REACT_APP_API_URL=http://localhost:5000
   ```

   if not done, the frontend application will launch on `http://localhost:3000`

## Running the Application

### Start the Backend Server

1. From the root directory, activate the virtual environment if not already activated
2. Run the Flask server:

   ```bash
   cd backend
   python src/main.py
   ```

   The backend server will start on `http://localhost:8000`

### Start the Frontend Development Server

1. In a new terminal, navigate to the frontend directory
2. Start the development server:

   ```bash
   # Using npm
   npm start

   # Using yarn
   yarn start
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

- Access the web application through your browser at `http://localhost:3000`
- Enter a list of cities in the search field
- Ask questions related to the cities you entered
- The application will provide answers based on the context of the documents

## Development

### Backend
- Generation of the `./db/` directory should not take longer than 10 minutes
- The `./db` directory serves as the vector store containing chunked data for LLM processing

### Frontend
- The React application uses modern hooks and components
- Styling is implemented using [your CSS framework]
- API calls are handled through axios

## Troubleshooting

### Backend Issues
- Ensure all Python dependencies are installed correctly
- Verify that the `.env` file contains the correct API keys
- Check that the `data` directory contains valid `.docx` files

### Frontend Issues
- Clear npm cache if dependencies fail to install: `npm cache clean --force`
- Ensure Node.js version is compatible
- Check console for any JavaScript errors
- Verify API endpoint configuration in the frontend `.env` file

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.