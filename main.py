from fuzz_prompt_gpt import *
from fuzz_prompt_llama import *
from fuzz_prompt_palm import *
import pickle
import json
import copy

def load_SPD_data():
    f1 = open('dataset/Security-Patch-Detection/SPD-small.json', encoding='utf-8')
    SPD_small = json.load(f1)
    return SPD_small

def load_DD_data():
    f = open('dataset/Defect-Detection/DD-small.json', encoding='utf-8')
    DD_data = json.load(f)
    return DD_data

def load_SPC_data():
    f1 = open('dataset/Stable-Patch-Classification/SPC-small.json', encoding='utf-8')
    SPC_small = json.load(f1)
    return SPC_small

def test_prompt(dataset=None, model=None, prompt_type='basic'):
    if dataset == 'SPD':

        f = open('prompts/SPD-prompt-basic-gpt.json', 'r')
        total_prompt = json.load(f)
        prompt_basic = total_prompt['base']
        prompt_one = total_prompt['one-shot']
        prompt_one_f = total_prompt['one-shot-f']
        prompt_few = total_prompt['few-shot']
        prompt_few_tf = total_prompt['few-shot-tf']
        prompt_few_ft = total_prompt['few-shot-ft']
        prompt_few_ff = total_prompt['few-shot-ff']
        prompt_prompt = total_prompt['prompt-eng']
        prompt_info_manual = total_prompt['info-manual']
        prompt_info_gpt = total_prompt['info-gpt']

        if prompt_type == 'basic':
            prompt = prompt_basic
        elif prompt_type == 'one-shot':
            prompt = prompt_one
        elif prompt_type == 'one-shot-f':
            prompt = prompt_one_f
        elif prompt_type == 'few-shot-tf':
            prompt = prompt_few_tf
        elif prompt_type == 'few-shot-ft':
            prompt = prompt_few_ft
        elif prompt_type == 'few-shot-ff':
            prompt = prompt_few_ff
        elif prompt_type == 'few-shot':
            prompt = prompt_few
        elif prompt_type == 'prompt-eng':
            prompt = prompt_prompt
        elif prompt_type == 'info-manual':
            prompt = prompt_info_manual
        elif prompt_type == 'info-gpt':
            prompt = prompt_info_gpt
        else:
            print("Please provide the correct prompt type!")
            exit()

        SPD_total = load_SPD_data()
        w = open('SPD_result-{}-gpt-{}.txt'.format(model, prompt_type), 'w', encoding='utf-8')

        counter=0
        len_total=len(SPD_total)

        for i in SPD_total:    
            counter+=1
            print("processing:", counter,"/",len_total)

            CVE_ID = i['CVE_ID']
            CWE_ID = i['CWE_ID']
            commit_id = i['commit_id']
            commit_msg = i['commit_message']
            diff_code = i['diff_code']
            patch_label = i['category']
            owner = i['owner']
            repo = i['repo']
            source = i['source']

            #try:
            if model == 'GPT-4':
                message = [commit_msg, diff_code]

                pmp = copy.deepcopy(prompt)
                # print(pmp)
                reponse = call_gpt_4(message, pmp)
                # print(prompt)
                # print(pmp)
                # print(message)

                w.write('{} || {}'.format(patch_label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'GPT-3.5':
                message = [commit_msg, diff_code]
                pmp = copy.deepcopy(prompt)
                reponse = call_gpt_3_5(message, pmp)
                w.write('{} || {}'.format(patch_label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'llama':
                message = [commit_msg, diff_code]
                pmp = copy.deepcopy(prompt)
                response = call_llama(message, pmp)
                w.write('{} || {}'.format(patch_label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'palm':
                palm = call_palm()
                message = [commit_msg, diff_code]
                pmp = copy.deepcopy(prompt)
                response = palm_chat(palm, message, pmp)
                # response = palm_reply(response, clean_message)
                w.write('{} || {}'.format(patch_label, reponse.last))
                w.write('\n')
                print(reponse.last)
            else:
                print("Please provide the correct model!")
                exit()
            #except:
            #    print("This sample exceeds the token limitation of the LLM!")
            #    exit()
            # exit()
        

    elif dataset == 'DD':
        f = open('prompts/DD-prompt-basic-gpt.json', 'r')
        total_prompt = json.load(f)
        prompt_basic = total_prompt['base']
        prompt_one = total_prompt['one-shot']
        prompt_one_f = total_prompt['one-shot-f']
        prompt_few = total_prompt['few-shot']
        prompt_few_tf = total_prompt['few-shot-tf']
        prompt_few_ft = total_prompt['few-shot-ft']
        prompt_few_ff = total_prompt['few-shot-ff']
        prompt_prompt = total_prompt['prompt-eng']
        prompt_info_manual = total_prompt['info-manual']
        prompt_info_gpt = total_prompt['info-gpt']

        if prompt_type == 'basic':
            prompt = prompt_basic
        elif prompt_type == 'one-shot':
            prompt = prompt_one
        elif prompt_type == 'one-shot-f':
            prompt = prompt_one_f
        elif prompt_type == 'few-shot-tf':
            prompt = prompt_few_tf
        elif prompt_type == 'few-shot-ft':
            prompt = prompt_few_ft
        elif prompt_type == 'few-shot-ff':
            prompt = prompt_few_ff
        elif prompt_type == 'few-shot':
            prompt = prompt_few
        elif prompt_type == 'prompt-eng':
            prompt = prompt_prompt
        elif prompt_type == 'info-manual':
            prompt = prompt_info_manual
        elif prompt_type == 'info-gpt':
            prompt = prompt_info_gpt
        else:
            print("Please provide the correct prompt type!")
            exit()
        
        DD_data = load_DD_data()

        w = open('DD_result-{}-gpt-{}.txt'.format(model, prompt_type), 'w', encoding='utf-8')

        counter=0
        len_total=len(DD_data)
        for i in DD_data:
            counter+=1
            print("processing:", counter,"/",len_total)
            func = i['func']
            label = i['target']
        

            if model == 'GPT-4':
                message = [func]
                pmp = copy.deepcopy(prompt)
                #print(message)
                # print(prompt)
                reponse = call_gpt_4(message, pmp)

                w.write('{} || {}'.format(label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'GPT-3.5':
                message = [func]
                pmp = copy.deepcopy(prompt)
                reponse = call_gpt_3_5(message, pmp)
                w.write('{} || {}'.format(label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'llama':
                message = [func]
                pmp = copy.deepcopy(prompt)
                response = call_llama(message, pmp)
                w.write('{} || {}'.format(label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'palm':
                palm = call_palm()
                message = [func]
                pmp = copy.deepcopy(prompt)
                response = palm_chat(palm, message, pmp)
                # response = palm_reply(response, clean_message)
                w.write('{} || {}'.format(label, reponse.last))
                w.write('\n')
                print(response.last)
            else:
                print("Please provide the correct model!")
                exit()

    
    elif dataset == 'SPC':
        f = open('prompts/SPC-prompt-basic-gpt.json', 'r')
        total_prompt = json.load(f)
        prompt_basic = total_prompt['base']
        prompt_one = total_prompt['one-shot']
        prompt_one_f = total_prompt['one-shot-f']
        prompt_few = total_prompt['few-shot']
        prompt_few_tf = total_prompt['few-shot-tf']
        prompt_few_ft = total_prompt['few-shot-ft']
        prompt_few_ff = total_prompt['few-shot-ff']
        prompt_prompt = total_prompt['prompt-eng']
        prompt_info_manual = total_prompt['info-manual']
        prompt_info_gpt = total_prompt['info-gpt']

        if prompt_type == 'basic':
            prompt = prompt_basic
        elif prompt_type == 'one-shot':
            prompt = prompt_one
        elif prompt_type == 'one-shot-f':
            prompt = prompt_one_f
        elif prompt_type == 'few-shot-tf':
            prompt = prompt_few_tf
        elif prompt_type == 'few-shot-ft':
            prompt = prompt_few_ft
        elif prompt_type == 'few-shot-ff':
            prompt = prompt_few_ff
        elif prompt_type == 'few-shot':
            prompt = prompt_few
        elif prompt_type == 'prompt-eng':
            prompt = prompt_prompt
        elif prompt_type == 'info-manual':
            prompt = prompt_info_manual
        elif prompt_type == 'info-gpt':
            prompt = prompt_info_gpt
        else:
            print("Please provide the correct prompt type!")
            exit()

        # SPC_total_data, _, _ = load_SPC_data()
        SPC_total_data = load_SPC_data()

        w = open('SPC_result-{}-gpt-{}.txt'.format(model, prompt_type), 'w', encoding='utf-8')
        
        counter=0
        len_total=len(SPC_total_data)
        for i in SPC_total_data:
            counter+=1
            print("processing:", counter,"/",len_total)
            commit_msg = i['content']['message']
            label = i['label']
            temp_code_diff = []
            for diff in i['content']['diff']:
                for k,v in diff.items():
                    temp_code_diff.append(k+'\n'+v)
            code_diff = ''
            for d in temp_code_diff:
                code_diff += d + '\n'
            # print(commit_msg)
            # print(code_diff)
            #try:
            if model == 'GPT-4':
                message = [commit_msg, code_diff]
                #print(message)
                pmp = copy.deepcopy(prompt)
                reponse = call_gpt_4(message, pmp)
                w.write('{} || {}'.format(label, reponse))
                w.write('\n')
                print(reponse)

            elif model == 'GPT-3.5':
                message = [commit_msg, code_diff]
                pmp = copy.deepcopy(prompt)
                reponse = call_gpt_3_5(message, pmp)
                w.write('{} || {}'.format(label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'llama':
                message = [commit_msg, code_diff]
                pmp = copy.deepcopy(prompt)
                response = call_llama(message, pmp)
                w.write('{} || {}'.format(label, reponse))
                w.write('\n')
                print(reponse)
            elif model == 'palm':
                palm = call_palm()
                message = [commit_msg, code_diff]
                pmp = copy.deepcopy(prompt)
                response = palm_chat(palm, message, pmp)
                # response = palm_reply(response, clean_message)
                w.write('{} || {}'.format(label, reponse.last))
                w.write('\n')
                print(reponse.last)
            else:
                print("Please provide the correct model!")
                exit()
            #except:
            #    print("This sample exceeds the token limitation of the LLM!")
            #    exit()
            #exit()


if __name__ == '__main__':

    test_prompt('SPD', 'GPT-3.5', 'few-shot-tf')


    
