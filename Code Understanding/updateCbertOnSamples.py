import csv
from pymongo import MongoClient
from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
depSampleDB = db.checkedDepSample
#masterDB = db.javaDBCodeT5p


for sample in depSampleDB.find():

    methodLevelComment = sample.get('methodLevelComment')
    helpCom_Summary = sample.get('helpCom_Summary')
    summaryASAP = sample.get('summaryASAP')
    codeT5p_Summary = sample.get('codeT5p_Summary')
    codeBert_Summary = sample.get('codeBert_Summary')

    bleuCodeBert = nltk_bleu(codeBert_Summary, methodLevelComment)
    meteorCodeBert = meteor_score(methodLevelComment, codeBert_Summary)
    rougeCodeBert = rouge_l(methodLevelComment, codeBert_Summary)

    bleuASAP = nltk_bleu(summaryASAP, methodLevelComment)
    meteorASAP = meteor_score(methodLevelComment, summaryASAP)
    rougeASAP = rouge_l(methodLevelComment, summaryASAP)

    bleuCodeT5p = nltk_bleu(codeT5p_Summary, methodLevelComment)
    meteorCodeT5p = meteor_score(methodLevelComment, codeT5p_Summary)
    rougeCodeT5p = rouge_l(methodLevelComment, codeT5p_Summary)

    bleuHelpCom = nltk_bleu(helpCom_Summary, methodLevelComment)
    meteorHelpCom = meteor_score(methodLevelComment, helpCom_Summary)
    rougeHelpCom = rouge_l(methodLevelComment, helpCom_Summary)


    depSampleDB.update_one(
        {'_id': sample.get('_id')},
        {
            "$set": {
                f"bleuCodeBert": bleuCodeBert,
                f"meteorCodeBert": meteorCodeBert,
                f"rougeCodeBert": rougeCodeBert,

                f"bleuASAP": bleuASAP,
                f"meteorASAP": meteorASAP,
                f"rougeASAP": rougeASAP,

                f"bleuCodeT5p": bleuCodeT5p,
                f"meteorCodeT5p": meteorCodeT5p,
                f"rougeCodeT5p": rougeCodeT5p,

                f"bleuHelpCom": bleuHelpCom,
                f"meteorHelpCom": meteorHelpCom,
                f"rougeHelpCom": rougeHelpCom,

            }
        }
    )   
    print("Updated dep sample db: ", sample.get('_id'))




print("Done Update")      
