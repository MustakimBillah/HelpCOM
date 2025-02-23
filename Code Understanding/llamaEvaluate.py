from ollama import Client
llama_host = 'http://10.18.208.5:11434'
client = Client(host=llama_host)
import csv
import re

def llama_evaluate(prompt): 
    response = client.chat(
        model='llama3.3',
        messages=[{ 'role': 'system', 'content': 'You are an expert Evaluator of JAVA Code Comments.'}, 
                  {'role':'user', 'content': prompt}]
                  )

    return response['message']['content']


#general_message = "Here is a piece of code with corresponding comments. Please rate each comment on a scale from 1 to 5, where a higher score indicates better quality. A good comment should: 1) accurately summarize the function of the code; 2) be expressed naturally and concisely, without burdening the developer with reading; 3) help the developer understand the code quickly. Your answer should be in the format 'Comment 0/1/2/3/4: {your rating}'.\n"
general_message = "Here is a piece of code with corresponding comments. Please rate each comment on a scale from 1 to 5, where a higher score indicates better quality. A good comment should: 1) accurately summarize the function of the code; 2) be expressed naturally and concisely, without burdening the developer with reading; 3) help the developer understand the code quickly. Your answer should be in the format 'Comment 1/2/3: {your rating}'.\n"

print('-----------------------------------------------------------------')
groundTruth_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryIndep.csv'
codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5SummaryIndep.csv'

dataID = []
gt=[]
codeList=[]
codeT5=[]


with open('/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeInDep.csv', mode="r") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)

    for row in csv_reader:
        codeBody = row[1]
        codeList.append(codeBody)

with open(groundTruth_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        gt.append(data)
        dataID.append(id)

with open(codeT5_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        codeT5.append(data)

referenceList=[]
predictionList_CodeT5=[]


for item in gt:
    target_id = item['id']
    referenceList.append(item['summary'])
    found = False
    for element in codeT5:
        if(target_id==element['id']):
            found=True
            predictionList_CodeT5.append(element['summary'])
            break
    if found == False:
        predictionList_CodeT5.append('')


#######CodeBert######################

codeBert_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeBertSummaryIndep.csv'
codeBert=[]

with open(codeBert_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        codeBert.append(data)

predictionList_CodeBert = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in codeBert:
        if(target_id==element['id']):
            found=True
            predictionList_CodeBert.append(element['summary'])
            break
    if found == False:
        predictionList_CodeBert.append('')

# #######ASAP_Base######################

asapBase_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/asapSummaryIndep.csv'
asapBase=[]

with open(asapBase_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        asapBase.append(data)

predictionList_ASAP = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in asapBase:
        if(target_id==element['id']):
            found=True
            predictionList_ASAP.append(element['summary'])
            break
    if found == False:
        predictionList_ASAP.append('')

# #######ASAP_4o######################

# asap4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/ASAPresults4o.csv'
# asap4o=[]

# with open(asap4o_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     #header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[2]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         asap4o.append(data)

# predictionList_ASAP_4o = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in asap4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList_ASAP_4o.append(element['summary'])
#             break
#     if found == False:
#         predictionList_ASAP_4o.append('')


# #######GPT_4o######################

# gpt4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gpt4oSummary.csv'
# gpt4o=[]

# with open(gpt4o_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         gpt4o.append(data)

# predictionList_gpt4o = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in gpt4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList_gpt4o.append(element['summary'])
#             break
#     if found == False:
#         predictionList_gpt4o.append('')


# #######helpCom_CodeLlama######################

# helpCom_codeLlama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_codeLlama.csv'
# helpCom_codeLlama=[]

# with open(helpCom_codeLlama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_codeLlama.append(data)

# predictionList_helpCom_codeLlama = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_codeLlama:
#         if(target_id==element['id']):
#             found=True
#             predictionList_helpCom_codeLlama.append(element['summary'])
#             break
#     if found == False:
#         predictionList_helpCom_codeLlama.append('')


# #######helpCom_llama######################

# helpCom_llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_llama.csv'
# helpCom_llama=[]

# with open(helpCom_llama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_llama.append(data)

# predictionList_helpCom_llama = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList_helpCom_llama.append(element['summary'])
#             break
#     if found == False:
#         predictionList_helpCom_llama.append('')


# #######helpCom_N_codellama######################

# helpCom_N_codellama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_codellama.csv'
# helpCom_N_codellama=[]

# with open(helpCom_N_codellama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_N_codellama.append(data)

# predictionList_helpCom_N_codellama = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_codellama:
#         if(target_id==element['id']):
#             found=True
#             predictionList_helpCom_N_codellama.append(element['summary'])
#             break
#     if found == False:
#         predictionList_helpCom_N_codellama.append('')


# #######helpCom_N_gpt4o######################

# helpCom_N_gpt4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_gpt4o.csv'
# helpCom_N_gpt4o = []

# with open(helpCom_N_gpt4o_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_N_gpt4o.append(data)

# predictionList_helpCom_N_gpt4o = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_gpt4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList_helpCom_N_gpt4o.append(element['summary'])
#             break
#     if found == False:
#         predictionList_helpCom_N_gpt4o.append('')


# #######helpCom_N_llama######################

# helpCom_N_llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_llama.csv'
# helpCom_N_llama = []

# with open(helpCom_N_llama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_N_llama.append(data)

# predictionList_helpCom_N_llama = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList_helpCom_N_llama.append(element['summary'])
#             break
#     if found == False:
#         predictionList_helpCom_N_llama.append('')


# #######helpCom_4o######################

# helpCom_4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpComOutput.csv'
# helpCom_4o = []

# with open(helpCom_4o_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     #header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_4o.append(data)

# predictionList_helpCom_4o = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList_helpCom_4o.append(element['summary'])
#             break
#     if found == False:
#         predictionList_helpCom_4o.append('')

# #######self_codeLlama######################

# self_codeLlama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/self_codeLlama.csv'
# self_codeLlama = []

# with open(self_codeLlama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         self_codeLlama.append(data)

# predictionList_self_codeLlama = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in self_codeLlama:
#         if(target_id==element['id']):
#             found=True
#             predictionList_self_codeLlama.append(element['summary'])
#             break
#     if found == False:
#         predictionList_self_codeLlama.append('')


# #######self_Llama######################

# self_Llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/self_Llama.csv'
# self_Llama = []

# with open(self_Llama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         self_Llama.append(data)

# predictionList_self_Llama = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in self_Llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList_self_Llama.append(element['summary'])
#             break
#     if found == False:
#         predictionList_self_Llama.append('')


print('-----------------------------------------------------------------')


resultList=[]



# Regular expression to extract comment numbers and scores
pattern = r"Comment (\d+): (\d)"

# for rowID, code, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13 in zip(dataID,codeList, predictionList_CodeT5, predictionList_CodeBert, predictionList_ASAP, predictionList_ASAP_4o, predictionList_gpt4o, predictionList_self_codeLlama, predictionList_self_Llama, predictionList_helpCom_llama, predictionList_helpCom_4o, predictionList_helpCom_codeLlama, predictionList_helpCom_N_llama, predictionList_helpCom_N_gpt4o, predictionList_helpCom_N_codellama):

#     message ="Code:\n<"+code+">\n"
#     message+="Comment 1: <"+c1+">\n"
#     message+="Comment 2: <"+c2+">\n"
#     message+="Comment 3: <"+c3+">\n"
#     message+="Comment 4: <"+c4+">\n"
#     message+="Comment 5: <"+c5+">\n"
#     message+="Comment 6: <"+c6+">\n"
#     message+="Comment 7: <"+c7+">\n"
#     message+="Comment 8: <"+c8+">\n"
#     message+="Comment 9: <"+c9+">\n"
#     message+="Comment 10: <"+c10+">\n"
#     message+="Comment 11: <"+c11+">\n"
#     message+="Comment 12: <"+c12+">\n"
#     message+="Comment 13: <"+c13+">"

#     try:
#         result=(llama_evaluate(general_message+message))
    
#         print(result)

#         resultList.append(result)
#     except:
#         print("error for: ", code)
    
#     if rowID == '67299dbda23f7e5639814e92':
#         break


for rowID, code, c1,c2,c3 in zip(dataID,codeList, predictionList_CodeT5,predictionList_CodeBert,predictionList_ASAP):

    message ="Code:\n<"+code+">\n"
    message+="Comment 1: <"+c1+">\n"
    message+="Comment 2: <"+c2+">\n"
    message+="Comment 3: <"+c3+">"

    try:
        result=(llama_evaluate(general_message+message))
    
        print(result)

        resultList.append(result)
    except:
        print("error for: ", code)