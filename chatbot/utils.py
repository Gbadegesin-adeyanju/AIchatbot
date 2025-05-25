import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="hi you are an climate change expert expert. your task to engage in conversations about climate chamge and environment in simple and understandable way by analysing and makimg use of examples. Ask question to better understand the user point of view and question. Do not answer questions that do not relate to climate change.",
)

chat_session = genai.ChatSession(
    model=model,
    history=[],  # Start with an empty history
)

def ask_gemini(message):
    # Add the user message to the history
    chat_session.history.append({"role": "user", "parts": [message]})
    
    # Send the message to the model and get a response
    response = chat_session.send_message(message)
    print(response)

    # extract the text
    response_text = response.text
    
    
    chat_session.history.append({"role": "model", "parts": response_text})    
    
    return f'{response_text}'