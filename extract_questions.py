import time
import fitz  # PyMuPDF
from openai import OpenAI
import os
from docx import Document
from dotenv import load_dotenv

load_dotenv()
oai_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=oai_key)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

standard_prompt = """
    Extract all data requests from the following text. Only include the data requrests and exclude any other text:
    {}
    """

custom_prompt = """
    You are an expert in CPUC. Please extract data requests for the given text. 

    Prompt for Extracting Data Requests: 
    1.	<Context for Category 1>, (replace with real text from the document).
    a.	Content of question 1.a. 
    b.	Content of question 1.b. 
    c.	Content of question 1.c. 
    2.	<Context for Category 2>, (replace with real text from the document).. 
    a.	Content of question 2.a. 
    b.	Content of question 2.b. 
    3.	<Context for Category 3>, (replace with real text from the document).. 
    a.	Content of question 3.a. 
    b.	Content of question 3.b. 

    Examples: 
    1.	Starting on Page 34 SoCalGas’ 2020 General Order 77-M Report (available at SoCalGas Annual 2020 REDACTED GO-77-M) identifies membership dues and subscriptions of $500 or more. 
    a.	Please identify all dues, donations, subscriptions, and contributions that are funded by SoCalGas ratepayers. 
    b.	To the extent any dues, donations, subscriptions, and contributions are ratepayer funded, please indicate the Exhibit and page(s) of SoCalGas’ GRC testimony where this information is provided. 
    c.	Does the number listed under the “Account Charged” column indicate whether an expense is assigned to ratepayers or shareholders? If so, please indicate what account numbers signify a shareholder expense and what account numbers signify a ratepayer expense. 
    2.	Starting at page 32 of the 2020 General Order 77-M Report, SoCalGas lists payments to outside attorneys and legal firms for the year ended December 31, 2020. 
    a.	Please explain the significance of the numbers in the top row of page 32 (107, 108, 184, 417, 832, and 923). 

    Instructions: 
    Use this format to extract questions and number them correctly from any given document. Ensure that the numbering is preserved exactly as it appears in the original document for cross-referencing purposes. Do not add, remove, or alter any content from the original document. Do not skip any request!

    {}
    """

prompts = [standard_prompt, custom_prompt]

# Function to extract data requests using OpenAI API
def extract_data_requests_from_text(prompt, text):
    prompt = prompt.format(text)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )

    extracted_dr = response.choices[0].message.content
    return extracted_dr

# Main function
def main(prompt, file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format: Only PDF and DOCX are supported.")
    
    data_requests = extract_data_requests_from_text(prompt, text)
    return data_requests

if __name__ == "__main__":
    prompt = input("Enter the prompt type (standard/custom): ")
    if prompt == "standard":
        aPrompt = standard_prompt
    elif prompt == "custom":
        aPrompt = custom_prompt
    else:
        raise ValueError("Invalid prompt type. Please enter 'standard' or 'custom'")

    file_path = 'A 22-03-015 Data Request CEJA-Sempra-02 -7 25 22_176.docx'
    
    start_time = time.time()

    extracted_requests = main(aPrompt, file_path)
    print(extracted_requests)

    end_time = time.time()
    print(f"\nTime taken: {end_time - start_time} seconds.")