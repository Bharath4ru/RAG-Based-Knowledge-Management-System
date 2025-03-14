from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config import Config

class LLMService:
    def __init__(self, vector_store):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.1,
            google_api_key=Config.GOOGLE_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vector_store.vector_store.as_retriever(),
            memory=self.memory
        )

    def get_response(self, query):
        try:
            response = self.chain.invoke({"question": query})
            return response["answer"]
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return "I encountered an error processing your request."
