#!/usr/bin/env python3
"""
Test script for arxiv_search_tool.
Calls the real arXiv API and prints results to console.
"""

import json
from research_tools import arxiv_search_tool


def print_results(results, query, max_results):
    """Print search results in a readable format."""
    print("=" * 80)
    print(f"arXiv Search Results")
    print("=" * 80)
    print(f"Query: {query}")
    print(f"Max Results: {max_results}")
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
    
    # Print each result
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Authors: {', '.join(result.get('authors', []))}")
        print(f"Published: {result.get('published', 'N/A')}")
        print(f"URL: {result.get('url', 'N/A')}")
        print(f"PDF Link: {result.get('link_pdf', 'N/A')}")
        summary = result.get('summary', 'N/A')
        # Truncate long summaries
        if len(summary) > 300:
            summary = summary[:300] + "..."
        print(f"Summary: {summary}")
        print("-" * 80)
    
    print("\n" + "=" * 80)
    print("Raw JSON Output:")
    print("=" * 80)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("=" * 80)


def main():
    """Main test function."""
    print("\n" + "=" * 80)
    print("Testing arxiv_search_tool")
    print("=" * 80 + "\n")
    
    # Test 1: Basic search with default max_results
    print("\n[Test 1] Basic search: 'machine learning' (default max_results=5)")
    print("-" * 80)
    results1 = arxiv_search_tool("machine learning")
    print_results(results1, "machine learning", 5)
    
    # Test 2: Search with custom max_results
    print("\n\n[Test 2] Search with max_results=3: 'quantum computing'")
    print("-" * 80)
    results2 = arxiv_search_tool("quantum computing", max_results=3)
    print_results(results2, "quantum computing", 3)
    
    # Test 3: Another query
    print("\n\n[Test 3] Search: 'neural networks' (max_results=2)")
    print("-" * 80)
    results3 = arxiv_search_tool("neural networks", max_results=2)
    print_results(results3, "neural networks", 2)
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
