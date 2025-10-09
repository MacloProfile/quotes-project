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

    def check(self, quote: str) -> tuple[bool, str] | bool:
        prompt = (
            f"Проверь цитату: «{quote}». "
            "Если она достоверна и подходит для публикации, ответь 'Да'. "
            "Если цитата сомнительная, запрещённая, содержит ненормативную лексику и не является случайным набором символов и тп, ответь 'Нет'."
            "Отвечай ТОЛЬКО Да или Нет"
        )

        if self.check_blacklist(quote):
            return False, "🚫 Цитата содержит запрещённые слова."

        ai_response = ask_ai_gemini(prompt).strip().lower()

        print(f"[GEMINI] {ai_response}, prompt - {prompt}")

        if ai_response == "да":
            return True, "✅ Цитата прошла модерацию."
        else:
            return False, "⚠️ Цитата отклонена ИИ и отправлена на ручную модерацию."
