# FixtureGPT 🎯

[![PyPI version](https://badge.fury.io/py/fixturegpt.svg)](https://badge.fury.io/py/fixturegpt)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful developer tool for **recording and replaying expensive AI/LLM outputs** during development and testing. Perfect for AI developers working with OpenAI, Anthropic, Claude, RAG pipelines, and agent workflows.

**NEW: ☁️ Cloud Sync** - Sync fixtures across your team with the FixtureGPT SaaS dashboard!

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

### ☁️ Cloud Sync Setup

Enable cloud sync to share fixtures across your team:

```python
from fixturegpt import configure_cloud_sync

# Option 1: Configure programmatically
configure_cloud_sync(
    api_key="your-api-key-here",
    sync_mode="both"  # local, cloud, or both
)

# Option 2: Use environment variables
# export FIXTUREGPT_API_KEY="your-api-key-here"
# export FIXTUREGPT_SYNC_MODE="both"
```

Get your API key at: [https://app.fixturegpt.com/dashboard/api-keys](https://app.fixturegpt.com/dashboard/api-keys)

## ✨ Features

### Core Features
- 🎯 **Record & Replay**: Automatically cache expensive function outputs
- 🔄 **Environment Control**: Switch between record/replay modes with `FIXTUREGPT_MODE`
- 🔐 **Smart Deduplication**: SHA256 hashing prevents duplicate recordings
- 💰 **Cost Tracking**: Estimate money saved by avoiding repeated API calls
- 🎨 **Beautiful CLI**: Rich terminal interface for managing fixtures
- 📦 **JSON Storage**: Human-readable fixture files in `./fixtures/`
- 🛡️ **Graceful Fallbacks**: Handles non-serializable objects elegantly

### ☁️ Cloud Sync Features
- 🌐 **Team Collaboration**: Share fixtures across team members instantly
- 📊 **Usage Analytics**: Track costs and performance in the dashboard
- 🔄 **Multi-Mode Sync**: Choose local-only, cloud-only, or hybrid sync
- 🚀 **Automatic Fallback**: Falls back to local cache if cloud is unavailable
- 🏷️ **Smart Organization**: Automatic tagging and categorization
- 📱 **Web Dashboard**: Manage fixtures from anywhere
- 🔐 **Access Control**: Team permissions and API key management

## 🎛️ Configuration

### Environment Modes

| Mode | Behavior |
|------|----------|
| `FIXTUREGPT_MODE=record` | Execute functions and save outputs to fixtures |
| `FIXTUREGPT_MODE=replay` | Return cached outputs without executing functions |
| Not set | Normal execution (no recording/replaying) |

### Cloud Sync Modes

| Sync Mode | Behavior |
|-----------|----------|
| `FIXTUREGPT_SYNC_MODE=local` | Save/load fixtures locally only (default) |
| `FIXTUREGPT_SYNC_MODE=cloud` | Save/load fixtures from cloud dashboard only |
| `FIXTUREGPT_SYNC_MODE=both` | Hybrid: local for speed, cloud for sharing |

### Environment Variables

```bash
# Core configuration
export FIXTUREGPT_MODE="record"           # record, replay
export FIXTUREGPT_SYNC_MODE="both"        # local, cloud, both

# Cloud sync configuration
export FIXTUREGPT_API_KEY="your-api-key"  # Get from dashboard
export FIXTUREGPT_API_URL="https://app.fixturegpt.com"  # Optional
```

## 🖥️ CLI Commands

After installation, use the `fixturegpt` command:

```bash
# View fixture statistics and cost savings
fixturegpt stats

# Show current configuration
fixturegpt config

# Inspect specific fixtures
fixturegpt diff "function_name"

# Clear all local fixtures
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

### Team Collaboration Workflow

```python
from fixturegpt import configure_cloud_sync, snapshot

# Team member A: Records fixtures
configure_cloud_sync("team-api-key", "both")
os.environ["FIXTUREGPT_MODE"] = "record"

# Expensive model calls get cached locally AND synced to team dashboard
result = snapshot("user_onboarding", expensive_llm_call, "Generate welcome email")

# Team member B: Replays same fixtures instantly
configure_cloud_sync("team-api-key", "both")
os.environ["FIXTUREGPT_MODE"] = "replay"

# Gets cached result from cloud (or local if available)
same_result = snapshot("user_onboarding", expensive_llm_call, "Generate welcome email")
```

## 🏗️ Advanced Usage

### Hybrid Sync Strategy
```python
# Best practice: Use "both" mode for optimal performance
configure_cloud_sync("your-api-key", "both")

# This provides:
# - Local cache for fastest access
# - Cloud sync for team sharing
# - Automatic fallback if cloud is unavailable
```

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
- Cloud dashboard provides detailed analytics

## 💰 Pricing

### Open Source Package
- ✅ **Free forever** - Local fixtures only
- ✅ All core features included
- ✅ CLI tools and local storage

### Cloud Sync Plans
- 🆓 **Free Tier**: 100 fixtures/month
- 💼 **Pro**: $19/month - Unlimited fixtures, team collaboration
- 🏢 **Team**: $49/month - Advanced analytics, priority support
- 🏭 **Enterprise**: Custom pricing - On-premises, SSO, compliance

[View detailed pricing →](https://app.fixturegpt.com/pricing)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 🌐 [FixtureGPT Dashboard](https://app.fixturegpt.com)
- 📖 [Documentation](https://docs.fixturegpt.com)
- 🐛 [Bug Reports](https://github.com/fixturegpt/fixturegpt/issues)
- 💬 [Discord Community](https://discord.gg/fixturegpt)
- 📧 [Email Support](mailto:support@fixturegpt.com)

---

**Made with ❤️ for the AI developer community** 