from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from tools import query_ufo_faqs, query_aliens


prompt = '''
You are a UFOologist. Answer questions about UFOs and aliens.
'''

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        ("placeholder", "{messages}")
    ]
)

tools = [query_ufo_faqs, query_aliens]

llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.7)
llm_with_prompt = chat_template | llm | llm.bind_tools(tools)

def call_agent(message_state : MessagesState):
    response = llm_with_prompt.invoke(message_state)
    return {"messages": [response]}

def is_there_tool_calls(state : MessagesState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tool_node'
    else:
        return '__end__'

graph = StateGraph(MessagesState)
tool_node = ToolNode(tools)
graph.add_node("agent", call_agent)
graph.add_node("tool_node", tool_node)
graph.add_conditional_edges("agent", is_there_tool_calls)
graph.add_edge("tool_node", "agent")
graph.add_edge("agent", "__end__")
graph.set_entry_point("agent")
app = graph.compile()

updated_messages = app.invoke({"messages": [HumanMessage(content="What is a UFO?")]})

print(updated_messages)
