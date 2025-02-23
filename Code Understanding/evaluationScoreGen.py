from pymongo import MongoClient
from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu


client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p

totalMethodsWithDocstring = 0

totalBleu=0
totalMeteor=0
totalRouge=0

for item in javaDBFinal.find():
    methods = item.get('methods')
    for index, method in enumerate(methods):
        docstring = method.get('Docstring')
        wordCount = len(docstring.split())
        if(wordCount > 0):
            totalMethodsWithDocstring+=1
            methodLevelComment = method.get('methodLevelComment')
            #codeT5p_Summary = method.get('codeT5p_Summary')
            codeBert_Summary = method.get('cBert_Summary')
            try:
                #bleuCodeT5p = nltk_bleu(codeT5p_Summary, methodLevelComment)
                #meteorCodeT5p = meteor_score(methodLevelComment, codeT5p_Summary)
                #rougeCodeT5p = rouge_l(methodLevelComment, codeT5p_Summary)
                
                bleuCodeBert = nltk_bleu(codeBert_Summary, methodLevelComment)
                meteorCodeBert = meteor_score(methodLevelComment, codeBert_Summary)
                rougeCodeBert = rouge_l(methodLevelComment, codeBert_Summary)



                print("updated scores for id :",item.get('_id')," index :",index," ")
            except Exception as e:
                print("exception ",e," occured for id :",item.get('_id'))

print("\nDone processing")
print("totlaMethodWithDocstring: ",totalMethodsWithDocstring)