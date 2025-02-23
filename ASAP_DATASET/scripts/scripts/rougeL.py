import os
import argparse
from rouge import Rouge

def computeRougeL(reference_file, model_output):
    # Initialize Rouge
    rouge = Rouge()

    # Read model output and reference file
    with open(model_output, "r", encoding="utf-8") as f:
        predictions = f.readlines()

    with open(reference_file, "r", encoding="utf-8") as f:
        references = f.readlines()

    # Calculate Rouge-L scores
    rouge_l_scores = rouge.get_scores(predictions, references, avg=True)

    return rouge_l_scores['rouge-l']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
      
    ## Required parameters  
    parser.add_argument("--ref_file", default=None, type=str, required=True,
                           help=".gold")
    parser.add_argument("--model_output", default=None, type=str, required=True,
                           help=".output") 
      
    args = parser.parse_args()    

    reference_file = args.ref_file
    model_output = args.model_output
      
    if not os.path.exists('only_number'):
       os.makedirs('only_number')
    
    rouge_l_score = computeRougeL(reference_file, model_output)
    
    print(rouge_l_score["f"])
    x = "poly_gcbert"  
    with open(f"only_number/{x}.rouge_l", "w") as ff:
        ff.write(str(rouge_l_score))
