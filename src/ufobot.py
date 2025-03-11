from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
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

llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.7)
llm_with_prompt = chat_template | llm

def call_agent(message_state : MessagesState):
    response = llm_with_prompt.invoke(message_state)
    return {"messages": [response]}

graph = StateGraph(MessagesState)
graph.add_node("agent", call_agent)
graph.add_edge("agent", "__end__")
graph.set_entry_point("agent")
app = graph.compile()

updated_messages = app.invoke({"messages": [HumanMessage(content="What is a UFO?")]})

print(updated_messages)
