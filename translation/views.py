from django.http import JsonResponse
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Check if environment variables are loaded correctly
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("OPENAI_API_VERSION")

if not api_key or not endpoint or not api_version:
    raise ValueError("Missing one or more environment variables: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION")

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

# Default Hello endpoint
def hello(request):
    return JsonResponse({'message': 'Hello'})

# Translation endpoint
def translate(request):
    input_list = request.GET.getlist('input_list')
    source_lang = request.GET.get('source_lang')
    trg_lang = request.GET.get('trg_lang')

    if not input_list or not source_lang or not trg_lang:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Define the system prompt for translation
    system_prompt = f"""
    - You are an AI translator. Translate the following list of {source_lang} phrases into {trg_lang}.
    - Return only the translation as a list in Output.

    Example:
    Input: ["Hello", "Good Morning", "Good Night", "How are you?", "Thank you", 
     "Welcome", "Goodbye", "See you", "Take care", "Sorry"]
    source_lang=English
    trg_lang=Hindi
    Output: ['नमस्ते', 'सुप्रभात', 'शुभ रात्रि', 'आप कैसे हैं?', 'धन्यवाद', 'स्वागत है', 'अलविदा', 'फिर मिलेंगे', 'ख्याल रखना', 'माफ़ करना']
    """

    user_prompt = f"Translate these sentences into {trg_lang}: {input_list}"

    # Call the OpenAI API for translation
    try:
        completion = client.chat.completions.create(
            model='oai4o', 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=512,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the translation from the response
        translation = completion.choices[0].message.content.split('`')[0]
        return JsonResponse({'translation': translation}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
