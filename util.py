# util.py
import os
from openai import OpenAI

from dotenv import load_dotenv

import logging

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing in environment (.env)")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


# Per-user conversation memory (stored in memory for now)
_conversations = {}

# Logging setup
logger = logging.getLogger("util")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/ai_interactions.log")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)


def initialize_conversation_for(user_id):
    """Initialize conversation memory for a user."""
    uid = str(user_id)
    _conversations[uid] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


def _get_conversation(user_id):
    uid = str(user_id)
    if uid not in _conversations:
        initialize_conversation_for(uid)
    return _conversations[uid]


def reset_conversation(user_id):
    """Reset a user's conversation memory."""
    uid = str(user_id)
    _conversations.pop(uid, None)
    initialize_conversation_for(uid)


def get_response(prompt: str, user_id):
    """Send user prompt to OpenAI and return the assistant's reply."""
    conv = _get_conversation(user_id)
    conv.append({"role": "user", "content": prompt})

    try:
        # this whole block must be indented by four spaces
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conv,
            temperature=0.7,
            max_tokens=512,
        )
    except Exception as e:
        # same indentation level as the 'try' block
        logger.exception("OpenAI API call failed")
        return f"OpenAI error: {e}"

    assistant_msg = response.choices[0].message
    conv.append({"role": assistant_msg.role, "content": assistant_msg.content})

    usage = getattr(response, "usage", None)
    logger.info("user=%s prompt=%s tokens=%s", user_id, prompt[:100], usage)
    return assistant_msg.content.strip()

