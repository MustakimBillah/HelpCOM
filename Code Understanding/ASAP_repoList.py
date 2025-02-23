import json

# Path to the input JSONL file and the output text file
input_file = 'path/ASAP_DATASET/Java_data/Java_data/testASAP.jsonl'
output_file = 'path/ASAP_DATASET/Java_data/Java_data/test_repo_ASAP.txt'

# Open the JSONL file and read it line by line
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # Parse the JSON object from each line
        data = json.loads(line.strip())

        Repo = data.get('repo')
        Path = data.get('path', '')
        Function_name = data.get('func_name')
        # Write the extracted data to the text file
        outfile.write(f"Please find some info about the location of the function in the repo.\n")
        outfile.write(f"Repo: {Repo}\n")
        outfile.write(f"Path: {Path}\n")
        outfile.write(f"Function_name: {Function_name}\n")
        outfile.write(f"##########\n")
        
print("done processing")