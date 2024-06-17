import random
from dictionary_databse import data
grades= ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"]
def get_question(grade_list):
    picked_grade = random.choice(grade_list)
    grade_int = picked_grade[-1]
    print(grade_int)
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
    option_list=[meaning]
    while len(option_list) < 4:
        random_option = random.choice(category_list)
        if random_option not in option_list:
            option_list.append(random_option)
    random.shuffle(option_list)
    return pick_ques,meaning,option_list
    
term_dict = {item["Term"]: item for item in data}
tag_dict = {}
for item in data:
    if item["Tag"] not in tag_dict:
        tag_dict[item["Tag"]] = []
    tag_dict[item["Tag"]].append(item["Meaning"])
    
def hash_get_question(grade_list, max_retries=10):
    for _ in range(max_retries):
        try:
            picked_grade = random.choice(grade_list)
            grade_int = picked_grade[-1]
            print(f"Grade int: {grade_int}")
            list_of_questions = [item["Term"] for item in data if item["Grade"] == grade_int]
            pick_ques = random.choice(list_of_questions)
            meaning = term_dict[pick_ques]["Meaning"]
            category = term_dict[pick_ques]["Tag"]
            category_list = tag_dict[category]
            option_list = [meaning]
            remaining_options = [opt for opt in category_list if opt != meaning]
            option_list.extend(random.sample(remaining_options, k=min(3, len(remaining_options))))
            while len(option_list) < 4:
                add_item=random.choice(category_list)
                if add_item not in option_list:
                    option_list.append(add_item)
            random.shuffle(option_list)
            return pick_ques, meaning, option_list
        except Exception as e:
            print(f"Retrying hash_get_question due to error: {str(e)}")
    print("Max retries reached for hash_get_question. Returning None.")
    return None, None, None
