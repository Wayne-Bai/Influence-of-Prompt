import os

def process_inquiry(inquiry):
    components = inquiry.split('||')
    standard = components[0].strip()
    response = components[1].strip()
    return standard, response


def count_vulnerabilities(file_path, type):
    
    if type=="DD":
    
        nan_count_0 = 0
        vul_count_0 = 0
        nan_count_1 = 0
        vul_count_1 = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            current_inquiry = ""

            for i, line in enumerate(lines):
                if '||' in line:
                    # If '||' is found, process the current inquiry
                    if current_inquiry:
                        standard, response = process_inquiry(current_inquiry)

                        if standard == '0':
                            if 'it is difficult to' not in response:
                                if 'NAN' in response or 'any obvious vulnerabilities' in response:
                                    nan_count_0 += 1
                                elif 'VUL' in response:
                                    vul_count_0 += 1
                        elif standard == '1':
                            if 'it is difficult to' not in response:
                                if 'NAN' in response or 'any obvious vulnerabilities' in response:
                                    nan_count_1 += 1
                                elif 'VUL' in response:
                                    vul_count_1 += 1

                        current_inquiry = ""

                # Append the current line to the current inquiry
                current_inquiry += line
        
        print("Standard 1 - NAN Count:", nan_count_1)
        print("Standard 1 - VUL Count:", vul_count_1)
        print("Standard 0 - NAN Count:", nan_count_0)
        print("Standard 0 - VUL Count:", vul_count_0)


    if type=="SPD":
    
        srp_count_s = 0
        nsp_count_s = 0
        srp_count_ns = 0
        nsp_count_ns = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            current_inquiry = ""

            for i, line in enumerate(lines):
                if '||' in line:
                    # If '||' is found, process the current inquiry
                    if current_inquiry:
                        standard, response = process_inquiry(current_inquiry)

                        if standard == 'security':
                            if 'it is difficult to' not in response:
                                if 'SRP' in response:
                                    srp_count_s += 1
                                elif 'NSP' in response:
                                    nsp_count_s += 1
                        elif standard == 'non-security':
                            if 'it is difficult to' not in response:
                                if 'SRP' in response:
                                    srp_count_ns += 1
                                elif 'NSP' in response:
                                    nsp_count_ns += 1

                        current_inquiry = ""

                # Append the current line to the current inquiry
                current_inquiry += line

        print("Security - SRP Count:", srp_count_s)
        print("Security - NSP Count:", nsp_count_s)
        print("non-security - SRP Count:", srp_count_ns)
        print("non-security - NSP Count:", nsp_count_ns)


    if type=="SPC":
    
        ack_count_t = 0
        nak_count_t = 0
        ack_count_f = 0
        nak_count_f = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            current_inquiry = ""

            for i, line in enumerate(lines):
                if '||' in line:
                    # If '||' is found, process the current inquiry
                    if current_inquiry:
                        standard, response = process_inquiry(current_inquiry)

                        if standard == 'true':
                            if 'it is difficult to' not in response:
                                if 'ACK' in response:
                                    ack_count_t += 1
                                elif 'NAK' in response:
                                    nak_count_t += 1
                        elif standard == 'false':
                            if 'it is difficult to' not in response:
                                if 'ACK' in response:
                                    ack_count_f += 1
                                elif 'NAK' in response:
                                    nak_count_f += 1

                        current_inquiry = ""

                # Append the current line to the current inquiry
                current_inquiry += line

        print("true - ACK Count:", ack_count_t)
        print("true - NAK Count:", nak_count_t)
        print("false - ACK Count:", ack_count_f)
        print("false - NAK Count:", nak_count_f)

# run all file of a type
def runfolder(folder_path, type):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") and filename.startswith(f"{type}_"):
            print(filename)
            file_path = os.path.join(folder_path, filename)
            count_vulnerabilities(file_path, type)

folder_path="result/result_prompt_basic_actlike"
#file_name="SPC_result-GPT-3.5-few-shot.txt"
type="SPD"

#count_vulnerabilities(folder_path+"/"+file_name, type)
runfolder(folder_path, type)