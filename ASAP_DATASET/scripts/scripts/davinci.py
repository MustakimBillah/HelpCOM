import argparse
import csv
import os
import json
from rank_bm25 import BM25Okapi
from time import sleep
import numpy as np
#import openai
import re
from openai import OpenAI
client_openAI = OpenAI(
    api_key = "sk-proj-dPQvN0GALJBgOPcFYYkWT3BlbkFJOMo2fRii5rMXSv7fxDEm"
)

def makestr(lst):
    p=""
    for w in lst:
        p=p+w+" "
    return p.strip()    
	#return lst
	
def main():
    parser = argparse.ArgumentParser()
    ## Required parameters  
    parser.add_argument("--open_key", default="", type=str, required=False,
                        help="")
    parser.add_argument("--model", default="davinci", type=str, required=False,
                        help="davinci")
    parser.add_argument("--pause_duration", default=6, type=str, required=False,
                        help="time to stop between samples")  
    parser.add_argument("--data_folder", default="Java_data", type=str, required=False,
                        help="data folder path ") 
    parser.add_argument("--mode", default="BM25", type=str, required=False,
                        help="fixed/BM25")    
    parser.add_argument("--use_repo", default="no", type=str, required=False,
                        help="yes/no")
    parser.add_argument("--use_id", default="yes", type=str, required=False,
                        help="yes/no")
    parser.add_argument("--use_dfg", default="yes", type=str, required=False,
                        help="yes/no")    
    
    parser.add_argument("--language", default="Java", type=str, required=False,
                        help="Java/Python/Ruby")
    args = parser.parse_args()

    args.number_of_fewshot_sample=3
    args.open_key = ""
    args.model = "davinci"
    args.pause_duration = 6
    args.data_folder = "/student/mjr175/method-level-comment-generation/ASAP_DATASET/Java_data/Java_data"
    args.mode = "BM25"
    args.use_repo = "no"
    args.use_id = "id3"
    args.use_dfg = "yes"
    args.language = "Java"
	
    #openai.api_key = args.open_key
    
    
    name=""
    if args.use_repo=="yes":
        name=name+"_repo"
        

    if args.use_dfg=="yes":
        name=name+"_dfg"
     
    if args.use_id=="id3":
        name=name+"_id3"     

    
    #making necessary forlders
    if not os.path.exists(args.language+'_result'):
       os.makedirs(args.language+'_result')
       
    
    if args.model=="davinci":
        target_model="gpt-3.5-turbo-instruct"
        #target_model="gpt-4o"


    #Reading data
    train_json = []
    for line in open(args.data_folder+'/train.jsonl', 'r', encoding="utf-8"):
        train_json.append(json.loads(line))
    print(len(train_json))
    
    
    test_json = []
    for line in open(args.data_folder+'/testASAP.jsonl', 'r', encoding="utf-8"):
        test_json.append(json.loads(line))
    print(len(test_json)) 
    
    
    train_code=[]
    train_nl=[]
    for i in range(len(train_json)):
        train_code.append(train_json[i]['code'])
        train_nl.append(makestr(train_json[i]['docstring_tokens']))    
    
        
    test_code=[]
    test_nl=[]
    for i in range(len(test_json)):
        test_code.append(test_json[i]['code'])
        test_nl.append(makestr(test_json[i]['docstring_tokens']))   
        
    if args.language in ["Python","airflow","airflowv2","grim","grimv2","h2o","h2ov2","probability","probabilityv2"]:
        for i in range(len(train_code)):
            m=train_code[i]
            m = re.sub(r'\"\"\"(.+?)\"\"\"', '', m)
            m = re.sub(r"\'\'\'(.+?)\'\'\'", '', m)
            m = m.replace(train_json[i]["docstring"],"")
            train_code[i]=m
        for i in range(len(test_code)):
            m=test_code[i]
            m = re.sub(r'\"\"\"(.+?)\"\"\"', '', m)
            m = re.sub(r"\'\'\'(.+?)\'\'\'", '', m)
            m = m.replace(test_json[i]["docstring"],"")
            test_code[i]=m

        
    train_repo=[]    
    with open(args.data_folder+"/train_repo.txt","r") as f:     
        text=f.read().strip()
        text=text.split("##########")   
        for ln in text:
            train_repo.append(ln)
            
    test_repo=[]
    with open(args.data_folder+"/test_repo_ASAP.txt","r") as f:     
        text=f.read().strip()
        text=text.split("##########") 
        for ln in text:
            test_repo.append(ln)        
            
            
    train_dfg=[]    
    with open(args.data_folder+"/train_dfg.txt","r",encoding="utf-8") as f:     
        text=f.read().strip()
        text=text.split("##########")   
        for ln in text:
            train_dfg.append(ln)
            
    test_dfg=[]
    with open(args.data_folder+"/test_dfg.txt","r") as f:     
        text=f.read().strip()
        text=text.split("##########") 
        for ln in text:
            test_dfg.append(ln)        
        
 

    train_id3=[]    
    with open(args.data_folder+"/train_id_type3.txt","r") as f:     
        text=f.read().strip()
        text=text.split("##########")   
        for ln in text:
            train_id3.append(ln)
            
    test_id3=[]
    with open(args.data_folder+"/test_id_type3.txt","r") as f:     
        text=f.read().strip()
        text=text.split("##########") 
        for ln in text:
            test_id3.append(ln) 
        
    
    if args.mode=="BM25":
        tokenized_corpus = [doc.split(" ") for doc in train_code]
        bm25 = BM25Okapi(tokenized_corpus)
    elif args.mode=="fixed":
        with open(args.data_folder+"/fixed_3.txt","r",encoding="utf-8") as f:
            context_fixed=f.read()
    i=380
    is_error=0
    error_count=0

    while i < (len(test_json)):   
        print(i)

        try:
            context=""            
            query = test_code[i]
            if args.mode=="BM25":
                if is_error==0:
                    tokenized_query = query.split(" ")
                    x=bm25.get_scores(tokenized_query)   
                    arr = np.array(x)
                    x=arr.argsort()[-int(args.number_of_fewshot_sample):][::-1]
                
                print(x)
                
                if (error_count%4==0 and error_count>0) and len(x)>1:
                    x=x[0:len(x)-1]
                    is_error=0
                
                for w in x:
                    context=context+train_code[w].strip()+"\n"
                    
                    if args.use_repo=="yes":
                        context=context+train_repo[w].strip()+"\n"                      
                    if args.use_id=="id3":
                        context=context+train_id3[w].strip()+"\n"                                                
                    if args.use_dfg=="yes":
                        context=context+train_dfg[w].strip()+"\n"                        
                        
                        
                    context=context+"Write down the original comment written by the developer.\n"
                    context=context+"Comment: "+train_nl[w]+"\n\n"
            elif args.mode=="fixed":
                context=context+context_fixed
            
            
            context=context+test_code[i].strip()+"\n"
            
            if args.use_repo=="yes":
                context=context+test_repo[i].strip()+"\n"        
                
            if args.use_dfg=="yes":
                context=context+test_dfg[i].strip()+"\n"                
                              
            if args.use_id=="id3":
                context=context+test_id3[i].strip()+"\n"  
                 
                
            context=context+"Write down the original comment written by the developer.\n"
            context=context+"Comment: "
            print(context)
            response = client_openAI.completions.create(
              model=target_model,

              temperature=0,
              max_tokens=250,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0,
              prompt=context
              
            )
            print("#####################model response###############")
            modelout=response.choices[0].text.split("\n")[0].strip()   
            # fr=open(args.language+'_result/'+args.model+"_"+args.mode+name+".txt","a", encoding="utf-8")
            # fr.write(str(i)+"\t"+modelout.strip()+"\n")
            # fr.close()
            print(modelout)
            dbID = test_json[i].get('_id')
            methodType =test_json[i].get('sampleType')

            file_path = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/ASAPresultsBase.csv'
            with open(file_path, "a", newline='', encoding="utf-8") as csvfile:
                print(f"dbID: {dbID}, methodType: {methodType}, modelout: {modelout.strip()}")
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([dbID, methodType,modelout.strip()])
                sleep(1)

            print("going_sleep")
            sleep(int(args.pause_duration))
            print("wakeup")
            i=i+1
            error_count=0
            is_error=0
        except Exception as e:
            print("error: ", e)
            is_error=1
            error_count=error_count+1
            print(error_count)
            if error_count==12:
                 fr=open(args.language+'_result/'+args.model+"_"+args.mode+name+".txt","a", encoding="utf-8")
                 fr.write(str(i)+"\t"+""+"\n")
                 fr.close()
                 i=i+1
                 error_count=0
                 is_error=0
            sleep(10)
            continue
    

    
    
main()
