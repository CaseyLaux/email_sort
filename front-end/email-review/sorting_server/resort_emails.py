from pymongo import MongoClient
import json
import sys
import subprocess
import os
import test_autoformat
sys.path.append("C:\\Users\\casey\\PycharmProjects\\email_sort\\")

from secrats import ColinGTK

client = MongoClient('localhost', 27017)
db = client[ColinGTK().Account_ID]

collection_string = ColinGTK().user + "re-sorted"
collection = db[collection_string]

def database_pull():
    # Fetch all documents from the collection, but only include the 'email_prompt' and 'completion' fields
    documents = collection.find({}, {"prompt": 1, "completion": 1})

    # Convert MongoDB Cursor to list of dicts
    documents_list = list(documents)

    # Remove the '_id' key from each document
    for document in documents_list:
        document.pop('_id', None)
    
    base_filename = "re-train_gpt_data_prime"
    extension = ".json"
    counter = 0
    filename = base_filename + extension

    # If filename exists, iterate the counter and append it to the filename
    while os.path.exists(filename):
        counter += 1
        filename = "{}_{}{}".format(base_filename, counter, extension)

    # Write the documents to a json file
    with open(filename, 'w') as file:
        file.write(json.dumps(documents_list, indent=4))
    return filename
        




if __name__ == "__main__":
    filename = database_pull()
    subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "./sorting_server/format_data.ps1", filename])
    test_autoformat.autoformat(filename)
    
