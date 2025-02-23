import csv
from pymongo import MongoClient
from bson.objectid import ObjectId
from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding    
#test_id = '67299dbda23f7e5639814e1c' 
#test_id = '67299dbda23f7e5639814e1d'        
sampleDB = db.depSample
totalBleu = 0
# Replace 'your_file.csv' with the path to your CSV file
with open('/student/mjr175/method-level-comment-generation/Code Understanding/prompt2.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Process each row
    for row in csv_reader:
        id = row[0]
        summary =row[1]
        sample = sampleDB.find_one({'_id':ObjectId(id)})
        methodLevelComment = sample.get('methodLevelComment')
        
        bleu = nltk_bleu(summary, methodLevelComment)
        meteor = meteor_score(methodLevelComment, summary)
        rouge = rouge_l(methodLevelComment, summary)
        totalBleu+=bleu
        # sampleDB.update_one(
        #     {'_id': sample.get('_id')},
        #     {
        #         "$set": {
        #             f"bleuHelpCom": bleu,
        #             f"meteorHelpCom": meteor,
        #             f"rougeHelpCom": rouge,
        #             f"helpCom_Summary": summary
        #         }
        #     }
        # )  
        print("updated sample: ",sample.get('_id')) 

print(totalBleu/380)