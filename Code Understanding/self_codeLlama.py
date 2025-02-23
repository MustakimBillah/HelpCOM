from pymongo import MongoClient
from bson.objectid import ObjectId
from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu
from time import sleep
import csv
from ollama import Client
llama_host = 'http://10.18.208.5:11434'


client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding    
       
sampleDB = db.checkedDepSample


def generateSummary(method):
    instruction =("""Write down only the summary part of the Javadoc comment (in one sentence) that would have been written by a developer for the following function,\n\n""")
    prompt = instruction + "\"" + method + "\"\n\n"
    # prompt+= "Where the implementations of the helper functions are as follows:\n"
    
    # for helper in helpers:
    #     prompt+='-------------------------------------------------------------------------------\n'
    #     prompt+= helper+"\n"
    #     prompt+='-------------------------------------------------------------------------------\n'
    
    llama_client = Client(host=llama_host)
    response = llama_client.chat(
    model='codellama:7b-instruct',
    messages=[{ 'role': 'system', 'content': 'You are an expert Java developer.'}, 
              {'role':'user', 'content': prompt}]
              )
    
    summary = response['message']['content']

    return summary


results = []

counter=0

for item in sampleDB.find():
    #print(item)
    #helpers = item.get('helpers').get('helpers')
    method = item.get('Syntax')
    # helperMethods = set()
    # for helper in helpers:
    #     helperBody = helper.get('MethodBody') 
    #     if(len(helperBody)==0):
    #         continue
    #     helperMethods.add(helperBody)
    try:
        HelpComSummary = generateSummary(method)
        #print(HelpComSummary)
        data = {
            '_id': item.get('_id'),
            'Summary': HelpComSummary
        }
        results.append(data)
        print(HelpComSummary)
        print('-----------------------')

    except Exception as e:
        print("Error generating summary: ",e)
        sleep(2)

    sleep(1)

with open('self_codeLlama.csv', mode='w', newline='') as file:
    # Get the headers from the dictionary keys
    fieldnames = results[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write headers
    writer.writerows(results)  # Write each dictionary as a r 


