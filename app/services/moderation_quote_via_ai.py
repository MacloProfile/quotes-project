from app.services.AI.ai_gemini import ask_ai_gemini
from app.services.AI.ai_yandex import ask_ai_yandex
from quotes_project.settings import YANDEXGPT_FOLDER, YANDEXGPT_API_TOKEN, GEMINI_API

class QuoteChecker:
    """
    Проверяет цитату:
      1. По локальному blacklist
      2. Через ИИ (внешний метод check_quote_ai)
    """

    def __init__(self):
        self.blacklist = {
            "госизмена", "экстремизм", "мятеж", "сепаратизм", "подрыв"
        }

    def check_blacklist(self, quote: str) -> bool:
        """Проверка по списку запрещённых слов."""
        text = quote.lower()
        return any(bad_word in text for bad_word in self.blacklist)

    def check(self, quote: str, source: str) -> tuple[bool, str] | bool:
        prompt = (
            f"Проверь цитату: «{quote}» и название источника «{source}»"
            "Если она подходит для публикации, ответь 'Да'. "
            "Если цитата сомнительная, запрещённая, содержит ненормативную лексику, является случайным набором букв или символов, ответь 'Нет'."
            "Отвечай ТОЛЬКО Да или Нет! Это важно. Только да или нет."
            "Примеры твоего ответа:"
            "1. Запрос: Проверь цитату: «Всегда очень тягостно новыми глазами увидеть то, с чем успел так или иначе сжиться» и название источника «Френсис Скотт Фицджеральд, 'Великий Гэтсби'». Твой ответ: Да"
            "2. Запрос: Проверь цитату: «Ыьышлвььл ьвыльв» и название источника «альывьла». Твой ответ: Нет."
            "Отвечай ТОЛЬКО Да или Нет, не пиши любой текст, кроме слов да или нет."
        )

        if self.check_blacklist(quote):
            return False, "🚫 Цитата содержит запрещённые слова."

        ai_response = "none"

        if GEMINI_API != "":
            ai_response = ask_ai_gemini(prompt).strip().split()[0].lower()
            print(f"[GEMINI] {ai_response}, prompt - {prompt}")
        if YANDEXGPT_API_TOKEN != "" and YANDEXGPT_FOLDER != "" and ai_response == "none":
            ai_response = ask_ai_yandex(prompt).strip().split()[0].lower()
            print(f"[YANDEXGPT] {ai_response}, prompt - {prompt}")

        if ai_response == "да":
            return True, "✅ Цитата прошла модерацию."
        else:
            return False, "⚠️ Цитата отклонена ИИ и отправлена на ручную модерацию."
