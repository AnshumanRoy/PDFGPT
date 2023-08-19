from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from chain import respond
import os
import configparser

if __name__ == '__main__':

    # Setting location for persist directory for later use.
    persist_directory = 'persist_directory'


    # Initializing ConfigParser object to read from config file.
    config = configparser.ConfigParser()
    config.read('config.ini')


    # Setting OpenAi API key as environment variable.
    os.environ["OPENAI_API_KEY"] = config.get('api_key', 'key')

    embeddings = OpenAIEmbeddings()

    print("Looking for persist directory...\n\n")


    # Checking if persist directory has not been created yet.
    if not os.path.isdir(persist_directory):
        
        # If the directory does not exist, the pdf file is read and divided into docs objects that are then stored into a persist directory.
        print("Persist directory not found. Creating directory from given context...")
        reader = PdfReader(config.get('file', 'path'))
        page_texts = [page.extract_text() for page in reader.pages]
        text = " ".join(page_texts)

        text_splitter = CharacterTextSplitter(
                    separator='\n', 
                    chunk_size=1300,
                    chunk_overlap=0
            )

        texts = text_splitter.create_documents([text])
        vectordb = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory)
        print("Directory created.\n\n")

    else:
        # If persist directory exists, it is used to retrieve docs for querying.
        print("Directory found.\n\n")
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    # Setting up the retriever to obtain the most relevant docs from the pdf to answer the query.
    print("Processing directory...")
    retriever = vectordb.as_retriever(search_type="mmr")

    print("Directory processed.\n\n")

    print("Ready to start answering. Entering answering loop.\n")

    flag = True
    while flag:
        
        query = input("Enter your query. Enter '`' to exit the app.\nQuery: ")

        if query == '`':
            print("\nExiting loop. Thanks for using the app.")
            flag = False
            break

        else:
            print(f"Response:{respond(query, retriever)['output_text']}\n\n")