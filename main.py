from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from handlers.chat_model_start_handler import ChatModelStartHandler
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from langchain.schema import SystemMessage
load_dotenv()

handler = ChatModelStartHandler()
chat = ChatOpenAI(
    callbacks=[handler]
)

tables = list_tables()


chat_prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content = (
                      "You are an AI that has access to a SQLite Database."
                      f"Here are the tables in the database: {tables}\n"
                      "Do not make any assumptions about what columns the tables have. Use the 'describe tables' function to find the names of the columns and use their names respectively."
        )),
        MessagesPlaceholder(variable_name= 'chat_history'),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ]
)

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)



tools = [run_query_tool, describe_tables_tool, write_report_tool]

agent = OpenAIFunctionsAgent(
    llm = chat,
    prompt = chat_prompt,
    tools = tools
)

agent_exec = AgentExecutor(
    agent= agent,
    #verbose= True,
    tools= tools,
    memory=memory
)

agent_exec('How many orders are there? Write the report to a file called num_orders.html.')
agent_exec('Repeat the exact same process for users.')