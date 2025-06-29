# FixtureGPT - Getting Started Guide

## 🎯 What is FixtureGPT?

FixtureGPT is a developer tool that **records and replays expensive function calls** to speed up development and testing of AI/LLM applications. Think of it as a smart cache for your expensive operations.

## 🚀 Quick Installation

### Option 1: Simple Copy Installation (Recommended)
```bash
# Clone or download the fixturegpt directory
# Then run:
python install.py
```

### Option 2: Direct Usage (No Installation)
```bash
# Just add the fixturegpt directory to your Python path
import sys
sys.path.append('/path/to/fixturegpt')
from fixturegpt import snapshot
```

## 📖 Basic Usage

### 1. Import and Set Mode
```python
import os
from fixturegpt import snapshot

# Set the mode
os.environ["FIXTUREGPT_MODE"] = "record"  # or "replay"
```

### 2. Wrap Your Expensive Functions
```python
# Instead of calling directly:
result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Use snapshot:
result = snapshot("greeting", openai.ChatCompletion.create,
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## 🎮 Interactive Demo

Run the demo to see all features in action:
```bash
python demo.py
```

## 🔧 Real-World Examples

### Example 1: OpenAI API Calls
```python
import os
import openai
from fixturegpt import snapshot

# Set your API key
openai.api_key = "your-api-key"

# Record mode - calls API and saves response
os.environ["FIXTUREGPT_MODE"] = "record"

def ask_gpt(question):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )

# This will call OpenAI API and save the result
answer = snapshot("python_question", ask_gpt, "What is Python?")
print(answer.choices[0].message.content)

# Switch to replay mode
os.environ["FIXTUREGPT_MODE"] = "replay"

# This will use the cached result (no API call!)
cached_answer = snapshot("python_question", ask_gpt, "What is Python?")
print("Same answer, no API call:", cached_answer.choices[0].message.content)
```

### Example 2: RAG Pipeline
```python
import os
from fixturegpt import snapshot

# Your expensive functions
def search_documents(query, top_k=5):
    # Expensive vector database search
    return vector_db.similarity_search(query, k=top_k)

def generate_response(query, context):
    # Expensive LLM call
    return llm.generate(f"Query: {query}\nContext: {context}")

# RAG pipeline with caching
os.environ["FIXTUREGPT_MODE"] = "record"

query = "What is machine learning?"

# Cache the expensive search
docs = snapshot("ml_search", search_documents, query, top_k=3)

# Cache the expensive generation
context = "\n".join([doc.content for doc in docs])
response = snapshot("ml_response", generate_response, query, context)

print(f"Response: {response}")

# Later, switch to replay mode for instant results
os.environ["FIXTUREGPT_MODE"] = "replay"
# Same calls will be instant!
```

### Example 3: Agent Tool Calls
```python
import os
from fixturegpt import snapshot

def web_search(query):
    # Expensive web search API call
    return search_api.search(query)

def code_execution(code):
    # Expensive code execution
    return code_executor.run(code)

# Agent workflow with caching
os.environ["FIXTUREGPT_MODE"] = "record"

# Cache tool outputs for consistent testing
search_results = snapshot("web_search_ai", web_search, "latest AI news")
code_result = snapshot("python_code", code_execution, "print('Hello, World!')")

# Your agent can now use these cached results
agent_response = process_agent_step(search_results, code_result)
```

## 🎛️ Environment Variables

| Variable | Values | Description |
|----------|--------|-------------|
| `FIXTUREGPT_MODE` | `record` | Call functions and save results |
| `FIXTUREGPT_MODE` | `replay` | Use cached results, skip function calls |

## 🔍 CLI Commands

### View Statistics
```bash
python -m fixturegpt.cli stats
```
Shows:
- Number of fixtures
- Total disk usage
- Estimated cost savings
- Detailed fixture list

### Inspect Fixtures
```bash
python -m fixturegpt.cli diff "fixture_name"
```
Shows:
- Original function arguments
- Saved response
- Timestamp

### Clear All Fixtures
```bash
python -m fixturegpt.cli clear
```

## 📁 Fixture Storage

Fixtures are stored as JSON files in `./fixtures/`:
```
fixtures/
├── openai_call-a1b2c3d4.json
├── vector_search-e5f6g7h8.json
└── data_processing-i9j0k1l2.json
```

Each fixture contains:
```json
{
  "name": "openai_call",
  "args": ["What is Python?"],
  "kwargs": {"model": "gpt-3.5-turbo"},
  "response": {"choices": [...]},
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🎯 Use Cases

### 1. **Prompt Engineering**
- Record LLM responses during prompt development
- Replay responses for consistent testing
- Avoid API costs during iteration

### 2. **Agent Development**
- Cache tool outputs for reproducible testing
- Speed up agent workflow debugging
- Consistent test environments

### 3. **RAG Pipeline Development**
- Cache expensive vector searches
- Record retrieval results
- Fast iteration on generation logic

### 4. **Data Processing**
- Cache expensive computations
- Record API responses
- Reproducible data science workflows

## ⚡ Performance Benefits

| Operation | Without FixtureGPT | With FixtureGPT (Replay) |
|-----------|-------------------|-------------------------|
| OpenAI API Call | ~2-5 seconds | ~0.001 seconds |
| Vector Search | ~0.5-2 seconds | ~0.001 seconds |
| Data Processing | ~10-60 seconds | ~0.001 seconds |

## 🔒 Best Practices

### 1. **Naming Conventions**
```python
# Good: Descriptive names
snapshot("user_greeting_gpt4", ...)
snapshot("product_search_embeddings", ...)

# Avoid: Generic names
snapshot("test", ...)
snapshot("call1", ...)
```

### 2. **Mode Management**
```python
# Set mode at the start of your script
import os
os.environ["FIXTUREGPT_MODE"] = "record"  # or "replay"

# Or use environment variables
# export FIXTUREGPT_MODE=replay
```

### 3. **Fixture Organization**
```python
# Use prefixes for different components
snapshot("rag_search", ...)      # RAG pipeline
snapshot("agent_tool", ...)      # Agent tools
snapshot("preprocessing", ...)   # Data preprocessing
```

### 4. **Development Workflow**
```python
# 1. Development phase - record real calls
os.environ["FIXTUREGPT_MODE"] = "record"

# 2. Testing phase - use cached results
os.environ["FIXTUREGPT_MODE"] = "replay"

# 3. Production - remove snapshots or use record mode
```

## 🚨 Troubleshooting

### Common Issues

**1. "No fixtures found" in replay mode**
- Make sure you've recorded fixtures first with `FIXTUREGPT_MODE=record`
- Check that function arguments match exactly

**2. "Not JSON serializable" warning**
- Some objects can't be saved as JSON
- FixtureGPT will still call the function, just won't cache the result

**3. CLI commands not working**
- Use: `python -m fixturegpt.cli stats` instead of `fixturegpt stats`
- Or install properly with `python install.py`

### Getting Help

1. **Check the demo**: `python demo.py`
2. **View fixture stats**: `python -m fixturegpt.cli stats`
3. **Inspect fixtures**: `python -m fixturegpt.cli diff "name"`

## 🎉 You're Ready!

FixtureGPT is now ready to speed up your AI/LLM development workflow. Start by:

1. **Recording** your expensive operations
2. **Replaying** them during development
3. **Monitoring** savings with CLI tools

Happy coding! 🚀 