# verify_max_iterations.py
"""
Verification script to test how to set max_iterations in LangChain 1.2.9's create_agent.
Run this to determine which approach works.
"""
from langchain import agents
from langchain_ollama import ChatOllama
from langchain_core.tools import StructuredTool
import inspect

print("=" * 80)
print("VERIFICATION: How to set max_iterations in LangChain 1.2.9")
print("=" * 80)

# 1. Check create_agent signature
print("\n[1] Checking create_agent signature:")
print("-" * 80)
try:
    sig = inspect.signature(agents.create_agent)
    params = list(sig.parameters.keys())
    print(f"Parameters: {params}")
    if "max_iterations" in params:
        print("✓ create_agent accepts max_iterations directly")
    else:
        print("✗ create_agent does NOT accept max_iterations")
    print(f"\nFull signature:\n{sig}")
except Exception as e:
    print(f"Error: {e}")

# 2. Check AgentExecutor
print("\n[2] Checking AgentExecutor:")
print("-" * 80)
try:
    from langchain.agents import AgentExecutor
    sig = inspect.signature(AgentExecutor.__init__)
    params = list(sig.parameters.keys())
    print(f"AgentExecutor.__init__ parameters: {params}")
    if "max_iterations" in params:
        print("✓ AgentExecutor accepts max_iterations")
    else:
        print("✗ AgentExecutor does NOT accept max_iterations")
except ImportError:
    print("✗ AgentExecutor not found in langchain.agents")
    # Try alternative import
    try:
        from langchain.agents.agent import AgentExecutor
        sig = inspect.signature(AgentExecutor.__init__)
        params = list(sig.parameters.keys())
        print(f"AgentExecutor (alt import) parameters: {params}")
        if "max_iterations" in params:
            print("✓ AgentExecutor accepts max_iterations")
    except:
        print("✗ AgentExecutor not found in alternative location")
except Exception as e:
    print(f"Error: {e}")

# 3. Check what create_agent returns
print("\n[3] Checking what create_agent returns:")
print("-" * 80)
try:
    llm = ChatOllama(model="llama3.1", temperature=0.1)
    tools = []
    agent = agents.create_agent(model=llm, tools=tools, system_prompt="Test")
    print(f"Agent type: {type(agent)}")
    print(f"Agent class: {agent.__class__.__name__}")
    print(f"Agent module: {agent.__class__.__module__}")
    
    # Check if agent.invoke accepts config
    if hasattr(agent, 'invoke'):
        sig = inspect.signature(agent.invoke)
        params = list(sig.parameters.keys())
        print(f"\nagent.invoke parameters: {params}")
        if "config" in params:
            print("✓ agent.invoke accepts 'config' parameter")
        else:
            print("✗ agent.invoke does NOT accept 'config' parameter")
        print(f"\nFull invoke signature:\n{sig}")
except Exception as e:
    print(f"Error: {e}")

# 4. Check for max_iterations in configurable fields
print("\n[4] Checking for configurable fields:")
print("-" * 80)
try:
    llm = ChatOllama(model="llama3.1", temperature=0.1)
    tools = []
    agent = agents.create_agent(model=llm, tools=tools, system_prompt="Test")
    
    # Check if agent has config_schema or similar
    if hasattr(agent, 'config_schema'):
        print(f"agent.config_schema: {agent.config_schema}")
    if hasattr(agent, 'input_schema'):
        print(f"agent.input_schema: {agent.input_schema}")
    if hasattr(agent, 'output_schema'):
        print(f"agent.output_schema: {agent.output_schema}")
except Exception as e:
    print(f"Error: {e}")

# 5. Check LangChain version
print("\n[5] Checking LangChain version:")
print("-" * 80)
try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("1. If create_agent accepts max_iterations → use it directly")
print("2. If AgentExecutor accepts max_iterations → wrap agent in AgentExecutor")
print("3. If agent.invoke accepts config → pass max_iterations in config dict")
print("4. Otherwise → may need to use middleware or manual iteration control")