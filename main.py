from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from langchain.schema import SystemMessage
load_dotenv()

chat = ChatOpenAI()

tables = list_tables()


chat_prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content = (
                      "You are an AI that has access to a SQLite Database."
                      f"Here are the tables in the database: {tables}\n"
                      "Do not make any assumptions about what tables exist or what columns they have. You can ask use the describe tables function."
        )),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ]
)

tools = [run_query_tool, describe_tables_tool]

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