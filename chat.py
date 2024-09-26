import chainlit as cl
from typing import List
from ctransformers import AutoModelForCausalLM

def get_prompt(instruction: str, history: List[str] = None) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the questions in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n"
    if history and len(history) > 0:
        prompt += f"This is the conversation history: {''.join(history)}. Now answer the question: "
    prompt += f"{instruction}\n\n### Response:\n"
    return prompt

@cl.on_message
async def on_message(message: cl.Message):
    # Retrieve message history from the user session
    message_history = cl.user_session.get("message_history")
    msg = cl.Message(content="")
    await msg.send()

    # Build the prompt using the helper function
    prompt = get_prompt(message.content, message_history)
    response = ""

    # Stream and build the response from the model
    for word in llm(prompt, stream=True):
        response += word
        await msg.stream_token(word)
    
    # Update the final message in the chat
    await msg.update()
    
    # Append the message and model response to history
    message_history.append(f"User: {message.content}")
    message_history.append(f"AI: {response}")

@cl.on_chat_start
def on_chat_start():
    # Initialize the message history as an empty list
    cl.user_session.set("message_history", [])
    
    # Load the pre-trained model globally
    global llm
    llm = AutoModelForCausalLM.from_pretrained(
        "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
    )
"""
def get_prompt(instruction: str, history: List[str] = None) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the questions in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n"
    if len(history) > 0:
        prompt += f"This is the conversation history: {''.join(history)}. Now answer the question: "
    prompt = f"{instruction}\n\n### Response:\n"
    return prompt

@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    msg = cl.Message(content="")
    await msg.send()
   
    prompt = get_prompt(message.content, message_history)
    response = ""
    for word in llm(prompt, stream=True):
        await msg.stream_token(word)
    await msg.update()
    message_history.append(response)

@cl.on_chat_start
def on_chat_start():
    cl.user_session.set("message_history", [])
    global llm
    llm = AutoModelForCausalLM.from_pretrained(
        "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
        )
    """