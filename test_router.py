"""Test suite for the LLM Prompt Router.

This script tests the router with all 15 required test messages and verifies:
1. Intent classification works correctly
2. Responses are generated for each intent
3. Logging is working properly
4. Error handling for unclear intents
"""

import json
from prompt_router import classify_intent, route_and_respond, process_message

# All 15 required test messages
TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose."
]

def test_classify_intent():
    """Test intent classification function."""
    print("\n" + "="*70)
    print("TEST 1: Intent Classification")
    print("="*70)
    
    for i, msg in enumerate(TEST_MESSAGES[:5], 1):
        try:
            intent = classify_intent(msg)
            print(f"\nMessage {i}: {msg[:50]}...")
            print(f"  Intent: {intent.get('intent')}")
            print(f"  Confidence: {intent.get('confidence')}")
            assert "intent" in intent, "Missing 'intent' key"
            assert "confidence" in intent, "Missing 'confidence' key"
            assert isinstance(intent["confidence"], (int, float)), "Confidence must be numeric"
            print("  ✓ PASSED")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")

def test_route_and_respond():
    """Test routing and response generation."""
    print("\n" + "="*70)
    print("TEST 2: Routing and Response Generation")
    print("="*70)
    
    for i, msg in enumerate(TEST_MESSAGES[5:10], 1):
        try:
            intent = classify_intent(msg)
            response = route_and_respond(msg, intent)
            print(f"\nMessage {i}: {msg[:50]}...")
            print(f"  Intent: {intent.get('intent')}")
            print(f"  Response (first 80 chars): {response[:80]}...")
            assert isinstance(response, str), "Response must be a string"
            assert len(response) > 0, "Response cannot be empty"
            
            # Check if unclear intent returns clarification
            if intent.get("intent") == "unclear":
                assert "?" in response, "Unclear intent should ask a question"
            print("  ✓ PASSED")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")

def test_error_handling():
    """Test error handling for unclear intents."""
    print("\n" + "="*70)
    print("TEST 3: Error Handling for Unclear Intents")
    print("="*70)
    
    unclear_messages = [
        "hey",
        "Can you write me a poem about clouds?",
        "Help me make this better."
    ]
    
    for i, msg in enumerate(unclear_messages, 1):
        try:
            intent = classify_intent(msg)
            response = route_and_respond(msg, intent)
            print(f"\nMessage {i}: {msg[:50]}...")
            print(f"  Intent: {intent.get('intent')}")
            if intent.get("intent") == "unclear":
                print(f"  Response (clarification): {response[:100]}...")
                assert "?" in response, "Should ask clarifying question"
            print("  ✓ PASSED")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")

def test_logging():
    """Test that logging works correctly."""
    print("\n" + "="*70)
    print("TEST 4: Logging to route_log.jsonl")
    print("="*70)
    
    try:
        # Process a test message
        test_msg = "Test logging message"
        response = process_message(test_msg)
        
        # Try to read the log file
        try:
            with open("route_log.jsonl", "r") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    print("\nLog entry structure:")
                    print(f"  Keys present: {list(last_entry.keys())}")
                    
                    required_keys = ["intent", "confidence", "user_message", "final_response"]
                    for key in required_keys:
                        assert key in last_entry, f"Missing '{key}' in log"
                        print(f"  ✓ {key} present")
                    
                    print(f"  Total log entries: {len(lines)}")
                    print("  ✓ PASSED")
                else:
                    print("  ✗ FAILED: Log file is empty")
        except FileNotFoundError:
            print("  ✗ FAILED: route_log.jsonl not found")
    except Exception as e:
        print(f"  ✗ FAILED: {str(e)}")

def test_all_messages():
    """Run a quick test on all 15 messages."""
    print("\n" + "="*70)
    print("TEST 5: Processing All 15 Test Messages")
    print("="*70)
    
    successful = 0
    for i, msg in enumerate(TEST_MESSAGES, 1):
        try:
            intent = classify_intent(msg)
            response = route_and_respond(msg, intent)
            successful += 1
            status = "✓"
        except Exception as e:
            status = "✗"
        
        intent_str = intent.get("intent", "error") if isinstance(intent, dict) else "error"
        print(f"{i:2d}. {status} [{intent_str:8s}] {msg[:55]:<55s}")
    
    print(f"\nSummary: {successful}/{len(TEST_MESSAGES)} messages processed successfully")

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# LLM PROMPT ROUTER TEST SUITE")
    print("#"*70)
    
    test_classify_intent()
    test_route_and_respond()
    test_error_handling()
    test_logging()
    test_all_messages()
    
    print("\n" + "#"*70)
    print("# TEST SUITE COMPLETE")
    print("#"*70)
