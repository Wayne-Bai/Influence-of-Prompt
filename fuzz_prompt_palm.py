import google.generativeai as palm
import os

def call_palm():
    palm.configure(api_key='') # add your key here
    return palm

def palm_chat(palm, msg, role=None):
    if role and role[0]['role'] == 'system':

        if len(msg) == 2:
            role[-1]['content'] = role[-1]['content'].format(msg[0], msg[1])
        else:
            role[-1]['content'] = role[-1]['content'].format(msg[0])
        messages = role[-1]['content']
        sys_messages = role[0]['content']
        print(messages)
        print(sys_messages)

        response = palm.chat(context=sys_messages, messages=messages)
        # examples = [(role['user'], role['assistant'])]
        # response = palm.chat(context=role['system'],examples=examples, messages=msg)
    else:
        if len(msg) == 2:
            role[-1]['content'] = role[-1]['content'].format(msg[0], msg[1])
        else:
            role[-1]['content'] = role[-1]['content'].format(msg[0])
        messages = role[-1]['content']
        print(messages)
        response = palm.chat(messages=messages)
    return response

def palm_reply(response, msg):
    response = response.reply(msg)
    return response

# palm_model = call_palm()
# message = 'Hello, how are you?'
# response = palm_chat(palm_model, message)
# print(response.last)