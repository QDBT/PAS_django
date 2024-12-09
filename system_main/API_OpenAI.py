import os
import openai
import tiktoken

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
Engine_Model="gpt-3.5-turbo"
Max_Token =     200

last_system_message = None
def OpenAI_API(take_from_view):
    global last_system_message
    messages=[]
    enc = tiktoken.encoding_for_model(Engine_Model)

    #messages.append({"role":"system","content":system_message})

    # Join the content into one sentence to avoid redundancy
    if take_from_view:
        if take_from_view.get('user_message'):
            for message in take_from_view.get('user_message'):
                messages.append({"role":"user", "content":message})
        if take_from_view.get('system_message'):
            for message in take_from_view.get('system_message'):
                messages.append({"role":"system", "content":message})

        print("Messages to be sent to the API:")
        print(f"{messages}")

    for message in messages:
        if message['role'] == "system":
            print(f"Role: {message['role']}, Content: {message['content']}")

    # Calculate and print the tokens for system and user messages 
    system_tokens = sum(len(enc.encode(message["content"])) for message in messages if message["role"] == "system")
    user_tokens = sum(len(enc.encode(message["content"])) for message in messages if message["role"] == "user")
    token_input = system_tokens + user_tokens

    completion = openai.chat.completions.create(
        model=Engine_Model,
        max_tokens=Max_Token,
        messages = messages
    )

    AI_answer= completion.choices[0].message.content
    token_respawn = len(enc.encode(AI_answer))

    #print(f"System Tokens: {system_tokens}")
    print(f"User Tokens: {user_tokens}")
    #print(f"Total Input Tokens: {total_input_tokens}")
    print(f"\n{AI_answer}")
    print(f"respawn_tokens={token_respawn}\n")

    #for token in respawn_tokens:
    #    token_text = enc.decode([token])
    #    print(f"Token: {token}, Text: '{token_text}'")
    return {
        "AI_answer": AI_answer,
        "token_respawn": token_respawn,
        "user_tokens": user_tokens,
        "token_input": token_input,
    }
