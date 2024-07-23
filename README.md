# Retrieval-Augmented Generation (RAG) Demo
This demo showcases how to use a simple Retrieval-Augmented Generation (RAG) system to answer queries based on the contents of a PDF document. It involves loading a PDF, splitting it into chunks, embedding the chunks, and using a vector store to perform similarity search and generate responses.

## Prerequisites
- Python 3.7 or later
- pip package manager
- OpenAI API key

## Installation
Clone the repository:

```
git clone https://github.com/harryvu/wb-demo.git
cd wb-demo
```

Create and activate a virtual environment (optional but recommended):

```
python -m venv .venv
source .venv/bin/activate   # On Windows, use `.venv\Scripts\activate`
```

Install the required packages:

```
pip install -r requirements.txt
```

Create a .env file in the project directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

## Usage
Place the PDF file (SP Market Attributes - January 2010.pdf) in the project directory.

## Run the demo script:

```
python rag_demo.py
```

## Script Overview
- Load Environment Variables: The script uses the dotenv package to load the OpenAI API key from a .env file.
- Load PDF Document: The script uses PyPDFLoader to load and read the contents of the specified PDF file.
- Split Document into Chunks: The document content is split into smaller chunks for efficient processing.
- Embed Chunks: Each chunk is embedded using OpenAIEmbeddings.
- Create Vector Store: The embedded chunks are stored in a FAISS vector store for efficient similarity search.
- Perform Similarity Search: The script searches for chunks similar to the query using the vector store.
- Generate Response: A response is generated using OpenAI's GPT model based on the retrieved chunks.

## Customization
- Changing the PDF File: To use a different PDF, replace SP Market Attributes - January 2010.pdf with your desired PDF file and update the pdfFileName variable in the script accordingly.
- Modifying the Query: Update the query variable in the script to change the query being asked.
- Adjusting Chunk Size: Modify the split_into_chunks function call to adjust the chunk size and overlap.

## Example
An example query provided in the script:

```
query="Why the global markets down by 3.97%?"
The script will generate a response based on the contents of the PDF document.

## Acknowledgements
This demo uses the following libraries:

LangChain
OpenAI
FAISS
dotenv


## License
This project is licensed under the MIT License.