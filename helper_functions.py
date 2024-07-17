# ===========================================================================
# Initialization
# ===========================================================================

import os
import time
import pandas as pd

# ===========================================================================
# Function: User input and error logging
# ===========================================================================

# To be included in every file.
from colorama import Fore, Style, init

prompt_colour = Fore.GREEN

def user_input(message):
    return input(f"{prompt_colour}{message}{Style.RESET_ALL}")

def coloured_text(colour, message):
    prompt_colour = ''

    if colour == "green":
        prompt_colour = Fore.GREEN
    elif colour == "cyan":
        prompt_colour = Fore.CYAN

    return (f"{prompt_colour}{message}{Style.RESET_ALL}")

import logging
init(autoreset=True)
logging.basicConfig(level=logging.ERROR, format=f"\n{Fore.RED}%(levelname)s: %(message)s{Style.RESET_ALL}")

# ===========================================================================
# Function: Check file accessibility and write to file
# ===========================================================================

def check_file_accessibility(file_path):
    try:
        # Attempt to open the file in read mode. If able to open, close immediately.
        with open(file_path, 'r+') as file:
            pass
        return True
    except IOError as e:
        print(f"Error: {e}")
        return False
    
def write_question_to_file(file_path, to_add):
    if check_file_accessibility(file_path):

        if isinstance(to_add, pd.Series):
            to_add = to_add.to_frame().T
            to_add.to_csv(file_path, mode='a', header=False, index=False)
        
        elif isinstance(to_add, list):
            new_data_df = pd.DataFrame(to_add)
            new_data_df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        print("Failed to update. Database CSV may be opened in another program.")
        try_again = input("Close the file and try again? (Y/N) [Yes/No] ").lower()
        if try_again == 'y' or try_again == 'yes':
            write_question_to_file(file_path, to_add)
        else:
            print("Database not updated.")
            return