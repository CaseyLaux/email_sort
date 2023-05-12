import base64
import openai
import requests

url = 'https://api.openai.com/v1/fine-tunes'
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    # Request successful
    print(response.json())
else:
    # Request failed
    print('Request failed with status code:', response.status_code)






def decode_string(encoded_string):
    # Convert the encoded string to bytes
    encoded_bytes = encoded_string.encode('utf-8')
    
    # Decode the Base64 bytes
    decoded_bytes = base64.b64decode(encoded_bytes)
    
    # Convert the decoded bytes back to a string
    decoded_string = decoded_bytes.decode('utf-8')
    
    return decoded_string

encoded_string = "c2stNHNFd3ZZZ09KaGpOSlRLQW8zRGFUM0JsYmtGSlVrV1V1UjA1eHVsckoxTFk3cHhE"
api_key = decode_string(encoded_string)
openai.api_key = api_key

def upload():
    upload_response = openai.File.create(
        file=open("./email_data_prepared.jsonl", "rb"),
        purpose='fine-tune'
    )
    file_id = upload_response.id
    print(upload_response)
    return upload_response, file_id



print(api_key)
if __name__ =="__main__":
    training_file_id = "file-7cS1Ts3lPoOV6w4rXvEqkS2I"
    encoded_string = "c2stNHNFd3ZZZ09KaGpOSlRLQW8zRGFUM0JsYmtGSlVrV1V1UjA1eHVsckoxTFk3cHhE"
    openai.api_key = decode_string(encoded_string)
    openai api fine_tunes.create -t training_file_id -m Davinci


    #upload_response, file_id = upload()
    #fine_tune_response = openai.FineTune.create(training_file=file_id)


