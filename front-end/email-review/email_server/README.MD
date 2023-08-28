This is the sorting server directory. It handles requests from the front end.
App.py does the magic of taking the output from EmailViewer and alters the emails.
    App.py currently is made to add the classification and rating from the front end to the email jsons. It can also delete the emails if there is enough email of that type.
email_indexer.py indexes the unsorted and sorted emails into the index.json in their respective directories.
