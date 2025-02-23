import math
import re
import xml.sax.saxutils
import sys

# Helper variables and settings
preserve_case = False
eff_ref_len = "shortest"

normalize1 = [
    ('<skipped>', ''),         # strip "skipped" tags
    (r'-\n', ''),              # strip end-of-line hyphenation and join lines
    (r'\n', ' '),              # join lines
]
normalize1 = [(re.compile(pattern), replace) for (pattern, replace) in normalize1]

normalize2 = [
    (r'([\{-\~\[-\` -\&\(-\+\:-\@\/])',r' \1 '), # tokenize punctuation
    (r'([^0-9])([\.,])',r'\1 \2 '),              # tokenize period/comma unless preceded by a digit
    (r'([\.,])([^0-9])',r' \1 \2'),              # tokenize period/comma unless followed by a digit
    (r'([0-9])(-)',r'\1 \2 ')                    # tokenize dash when preceded by a digit
]
normalize2 = [(re.compile(pattern), replace) for (pattern, replace) in normalize2]

# Normalization function
def normalize(s):
    '''Normalize and tokenize text.'''
    for (pattern, replace) in normalize1:
        s = re.sub(pattern, replace, s)
    s = xml.sax.saxutils.unescape(s, {'&quot;':'"'})
    s = " %s " % s
    if not preserve_case:
        s = s.lower()
    for (pattern, replace) in normalize2:
        s = re.sub(pattern, replace, s)
    return s.split()

# Count n-grams in a list of words
def count_ngrams(words, n=4):
    counts = {}
    for k in range(1, n+1):
        for i in range(len(words)-k+1):
            ngram = tuple(words[i:i+k])
            counts[ngram] = counts.get(ngram, 0)+1
    return counts

# Process reference sentence
def cook_refs(refs, n=4):
    '''Prepare reference n-grams.'''
    refs = [normalize(refs)]
    maxcounts = {}
    for ref in refs:
        counts = count_ngrams(ref, n)
        for (ngram, count) in counts.items():
            maxcounts[ngram] = max(maxcounts.get(ngram, 0), count)
    return ([len(ref) for ref in refs], maxcounts)

# Process candidate sentence
def cook_test(test, refs, n=4):
    '''Prepare test n-grams and match with reference.'''
    test = normalize(test)
    result = {"testlen": len(test)}
    
    reflens, refmaxcounts = refs
    if eff_ref_len == "shortest":
        result["reflen"] = min(reflens)
    elif eff_ref_len == "average":
        result["reflen"] = float(sum(reflens)) / len(reflens)
    elif eff_ref_len == "closest":
        min_diff = None
        for reflen in reflens:
            if min_diff is None or abs(reflen - len(test)) < min_diff:
                min_diff = abs(reflen - len(test))
                result['reflen'] = reflen

    result["guess"] = [max(len(test)-k+1, 0) for k in range(1, n+1)]
    result['correct'] = [0] * n
    counts = count_ngrams(test, n)
    for (ngram, count) in counts.items():
        result["correct"][len(ngram)-1] += min(refmaxcounts.get(ngram, 0), count)
    return result

# Calculate BLEU score from processed n-grams
def score_cooked(comps, n=4, smooth=1):
    total = {'testlen': comps['testlen'], 'reflen': comps['reflen'], 'guess': comps['guess'], 'correct': comps['correct']}
    logbleu = 0.0
    for k in range(n):
        correct = total['correct'][k]
        guess = total['guess'][k]
        addsmooth = 1 if smooth and k > 0 else 0
        logbleu += math.log(correct + addsmooth + sys.float_info.min) - math.log(guess + addsmooth)
    logbleu /= float(n)
    brevPenalty = min(0, 1 - float(total['reflen'] + 1) / (total['testlen'] + 1))
    bleu_score = math.exp(logbleu + brevPenalty)
    return bleu_score * 100  # Return percentage BLEU score

# Main function to calculate BLEU score for two strings
def calculate_bleu(reference, prediction, n=4, smooth=1):
    '''Calculate BLEU score between a reference and a prediction.'''
    refs = cook_refs(reference, n)
    test = cook_test(prediction, refs, n)
    return score_cooked(test, n, smooth)

# Example usage:
reference_text = "Verifies the content of the {@link HttpRequest} that's internally created and passed through to the http client"
prediction_text = "Test internal http request ."
bleu_score = calculate_bleu(reference_text, prediction_text)
print("BLEU score:", bleu_score)
