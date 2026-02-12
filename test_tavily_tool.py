#!/usr/bin/env python3
"""
Test script for tavily_search_tool.
Calls the real Tavily API and prints results to console.
"""

import json
import os
from research_tools import tavily_search_tool


def print_results(results, query, max_results, include_images):
    """Print search results in a readable format."""
    print("=" * 80)
    print(f"Tavily Search Results")
    print("=" * 80)
    print(f"Query: {query}")
    print(f"Max Results: {max_results}")
    print(f"Include Images: {include_images}")
    print(f"Number of Results: {len(results)}")
    print("=" * 80)
    print()
    
    if not results:
        print("No results returned.")
        return
    
    # Check for errors
    if "error" in results[0]:
        print(f"ERROR: {results[0]['error']}")
        return
    
    # Separate regular results from image results
    regular_results = [r for r in results if "image_url" not in r]
    image_results = [r for r in results if "image_url" in r]
    
    # Print regular results
    for i, result in enumerate(regular_results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"URL: {result.get('url', 'N/A')}")
        content = result.get('content', 'N/A')
        # Truncate long content
        if len(content) > 500:
            content = content[:500] + "..."
        print(f"Content: {content}")
        print("-" * 80)
    
    # Print image results if any
    if image_results:
        print(f"\n--- Image Results ({len(image_results)} images) ---")
        for i, img_result in enumerate(image_results, 1):
            print(f"Image {i}: {img_result.get('image_url', 'N/A')}")
        print("-" * 80)
    
    print("\n" + "=" * 80)
    print("Raw JSON Output:")
    print("=" * 80)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("=" * 80)


def main():
    """Main test function."""
    print("\n" + "=" * 80)
    print("Testing tavily_search_tool")
    print("=" * 80 + "\n")
    
    # Check for API key
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("WARNING: TAVILY_API_KEY not found in environment variables.")
        print("The tool will raise a ValueError if called without an API key.")
        print("=" * 80 + "\n")
    
    try:
        # Test 1: Basic search without images
        print("\n[Test 1] Basic search: 'latest AI developments' (max_results=5, include_images=False)")
        print("-" * 80)
        results1 = tavily_search_tool("latest AI developments", max_results=5, include_images=False)
        print_results(results1, "latest AI developments", 5, False)
        
        # Test 2: Search with images
        print("\n\n[Test 2] Search with images: 'artificial intelligence' (max_results=3, include_images=True)")
        print("-" * 80)
        results2 = tavily_search_tool("artificial intelligence", max_results=3, include_images=True)
        print_results(results2, "artificial intelligence", 3, True)
        
        # Test 3: Another query
        print("\n\n[Test 3] Search: 'Python programming' (max_results=2, include_images=False)")
        print("-" * 80)
        results3 = tavily_search_tool("Python programming", max_results=2, include_images=False)
        print_results(results3, "Python programming", 2, False)
        
    except ValueError as e:
        print(f"\nERROR: {e}")
        print("Please set TAVILY_API_KEY in your .env file or environment variables.")
    except Exception as e:
        print(f"\nERROR: {e}")
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
