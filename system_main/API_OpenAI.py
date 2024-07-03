import os
import openai
import tiktoken

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
Engine_Model="gpt-3.5-turbo"
Max_Token =     100

last_system_message = None
def OpenAI_API(contextx,system_message=None):
    global last_system_message
    messages=[]
    enc = tiktoken.encoding_for_model(Engine_Model)

    messages.append({"role":"system","content":system_message})


    # Join the content into one sentence to avoid redundancy
    combined_content = "".join(contextx)
    messages.append({"role": "user", "content": combined_content})

    print("Messages to be sent to the API:")
    print(f"{messages}")

    for message in messages:
        if message['role'] == "system":
            print(f"Role: {message['role']}, Content: {message['content']}")

    # Calculate and print the tokens for system and user messages
    system_tokens = sum(len(enc.encode(message["content"])) for message in messages if message["role"] == "system")
    user_tokens = sum(len(enc.encode(message["content"])) for message in messages if message["role"] == "user")
    total_input_tokens = system_tokens + user_tokens

    completion = openai.chat.completions.create(
        model=Engine_Model,
        max_tokens=Max_Token,
        messages = messages
    )

    respawn_message= completion.choices[0].message.content
    respawn_tokens = enc.encode(respawn_message)

    print(f"System Tokens: {system_tokens}")
    print(f"User Tokens: {user_tokens}")
    print(f"Total Input Tokens: {total_input_tokens}")
    print(f"\n{respawn_message}")
    print(f"respawn_tokens={len(respawn_tokens)}\n")

    #for token in respawn_tokens:
    #    token_text = enc.decode([token])
    #    print(f"Token: {token}, Text: '{token_text}'")

    return(respawn_message)
