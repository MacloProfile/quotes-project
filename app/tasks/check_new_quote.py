from celery import shared_task

from app.models.quote import Quote
from app.services.moderation_quote_via_ai import QuoteChecker


@shared_task
def moderate_quote_task(quote_id: int):
    print(f"[CELERY] Запущена модерация цитаты ID={quote_id}")
    try:
        quote_obj = Quote.objects.get(id=quote_id)
        checker = QuoteChecker()
        if quote_obj.status is None:
            ai_ok, ai_comment = checker.check(quote_obj.quote)
            quote_obj.status = ai_ok
            quote_obj.moderation_comment = ai_comment
            quote_obj.save()
    except Quote.DoesNotExist:
        pass
