import os
from mistralai import Mistral
from dotenv import load_dotenv


mistral_api_key = os.getenv("MISTRAL_TOKEN")
model = "mistral-large-latest"

def get_question_prompt(topic: str) -> str:
    question_prompt = f"Придумай вопрос для программы “Поле чудес” на тему “{topic}”. В твоем ответе должен быть только вопрос, без пояснений. Ответом должно быть одно слово без пробелов"
    return question_prompt


def get_answer_prompt(question: str) -> str:
    answer_prompt = f"Дай ответ на следующий вопрос одним словом, без пояснений и прочисх символов, кроме букв. Вопрос: {question}"
    return answer_prompt


def get_question_with_answer(topic: str) -> tuple[str, str]:
    client = Mistral(api_key=mistral_api_key)
    question_prompt = get_question_prompt(topic)
    chat_question = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": question_prompt,
        },
    ]
    )
    question = chat_question.choices[0].message.content
    answer_prompt = get_answer_prompt(question)
    chat_answer = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": answer_prompt,
        },
    ]
    )
    answer = chat_answer.choices[0].message.content
    return question, answer.upper()


