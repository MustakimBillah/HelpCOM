from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
docStringMethods = db.docStringMethods.find()


codeT5p_SIDE = 0
codeBERT_SIDE = 0
count = 0


for item in docStringMethods:
    codeT5p_SIDE+=item.get('sideCodeT5p')
    codeBERT_SIDE+=item.get('sideCodeBert')
    count+=1


print("AVG SIDE CodeT5p: ",round(codeT5p_SIDE/count,2))
print("AVG SIDE CodeBERT: ",round(codeBERT_SIDE/count,2))


