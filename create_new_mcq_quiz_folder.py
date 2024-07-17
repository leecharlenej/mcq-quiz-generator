# ===========================================================================
# Initialization
# ===========================================================================

import os

import helper_functions

# ===========================================================================
# Function: Creates quiz folder, image folder and quiz CSV database
# ===========================================================================

def create_new_mcq_quiz_folder():

    # User to input name of new quiz folder.
    input_mcq_quiz_folder_name = helper_functions.user_input("Enter name of quiz folder (E.g. NCL Quiz 1): ").lower()
    mcq_quiz_folder_name = input_mcq_quiz_folder_name.replace(" ", "_")

    # User to output path of main folder where quiz folder will be saved.
    main_folder_path = helper_functions.user_input("Enter path of quiz folder (E.g. G:\My Drive\quiz_folder): ")

    # Create path of new quiz folder.
    mcq_quiz_folder_path = main_folder_path + "/" + mcq_quiz_folder_name

    # Check existence of folder. If doesn't exist, create new one.
    # - Create new CSV file to store quiz questions, with headers specified by user.
    # Otherwise, prompt user to create new folder.
    if not os.path.exists(mcq_quiz_folder_path):
        os.makedirs(mcq_quiz_folder_path)
        os.makedirs(mcq_quiz_folder_path + "/" + "images")
        create_new_quiz_db_csv(mcq_quiz_folder_path)

    else:
        helper_functions.logging.error("Folder already exists.")
        input_create_new = helper_functions.user_input("Do you want to create a new folder? (Y/N) [Yes/No] ").lower()
        if input_create_new == "y" or input_create_new == "yes":
            print('\n=============================================')
            create_new_mcq_quiz_folder()


# ===========================================================================
# Function: Creates quiz CSV database
# ===========================================================================
    
def create_new_quiz_db_csv(mcq_quiz_folder_path):
    with open(mcq_quiz_folder_path + "/quiz_db.csv", "w") as quiz_db:
        quiz_headers = ["ID", "Type", "Topic", "Sub_topic", "Image", "Image_file", "Question"]
        print("\nThe headers already in the quiz database are: ID, Type, Topic, Sub_topic, Image, Image_file, Question and Answer.")
        num_headers = int(helper_functions.user_input("Enter number of options: "))

        for i in range(num_headers):
            quiz_headers.append(f"Option{str(i+1)}")

        quiz_headers.append("Answer")

        quiz_db.write(",".join(quiz_headers) + "\n")

# ===========================================================================
# Test mode
# ===========================================================================
def test(mode):
    if mode == 1:
        create_new_mcq_quiz_folder()

if __name__ == "__main__":
    test(0) # 0 for no test
