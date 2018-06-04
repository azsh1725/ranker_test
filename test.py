import sys
import pandas as pd
import re
import numpy as np
import string
import os

path_to_script_answers = sys.argv[1]
path_to_qa = sys.argv[2]
log_file_for_correct = "correct.csv"
log_file_for_wrong = "wrong.csv"
#path_to_question = "questions.txt"
qa_df = pd.read_csv(path_to_qa, sep=";", header=None, names=["quest", "answer"])
script_ans = []
with open(path_to_script_answers, "r", encoding="utf-8") as sa_in:
    ans = sa_in.read().split(";\n")
    for i in range(len(ans) - 1):
        script_ans.append(ans[i])

#path_to_text = "wiki_article.txt"
answer_without_punc = []
#qa_df["answer"] = qa_df["answer"].str.replace(re.escape(string.punctuation), " ")
#qa_df["answer"] = qa_df["answer"].str.replace(" +", " ")


#print(qa_df["answer"][0])

text_result = []
paragraph_result = []
questions = qa_df.quest.values.tolist()

qa_df["script_answer"] = script_ans

correct_answer = []
for index, row in qa_df.iterrows():
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    data = regex.sub(' ', str(row["answer"]))
    data = re.sub(" +", " ", data)
    answer_without_punc.append(data)
    text_result.append(row["script_answer"])

    if (str(data) in row["script_answer"]):
        #print("correct row:\n{}\n".format(row))
        correct_answer.append(1)
    else:
        correct_answer.append(0)

answer_list = answer_without_punc
question_list = qa_df["quest"].values.tolist()
#print("correct answers: {}".format(correct_answer))
print("{}% correct".format(round(np.sum(correct_answer)/qa_df.shape[0]*100, 2)))

if os.path.exists(log_file_for_correct):
    os.remove(log_file_for_correct)

if os.path.exists(log_file_for_wrong):
    os.remove(log_file_for_wrong)

for c, t, q, correctness in zip(answer_list, text_result, question_list, correct_answer):
    if correctness == 1:
        with open(log_file_for_correct, "a", encoding="utf-8") as out:
            out.write("{};{};{};\n".format(q, t, c))
    else:
        with open(log_file_for_wrong, "a", encoding="utf-8") as out:
            out.write("{};{};{};\n".format(q, t, c))
    #print("correctness: {}\nquestion: {}\nright answer: {}\ntext: {}\n".format(correctness, q, c, t))