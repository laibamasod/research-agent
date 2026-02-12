#!/usr/bin/env python3
"""
Single-file autonomous agent using Ollama (Llama 3.1) and Tavily web search.
The agent autonomously decides when to use the web search tool.
"""

import os
import re
import sys
from typing import Optional

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Configuration
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OLLAMA_MODEL = "llama3.1"
MAX_TOOL_ITERATIONS = 3

# Initialize Ollama LLM
llm = ChatOllama(model=OLLAMA_MODEL)

# Initialize Tavily client
tavily_client: Optional[TavilyClient] = None
if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
else:
    print("Warning: TAVILY_API_KEY not set. Web search will not work.", file=sys.stderr)


def web_search(query: str) -> str:
    """
    Perform a web search using Tavily and return a concise summary.
    
    Args:
        query: The search query string
        
    Returns:
        A formatted string containing search results (titles and snippets)
    """
    if not tavily_client:
        return "Error: Tavily API key not configured. Cannot perform web search."
    
    try:
        response = tavily_client.search(
            query=query,
            max_results=5,
            search_depth="basic"
        )
        
        results = response.get("results", [])
        if not results:
            return "No search results found."
        
        summary_parts: list[str] = []
        for result in results:
            title = result.get("title", "No title")
            content = result.get("content", "No content")
            url = result.get("url", "")
            
            summary_parts.append(f"Title: {title}\nContent: {content}\nURL: {url}\n")
        
        return "\n".join(summary_parts)
    except Exception as e:
        return f"Error performing web search: {str(e)}"


def call_llm(messages: list[dict[str, str]], system_prompt: str) -> str:
    """
    Call Ollama LLM with the given messages and system prompt.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        system_prompt: System prompt string
        
    Returns:
        The LLM's response text
    """
    try:
        # Convert messages to LangChain message format
        langchain_messages = [SystemMessage(content=system_prompt)]
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
        
        # Call LLM
        response = llm.invoke(langchain_messages)
        
        return response.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"


def parse_tool_call(response: str) -> Optional[tuple[str, str]]:
    """
    Parse a TOOL_CALL from the LLM response.
    
    Expected format: TOOL_CALL web_search: <query>
    
    Args:
        response: The LLM response text
        
    Returns:
        A tuple of (tool_name, query) if found, None otherwise
    """
    pattern = r"TOOL_CALL\s+(\w+):\s*(.+)"
    match = re.search(pattern, response)
    if match:
        tool_name = match.group(1)
        query = match.group(2).strip()
        return (tool_name, query)
    return None


# def run_agent(user_question: str, debug: bool = False) -> str:
#     """
#     Run the autonomous agent loop to answer a user question WITH tool access.
#     
#     Args:
#         user_question: The user's question
#         debug: If True, print debug information
#         
#     Returns:
#         The final answer from the agent
#     """
#     system_prompt = """You are a helpful AI assistant with access to a web search tool.
# 
# Available tool:
# - web_search(query): Search the web for current information. Use this when you need up-to-date information, current dates, recent events, or any information that may have changed recently.
# 
# To use a tool, output a line in this exact format:
# TOOL_CALL web_search: <your search query>
# 
# After you receive tool results, you can either:
# 1. Use the information to answer the user's question directly
# 2. Make another tool call if needed (up to 3 iterations)
# 
# If you don't need current information, answer directly without using tools.
# 
# Be concise and helpful in your responses."""
# 
#     conversation_history: list[dict[str, str]] = [
#         {"role": "user", "content": user_question}
#     ]
#     
#     tool_used = False
#     iterations = 0
#     
#     while iterations < MAX_TOOL_ITERATIONS:
#         iterations += 1
#         
#         if debug:
#             print(f"\n[Debug] Iteration {iterations}", file=sys.stderr)
#             print(f"[Debug] Messages: {conversation_history}", file=sys.stderr)
#         
#         # Call LLM
#         response = call_llm(conversation_history, system_prompt)
#         
#         if debug:
#             print(f"[Debug] LLM Response: {response}", file=sys.stderr)
#         
#         # Check for tool call
#         tool_call = parse_tool_call(response)
#         
#         if tool_call:
#             tool_name, query = tool_call
#             
#             if debug:
#                 print(f"[Debug] Tool call detected: {tool_name} with query: {query}", file=sys.stderr)
#             
#             if tool_name == "web_search":
#                 tool_used = True
#                 # Execute tool
#                 tool_result = web_search(query)
#                 
#                 if debug:
#                     print(f"[Debug] Tool result: {tool_result[:200]}...", file=sys.stderr)
#                 
#                 # Add assistant's tool request and tool result to conversation
#                 conversation_history.append({
#                     "role": "assistant",
#                     "content": f"I need to search for: {query}"
#                 })
#                 conversation_history.append({
#                     "role": "user",
#                     "content": f"Tool result (web_search for '{query}'):\n{tool_result}\n\nNow answer the original question using this information."
#                 })
#             else:
#                 # Unknown tool, treat as regular response
#                 break
#         else:
#             # No tool call, this is the final answer
#             break
#     
#     if tool_used and not debug:
#         print("[Info] Web search tool was used.", file=sys.stderr)
#     
#     return response


def run_agent_no_tools(user_question: str, debug: bool = False) -> str:
    """
    Run the autonomous agent loop to answer a user question WITHOUT tool access.
    This agent can only use its training knowledge and cannot access web search.
    
    Args:
        user_question: The user's question
        debug: If True, print debug information
        
    Returns:
        The final answer from the agent
    """
    system_prompt = """You are a helpful AI assistant. Answer questions based on your training knowledge.
    
You do not have access to web search or any external tools. You can only answer based on the information you were trained on.
If you don't know the answer or need current information, be honest about your limitations.

Be concise and helpful in your responses."""

    conversation_history: list[dict[str, str]] = [
        {"role": "user", "content": user_question}
    ]
    
    if debug:
        print(f"[Debug] Messages: {conversation_history}", file=sys.stderr)
    
    # Call LLM once (no tool iteration loop needed)
    response = call_llm(conversation_history, system_prompt)
    
    if debug:
        print(f"[Debug] LLM Response: {response}", file=sys.stderr)
    
    return response


def main() -> None:
    """Main console REPL entry point."""
    print("Autonomous Agent with Ollama (NO TOOLS)")
    print("=" * 50)
    print(f"Model: {OLLAMA_MODEL}")
    print("Mode: Agent WITHOUT tool access (for comparison testing)")
    print("Type your question (or 'exit' to quit):\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input or user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            print("\nAgent: ", end="", flush=True)
            answer = run_agent_no_tools(user_input, debug=False)
            print(answer)
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}", file=sys.stderr)
            print()


if __name__ == "__main__":
    main()
