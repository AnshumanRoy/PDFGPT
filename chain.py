from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

def respond(query, retriever):
    docs = retriever.get_relevant_documents(query)[:5]
    chain = load_qa_chain(OpenAI(temperature=0.2), chain_type="stuff")
    return chain({"input_documents": docs, "question": query}, return_only_outputs=True)