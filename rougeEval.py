from rouge import Rouge
import sys
import json

#NOTE: factoid questions marked with (F) at beginning of question

def rougeCalc(hypothesis, reference):
    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference)
    return scores



def main():
    groundTruth = sys.argv[1]
    systemOutputFile = sys.argv[2] #json of question answer from system
    with open(systemOutputFile) as json_file:
        outputData = json.load(json_file)
    groundTruthFile = open(groundTruth, 'r')
    groundTruthLines = groundTruthFile.readlines()
    questionAnswerMap = {}
    questionAnswerFactoidMap = {}
    questionAnswerNonFactoidMap = {}
    #list of dict's for rouge-1, rouge-2, rouge-l with dict keys r,p,f
    rougeAvg = [{'rouge-1': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-2': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-l': {'r': 0.0, 'p': 0.0, 'f': 0.0}}]
    rougeFactoidAvg = [{'rouge-1': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-2': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-l': {'r': 0.0, 'p': 0.0, 'f': 0.0}}]
    rougeNonFactoidAvg = [{'rouge-1': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-2': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-l': {'r': 0.0, 'p': 0.0, 'f': 0.0}}]
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
        output = rougeCalc(outputData[key], questionAnswerMap[key])
        rougeAvg[0]['rouge-1']['r'] += output[0]['rouge-1']['r']
        rougeAvg[0]['rouge-1']['p'] += output[0]['rouge-1']['p']
        rougeAvg[0]['rouge-1']['f'] += output[0]['rouge-1']['f']
        rougeAvg[0]['rouge-2']['r'] += output[0]['rouge-1']['r']
        rougeAvg[0]['rouge-2']['p'] += output[0]['rouge-1']['p']
        rougeAvg[0]['rouge-2']['f'] += output[0]['rouge-1']['f']
        rougeAvg[0]['rouge-l']['r'] += output[0]['rouge-1']['r']
        rougeAvg[0]['rouge-l']['p'] += output[0]['rouge-1']['p']
        rougeAvg[0]['rouge-l']['f'] += output[0]['rouge-1']['f']
        if key in questionAnswerFactoidMap: #factoid
            rougeFactoidAvg[0]['rouge-1']['r'] += output[0]['rouge-1']['r']
            rougeFactoidAvg[0]['rouge-1']['p'] += output[0]['rouge-1']['p']
            rougeFactoidAvg[0]['rouge-1']['f'] += output[0]['rouge-1']['f']
            rougeFactoidAvg[0]['rouge-2']['r'] += output[0]['rouge-1']['r']
            rougeFactoidAvg[0]['rouge-2']['p'] += output[0]['rouge-1']['p']
            rougeFactoidAvg[0]['rouge-2']['f'] += output[0]['rouge-1']['f']
            rougeFactoidAvg[0]['rouge-l']['r'] += output[0]['rouge-1']['r']
            rougeFactoidAvg[0]['rouge-l']['p'] += output[0]['rouge-1']['p']
            rougeFactoidAvg[0]['rouge-l']['f'] += output[0]['rouge-1']['f']

        else: #nonfactoid
            rougeNonFactoidAvg[0]['rouge-1']['r'] += output[0]['rouge-1']['r']
            rougeNonFactoidAvg[0]['rouge-1']['p'] += output[0]['rouge-1']['p']
            rougeNonFactoidAvg[0]['rouge-1']['f'] += output[0]['rouge-1']['f']
            rougeNonFactoidAvg[0]['rouge-2']['r'] += output[0]['rouge-1']['r']
            rougeNonFactoidAvg[0]['rouge-2']['p'] += output[0]['rouge-1']['p']
            rougeNonFactoidAvg[0]['rouge-2']['f'] += output[0]['rouge-1']['f']
            rougeNonFactoidAvg[0]['rouge-l']['r'] += output[0]['rouge-1']['r']
            rougeNonFactoidAvg[0]['rouge-l']['p'] += output[0]['rouge-1']['p']
            rougeNonFactoidAvg[0]['rouge-l']['f'] += output[0]['rouge-1']['f']


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

    rougeFactoidAvg[0]['rouge-1']['r'] = rougeFactoidAvg[0]['rouge-1']['r'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-1']['p'] = rougeFactoidAvg[0]['rouge-1']['p'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-1']['f'] = rougeFactoidAvg[0]['rouge-1']['f'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-2']['r'] = rougeFactoidAvg[0]['rouge-1']['r'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-2']['p'] = rougeFactoidAvg[0]['rouge-1']['p'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-2']['f'] = rougeFactoidAvg[0]['rouge-1']['f'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-l']['r'] = rougeFactoidAvg[0]['rouge-1']['r'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-l']['p'] = rougeFactoidAvg[0]['rouge-1']['p'] / len(questionAnswerFactoidMap)
    rougeFactoidAvg[0]['rouge-l']['f'] = rougeFactoidAvg[0]['rouge-1']['f'] / len(questionAnswerFactoidMap)

    rougeNonFactoidAvg[0]['rouge-1']['r'] = rougeNonFactoidAvg[0]['rouge-1']['r'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-1']['p'] = rougeNonFactoidAvg[0]['rouge-1']['p'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-1']['f'] = rougeNonFactoidAvg[0]['rouge-1']['f'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-2']['r'] = rougeNonFactoidAvg[0]['rouge-1']['r'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-2']['p'] = rougeNonFactoidAvg[0]['rouge-1']['p'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-2']['f'] = rougeNonFactoidAvg[0]['rouge-1']['f'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-l']['r'] = rougeNonFactoidAvg[0]['rouge-1']['r'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-l']['p'] = rougeNonFactoidAvg[0]['rouge-1']['p'] / len(questionAnswerNonFactoidMap)
    rougeNonFactoidAvg[0]['rouge-l']['f'] = rougeNonFactoidAvg[0]['rouge-1']['f'] / len(questionAnswerNonFactoidMap)

    print(rougeAvg)
    print(rougeFactoidAvg)
    print(rougeNonFactoidAvg)


if __name__=="__main__":
    main()
