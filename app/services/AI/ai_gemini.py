import google.generativeai as genai

from quotes_project.settings import GEMINI_API

genai.configure(api_key=GEMINI_API)


def ask_ai_gemini(question: str) -> str:
    """
    Отправляет вопрос в Gemini и возвращает ответ
    """
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    try:
        response = model.generate_content(question)
    except Exception as e:
        print("Ошибка Gemini:", e)
        return "None"

    return response.text.strip()
