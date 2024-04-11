import json
import pickle
from github import Github
from github import RateLimitExceededException
from git import Repo, diff
import calendar
import time

# TODO: Test HuggingFace Datasets
def huggingface_login():
    from datasets import load_dataset

    # If the dataset is gated/private, make sure you have run huggingface-cli login
    dataset = load_dataset("sunlab/patch_db")
    #print(type(dataset['train']))
    #print(dataset['train'].features)
    print(len(dataset['train']))
    print(dataset['train'][0])

# TODO: Check PKL files => Stable-Patch-Classification
def preprocess_SPC():
    with open('dataset/Stable-Patch-Classification/data/train.pkl', 'rb') as f:
    # with open('dataset/Stable-Patch-Classification/data/dict.pkl', 'rb') as f:
        data = pickle.load(f)

    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0

    f1 = open('dataset/Stable-Patch-Classification/data/true.json', 'w')
    f2 = open('dataset/Stable-Patch-Classification/data/false.json', 'w')

    true_data = []
    false_data = []

    # Access Toekn: "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"
    # Access Token: "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"
    # Access Token: "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"
    
    repo1 = Github("").get_repo("torvalds/linux") # add your token here
    repo2 = Github("").get_repo("torvalds/linux") # add your token here
    repo3 = Github("").get_repo("torvalds/linux") # add your token here
    
    for i in data:
        if data.index(i) <= 4900 or (data.index(i) > 14701 and data.index(i) <= 19600) or (data.index(i) > 29401 and data.index(i) <= 34300):
            temp = {
                'id': '',
                'label': '',
                'content': {} 
            }
            if i['stable'] == 'false':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo1, i['id'])
                false_data.append(temp)
                flag1 += 1
            elif i['stable'] == 'true':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo1,i['id'])
                true_data.append(temp)
                flag2 += 1
            else:
                flag3 += 1
            flag4 += 1
            print(f'Current Process:{flag4}/{len(data)}')

        elif (data.index(i) > 4900 and data.index(i) <= 9800) or (data.index(i) > 19600 and data.index(i) <= 24500) or (data.index(i) > 34300 and data.index(i) <= 39200):
            temp = {
                'id': '',
                'label': '',
                'content': {} 
            }
            if i['stable'] == 'false':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo2, i['id'])
                false_data.append(temp)
                flag1 += 1
            elif i['stable'] == 'true':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo2,i['id'])
                true_data.append(temp)
                flag2 += 1
            else:
                flag3 += 1
            flag4 += 1
            print(f'Current Process:{flag4}/{len(data)}')

        elif (data.index(i) > 9800 and data.index(i) <= 14700) or (data.index(i) > 24500 and data.index(i) <= 29400) or (data.index(i) > 39200 and data.index(i) <= 44100):
            temp = {
                'id': '',
                'label': '',
                'content': {} 
            }
            if i['stable'] == 'false':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo3, i['id'])
                false_data.append(temp)
                flag1 += 1
            elif i['stable'] == 'true':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo3,i['id'])
                true_data.append(temp)
                flag2 += 1
            else:
                flag3 += 1
            flag4 += 1
            print(f'Current Process:{flag4}/{len(data)}')
        
        elif data.index(i) == 14701 or data.index(i) == 29401 or data.index(i) == 44101:
            search_rate_limit = Github().get_rate_limit().search
            print('search remaining: {}. For now, we are waiting for 40min to reset the limitation'.format(search_rate_limit.remaining))
            time.sleep(2401)
            temp = {
                'id': '',
                'label': '',
                'content': {} 
            }
            if i['stable'] == 'false':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo1, i['id'])
                false_data.append(temp)
                flag1 += 1
            elif i['stable'] == 'true':
                temp['id'] = i['id']
                temp['label'] = i['stable']
                temp['content'] = crawl_github(repo1,i['id'])
                true_data.append(temp)
                flag2 += 1
            else:
                flag3 += 1
            flag4 += 1
            print(f'Current Process:{flag4}/{len(data)}')
        # # check point
        # if i == data[5]:
        #     print(temp)
        #     print(true_data)
        #     print(false_data)
        #     exit()
    json.dump(true_data, f1)
    json.dump(false_data, f2)

    print(f'false: {flag1}')
    print(f'true: {flag2}')
    print(f'none: {flag3}')
    print(f'total: {flag4}')
    print(f'true data: {len(true_data)}')
    print(f'false data: {len(false_data)}')

# ISSUE: RateLimitExceededException
def crawl_github(repo, id):

    while True:
        try: 
            content = {
                'message': "",
                'diff': []

            }
            
            commit = repo.get_commit(id)
            msg = commit.commit.message
            content['message'] = msg

            diff = commit.files
            
            for file in diff:
                filechange = {}
                filechange[file.filename] = file.patch
                content['diff'].append(filechange)

            return content
        except StopIteration:
                    break  # loop end
        except RateLimitExceededException:
            search_rate_limit = Github().get_rate_limit().search
            print('search remaining: {}. For now, we are waiting for one hour to reset the limitation'.format(search_rate_limit.remaining))
            reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
            # add 10 seconds to be sure the rate limit has been reset
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 3601
            time.sleep(sleep_time)
            continue

def preprocess_DD():
    
    f = open('dataset/Defect-Detection/function.json')
    data = json.load(f)

    flag1 = 0
    flag2 = 0

    for i in data:
        if i['target'] == 0:
            flag1 += 1
        elif i['target'] == 1:
            flag2 += 1
    print(f'0: {flag1}')
    print(f'1: {flag2}')
    print(f'total: {len(data)}')

# TODO: Check JSON files => Security-Patch-Detection
def preprocess_SPD():
    
    f = open('dataset/Security-Patch-Detection/patch_db.json')
    data = json.load(f)

    f1 = open('dataset/Security-Patch-Detection/security.json', 'w')
    f2 = open('dataset/Security-Patch-Detection/non-security.json', 'w')

    category = []
    flag1 = 0
    flag2 = 0

    security = []
    non_security = []

    for i in data:
        if i['category'] not in category:
            category.append(i['category'])
        if i['category'] == 'non-security':
            non_security.append(i)
            flag1 += 1
        elif i['category'] == 'security':
            security.append(i)
            flag2 += 1

    json.dump(security, f1)
    json.dump(non_security, f2)

    print(f'non-security: {flag1}')
    print(f'security: {flag2}')
    print(category)
    print(f'total: {len(data)}')

    flag1 = 0
    flag2 = 0

if __name__ == '__main__':
    # huggingface_login()
    preprocess_SPC()
    # crawl_github()
    # preprocess_DD()
    # preprocess_SPD()