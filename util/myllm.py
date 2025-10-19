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

def build_prompt(conversation, max_n_char, min_n_char):
    return f"""
Summarize the conversation in one sentence that captures the customer’s intent using their own words as closely as possible.

Start with “I” or “We” (first-person view).
Do not mention the bot or emotions.
Keep it under {max_n_char} characters.
If the customer asked to speak to an agent, summarize their intent before that request.
If there are multiple intents, capture the one that still needs resolution.

Conversation:
{conversation}
    """

def get_summary(conversation, max_n_char, min_n_char):
    system_prompt = build_prompt(conversation, max_n_char, min_n_char)
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