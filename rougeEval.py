from rouge import Rouge
import sys

#NOTE: factoid questions marked with (F) at beginning of question

def rougeCalc(hypothesis, reference):
    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference)
    return scores



def main():
    groundTruth = sys.argv[1] #contains lines of: sourceUrl url
    groundTruthFile = open(groundTruth, 'r')
    groundTruthLines = groundTruthFile.readlines()
    questionAnswerMap = {}
    questionAnswerFactoidMap = {}
    questionAnswerNonFactoidMap = {}
    #list of dict's for rouge-1, rouge-2, rouge-l with dict keys r,p,f
    rougeAvg = [{'rouge-1': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-2': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-l': {'r': 0.0, 'p': 0.0, 'f': 0.0}}]
    rougeFactoidAvg = []
    rougeNonFactoidAvg = []
    #parse into question answer maps, and split based on factoid/non-factoid
    for line in groundTruthLines:
        answer = line.strip().split("?")[1]
        if (answer[0:4] == ' (F)'): #factoid
            answer = line.strip().split("?")[1][4:]
            questionAnswerFactoidMap[line.strip().split("?")[0]] = answer
        else: #nonfactoid
            questionAnswerNonFactoidMap[line.strip().split("?")[0]] = answer
        questionAnswerMap[line.strip().split("?")[0]] = answer
    for key in questionAnswerMap:
        #need to get system answer to pass in as hypothesis
        output = rougeCalc(" ", questionAnswerMap[key])
        rougeAvg[0]['rouge-1']['r'] += output[0]['rouge-1']['r']
        rougeAvg[0]['rouge-1']['p'] += output[0]['rouge-1']['p']
        rougeAvg[0]['rouge-1']['f'] += output[0]['rouge-1']['f']
        rougeAvg[0]['rouge-2']['r'] += output[0]['rouge-1']['r']
        rougeAvg[0]['rouge-2']['p'] += output[0]['rouge-1']['p']
        rougeAvg[0]['rouge-2']['f'] += output[0]['rouge-1']['f']
        rougeAvg[0]['rouge-l']['r'] += output[0]['rouge-1']['r']
        rougeAvg[0]['rouge-l']['p'] += output[0]['rouge-1']['p']
        rougeAvg[0]['rouge-l']['f'] += output[0]['rouge-1']['f']

    #there is a better way to do this lol
    #will take the outputs & put into some kind of table for poster
    rougeAvg[0]['rouge-1']['r'] = rougeAvg[0]['rouge-1']['r'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-1']['p'] = rougeAvg[0]['rouge-1']['p'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-1']['f'] = rougeAvg[0]['rouge-1']['f'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-2']['r'] = rougeAvg[0]['rouge-1']['r'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-2']['p'] = rougeAvg[0]['rouge-1']['p'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-2']['f'] = rougeAvg[0]['rouge-1']['f'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-l']['r'] = rougeAvg[0]['rouge-1']['r'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-l']['p'] = rougeAvg[0]['rouge-1']['p'] / len(questionAnswerMap)
    rougeAvg[0]['rouge-l']['f'] = rougeAvg[0]['rouge-1']['f'] / len(questionAnswerMap)


if __name__=="__main__":
    main()
