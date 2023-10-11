from pymongo import MongoClient
import json
import sys
import subprocess
import os
import test_autoformat
import openai
sys.path.append("C:\\Users\\casey\\PycharmProjects\\email_sort")





def resort_emails(username):
    
    client = MongoClient('localhost', 27017)
    db = client[username]
    

    def delete_documents(ids_to_delete):
        csDB = client["cold_storage"]
        resortedCS_collection = csDB["re-sorted"]
        for id in ids_to_delete:
            document = collection.find_one({"_id": id})
            resortedCS_collection.insert_one(document)
            print(id)
            collection.delete_one({"_id": id})

    collection_string = "re-sorted"
    collection = db[collection_string]

    def database_pull():

        # Fetch all documents from the collection, but only include the 'email_prompt' and 'completion' fields
        documents = collection.find({}, {"prompt": 1, "completion": 1, "_id": 1})

        # Convert MongoDB Cursor to list of dicts
        documents_list = list(documents)
        ids_to_delete = [document['_id'] for document in documents_list]
        if documents_list == []:
            exit(print("No documents found in collection"))
        
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
        return filename, ids_to_delete

    filename, deleteData = database_pull()
    test_autoformat.autoformat(filename)
    openai.api_key = "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"
    train_data = filename.replace(".json", "_prepared.jsonl")
    path = os.getcwd()

    if not os.path.exists(train_data):
        train_data = filename.replace(".json", "_prepared_train.jsonl")
        valid_data = filename.replace(".json", "_prepared_valid.jsonl")
        openai.File.create(
            file=open(train_data, "rb"),
            purpose='fine-tune'
        )
        openai.File.create(
            file=open(valid_data, "rb"),
            purpose='fine-tune'
        )
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "./front-end/email-review/sorting_server/train_model.ps1", train_data, valid_data])

    openai.File.create(
        file=open(train_data, "rb"),
        purpose='fine-tune'
    )
    
    subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "./front-end/email-review/sorting_server/train_model.ps1", train_data])
    delete_documents(deleteData)
if __name__ == "__main__":
    resort_emails()
    print("Done")