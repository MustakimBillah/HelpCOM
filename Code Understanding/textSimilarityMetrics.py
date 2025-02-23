from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu
import csv

def calculateScores(refList,predList):
    totalBleu = 0
    totalRouge = 0
    totalMeteor = 0

    for ref,pred in zip(refList,predList):
        totalBleu+=nltk_bleu(pred, ref)
        totalRouge+=rouge_l(ref, pred)
        totalMeteor+=meteor_score(ref, pred)

    return round(totalBleu/len(refList),4), round(totalRouge/len(refList),4), round(totalMeteor/len(refList),4)


# start calculating for 380 dependent methods
print("Text similarity scores")
print('-----------------------------------------------------------------')
groundTruth_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryPHP.csv'
#codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5Summary.csv'

gt=[]

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



#######helpCom_N_gpt4o######################

helpCom_N_gpt4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_gpt4o_PHP.csv'
helpCom_N_gpt4o = []
referenceList=[]
predictionList=[]

with open(helpCom_N_gpt4o_filePath, mode="r") as file:
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
        helpCom_N_gpt4o.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    referenceList.append(item['summary'])
    found = False
    for element in helpCom_N_gpt4o:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

bleu,rouge,meteor = calculateScores(referenceList, predictionList)
print('helpCom_N_level_gpt4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)




# codeT5=[]





# with open(codeT5_filePath, mode="r") as file:
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
#         codeT5.append(data)




# for item in gt:
#     target_id = item['id']
#     referenceList.append(item['summary'])
#     found = False
#     for element in codeT5:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# #print(referenceList)
# #print(predictionList)

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('CodeT5 bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)



# #######CodeBert######################

# codeBert_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeBertSummary.csv'
# codeBert=[]

# with open(codeBert_filePath, mode="r") as file:
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
#         codeBert.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in codeBert:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('CodeBert bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


# #######ASAP_Base######################

# asapBase_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/ASAPresultsBase.csv'
# asapBase=[]

# with open(asapBase_filePath, mode="r") as file:
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
#         asapBase.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in asapBase:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('ASAP_Base bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)




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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in asap4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('ASAP_4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in gpt4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('GPT_4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_codeLlama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('helpCom_codeLlama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('helpCom_llama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_codellama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('helpCom_N_level_codellama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_gpt4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('helpCom_N_level_gpt4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('helpCom_N_level_llama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('helpCom_4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)

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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in self_codeLlama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('self_codeLlama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in self_Llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# bleu,rouge,meteor = calculateScores(referenceList, predictionList)
# print('self_Llama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)

# print('-----------------------------------------------------------------')


