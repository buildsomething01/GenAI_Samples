import os
import requests
import json
import sys
import subprocess
# Ensure the package is installed and the path is correct
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("terminal")
DEFAULT_WORKSPACE = os.path.expanduser("~/mcp/workspace")

#@mcp.tool()
def run_command(command :str) ->str :
    """
    Run a terminal command inside the workspace directory.

    Args:
        command : The shell command to run.

    Returns:
        str : The output of the command.    
    """
    try:
        result = subprocess.run(command, shell=True,cwd=DEFAULT_WORKSPACE, check=True, capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)


@mcp.tool("findcurrency")
def findcurrency(country):
    """Find the currency of a country"""
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)
    data = response.json()
    if data and 'currencies' in data[0]:
    # Extract the first currency's name
        for currency_code, currency_info in data[0]['currencies'].items():
            currency_name = currency_info.get('name', 'Currency name not found')
            return currency_name

@mcp.tool("findcapital")
def findcapital(country):
    """Find the capital of a country"""
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)
    data = response.json()
    capital = data[0]['capital']
    return capital

@mcp.tool("findlanguage")
def findlanguage(country):
    """Find the language of a country"""
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)
    data = response.json()
    if data and 'languages' in data[0]:
         languages = list(data[0]['languages'].values())  # Extract all language names
         return ", ".join(languages)
   


if  __name__ == "__main__":
    try:
        print(" MCP server is starting...", flush=True)
        mcp.run(transport="stdio")
    except Exception as e:
        import traceback
        print("MCP server crashed:\n", traceback.format_exc(), flush=True)
