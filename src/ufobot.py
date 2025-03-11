from langgraph.graph import StateGraph, MessageState
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import AnthropicChatModel
from langchain_core.messages import HumanMessage, SystemMessage


prompt = '''
You are a UFOologist. Answer questions about UFOs and aliens.
'''

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        ("placeholder", "{messages}")
    ]
)

llm = AnthropicChatModel(model="claude-3-5-sonnet", temperature=0.7)
