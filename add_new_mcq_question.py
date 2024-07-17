# ===========================================================================
# Initialization
# ===========================================================================

import pandas as pd

import helper_functions

# ===========================================================================
# Function: Main
# ===========================================================================

def add_new_mcq_question():

    # User to input name of quiz folder and read quiz CSV into database.
    mcq_quiz_folder_path = helper_functions.user_input("Enter path of quiz folder (E.g. G:\My Drive\quiz_folder): ")
    mcq_quiz_db_file_path = mcq_quiz_folder_path + "/quiz_db.csv"
    quiz_df = pd.read_csv(mcq_quiz_db_file_path)

    # Get headers, last question ID, topics from quiz database.
    quiz_headers = quiz_df.columns
    quiz_topics = quiz_df["Topic"].unique()
    quiz_last_qn_id = 0

    if not quiz_df.empty:
        try:
            quiz_last_qn_id = quiz_df['ID'].max()
        except IndexError:  # In case the column 'ID' is there but it's empty
            quiz_last_qn_id = 0


    print("Headers in quiz database: ")
    print(quiz_headers.to_list(), "\n")

    # User to input number of questions.
    to_add = []
    num_questions = int(helper_functions.user_input("Enter number of questions to add: "))

    while num_questions > 0:

        # Create a dictionary to store new question.
        new_question = {}

        print("\n-------------- New question ------------------")

        for header in quiz_headers:

            if header == "ID":
                quiz_last_qn_id += 1
                new_question["ID"] = quiz_last_qn_id
            
            elif header =="Type":
                new_question["Type"] = "Base"
            
            elif header == "Topic":
                
                new_question_topic(new_question, quiz_topics)

                print(helper_functions.coloured_text("green", "\nID:"), new_question["ID"])
                print(helper_functions.coloured_text("green", "Type:"), new_question["Type"])
                print(helper_functions.coloured_text("green", "Topic:"), new_question["Topic"])

            elif header == "Image":
                new_question["Image"] = helper_functions.user_input('Does the question have an image? (Y/N) [Yes/No] ').strip().lower()

                if new_question["Image"] == "y" or new_question["Image"] == "yes":
                    new_question["Image_file"] = helper_functions.user_input('Image file name (E.g. image1.jpg): ')
                else:
                    new_question['Image_file'] = "NA"

            elif header == "Image_file":
                continue

            elif header == "Answer":
                answer = int(helper_functions.user_input('Which option is the answer (E.g. 2)? '))
                new_question['Answer'] = new_question['Option'+str(answer)]

            else:
                new_question[header] = helper_functions.user_input(f'{header}: ').strip()

        ############### Review and confirm the new question.
        print("\n-------------- Review question ---------------")
        for key, value in new_question.items():
            print(f"{helper_functions.coloured_text('cyan', key)}: {value}")

        confirm = helper_functions.user_input("\nConfirm this question? (Y/N/R) [Yes/No/Redo]: ").strip().lower()

        if confirm == "y" or confirm == "yes":
            to_add.append(new_question)
            num_questions -= 1

        elif confirm == 'r' or confirm == 'redo':
            print("\n-------------- Redo question ----------------")
            print("Redo question.")
            quiz_last_qn_id -= 1
            continue

        else:
            print("\n-------------- Deleted question ---------------")
            print("Question discarded.")
            num_questions -= 1

        print("\n-------------- Completed question -----------")

    ############### Check file accessibility. Write the new question to the quiz database.
    helper_functions.write_question_to_file(mcq_quiz_db_file_path, to_add)

# ===========================================================================
# Function: Topic
# ===========================================================================

def new_question_topic(new_question, quiz_topics):
    print("\nChoose topic number or create new topic: ")
    for i, topic in enumerate(quiz_topics):
        print(str(i+1) + ". " + topic)
    print(f"{len(quiz_topics)+1}. Other")

    topic_num = int(helper_functions.user_input("\nOption: ")) - 1

    if topic_num in range(len(quiz_topics)):
        new_question['Topic'] = quiz_topics[topic_num]

    elif topic_num == len(quiz_topics):
        input_topic = helper_functions.user_input('Enter new topic: ')

        if input_topic not in quiz_topics:
            new_question['Topic'] = input_topic
        else:
            new_question['Topic'] = input_topic
        
# ===========================================================================
# Test mode
# ===========================================================================
def test(mode):
    if mode == 1:
        add_new_mcq_question()

if __name__ == "__main__":
    test(0) # 0 for no test