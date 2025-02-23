import re
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p

def extract_first_paragraph(docstring):
    # Remove the /** and */ surrounding the docstring and clean leading * on each line
    cleaned_docstring = re.sub(r'^\s*/\*\*|\*/\s*$', '', docstring, flags=re.MULTILINE)
    cleaned_docstring = re.sub(r'^\s*\* ?', '', cleaned_docstring, flags=re.MULTILINE)
    
    # Split based on a double newline or single newline followed by space or newline
    paragraphs = re.split(r'\n\s*\n|\n(?=\s*\*)', cleaned_docstring.strip())
    
    # Return the first non-empty paragraph
    return paragraphs[0].strip() if paragraphs else ''



for item in javaDBFinal.find():
    methods = item.get('methods')
    for index, method in enumerate(methods):
        docstring = method.get('Docstring')
        methodLevelComment = extract_first_paragraph(docstring)

        javaDBFinal.update_one(
            {'_id': item.get('_id')},
            {"$set":{f"methods.{index}.methodLevelComment":methodLevelComment}}
        )

        print(item.get('_id'),"  ",index," comment: ",methodLevelComment)