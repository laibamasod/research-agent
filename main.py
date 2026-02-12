#!/usr/bin/env python3
"""
Console-based testing script for the research agent.
"""

from research_agent import find_references


def main():
    """Main console interface for testing research tasks."""
    print("=" * 60)
    print("Research Agent - Console Testing")
    print("=" * 60)
    print("\nThis tool can search:")
    print("  - arXiv for academic papers")
    print("  - Tavily for general web search")
    print("  - Wikipedia for encyclopedic summaries")
    print("\n" + "-" * 60)
    
    while True:
        print("\nEnter a research task (or 'quit' to exit):")
        task = input("> ").strip()
        
        if task.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not task:
            print("Please enter a valid task.")
            continue
        
        print("\n" + "=" * 60)
        print(f"Researching: {task}")
        print("=" * 60)
        print("\nProcessing... (this may take a moment)\n")
        
        try:
            result = find_references(task)
            print("\n" + "-" * 60)
            print("RESULT:")
            print("-" * 60)
            print(result)
            print("\n" + "=" * 60)
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    main()
