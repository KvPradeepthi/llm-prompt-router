import json
import os
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompts for different personas
SYSTEM_PROMPTS = {
    "code": """You are an expert programmer who provides production-quality code. Your responses must contain only code blocks and brief, technical explanations. Always include robust error handling and adhere to idiomatic style for the requested language. Do not engage in conversational chatter.""",
    
    "data": """You are a data analyst who interprets data patterns. Assume the user is providing data or describing a dataset. Frame your answers in terms of statistical concepts like distributions, correlations, and anomalies. Whenever possible, suggest appropriate visualizations (e.g., 'a bar chart would be effective here').""",
    
    "writing": """You are a writing coach who helps users improve their text. Your goal is to provide feedback on clarity, structure, and tone. You must never rewrite the text for the user. Instead, identify specific issues like passive voice, filler words, or awkward phrasing, and explain how the user can fix them.""",
    
    "career": """You are a pragmatic career advisor. Your advice must be concrete and actionable. Before providing recommendations, always ask clarifying questions about the user's long-term goals and experience level. Avoid generic platitudes and focus on specific steps the user can take.""",
}

# Classifier prompt
CLASSIFIER_PROMPT = """Your task is to classify the user's intent. Based on the user message below, choose one of the following labels: code, data, writing, career, unclear. Respond with a single JSON object containing two keys: 'intent' (the label you chose) and 'confidence' (a float from 0.0 to 1.0, representing your certainty). Do not provide any other text or explanation."""

def classify_intent(message: str) -> dict:
    """Classify user message intent using LLM."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        intent_data = json.loads(response_text)
        
        # Validate structure
        if "intent" in intent_data and "confidence" in intent_data:
            return {
                "intent": intent_data["intent"],
                "confidence": float(intent_data["confidence"])
            }
        else:
            return {"intent": "unclear", "confidence": 0.0}
            
    except (json.JSONDecodeError, ValueError, KeyError):
        # Handle malformed JSON or parsing errors
        return {"intent": "unclear", "confidence": 0.0}
    except Exception as e:
        print(f"Error in classify_intent: {e}")
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, intent: dict) -> str:
    """Route message to appropriate persona and generate response."""
    intent_label = intent.get("intent", "unclear")
    
    # Handle unclear intent
    if intent_label == "unclear":
        return "I'm not sure how to help with that. Are you asking for help with coding, data analysis, writing, or career advice?"
    
    # Get system prompt for the intent
    system_prompt = SYSTEM_PROMPTS.get(intent_label, SYSTEM_PROMPTS["unclear"] if "unclear" in SYSTEM_PROMPTS else "I'm not sure how to help with that.")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in route_and_respond: {e}")
        return f"Error generating response: {str(e)}"

def log_request(user_message: str, intent: dict, final_response: str) -> None:
    """Log routing decision and response to route_log.jsonl."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "intent": intent.get("intent", "unclear"),
        "confidence": intent.get("confidence", 0.0),
        "final_response": final_response
    }
    
    try:
        with open("route_log.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Error logging request: {e}")

def process_message(message: str) -> str:
    """Main function to process user message through the router."""
    # Step 1: Classify intent
    intent = classify_intent(message)
    
    # Step 2: Route and respond
    response = route_and_respond(message, intent)
    
    # Step 3: Log the request
    log_request(message, intent, response)
    
    return response

if __name__ == "__main__":
    # Test with sample messages
    test_messages = [
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
    
    for msg in test_messages:
        print(f"\n{'='*60}")
        print(f"User: {msg}")
        print(f"{'='*60}")
        response = process_message(msg)
        print(f"Response: {response}")
