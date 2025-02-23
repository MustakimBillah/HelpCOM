from pymongo import MongoClient
from bson.objectid import ObjectId
import openai
from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu
from time import sleep
import csv

openai.api_key = ""

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding    
       
sampleDB = db.checkedDepSample



def generateSummary(method, helpers):
    instruction =("""Write down only the summary part of the Javadoc comment that would have been written by a developer for the following function,\n\n""")
    prompt = instruction + "\"" + method + "\"\n\n"
    prompt+= "Where the implementations of the helper functions are as follows:\n"
    
    for helper in helpers:
        prompt+='-------------------------------------------------------------------------------\n'
        prompt+= helper+"\n"
        prompt+='-------------------------------------------------------------------------------\n'
    
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are an expert Java developer."},
            {"role": "user", "content": prompt}
            ]
            )
    summary = completion.choices[0].message["content"]

    return summary


results = []

for item in sampleDB.find():
    #print(item)
    helpers = item.get('helpers').get('helpers')
    method = item.get('Syntax')
    helperMethods = set()
    for helper in helpers:
        helperBody = helper.get('MethodBody') 
        if(len(helperBody)==0):
            continue
        helperMethods.add(helperBody)
    try:
        HelpComSummary = generateSummary(method, helperMethods)
        #print(HelpComSummary)
        data = {
            '_id': item.get('_id'),
            'HelpComSummary': HelpComSummary
        }
        results.append(data)
        print(data)
    except Exception as e:
        print("Error generating summary: ",e)
        sleep(2)

    sleep(1)

with open('filename.csv', mode='w', newline='') as file:
    # Get the headers from the dictionary keys
    fieldnames = results[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write headers
    writer.writerows(results)  # Write each dictionary as a r 
# Tests the internal HTTP request handling by verifying that the actual HTTP requests generated match the expected requests for various HTTP methods.

for item in results:
    sample = sampleDB.find_one({'_id':ObjectId(item.get('_id'))})
    methodLevelComment = sample.get('methodLevelComment')
    
    bleu = nltk_bleu(item.get('HelpComSummary'), methodLevelComment)
    meteor = meteor_score(methodLevelComment, item.get('HelpComSummary'))
    rouge = rouge_l(methodLevelComment, item.get('HelpComSummary'))

    sampleDB.update_one(
        {'_id': item.get('_id')},
        {
            "$set": {
                f"bleuHelpCOM": bleu,
                f"meteorHelpCOM": meteor,
                f"rougeHelpCOM": rouge,
                f"HelpComSummary": item.get('HelpComSummary')
            }
        }
    )  
    print("updated sample: ",item.get('_id')) 