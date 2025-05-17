import requests
import os
import sys
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain import hub 
import asyncio
from contextlib import AsyncExitStack # Ensures all async resources are properly closed
from typing import Optional, List   
from mcp import ClientSession, StdioServerParameters  # MCP session management and startup parameters
from mcp.client.stdio import stdio_client 
from langchain_mcp_adapters.tools import load_mcp_tools   
from langchain.agents import create_structured_chat_agent
#from langgraph.prebuilt import create_react_agent 

load_dotenv()

if len(sys.argv) < 2:
    print("Usage: python client_langchain_google_genai_bind_tools.py <path_to_server_script>")
    sys.exit(1)
server_script = sys.argv[1]

server_params = StdioServerParameters(
    command="python" if server_script.endswith(".py") else "node",
    args=[server_script],
)

mcp_client = None






async def lookup_async(country: str) -> str:
    template = """Given the Country {country}, what is the currency, capital and language? 
    your Answer should be in the format: The currency of country is currency, the capital is capital and the language is language"""

    prompt_template = PromptTemplate(template=template, input_variables=["country"])
    global mcp_client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

                # 3. Load MCP tools
            tools = await load_mcp_tools(session)
    
            for tool in tools:
             print(f"Loaded tool: {tool.name}, args_schema: {tool.args_schema}") 

            llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-4o",
                )
        
            react_prompt = hub.pull("hwchase17/structured-chat-agent")
            #agent = create_react_agent( llm=llm,tools=tools,prompt=react_prompt)
            agent = create_structured_chat_agent(llm=llm, tools=tools,prompt=react_prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)

    #agent = create_react_agent( llm=llm,tools=tools,prompt=react_prompt)
    #agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)
            query = (
                f"Given the Country {country}, what is the currency, capital and language? "
                )
            result = await agent_executor.ainvoke({"input": query})
            return result["output"] if "output" in result else result
    #result = await agent_executor.invoke(input={"input": prompt_template.format_prompt(country=country)})
    #return result

if __name__ == "__main__":  
    country = "India"
    result = asyncio.run(lookup_async("India"))
    print(result)
    