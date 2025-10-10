from app.services.AI.ai_gemini import ask_ai_gemini


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
            "Отвечай ТОЛЬКО Да или Нет"
            "Примеры твоего ответа:"
            "1. Запрос: Проверь цитату: «Всегда очень тягостно новыми глазами увидеть то, с чем успел так или иначе сжиться» и название источника «Френсис Скотт Фицджеральд, 'Великий Гэтсби'». Твой ответ: Да"
            "2. Запрос: Проверь цитату: «Ыьышлвььл ьвыльв» и название источника «альывьла». Твой ответ: Нет"
        )

        if self.check_blacklist(quote):
            return False, "🚫 Цитата содержит запрещённые слова."

        ai_response = ask_ai_gemini(prompt).strip().lower()

        print(f"[GEMINI] {ai_response}, prompt - {prompt}")

        if ai_response == "да":
            return True, "✅ Цитата прошла модерацию."
        else:
            return False, "⚠️ Цитата отклонена ИИ и отправлена на ручную модерацию."
