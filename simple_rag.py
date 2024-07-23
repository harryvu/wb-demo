import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
#from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from chunking import split_into_chunks
from openai import OpenAI

# Load .env file
load_dotenv()
oai_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=oai_key)

# Load pdf file, split it into chunks, embed each chunk and load it into the vector store.
cwd = os.path.abspath(os.path.dirname(__file__))
pdfFileName = "SP Market Attributes - January 2010.pdf"
fullPath = os.path.join(cwd, pdfFileName)

loader = PyPDFLoader(fullPath)
pages = loader.load()
# pages: Document[]

full_text = " ".join([page.page_content for page in pages])
chunks = split_into_chunks(full_text, 1000, 200)

embeddings_model = OpenAIEmbeddings(openai_api_key=oai_key)
db = FAISS.from_documents(pages, embeddings_model)

# Load vector store from disk
# db = FAISS.load_local("vector_store", embeddings_model)

# Save the vector store to disk
#db.save_local("vector_store")

query="Why the global markets down by 3.97%?"

docs = db.similarity_search_with_score(query)
#print(docs[0][0].page_content)

# join all page_content of each result into a single string
content = "\n\n".join([doc[0].page_content for doc in docs])

template = \
"You are an intelligent assistant helping developer with their questions about Containerized applications. " + \
"Use 'you' to refer to the individual asking the questions even if they ask with 'I'. " + \
"Answer the following question using only the data provided in the sources below. " + \
"Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response at the end of the answer in the square brackets. " + \
"The answer should always be written in full, completete sentences. " + \
"If you cannot answer using the sources below, say you don't know. " + \
"""

Question: '{q}'?

Sources: (as specific to page level as possible)
{retrieved}

Answer:
"""

prompt = template.format(q=query, retrieved=content)
response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
            {"role": "system", "content": "You are helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    temperature=0
)

print(response.choices[0].message.content)