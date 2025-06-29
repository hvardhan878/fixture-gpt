#!/usr/bin/env python3
"""
FixtureGPT Cloud Sync Example
Demonstrates how to use FixtureGPT with cloud sync to the SaaS dashboard.
"""

import os
import time
import random
from fixturegpt import snapshot, configure_cloud_sync

def simulate_openai_call(prompt: str, model: str = "gpt-4"):
    """Simulate an expensive OpenAI API call."""
    print(f"🤖 [OpenAI] Calling {model} with prompt: '{prompt[:50]}...'")
    time.sleep(0.5)  # Simulate API latency
    
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
    """Simulate an expensive vector search operation."""
    print(f"🔍 [VectorDB] Searching '{query}' in {collection} (top {top_k})")
    time.sleep(0.3)  # Simulate search latency
    
    # Simulate search results
    results = []
    for i in range(top_k):
        results.append({
            "id": f"doc_{i}",
            "score": 0.95 - (i * 0.1),
            "text": f"Document {i} about {query}. This contains relevant information about the topic.",
            "metadata": {"source": f"source_{i}.pdf", "page": i + 1}
        })
    
    return results

def demo_cloud_sync():
    """Demonstrate cloud sync functionality."""
    print("🌟 FixtureGPT Cloud Sync Demo")
    print("=" * 60)
    
    # Option 1: Configure via environment variables
    print("\n📋 Step 1: Configure Cloud Sync")
    print("You can configure cloud sync in two ways:")
    print("1. Environment variables:")
    print("   export FIXTUREGPT_API_KEY='your-api-key-here'")
    print("   export FIXTUREGPT_SYNC_MODE='both'  # local, cloud, or both")
    print("   export FIXTUREGPT_API_URL='https://app.fixturegpt.com'")
    print()
    print("2. Programmatically:")
    print("   configure_cloud_sync('your-api-key-here', 'both')")
    
    # For demo purposes, we'll simulate having an API key
    demo_api_key = os.getenv('FIXTUREGPT_API_KEY', 'demo-key-12345')
    
    if demo_api_key == 'demo-key-12345':
        print("\n⚠️  Using demo API key. Get your real API key from https://app.fixturegpt.com")
    
    # Configure cloud sync
    configure_cloud_sync(demo_api_key, 'both')
    
    # Set to record mode
    os.environ["FIXTUREGPT_MODE"] = "record"
    
    print("\n🔴 Step 2: Recording with Cloud Sync")
    print("Recording fixtures locally AND syncing to cloud dashboard...")
    
    # Record some expensive operations
    result1 = snapshot("cloud_openai_test", simulate_openai_call, "What is Python?")
    print(f"✅ Result: {result1['choices'][0]['message']['content'][:60]}...")
    
    result2 = snapshot("cloud_vector_test", simulate_vector_search, "machine learning", top_k=3)
    print(f"✅ Found {len(result2)} documents")
    
    # Switch to replay mode
    print("\n📼 Step 3: Replaying from Cloud")
    os.environ["FIXTUREGPT_MODE"] = "replay"
    
    # These should replay from local cache (fastest)
    print("Replaying from local cache...")
    start_time = time.time()
    result3 = snapshot("cloud_openai_test", simulate_openai_call, "What is Python?")
    result4 = snapshot("cloud_vector_test", simulate_vector_search, "machine learning", top_k=3)
    end_time = time.time()
    
    print(f"⚡ Local replay completed in {end_time - start_time:.3f}s")
    
    # Simulate cloud-only mode
    print("\n☁️  Step 4: Cloud-Only Mode")
    print("Setting sync mode to 'cloud' - will load from dashboard only...")
    
    # Configure for cloud-only
    configure_cloud_sync(demo_api_key, 'cloud')
    
    # This would try to load from cloud (will fail with demo key)
    try:
        result5 = snapshot("cloud_only_test", simulate_openai_call, "How does RAG work?")
        print(f"✅ Cloud result: {result5['choices'][0]['message']['content'][:60]}...")
    except Exception as e:
        print(f"⚠️  Cloud sync failed (expected with demo key): Will fall back to live call")
        result5 = snapshot("cloud_only_test", simulate_openai_call, "How does RAG work?")
        print(f"✅ Fallback result: {result5['choices'][0]['message']['content'][:60]}...")

def demo_team_collaboration():
    """Demonstrate team collaboration features."""
    print("\n" + "=" * 60)
    print("👥 Team Collaboration Demo")
    print("=" * 60)
    
    print("With FixtureGPT Cloud Sync, your team can:")
    print("• 🔄 Share fixtures across team members")
    print("• 📊 Track usage and costs in the dashboard")
    print("• 🎯 Organize fixtures by project/environment")
    print("• 🔍 Search and browse all team fixtures")
    print("• 📈 Monitor savings and performance metrics")
    
    print("\nExample team workflow:")
    print("1. Developer A records expensive LLM calls")
    print("2. Fixtures automatically sync to team dashboard")
    print("3. Developer B can replay the same calls instantly")
    print("4. Team lead monitors costs and usage patterns")
    print("5. QA team uses fixtures for consistent testing")

def demo_advanced_features():
    """Demonstrate advanced cloud sync features."""
    print("\n" + "=" * 60)
    print("🚀 Advanced Features")
    print("=" * 60)
    
    print("Advanced cloud sync features:")
    print("• 🏷️  Automatic tagging and categorization")
    print("• 🔐 Team access controls and permissions")
    print("• 📱 Mobile dashboard for monitoring")
    print("• 🔔 Slack/email notifications for usage alerts")
    print("• 📊 Cost analytics and budget tracking")
    print("• 🌍 Multi-region fixture replication")
    print("• 🔄 Automatic fixture cleanup and archiving")
    print("• 📝 Fixture documentation and comments")

def main():
    """Main demo function."""
    print("🎯 FixtureGPT Cloud Sync - Complete Demo")
    print("=" * 60)
    
    demo_cloud_sync()
    demo_team_collaboration()
    demo_advanced_features()
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. 🔑 Get your API key: https://app.fixturegpt.com/dashboard/api-keys")
    print("2. 💰 Choose your plan: https://app.fixturegpt.com/pricing")
    print("3. 📚 Read the docs: https://docs.fixturegpt.com")
    print("4. 💬 Join our Discord: https://discord.gg/fixturegpt")
    
    print("\nHappy caching! 🚀")

if __name__ == "__main__":
    main() 