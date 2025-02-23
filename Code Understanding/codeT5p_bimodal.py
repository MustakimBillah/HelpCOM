from transformers import AutoModel, AutoTokenizer
from pymongo import MongoClient

checkpoint = "Salesforce/codet5p-220m-bimodal"
device = "cuda"  # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBFinal.find()


javaDBFinalList = []

for element in javaDBFinal:
    javaDBFinalList.append(element)


client.close()

count = 0

for item in javaDBFinalList:
    methods = item.get('methods')
    for method in methods:
        Docstring = method.get('Docstring')
        wordCount = len(Docstring.split())
        if (wordCount > 0):
            count+=1
            code = method.get('Syntax')
            input_ids = tokenizer(code, return_tensors="pt").input_ids.to(device)
            generated_ids = model.generate(input_ids, max_length=20)
            summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            method['codeT5p_Summary'] = summary 
            print("Count :",count," Summary: ",summary)


client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding  
javaDBCodeT5p = db.javaDBCodeT5p

for item in javaDBFinalList:
    javaDBCodeT5p.insert_one(item)
    print("Added item : ",item.get('_id'))
