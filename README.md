#  LangChain Agent + MCP Tools over STDIO (GPT-4o + Structured Tools)

This project demonstrates how to use [LangChain](https://www.langchain.com/) agents with [Model Context Protocol (MCP)](https://github.com/langchain-ai/langchain/tree/master/libs/langchain-mcp) tools executed over **STDIO**, allowing tool calls to be served from an external Python process in a clean, structured, and isolated way.

✅ Compatible with OpenAI's tool-calling models like `gpt-4o`, `gpt-4-0613`, and `gpt-3.5-turbo-0613`.

---

## What This Repo Shows

- LangChain agent with structured tool calling (not ReAct)
- MCP tools registered in a separate `terminal_server.py`
- Communication between LangChain and tool server via **STDIO**
- Async execution using `asyncio` and `ClientSession`
- Agent asks: “What is the currency, capital, and language of India?” → Tools are called individually to fetch each answer

---

What the Agent Does

Loads the following tools from mcp_server.py:
findcurrency
findcapital
findlanguage
Passes them as structured tools to LangChain agent
Invokes the agent with the question:
"What is the currency, capital and language of India?"
Agent responds by calling tools one by one, collecting results, and forming a final answer
--------
How the output of the react agent looks like
Entering new AgentExecutor chain...
Thought: I need to find the currency, capital, and language of India using the available tools.
Action:
```
{
  "action": "findcurrency",
  "action_input": {"country": "India"}
}
```Processing request of type CallToolRequest
Indian rupeeAction:
```
{
  "action": "findcapital",
  "action_input": {"country": "India"}
}
```Processing request of type CallToolRequest
New DelhiAction:
```
{
  "action": "findlanguage",
  "action_input": {"country": "India"}
}
```Processing request of type CallToolRequest
English, Hindi, TamilAction:
```
{
  "action": "Final Answer",
  "action_input": "The currency of India is the Indian rupee. The capital of India is New Delhi. The languages of India include English, Hindi, and Tamil."
}
```

> Finished chain.
The currency of India is the Indian rupee. The capital of India is New Delhi. The languages of India include English, Hindi, and Tamil.

Key learning
tructured tool calling	Uses create_structured_chat_agent with OpenAI-compatible models . It was not working with simple react prompt  because of the output parsing . Langchian was not able to make a function call .
