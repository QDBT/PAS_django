import os
import openai
import tiktoken

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
Engine_Model="gpt-3.5-turbo"

last_system_message = None
def OpenAI_API(contextx,system_message=None):
    global last_system_message
    messages=[]
    enc = tiktoken.encoding_for_model(Engine_Model)

    if system_message and system_message != last_system_message:
        messages.append({"role":"system","content":system_message})
        last_system_message = system_message


    messages.extend([
        {"role":"user","content":content} for content in contextx
    ])

    completion = openai.chat.completions.create(
        model=Engine_Model,
        max_tokens=20,
        messages = messages
    )
    respawn_message= completion.choices[0].message.content
    tokens = enc.encode(respawn_message)
    print(respawn_message)
    print(len(tokens))

    for token in tokens:
        token_text = enc.decode([token])
        print(f"Token: {token}, Text: '{token_text}'")

content=[
    "for i in range(1,10):\n print('i=',x)",
]
system_message="show only code"
OpenAI_API(content,system_message)