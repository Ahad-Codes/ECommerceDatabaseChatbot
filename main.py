from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables
from langchain.schema import SystemMessage
load_dotenv()

chat = ChatOpenAI()

tables = list_tables()


chat_prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content = f"You are an AI that has access to a SQLite Database. These are the following tables:  \n{tables}"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ]
)

tools = [run_query_tool]

agent = OpenAIFunctionsAgent(
    llm = chat,
    prompt = chat_prompt,
    tools = tools
)

agent_exec = AgentExecutor(
    agent= agent,
    verbose= True,
    tools= tools
)

agent_exec('How many users have provided a shipping address?')