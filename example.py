"""Example usage of FixtureGPT."""

import os
import time
import random
from fixturegpt import snapshot

# Set to record mode first
os.environ["FIXTUREGPT_MODE"] = "record"

def expensive_llm_call(prompt: str, model: str = "gpt-3.5-turbo"):
    """Simulate an expensive LLM API call."""
    print(f"🔥 Making expensive API call for: '{prompt}'")
    time.sleep(1)  # Simulate network delay
    
    # Simulate different responses
    responses = [
        f"Response to '{prompt}': This is a helpful answer about your query.",
        f"Regarding '{prompt}': Here's what I think about that topic.",
        f"About '{prompt}': Let me provide you with detailed information."
    ]
    
    return {
        "model": model,
        "choices": [{
            "message": {
                "content": random.choice(responses)
            }
        }],
        "usage": {
            "prompt_tokens": len(prompt.split()) * 2,
            "completion_tokens": 50,
            "total_tokens": len(prompt.split()) * 2 + 50
        }
    }

def expensive_vector_search(query: str, top_k: int = 5):
    """Simulate an expensive vector database search."""
    print(f"🔍 Searching vector database for: '{query}'")
    time.sleep(0.5)  # Simulate search time
    
    return [
        {"text": f"Document {i} about {query}", "score": 0.9 - i*0.1}
        for i in range(top_k)
    ]

def main():
    print("🚀 FixtureGPT Example")
    print("=" * 50)
    
    # Example 1: LLM calls
    print("\n📝 Example 1: LLM Calls")
    result1 = snapshot("user_question", expensive_llm_call, "What is Python?")
    print(f"Result: {result1['choices'][0]['message']['content'][:50]}...")
    
    # Example 2: Vector search
    print("\n🔍 Example 2: Vector Search")
    docs = snapshot("python_search", expensive_vector_search, "Python programming", top_k=3)
    print(f"Found {len(docs)} documents")
    
    # Example 3: Same call again (should use cache in replay mode)
    print("\n🔄 Example 3: Repeated Call")
    os.environ["FIXTUREGPT_MODE"] = "replay"
    result2 = snapshot("user_question", expensive_llm_call, "What is Python?")
    print(f"Result: {result2['choices'][0]['message']['content'][:50]}...")
    
    print("\n✅ Examples complete! Check ./fixtures/ for saved data")
    print("💡 Try: fixturegpt stats")

if __name__ == "__main__":
    main() 