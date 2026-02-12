# Research Agent

An autonomous research agent powered by LangChain and Ollama that performs comprehensive research tasks by intelligently using multiple information sources including arXiv, Tavily web search, and Wikipedia.

## Overview

The Research Agent is an AI-powered tool that autonomously conducts research on any given topic by:
- Searching academic papers on arXiv
- Performing web searches using Tavily
- Retrieving encyclopedic information from Wikipedia
- Synthesizing information from multiple sources to provide comprehensive answers

The agent uses LangChain's agent framework with Ollama (Llama 3.1) as the underlying LLM, making intelligent decisions about which tools to use and when to use them.

## Features

- **Multi-source Research**: Integrates three powerful research tools:
  - **arXiv**: Search for academic research papers and scientific publications
  - **Tavily**: General-purpose web search for current news and recent developments
  - **Wikipedia**: Encyclopedic summaries and background information

- **Autonomous Decision Making**: The agent intelligently selects which tools to use based on the research task

- **Source Attribution**: Automatically extracts and tracks URLs from all sources for proper citation

- **Evaluation Framework**: Built-in evaluation tools to assess source quality and domain trustworthiness

- **Flexible Interface**: Multiple entry points including console interface and programmatic API

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally
- Tavily API key (for web search functionality)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd research-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root:
```env
TAVILY_API_KEY=your_tavily_api_key_here
DLAI_TAVILY_BASE_URL=optional_custom_base_url
```

4. Ensure Ollama is running with the Llama 3.1 model:
```bash
ollama pull llama3.1
```

## Usage

### Console Interface

Run the interactive console interface:
```bash
python main.py
```

This will start an interactive session where you can enter research tasks and receive comprehensive answers.

### Programmatic Usage

Use the agent in your Python code:
```python
from research_agent import find_references

# Perform a research task
result = find_references("What are the latest developments in quantum computing?")
print(result)
```

### Custom Model

You can specify a different Ollama model:
```python
result = find_references(
    "Explain neural networks",
    model="llama3.1"  # or any other Ollama model
)
```

## Project Structure

```
research-agent/
├── research_agent.py      # Main agent implementation using LangChain
├── research_tools.py       # Core research tool implementations (arXiv, Tavily, Wikipedia)
├── tool_wrappers.py        # Wrappers that format tool outputs for LangChain
├── main.py                 # Console interface entry point
├── agent_console.py        # Alternative console interface (no tools)
├── utils.py                # Utility functions for evaluation and formatting
├── evaluation.py           # Evaluation framework for source quality
├── max_iterations.py       # Verification script for LangChain agent configuration
├── test_arxiv_tool.py      # Tests for arXiv tool
├── test_tavily_tool.py     # Tests for Tavily tool
├── test_wikipedia_tool.py  # Tests for Wikipedia tool
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Research Tools

### arXiv Search Tool
- **Purpose**: Find academic research papers and scientific publications
- **Parameters**:
  - `query` (required): Search keywords
  - `max_results` (optional, default: 5, max: 5): Number of results
- **Returns**: Papers with title, authors, publication date, URL, summary, and PDF link

### Tavily Search Tool
- **Purpose**: General-purpose web search for current information
- **Parameters**:
  - `query` (required): Search keywords
  - `max_results` (optional, default: 5): Number of results
  - `include_images` (optional, default: False): Include image results
- **Returns**: Web results with title, content snippet, and URL

### Wikipedia Search Tool
- **Purpose**: Get encyclopedic summaries and background information
- **Parameters**:
  - `query` (required): Search keywords
  - `sentences` (optional, default: 5): Number of sentences in summary
- **Returns**: Article title, summary, and URL

## Evaluation

The project includes evaluation tools to assess the quality of research results:

```python
from utils import evaluate_tavily_results

TOP_DOMAINS = {
    "wikipedia.org", "nature.com", "science.org", "arxiv.org",
    "nasa.gov", "mit.edu", "stanford.edu", "harvard.edu"
}

flag, report = evaluate_tavily_results(TOP_DOMAINS, research_output, min_ratio=0.4)
```

This evaluates whether the research results come from trusted domains and generates a markdown report.

## Configuration

### Agent Settings

The agent is configured with:
- **Model**: Llama 3.1 (default, configurable)
- **Temperature**: 0.1 (for consistent, focused responses)
- **Recursion Limit**: 5 iterations (prevents infinite loops)
- **Max Results**: 5 papers per arXiv search (maximum allowed)

### Environment Variables

- `TAVILY_API_KEY`: Required for Tavily web search functionality
- `DLAI_TAVILY_BASE_URL`: Optional custom Tavily API base URL

## Examples

### Example 1: Academic Research
```python
result = find_references("Find recent papers on transformer architectures in NLP")
```

### Example 2: Current Events
```python
result = find_references("What are the latest developments in AI safety research?")
```

### Example 3: General Knowledge
```python
result = find_references("Explain the theory of relativity")
```

## Dependencies

Key dependencies include:
- `langchain`: Agent framework
- `langchain-ollama`: Ollama integration
- `tavily-python`: Web search API
- `wikipedia`: Wikipedia API wrapper
- `requests`: HTTP requests
- `python-dotenv`: Environment variable management

See `requirements.txt` for the complete list.

## Limitations

- The agent is limited to 5 iterations per task to prevent excessive API calls
- arXiv searches are limited to 5 results maximum
- Requires Ollama running locally with appropriate models
- Tavily API key required for web search functionality

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

[Add your license information here]

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Uses [Ollama](https://ollama.ai/) for local LLM inference
- Integrates [Tavily](https://tavily.com/) for web search
- Uses [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) for encyclopedic information
