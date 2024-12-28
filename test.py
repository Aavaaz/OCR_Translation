import requests

# Define the base URL of your Django server
base_url = "http://127.0.0.1:8000/"

# Input data for translation
input_list = ["I am", "Going Home", "Tourist"]
source_lang = "English"
trg_lang = "Hindi"

# Prepare the query parameters
params = {
    'input_list': input_list,
    'source_lang': source_lang,
    'trg_lang': trg_lang
}

# Define the translate endpoint URL (without the 'api/' prefix)
translate_url = base_url + "api/translate/"

# Send GET request to the translate endpoint
response_translate = requests.get(translate_url, params=params)

# Handle the response
if response_translate.status_code == 200:
    print("Translation Endpoint Response:", response_translate.json())  # Expected to print the translation result
else:
    print("Error in 'translate' endpoint:", response_translate.status_code, response_translate.text)
