import replicate
import os

def call_llama(msg, role=None):
    os.environ['REPLICATE_API_TOKEN'] = ''  # add your API key here

    if role and role[0]['role'] == 'system':

        if len(msg) == 2:
            role[-1]['content'] = role[-1]['content'].format(msg[0], msg[1])
        else:
            role[-1]['content'] = role[-1]['content'].format(msg[0])
        messages = role[-1]['content']
        sys_messages = role[0]['content']
        # print(messages)
        # print(sys_messages)

        output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": messages,
            "system_prompt": sys_messages
        }
        )

        output = ''.join(output)
        return output
    else:
        if len(msg) == 2:
            role[-1]['content'] = role[-1]['content'].format(msg[0], msg[1])
        else:
            role[-1]['content'] = role[-1]['content'].format(msg[0])
        messages = role[-1]['content']
        # print(messages)
        output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": messages
        }
        )

        output = ''.join(output)
        return output


