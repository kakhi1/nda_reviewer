#!/usr/bin/env python
import sys
import warnings
import sys
import warnings
from tkinter import Tk, filedialog
from nda_reviewer.crew import NdaReviewer

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def get_file_from_user():
    """
    Open a file dialog for the user to select a file.
    """
    # Create a root Tkinter window (hidden)
    root = Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Bring the dialog to the front

    # Open the file dialog and allow user to select a file
    file_path = filedialog.askopenfilename(
        title="Select NDA Document",
        filetypes=[
            ("PDF Files", "*.pdf"),
            ("Word Files", "*.docx"),
            ("All Files", "*.*"),
        ],
    )

    # Close the Tkinter root window
    root.destroy()

    if not file_path:
        raise Exception("No file was selected. Please choose a valid file.")

    return file_path





# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'AI LLMs'
#     }
#     NdaReviewer().crew().kickoff(inputs=inputs)

def run():
    """
    Run the crew with user file input.
    """
    # Create main window
    root = Tk()
    root.title("NDA Reviewer")
    root.geometry("400x200")
    
    def start_review():
        try:
            # Open file picker for user to select a file
            file_path = get_file_from_user()
            if file_path:
                print(f"File selected: {file_path}")
                
                inputs = {
                    "uploaded_file": file_path,
                }
                
                print(f"Inputs being passed to kickoff: {inputs}")
                
                # Close the GUI window before running the crew
                root.destroy()
                
                # Kick off the crew
                crew = NdaReviewer().crew()
                crew.kickoff(inputs=inputs)
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Add welcome text
    from tkinter import Label, Button
    welcome_label = Label(root, text="Welcome to NDA Reviewer\nClick the button below to select a document", pady=20)
    welcome_label.pack()
    
    # Add start button
    start_button = Button(root, text="Choose File and Start Review", command=start_review, pady=10)
    start_button.pack()
    
    # Start the GUI event loop
    root.mainloop()





def train():
    """
    Train the crew for a given number of iterations.
    
    """
    file_path = get_file_from_user()
    inputs = {
        # "topic": "NDA Review",
        "uploaded_file": file_path,  # Ensure this is a string
    }

    try:
        NdaReviewer().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        NdaReviewer().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    file_path = get_file_from_user()
    inputs = {
        # "topic": "NDA Review",
        "uploaded_file": file_path,  # Ensure this is a string
    }
    try:
        NdaReviewer().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


