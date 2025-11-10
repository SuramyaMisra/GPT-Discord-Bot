# GPT-Discord-Bot

A simple Discord bot built in Python that connects ChatGPT to your server through the OpenRouter API.  
It lets users chat with an AI directly inside Discord using clean slash commands.

---

## 📌 About the project
This bot was created as a small side project to learn how to:
- integrate APIs in Python,
- build Discord slash commands,
- and handle environment variables securely using `.env`.

It doesn’t require any paid OpenAI account — everything runs through [OpenRouter](https://openrouter.ai), which gives free access to GPT-based models.

---

## ⚙️ Features
- `/ask` — send a message and get a ChatGPT-style reply  
- `/reset` — clear your conversation memory  
- Per-user chat sessions  
- Logging system that records all activity inside `logs/ai_interactions.log`  
- Uses `.env` to keep all keys private and out of source code

---

