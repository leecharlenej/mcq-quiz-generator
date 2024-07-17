# ===========================================================================
# Initialization
# ===========================================================================

import openai
import pandas as pd
import re
import textwrap

import helper_functions

# ===========================================================================
# Function: ChatGPT prompt
# ===========================================================================

def chat_with_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o",  # Update the model to the current version
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

# ===========================================================================
# Function: Main
# ===========================================================================

# Main function
def chatgpt_new_question_or_edit():

  mcq_quiz_db_file_path, quiz_df, quiz_headers, quiz_topics, quiz_last_qn_id = chatgpt_admin()

  ############### Filter current question database based on topic
  # User to choose topic
  print("\nChoose topic number: ")
  for i, topic in enumerate(quiz_topics):
     print(f"{i+1}. {topic}")

  # User to choose topic number
  topic_num = int(helper_functions.user_input("\nOption: ")) - 1

  print('\n-------------- Question database -------------')
  # Check if topic number is within the range, create a copy of filtered dataframe and add new column for selection numbers.
  if topic_num in range(len(quiz_topics)):
    selected_topic_df = quiz_df[quiz_df["Topic"] == quiz_topics[topic_num]].copy()
    selected_topic_ID = selected_topic_df.index.tolist()

    for row in selected_topic_df.itertuples():
      print(f"{row.Index}. {row.Question}")

    # User to choose question number
    while True:
        try:
            question_num = int(helper_functions.user_input("\nChoose question number: "))
            if question_num in selected_topic_ID:
                break
            else:
                helper_functions.logging.error("Invalid number. Please enter a valid number from list above.")
        except ValueError:
            helper_functions.logging.error("Please enter a valid number.")

    print('\n-------------- Review question ---------------')
    gpt_question = selected_topic_df.loc[question_num].copy()
    gpt_question_string = ""

    for key, value in gpt_question.items():

        if key in {"Type", "Image", "Image file"}:
          continue
        else:
          print(f"{helper_functions.coloured_text('cyan', key)}: {value}")
          if key not in {"ID", "Topic", "Sub-topic"}:
            gpt_question_string += f"{key}: {value}\n"

    ############### ChatGPT questions: Rephrase question or come up with similar question
    # ChatGPT menu
    print('\n-------------- ChatGPT assistant -------------')
    gpt_output = chatgpt_assistant(gpt_question_string)
    print(gpt_output)

    print('\n-------------- Add to database ---------------')
    add_to_quiz_db = helper_functions.user_input('Add to quiz database? (Y/N) [Yes/No]: ').lower()

    if add_to_quiz_db == 'y' or add_to_quiz_db == 'yes':
      gpt_question["Type"] = "ChatGPT"
      question_data = extract_question_options_answer(gpt_output)
      print(question_data)

      for key, value in question_data.items():
        if key == 'Options':
          for option_key, option_value in value.items():
            gpt_question[f"{option_key}"] = option_value
        else:
          gpt_question[key] = value

      print("\n")
      for key, value in gpt_question.items():
          print(f"{helper_functions.coloured_text('cyan', key)}: {value}")

      # Add question to CSV file.
      helper_functions.write_question_to_file(mcq_quiz_db_file_path, gpt_question)

# ===========================================================================
# Function: Admin to input OpenAI API key and read CSV into dataframe
# ===========================================================================

def chatgpt_admin():
  # Admin to input the OpenAI API key.
  openai.api_key = helper_functions.user_input('Enter your OpenAI API key: ')

  ############### Current question database
  # Access the quiz_db.csv file
  mcq_quiz_folder_path = helper_functions.user_input("Enter path of quiz folder (E.g. G:\My Drive\quiz_folder): ")
  mcq_quiz_db_file_path = mcq_quiz_folder_path + "/quiz_db.csv"
  quiz_df = pd.read_csv(mcq_quiz_db_file_path)

  # Load quiz_db.csv to get topics and create an edited question dictionary.
  quiz_df = pd.read_csv(mcq_quiz_db_file_path, keep_default_na=False)

  # Get headers, last question ID, topics from quiz database.
  quiz_headers = quiz_df.columns
  quiz_topics = quiz_df["Topic"].unique()
  quiz_last_qn_id = quiz_df['ID'].iloc[-1]

  return mcq_quiz_db_file_path, quiz_df, quiz_headers, quiz_topics, quiz_last_qn_id

# ===========================================================================
# Function: ChatGPT assistant
# ===========================================================================

def chatgpt_assistant(selected_question_string):
  options = {1: 'ChatGPT to rephrase question.',
             2: 'ChatGPT to come up with similar question.'}

  print('Choose an option:')
  for i in range(len(options)):
      print(f'{i+1}. {options[i+1]}')

  # Selected question to ChatGPT
  selected_option = int(helper_functions.user_input('\nOption: '))

  if selected_option == 1:
    print('\n-------------- Rephrased question ------------')
    rephrase_question_prompt = "Please rephrase the entire following question and options (Options need not have the same idea and can be completely new.), and output in the same format:\n" + selected_question_string
    gpt_output = chat_with_gpt(rephrase_question_prompt)

  elif selected_option == 2:
    print('\n-------------- Similar question --------------')
    similar_question_prompt = "Please create a completely new MCQ question, testing the same concept as the following question, and output in the same format:\n" + selected_question_string
    gpt_output = chat_with_gpt(similar_question_prompt)

  return gpt_output


# ===========================================================================
# Function: ChatGPT output
# ===========================================================================

def extract_question_options_answer(data):
    
    # Regex pattern to extract the question, multiple options, and the answer
    pattern = r"""
    Question:\s+(.*?)\n       # Capture the question
    (                         # Start of the group for options
      (?:Option\d+:\s+.*?\n)+ # Non-capturing group for one or more options
    )                         # End of the group for options
    Answer:\s+(.*)            # Capture the answer
    """

    # Perform regex search with verbose mode for multiline with comments
    match = re.search(pattern, data, re.VERBOSE)

    if match:
        question = match.group(1)
        options_block = match.group(2)  # This contains all options as a single block
        answer = match.group(3)

        # Split the options block into individual options
        options = re.findall(r"Option\d+:\s+(.*?)\n", options_block)

        # Organize data into a dictionary
        question_data = {
            "Question": question,
            "Options": {f"Option{idx+1}": option for idx, option in enumerate(options)},
            "Answer": answer
        }
        return question_data
    else:
        return "No match found."


# ===========================================================================
# Test mode
# ===========================================================================
def test(mode):
    if mode == 1:
      chatgpt_new_question_or_edit()

    elif mode == 2:
      gpt_output = """Question: What is the server IP for the domain comp.nus.edu.sg?
Option1: MainServer.comp.nus.edu.sg
Option2: 192.168.0.1
Option3: 45.60.35.225
Option4: Unknown
Answer: 45.60.35.225"""
      question_data = extract_question_options_answer(gpt_output)
      print(question_data)

if __name__ == "__main__":
    test(0) # 0 for no test