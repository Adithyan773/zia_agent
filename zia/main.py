from fastapi import FastAPI
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from sqlmodel import Session, select
from database import ChatHistory, engine
from langchain_community.chat_message_histories import ChatMessageHistory
from config import settings
from chroma import vector_db  

app = FastAPI(title="Zia")
groq_api = settings.GROQ_API_KEY
model = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api)

def save_chat(user_query: str, ai_response: str, thread_id: str):
    with Session(engine) as session:
        chat = ChatHistory(user_query=user_query,ai_response=ai_response,thread_id=thread_id)
        session.add(chat)
        session.commit()

def get_last_chats(thread_id: int, limit: int = 5):
    with Session(engine) as session:
        statement = (
            select(ChatHistory)
            .where(ChatHistory.thread_id ==thread_id)
            .order_by(ChatHistory.timestamp.desc())
            .limit(limit)
        )
        results =session.exec(statement).all()
    return results

@app.get("/zia")
def zia(query: str,thread_id: int):
        retriever =vector_db.similarity_search(query, 5)
        combined_inputs =query + "\n\n" + "\n".join([doc.page_content for doc in retriever])
        chat_history =get_last_chats(thread_id)
        message_history = ChatMessageHistory()
        for chat in reversed(chat_history):  
            message_history.add_user_message(chat.user_query)
            message_history.add_ai_message(chat.ai_response)
        messages =[
            SystemMessage(content="You are a helpful assistant named Zia. You work as a business development manager at Zoople. Your task is to help students with their queries. Answer the queries using only the given context—do not provide general statements or meta-commentary like 'Based on the context provided.' Avoid generating your own content or making assumptions. Ensure that your responses are clear, concise, and based purely on the context provided, with a friendly and convincing tone, you are the head so act like politely."),
            *message_history.messages,  
            HumanMessage(content=combined_inputs),  
        ]
        res =model.invoke(messages)
        save_chat(user_query=query, ai_response=res.content, thread_id=thread_id)

        return{res.content}
   
