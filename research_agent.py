# =========================
# Imports
# =========================

# --- Standard library 
from datetime import datetime

# --- Third-party ---
from langchain_ollama import ChatOllama
from langchain import agents
from langchain_core.tools import StructuredTool

# --- Local / project ---
from tool_wrappers import arxiv_wrapper, tavily_wrapper, wikipedia_wrapper
import utils


# =========================
# Find References
# =========================
def find_references(task: str, model: str = "llama3.1", return_messages: bool = False):
    """Perform a research task using external tools (arxiv, tavily, wikipedia)."""
    
    # Extract model name if it's in "ollama:llama3.1" format
    if model.startswith("ollama:"):
        model = model.replace("ollama:", "")
    
    # Initialize LLM
    llm = ChatOllama(model=model, temperature=0.1)
    
    # Create LangChain Tools using wrappers (which now track internally)
    tools = [
        StructuredTool.from_function(
            arxiv_wrapper,
            name="arxiv_search_tool",
            description="Searches arXiv for academic research papers. Use this for finding scientific papers, academic articles, or research publications. IMPORTANT: Only pass 'query' parameter. Do NOT pass max_results - it automatically uses 5 (which is also the maximum). Parameters: query (required, string), max_results (DO NOT USE - auto-set to 5, maximum 5)."
        ),
        StructuredTool.from_function(
            tavily_wrapper,
            name="tavily_search_tool",
            description="Performs a general-purpose web search using Tavily. Use this for finding current news, recent developments, or general web information. Parameters: query (required), max_results (optional, default 5), include_images (optional, default False)."
        ),
        StructuredTool.from_function(
            wikipedia_wrapper,
            name="wikipedia_search_tool",
            description="Searches Wikipedia for encyclopedic summaries and overviews. Use this for getting general knowledge, definitions, or background information on topics. Parameters: query (required), sentences (optional, default 5)."
        )
    ]
    
    # System prompt with tool descriptions
    system_prompt = f"""You are a research assistant with access to three tools:

1. arxiv_search_tool: Searches arXiv for academic research papers. Use this for finding scientific papers, academic articles, or research publications. IMPORTANT: Only pass the 'query' parameter. Do NOT specify max_results - it defaults to 5 and that is the maximum allowed.

2. tavily_search_tool: Performs a general-purpose web search using Tavily. Use this for finding current news, recent developments, or general web information.

3. wikipedia_search_tool: Searches Wikipedia for encyclopedic summaries and overviews. Use this for getting general knowledge, definitions, or background information on topics.

Today is {datetime.now().strftime('%Y-%m-%d')}.

Use the appropriate tools to gather information and provide a comprehensive answer to the user's task."""

    try:
        # Create agent using LangChain 1.2.9's create_agent
        agent = agents.create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt
        )
        
        # Invoke the agent with the task and recursion limit
        result = agent.invoke(
            {"messages": [{"role": "user", "content": task}]},
            config={"recursion_limit": 5}  # Limits agent iterations to 5
        )
        
        # Extract the response - result format may vary, try common patterns
        if isinstance(result, dict):
            if "messages" in result:
                # Get the last message
                messages = result["messages"]
                if messages:
                    last_msg = messages[-1]
                    if hasattr(last_msg, "content"):
                        result_text = last_msg.content
                    elif isinstance(last_msg, dict) and "content" in last_msg:
                        result_text = last_msg["content"]
                    else:
                        result_text = str(last_msg)
                else:
                    result_text = str(result)
            elif "output" in result:
                result_text = result["output"]
            else:
                result_text = str(result)
        else:
            result_text = str(result)
        
        # Handle return_messages flag (for compatibility)
        if return_messages:
            return (result_text, [{"role": "user", "content": task}])
        return result_text
        
    except Exception as e:
        return f"[Model Error: {e}]"