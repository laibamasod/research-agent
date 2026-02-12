#!/usr/bin/env python3
"""
Test script for wikipedia_search_tool.
Calls the real Wikipedia API and prints results to console.
"""

import json
from research_tools import wikipedia_search_tool


def print_results(results, query, sentences):
    """Print search results in a readable format."""
    print("=" * 80)
    print(f"Wikipedia Search Results")
    print("=" * 80)
    print(f"Query: {query}")
    print(f"Sentences: {sentences}")
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
    
    # Print result (Wikipedia typically returns one result)
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"URL: {result.get('url', 'N/A')}")
        summary = result.get('summary', 'N/A')
        # Count actual sentences in summary
        sentence_count = summary.count('.') + summary.count('!') + summary.count('?')
        print(f"Summary (approx. {sentence_count} sentences):")
        print("-" * 80)
        print(summary)
        print("-" * 80)
    
    print("\n" + "=" * 80)
    print("Raw JSON Output:")
    print("=" * 80)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("=" * 80)


def main():
    """Main test function."""
    print("\n" + "=" * 80)
    print("Testing wikipedia_search_tool")
    print("=" * 80 + "\n")
    
    # Test 1: Basic search with default sentences
    print("\n[Test 1] Basic search: 'artificial intelligence' (default sentences=5)")
    print("-" * 80)
    results1 = wikipedia_search_tool("artificial intelligence")
    print_results(results1, "artificial intelligence", 5)
    
    # Test 2: Search with custom sentences
    print("\n\n[Test 2] Search with sentences=3: 'machine learning'")
    print("-" * 80)
    results2 = wikipedia_search_tool("machine learning", sentences=3)
    print_results(results2, "machine learning", 3)
    
    # Test 3: Another query with more sentences
    print("\n\n[Test 3] Search: 'quantum computing' (sentences=10)")
    print("-" * 80)
    results3 = wikipedia_search_tool("quantum computing", sentences=10)
    print_results(results3, "quantum computing", 10)
    
    # Test 4: Test with a different topic
    print("\n\n[Test 4] Search: 'Python programming language' (sentences=7)")
    print("-" * 80)
    results4 = wikipedia_search_tool("Python programming language", sentences=7)
    print_results(results4, "Python programming language", 7)
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
