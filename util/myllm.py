import os
import openai
from dotenv import load_dotenv

load_dotenv() 
openai_api_key = os.environ.get('SUMMARISER_OPENAI_KEY')
azure_endpoint = os.environ.get('SUMMARISER_OPTIONS_API_BASE')
azure_api_version = os.environ.get('SUMMARISER_OPTIONS_API_VERSION')
openai_model = os.environ.get('SUMMARISER_OPTIONS_CHAT_MODEL_DEPLOYMENT_ID')

client = openai.AzureOpenAI(
    azure_endpoint = azure_endpoint,
    api_version= azure_api_version,
    api_key=openai_api_key
    )

def build_prompt(conversation, max_n_char, min_n_char, prompt_template):
    return prompt_template.format(max_n_char=max_n_char, conversation=conversation, min_n_char=min_n_char)

def get_summary(conversation, max_n_char, min_n_char, prompt_template):
    system_prompt = build_prompt(conversation, max_n_char, min_n_char, prompt_template)
    try:
        response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip(), system_prompt, None
    except Exception as e:
        return None, system_prompt, f"Chat completion API error: {str(e)}"