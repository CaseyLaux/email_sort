SiemlessEmail
This project is an email client that will pull emails from multiple addresses and store them in one client. During this import process there will be a fine tunned gpt model that rates and classifies.


The data flow for pulling the emails is as follows

|pullemails.py| >>emaildata>> >>accountdata>> |mongoDB[username][emails]| >>emaildata>> |gptapi| >>BS_emaildata>> |mongoDB[username][bot_sorted]|

