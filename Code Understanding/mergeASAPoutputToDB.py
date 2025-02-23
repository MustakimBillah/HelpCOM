import csv
from pymongo import MongoClient
from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
indepSampleDB = db.indepSample
depSampleDB = db.depSample

# Path to your CSV file
csv_file_path = '/student/mjr175/method-level-comment-generation/ASAP_DATASET/scripts/scripts/results.csv'

# Open and read the CSV file
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Process each row
    for row in csv_reader:
        dbID = row[0]
        methodType = row[1]
        commentASAP = row[2]  # Remove leading/trailing whitespace
        
        if(methodType=='dependent'):
            sample = depSampleDB.find_one({'_id':ObjectId(dbID)})
            methodLevelComment = sample.get('methodLevelComment')
            
            bleuASAP = nltk_bleu(commentASAP, methodLevelComment)
            meteorASAP = meteor_score(methodLevelComment, commentASAP)
            rougeASAP = rouge_l(methodLevelComment, commentASAP)

            depSampleDB.update_one(
                {'_id': sample.get('_id')},
                {
                    "$set": {
                        f"bleuASAP": bleuASAP,
                        f"meteorASAP": meteorASAP,
                        f"rougeASAP": rougeASAP,
                        f"summaryASAP": commentASAP
                    }
                }
            )   
            print("Updated dep sample db: ", dbID)
        else:
            sample = indepSampleDB.find_one({'_id':ObjectId(dbID)})
            methodLevelComment = sample.get('methodLevelComment')
            
            bleuASAP = nltk_bleu(commentASAP, methodLevelComment)
            meteorASAP = meteor_score(methodLevelComment, commentASAP)
            rougeASAP = rouge_l(methodLevelComment, commentASAP)

            indepSampleDB.update_one(
                {'_id': sample.get('_id')},
                {
                    "$set": {
                        f"bleuASAP": bleuASAP,
                        f"meteorASAP": meteorASAP,
                        f"rougeASAP": rougeASAP,
                        f"summaryASAP": commentASAP
                    }
                }
            )  
            print("Updated indep sample db: ", dbID)


print("Done Update")      
