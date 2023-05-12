import os
import json




def index_emails():
    # Set the email_directory to an absolute path
    email_directory = os.path.abspath('front-end/email-review/public/human_sorted/')
    print(os.getcwd())
    # Make sure the directory exists
    if not os.path.exists(email_directory):
        print(f"The 'human_sorted' directory does not exist at {email_directory}")
        exit(1)

    # List all files in the email directory
    files = os.listdir(email_directory)

    # Filter out only the JSON files
    email_files = [file for file in files if file.endswith('json')]

# Write the array of email filenames to index.json
    with open(os.path.join(email_directory, 'index.json'), 'w') as index_file:
        print(email_files)
        json.dump(email_files, index_file)

    print(f"index.json has been created in the {email_directory} directory.")
if __name__ == "__main__":
    index_emails()

