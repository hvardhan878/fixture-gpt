#!/usr/bin/env python3
"""
FixtureGPT Demo - Complete demonstration of all features
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Add the current directory to Python path so we can import fixturegpt
sys.path.insert(0, str(Path(__file__).parent))

from fixturegpt import snapshot

def simulate_openai_call(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
    """Simulate an expensive OpenAI API call."""
    print(f"🤖 [OpenAI] Calling {model} with prompt: '{prompt[:50]}...'")
    time.sleep(0.8)  # Simulate API latency
    
    responses = {
        "What is Python?": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "Explain machine learning": "Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed.",
        "How does RAG work?": "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation to provide more accurate and contextual responses."
    }
    
    return {
        "id": f"chatcmpl-{hash(prompt) % 10000}",
        "object": "chat.completion",
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": responses.get(prompt, f"This is a response to: {prompt}")
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(prompt.split()) * 2,
            "completion_tokens": 50,
            "total_tokens": len(prompt.split()) * 2 + 50
        }
    }

def simulate_vector_search(query: str, collection: str = "documents", top_k: int = 5):
    """Simulate an expensive vector database search."""
    print(f"🔍 [VectorDB] Searching '{collection}' for: '{query}' (top_k={top_k})")
    time.sleep(0.5)  # Simulate search time
    
    return [
        {
            "id": f"doc_{i}",
            "text": f"Document {i} about {query}: This contains relevant information about the topic.",
            "metadata": {"source": f"source_{i}.pdf", "page": i + 1},
            "score": 0.95 - (i * 0.1)
        }
        for i in range(top_k)
    ]

def simulate_expensive_computation(data: list, operation: str = "analyze"):
    """Simulate an expensive data processing operation."""
    print(f"⚡ [Compute] Running {operation} on {len(data)} items")
    time.sleep(1.2)  # Simulate processing time
    
    return {
        "operation": operation,
        "input_size": len(data),
        "results": {
            "processed": len(data),
            "insights": f"Analysis complete for {operation}",
            "score": 0.87
        },
        "execution_time": "1.2s"
    }

def demo_basic_usage():
    """Demo 1: Basic record and replay functionality."""
    print("\n" + "="*60)
    print("🎯 DEMO 1: Basic Record & Replay")
    print("="*60)
    
    # Set to record mode
    os.environ["FIXTUREGPT_MODE"] = "record"
    print("📝 Mode: RECORD - Will call actual functions and save results")
    
    # Record some expensive operations
    result1 = snapshot("openai_python", simulate_openai_call, "What is Python?")
    print(f"✅ Result: {result1['choices'][0]['message']['content'][:60]}...")
    
    result2 = snapshot("vector_search_ml", simulate_vector_search, "machine learning", top_k=3)
    print(f"✅ Found {len(result2)} documents")
    
    # Switch to replay mode
    print("\n🔄 Switching to REPLAY mode...")
    os.environ["FIXTUREGPT_MODE"] = "replay"
    
    # Same calls should now use cached results (much faster!)
    start_time = time.time()
    result3 = snapshot("openai_python", simulate_openai_call, "What is Python?")
    result4 = snapshot("vector_search_ml", simulate_vector_search, "machine learning", top_k=3)
    end_time = time.time()
    
    print(f"⚡ Replay completed in {end_time - start_time:.3f}s (vs ~1.3s for live calls)")
    print(f"✅ Same result: {result3['choices'][0]['message']['content'][:60]}...")

def demo_rag_pipeline():
    """Demo 2: Complete RAG pipeline with caching."""
    print("\n" + "="*60)
    print("🔍 DEMO 2: RAG Pipeline with FixtureGPT")
    print("="*60)
    
    os.environ["FIXTUREGPT_MODE"] = "record"
    
    query = "Explain machine learning"
    
    # Step 1: Vector search (expensive)
    docs = snapshot("rag_search", simulate_vector_search, query, "knowledge_base", 5)
    print(f"📚 Retrieved {len(docs)} relevant documents")
    
    # Step 2: Generate response using retrieved docs (expensive)
    context = " ".join([doc["text"] for doc in docs[:3]])
    response = snapshot("rag_generate", simulate_openai_call, query, "gpt-4")
    print(f"🤖 Generated response: {response['choices'][0]['message']['content'][:80]}...")
    
    # Step 3: Now replay the entire pipeline instantly
    print("\n🔄 Replaying RAG pipeline...")
    os.environ["FIXTUREGPT_MODE"] = "replay"
    
    start_time = time.time()
    cached_docs = snapshot("rag_search", simulate_vector_search, query, "knowledge_base", 5)
    cached_response = snapshot("rag_generate", simulate_openai_call, query, "gpt-4")
    end_time = time.time()
    
    print(f"⚡ Full RAG pipeline replayed in {end_time - start_time:.3f}s")

def demo_cli_features():
    """Demo 3: CLI features."""
    print("\n" + "="*60)
    print("💻 DEMO 3: CLI Features")
    print("="*60)
    
    print("📊 Fixture Statistics:")
    subprocess.run([sys.executable, "-m", "fixturegpt.cli", "stats"])
    
    print("\n🔍 Fixture Details for 'openai_python':")
    subprocess.run([sys.executable, "-m", "fixturegpt.cli", "diff", "openai_python"])

def demo_advanced_scenarios():
    """Demo 4: Advanced scenarios and edge cases."""
    print("\n" + "="*60)
    print("🚀 DEMO 4: Advanced Scenarios")
    print("="*60)
    
    os.environ["FIXTUREGPT_MODE"] = "record"
    
    # Scenario 1: Complex data structures
    complex_data = [{"id": i, "value": f"item_{i}"} for i in range(100)]
    result = snapshot("data_processing", simulate_expensive_computation, complex_data, "deep_analysis")
    print(f"🔬 Processed {result['input_size']} items: {result['results']['insights']}")
    
    # Scenario 2: Function with multiple parameters
    result = snapshot("multi_param", simulate_vector_search, "AI research", "papers", 10)
    print(f"📄 Found {len(result)} research papers")
    
    # Scenario 3: Fallback behavior (no fixture exists)
    os.environ["FIXTUREGPT_MODE"] = "replay"
    result = snapshot("new_query", simulate_openai_call, "How does RAG work?")
    print(f"🔄 Fallback worked: {result['choices'][0]['message']['content'][:60]}...")

def main():
    """Run the complete FixtureGPT demonstration."""
    print("🎉 FixtureGPT Complete Demo")
    print("🎯 A Python tool for AI/LLM developers to cache expensive operations")
    
    # Clean start
    if Path("fixtures").exists():
        import shutil
        shutil.rmtree("fixtures")
        print("🧹 Cleaned previous fixtures")
    
    # Run all demos
    demo_basic_usage()
    demo_rag_pipeline()
    demo_advanced_scenarios()
    demo_cli_features()
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE!")
    print("="*60)
    print("🎯 Key Features Demonstrated:")
    print("  • ✅ Record/Replay expensive function calls")
    print("  • ✅ SHA256 hashing for deduplication")
    print("  • ✅ JSON serialization with graceful fallbacks")
    print("  • ✅ CLI tools for stats and debugging")
    print("  • ✅ Cost estimation for LLM calls")
    print("  • ✅ RAG pipeline optimization")
    print("  • ✅ Fallback to live calls when needed")
    print("\n💡 Try these commands:")
    print("  python -m fixturegpt.cli stats")
    print("  python -m fixturegpt.cli diff 'openai_python'")
    print("  python -m fixturegpt.cli clear")
    print("\n🚀 Ready for production use!")

if __name__ == "__main__":
    main() 