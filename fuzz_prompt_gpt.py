import os
import openai

openai.api_key = "" # add your API key here
openai.Model.list()

def call_gpt_3_5(msg, role=None):
    if role:
        if len(msg) == 2:
            role_cp = role.copy()
            # print(role_cp)
            role_cp[-1]['content'] = role_cp[-1]['content'].format(msg[0], msg[1])
        else:
            role_cp = role.copy()
            #print(role_cp)
            role_cp[-1]['content'] = role_cp[-1]['content'].format(msg[0])
        messages = role_cp
    else:
        messages = [
        {"role": "system", "content": "You are a helpful assistant."}]
    
        temp = {
            "role": "user",
            "content": msg
        }
        messages.append(temp)

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
    return response['choices'][0]['message']['content']


def call_gpt_4(msg, role=None):
    if role:
        if len(msg) == 2:
            role_cp = role.copy()
            # print(role_cp)
            role_cp[-1]['content'] = role_cp[-1]['content'].format(msg[0], msg[1])
        else:
            role_cp = role.copy()
            #print(role_cp)
            role_cp[-1]['content'] = role_cp[-1]['content'].format(msg[0])
        messages = role_cp
        # print(messages)
    else:
        messages = [
        {"role": "system", "content": "You are a helpful assistant."}]
    
        temp = {
            "role": "user",
            "content": msg
        }
        messages.append(temp)

    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0
        )
    return response['choices'][0]['message']['content']
