# FixtureGPT 🎯

[![PyPI version](https://badge.fury.io/py/fixturegpt.svg)](https://badge.fury.io/py/fixturegpt)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful developer tool for **recording and replaying expensive AI/LLM outputs** during development and testing. Perfect for AI developers working with OpenAI, Anthropic, Claude, RAG pipelines, and agent workflows.

## 🚀 Quick Start

### Installation

```bash
pip install fixturegpt
```

### Basic Usage

```python
import os
from fixturegpt import snapshot

# Set environment variable to control behavior
os.environ["FIXTUREGPT_MODE"] = "record"  # or "replay"

# Wrap your expensive function calls
def expensive_llm_call(prompt):
    # Your actual LLM call here
    return openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

# Use snapshot to record/replay
result = snapshot("user_question", expensive_llm_call, "What is the meaning of life?")
```

## ✨ Features

- 🎯 **Record & Replay**: Automatically cache expensive function outputs
- 🔄 **Environment Control**: Switch between record/replay modes with `FIXTUREGPT_MODE`
- 🔐 **Smart Deduplication**: SHA256 hashing prevents duplicate recordings
- 💰 **Cost Tracking**: Estimate money saved by avoiding repeated API calls
- 🎨 **Beautiful CLI**: Rich terminal interface for managing fixtures
- 📦 **JSON Storage**: Human-readable fixture files in `./fixtures/`
- 🛡️ **Graceful Fallbacks**: Handles non-serializable objects elegantly

## 🎛️ Environment Modes

| Mode | Behavior |
|------|----------|
| `FIXTUREGPT_MODE=record` | Execute functions and save outputs to fixtures |
| `FIXTUREGPT_MODE=replay` | Return cached outputs without executing functions |
| Not set | Normal execution (no recording/replaying) |

## 🖥️ CLI Commands

After installation, use the `fixturegpt` command:

```bash
# View fixture statistics and cost savings
fixturegpt stats

# Inspect specific fixtures
fixturegpt diff "function_name"

# Clear all fixtures
fixturegpt clear
```

## 📊 Use Cases

### LLM Development
```python
from fixturegpt import snapshot
import openai

def ask_gpt(question):
    return openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )

# Record expensive GPT-4 calls during development
answer = snapshot("research_question", ask_gpt, "Explain quantum computing")
```

### RAG Pipeline Testing
```python
def retrieve_documents(query):
    # Expensive vector database search
    return vector_db.similarity_search(query, k=10)

# Cache retrieval results for consistent testing
docs = snapshot("rag_retrieval", retrieve_documents, "machine learning basics")
```

### Agent Workflows
```python
def agent_tool_call(tool_name, params):
    # Expensive tool execution
    return agent.execute_tool(tool_name, params)

# Record tool outputs for debugging
result = snapshot("web_search", agent_tool_call, "search", {"query": "latest AI news"})
```

## 🏗️ Advanced Usage

### Custom Fixture Directory
```python
# Fixtures are saved to ./fixtures/ by default
# You can organize them however you like
```

### Handling Non-Serializable Objects
FixtureGPT gracefully handles objects that can't be JSON-serialized by converting them to string representations.

### Cost Estimation
The CLI provides cost estimates based on typical LLM pricing:
- Default estimate: $0.002 per API call
- Tracks total calls avoided
- Shows cumulative savings

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](https://docs.fixturegpt.com)
- 🐛 [Bug Reports](https://github.com/fixturegpt/fixturegpt/issues)
- 💬 [Discussions](https://github.com/fixturegpt/fixturegpt/discussions)

---

**Made with ❤️ for the AI developer community** 