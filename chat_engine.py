from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class ChatEngine:
    """Handles RAG and direct LLM responses"""
    
    @staticmethod
    def answer_with_rag(vectorstore, llm, question):
        """Answer question using RAG (Retrieval Augmented Generation)"""
        # Create a custom prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}
        
        Answer: """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        result = qa_chain({"query": question})
        return result["result"], result["source_documents"]
    
    @staticmethod
    def answer_with_llm(llm, question):
        """Answer question using direct LLM without context"""
        response = llm.invoke(question)
        return response.content