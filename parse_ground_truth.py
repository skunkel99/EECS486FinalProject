import json

groundTruth = {}

with open("ground_truth.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        lst = line.split("?")
        query = lst[0]
        answer = lst[1][1:].replace("(F)", "").replace("\n", "")

        groundTruth[query] = answer

with open("ground_truth.json", "w") as file:
    json.dump(groundTruth, file)
