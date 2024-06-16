import random
from dictionary_databse import data
grades= ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"]
def get_question(grade_list):
    picked_grade = random.choice(grade_list)
    grade_int = picked_grade[-1]
    list_of_questions = []
    for item in data:
        if item["Grade"] == grade_int:
            list_of_questions.append(item["Term"])
    pick_ques=random.choice(list_of_questions)
    # search back the meaning in the dictionary
    for item in data:
        if item["Term"] == pick_ques:
            meaning = item["Meaning"]
            category= item["Tag"]
    category_list = []
    for item in data:
        if item["Tag"] == category:
            category_list.append(item["Meaning"])
    option_list=[]
    while len(option_list) < 4:
        random_option = random.choice(category_list)
        if random_option != meaning:
            option_list.append(random_option)
    option_list.append(meaning)
    random.shuffle(option_list)
    return pick_ques,meaning,option_list

print(get_question(grades))