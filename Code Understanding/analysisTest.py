from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p.find()


depT5Blue = 0
depCBertBleu = 0
depCount = 0

indepT5Blue = 0
indepCBertBleu = 0
indepCount = 0
maxBlueT5Dep = 0
maxBleuT5Indep = 0

for element in javaDBFinal:
    methods = element.get('methods')
    for method in methods:

        docstring = method.get('Docstring')
        bleuCodeBert = method.get('bleuCodeBert')
        bleuCodeT5p = method.get('bleuCodeT5p')
        
        if(len(docstring)==0):
            continue

        # if(method.get('FunctionName').startswith('get') or method.get('FunctionName').startswith('set')):
        #     continue
        # if(bleuCodeBert<=0.09 or bleuCodeT5p<=0.09):
        #     continue

        if (method.get('isDependent')==True):
            depT5Blue += bleuCodeT5p
            depCBertBleu += bleuCodeBert
            depCount += 1
            maxBlueT5Dep = max(maxBlueT5Dep,bleuCodeT5p)
        else:
            indepT5Blue += bleuCodeT5p
            indepCBertBleu += bleuCodeBert
            indepCount += 1
            maxBleuT5Indep = max(maxBleuT5Indep,bleuCodeT5p)

print('T5 dep max: ',maxBlueT5Dep, ' count: ',depCount)
print('T5 indep max: ',maxBleuT5Indep, ' count: ',indepCount)

print('Avg blue for dependent methods --> codeT5: ',depT5Blue/depCount,' codeBert: ',depCBertBleu/depCount)
print('Avg blue for independent methods --> codeT5: ',indepT5Blue/indepCount,' codeBert: ',indepCBertBleu/indepCount)