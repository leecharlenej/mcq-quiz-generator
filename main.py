# ===========================================================================
# Initialization
# ===========================================================================

import sys

import helper_functions
import create_new_mcq_quiz_folder
import add_new_mcq_question
import chatgpt_new_question_or_edit
import generate_mcq_quiz

# ===========================================================================
# Main programme
# ===========================================================================

options = {1: "Create a new MCQ quiz folder",
           2: "Add a new MCQ question",
           3: "ChatGPT a new question/ edit a question",
           4: "Generate a MCQ quiz",
           5: "Exit"}

print("╔═════════════════════════════════════╗")
print("║ Welcome to the MCQ Quiz Generator   ║")
print("╚═════════════════════════════════════╝")

while True:

    print("\n-------------- Start ------------------------")
    print("Choose an option:")
    for i in range(len(options)):
        print(f"{i+1}. {options[i+1]}")

    try:
        selected_option = int(helper_functions.user_input("\nOption: "))
    except ValueError:
        helper_functions.logging.error("Please enter a number.")
        continue

    if selected_option == 1:
        print("\n============== Option 1 =====================")
        print("╔═════════════════════════════════════╗")
        print("║ 1. Create a new MCQ quiz folder     ║")
        print("╚═════════════════════════════════════╝")
        create_new_mcq_quiz_folder.create_new_mcq_quiz_folder()
        print("\n============== Done =========================")

    elif selected_option == 2:
        print("\n============== Option 2 =====================")
        print("╔═════════════════════════════════════╗")
        print("║ 2. Add a new MCQ question           ║")
        print("╚═════════════════════════════════════╝")
        add_new_mcq_question.add_new_mcq_question()
        print("\n============== Done =========================")

    elif selected_option == 3:
        print("\n============== Option 3 =====================")
        print("╔═════════════════════════════════════╗")
        print("║ 3. ChatGPT current question         ║")
        print("╚═════════════════════════════════════╝")
        chatgpt_new_question_or_edit.chatgpt_new_question_or_edit()
        print("\n============== Done =========================")

    elif selected_option == 4:
        print("\n============== Option 4 =====================")
        print("╔═════════════════════════════════════╗")
        print("║ 4. Generate a MCQ quiz              ║")
        print("╚═════════════════════════════════════╝")
        generate_mcq_quiz.generate_mcq_quiz()
        print("\n============== Done =========================\n")

    elif selected_option == 5:
        print("\n============== Option 5 =====================")
        print("╔═════════════════════════════════════╗")
        print("║ 5. Exit                             ║")
        print("╚═════════════════════════════════════╝")
        print("Goodbye!")
        print("\n============== Exit =========================")
        sys.exit()

    else:
        helper_functions.logging.error("Invalid option. Please enter a valid number (1-5).")