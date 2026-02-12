# =========================
# Tool Wrappers for LangChain
# =========================
"""
Wrapper functions that convert tool results (list[dict]) to formatted strings
for use with LangChain agents. These wrappers use proper type hints so
StructuredTool.from_function() can automatically handle parameter conversion.
"""

# --- Local / project ---
import research_tools


def arxiv_wrapper(query: str, max_results: int = 5) -> str:
    """
    Wrapper for arxiv_search_tool that returns a formatted string.
    Also tracks the call and extracts URLs for source attribution.
    
    Args:
        query: Search keywords for research papers.
        max_results: Maximum number of results to return (default 5).
    
    Returns:
        Formatted string containing paper information.
    """
    try:
        # Enforce maximum of 5 results
        original_max = max_results
        max_results = min(max_results, 5)
        if original_max > 5:
            print(f"[DEBUG] max_results clamped from {original_max} to 5")
        
        print(f"[DEBUG] Calling arxiv_search_tool with query: '{query}', max_results: {max_results}")
        results = research_tools.arxiv_search_tool(query, max_results)
        if not results or "error" in results[0]:
            error_msg = f"Error: {results[0].get('error', 'Unknown error')}" if results else "No results found."
            print(f"[DEBUG] arxiv_search_tool error: {error_msg}")
            return error_msg
        
        # Extract URLs from raw results
        urls = []
        for paper in results:
            if "url" in paper and paper["url"]:
                urls.append(paper["url"])
            if "link_pdf" in paper and paper["link_pdf"]:
                urls.append(paper["link_pdf"])
        
        # Debug print
        print(f"[DEBUG] arxiv_search_tool found {len(results)} papers, {len(urls)} URLs:")
        for url in urls:
            print(f"[DEBUG]   - {url}")
        
        # Format the result
        formatted = []
        for i, paper in enumerate(results, 1):
            formatted.append(f"Paper {i}: {paper.get('title', 'N/A')}")
            formatted.append(f"  Authors: {', '.join(paper.get('authors', []))}")
            formatted.append(f"  Published: {paper.get('published', 'N/A')}")
            formatted.append(f"  URL: {paper.get('url', 'N/A')}")
            formatted.append(f"  Summary: {paper.get('summary', 'N/A')[:200]}...")
            formatted.append("")
        return "\n".join(formatted)
    except Exception as e:
        error_msg = f"Error calling arxiv_search_tool: {str(e)}"
        print(f"[DEBUG] arxiv_search_tool exception: {error_msg}")
        return error_msg


def tavily_wrapper(query: str, max_results: int = 5, include_images: bool = False) -> str:
    """
    Wrapper for tavily_search_tool that returns a formatted string.
    Also tracks the call and extracts URLs for source attribution.
    
    Args:
        query: Search keywords for retrieving information from the web.
        max_results: Number of results to return (default 5).
        include_images: Whether to include image results (default False).
    
    Returns:
        Formatted string containing search results.
    """
    try:
        print(f"[DEBUG] Calling tavily_search_tool with query: '{query}', max_results: {max_results}, include_images: {include_images}")
        results = research_tools.tavily_search_tool(query, max_results, include_images)
        if not results or "error" in results[0]:
            error_msg = f"Error: {results[0].get('error', 'Unknown error')}" if results else "No results found."
            print(f"[DEBUG] tavily_search_tool error: {error_msg}")
            return error_msg
        
        # Extract URLs from raw results
        urls = []
        for item in results:
            if "url" in item and item["url"]:
                urls.append(item["url"])
            if "image_url" in item and item["image_url"]:
                urls.append(item["image_url"])
        
        # Debug print
        print(f"[DEBUG] tavily_search_tool found {len(results)} results, {len(urls)} URLs:")
        for url in urls:
            print(f"[DEBUG]   - {url}")
        
        # Format the result
        formatted = []
        regular_results = [r for r in results if "image_url" not in r]
        image_results = [r for r in results if "image_url" in r]
        
        for i, result in enumerate(regular_results, 1):
            formatted.append(f"Result {i}: {result.get('title', 'N/A')}")
            formatted.append(f"  URL: {result.get('url', 'N/A')}")
            formatted.append(f"  Content: {result.get('content', 'N/A')[:300]}...")
            formatted.append("")
        
        if image_results:
            formatted.append(f"Found {len(image_results)} images.")
        
        return "\n".join(formatted)
    except Exception as e:
        error_msg = f"Error calling tavily_search_tool: {str(e)}"
        print(f"[DEBUG] tavily_search_tool exception: {error_msg}")
        return error_msg


def wikipedia_wrapper(query: str, sentences: int = 5) -> str:
    """
    Wrapper for wikipedia_search_tool that returns a formatted string.
    Also tracks the call and extracts URLs for source attribution.
    
    Args:
        query: Search keywords for the Wikipedia article.
        sentences: Number of sentences in the summary (default 5).
    
    Returns:
        Formatted string containing Wikipedia article information.
    """
    try:
        print(f"[DEBUG] Calling wikipedia_search_tool with query: '{query}', sentences: {sentences}")
        results = research_tools.wikipedia_search_tool(query, sentences)
        if not results or "error" in results[0]:
            error_msg = f"Error: {results[0].get('error', 'Unknown error')}" if results else "No results found."
            print(f"[DEBUG] wikipedia_search_tool error: {error_msg}")
            return error_msg
        
        # Extract URLs from raw results
        urls = []
        for item in results:
            if "url" in item and item["url"]:
                urls.append(item["url"])
        
        # Debug print
        print(f"[DEBUG] wikipedia_search_tool found {len(results)} result(s), {len(urls)} URLs:")
        for url in urls:
            print(f"[DEBUG]   - {url}")
        
        # Format the result
        result = results[0]
        formatted = [
            f"Title: {result.get('title', 'N/A')}",
            f"URL: {result.get('url', 'N/A')}",
            f"Summary: {result.get('summary', 'N/A')}"
        ]
        return "\n".join(formatted)
    except Exception as e:
        error_msg = f"Error calling wikipedia_search_tool: {str(e)}"
        print(f"[DEBUG] wikipedia_search_tool exception: {error_msg}")
        return error_msg
