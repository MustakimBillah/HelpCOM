import nltk
from nltk.translate.bleu_score import *

# bleu function used in DeepCom EMSE paper

def nltk_bleu(predicted_text, ground_truth):
    hypotheses = []
    hypotheses.append(predicted_text)
    references = []
    references.append(ground_truth)
    refs = []
    count = 0
    total_score = 0.0

    cc = SmoothingFunction()

    for hyp, ref in zip(hypotheses, references):
        hyp = hyp.split()
        ref = ref.split()

        score = nltk.translate.bleu([ref], hyp, smoothing_function=cc.method4)
        total_score += score
        count += 1

    avg_score = total_score / count
    # print ('avg_score: %.2f' % avg_score)
    return avg_score


predicted_text = "Factory for calculating the expansion point"
predicted_text = "Expansion function for Nelder-Mead algorithm. Expands the simplex in the direction of the reflected point and replaces the worst point with the new point if it is better"
ground_truth = """Creates the condition function pair for an expansion"""

print(nltk_bleu(predicted_text,ground_truth))


