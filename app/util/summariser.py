import os
from util.log_config import get_logger
from util.myllm import get_summary
from dotenv import load_dotenv
from util.load_from_s3 import load_prompt_data

load_dotenv() 

logger = get_logger(__name__)

MIN_N_CHARACTERS = int(os.environ.get('SUMMARISER_MIN_N_CHARACTERS', 10))
MAX_N_CHARACTERS = int(os.environ.get('SUMMARISER_MAN_N_CHARACTERS',150))
AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_S3_OBJECT_KEY = os.environ.get('AWS_S3_PROMPT_OBJECT_KEY')

prompt_template = load_prompt_data(AWS_S3_BUCKET_NAME, AWS_S3_OBJECT_KEY)

def summariser(conversation, max_n_char=MAX_N_CHARACTERS, min_n_char=MIN_N_CHARACTERS):
    try:
        if isinstance(conversation, str):
            conversation_text = conversation
        else:
            conversation_text = "\n".join([f"{item['role'].capitalize()}: {item['content']}" for item in conversation])
        
        # Get final summary from LLM 
        logger.info(f"Request to summarise: {conversation_text} on {max_n_char} - {min_n_char} characters")
        summary, system_prompt, err = get_summary(conversation_text, max_n_char, min_n_char, prompt_template)
        if err:
            logger.error(f"Error in getting summary from LLM: {err}")
            return {"status": "error", "message": err}

        # Return JSON object
        logger.info(f"Query summarised successfully: {summary}")
        return {
            "status": "success",
            "conversation": conversation,
            "summary": summary,
            "max_number_of_characters": max_n_char,
            "min_number_of_characters": min_n_char,
            "system_prompt": system_prompt
        }

    except Exception as e:
        logger.error(f"Unexpected error in summariser: {str(e)}")
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}