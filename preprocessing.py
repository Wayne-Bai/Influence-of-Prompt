import json

def generate_small_SPD():
    f1 = open('dataset/Security-Patch-Detection/security.json')
    SPD_security = json.load(f1)

    f2 = open('dataset/Security-Patch-Detection/non-security.json')
    SPD_non_security = json.load(f2)

    count1 = 0
    count2 = 0
    small_SPD = []

    for i in SPD_non_security:
        if i['category'] == 'non-security' and len(i['commit_message'].split()) + len(i['diff_code'].split()) < 500:
            small_SPD.append(i)
            count2 += 1
        if count2 == 1002:
            break

    with open('dataset/Security-Patch-Detection/SPD-small-tmp.json', 'w', encoding='utf-8') as w:
        json.dump(small_SPD, w, ensure_ascii=False, indent=4)

    print(len(small_SPD))

def generate_small_DD():
    f = open('dataset/Defect-Detection/function.json')
    DD_data = json.load(f)
    
    count1 = 0
    count2 = 0
    small_DD = []

    for i in DD_data:
        if count2 < 1002 and i['target'] == 1 and len(i['func'].split()) < 500:
            small_DD.append(i)
            count2 += 1
        if count2 == 1002:
            break

    with open('dataset/Defect-Detection/DD-small-tmp.json', 'w', encoding='utf-8') as w:
        json.dump(small_DD, w, ensure_ascii=False, indent=4)

    print(len(small_DD))

def generate_small_SPC():
    f1 = open('dataset/Stable-Patch-Classification/false.json')
    SPC_false = json.load(f1)
    f2 = open('dataset/Stable-Patch-Classification/true.json')
    SPC_true = json.load(f2)

    count1 = 0
    count2 = 0
    small_SPC = []

    for i in SPC_false:
        if i['label'] == 'false':
            temp_code_diff = []
            for diff in i['content']['diff']:
                for k,v in diff.items():
                    temp_code_diff.append(k+'\n'+v)
            code_diff = ''
            for d in temp_code_diff:
                code_diff += d + '\n'
            message = i['content']['message']
            if len(code_diff.split()) + len(message.split()) < 500:
                small_SPC.append(i)
                count1 += 1
        if count1 == 1002:
            break


    with open('dataset/Stable-Patch-Classification/SPC-small-tmp.json', 'w', encoding='utf-8') as w:
        json.dump(small_SPC, w, ensure_ascii=False, indent=4)

    print(len(small_SPC))

#generate_small_SPD()
generate_small_DD()
#generate_small_SPC()
