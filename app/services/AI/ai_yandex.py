from yandex_cloud_ml_sdk import YCloudML

from quotes_project.settings import YANDEXGPT_FOLDER, YANDEXGPT_API_TOKEN


def ask_ai_yandex(question: str) -> str:
    """
    Отправляет вопрос в YandexGPT и возвращает ответ
    """
    try:
        sdk = YCloudML(folder_id=YANDEXGPT_FOLDER, auth=YANDEXGPT_API_TOKEN)
        model = sdk.models.completions("yandexgpt-lite", model_version="latest")
        model = model.configure(temperature=0.2)

        result = model.run(
            [
                {"role": "system", "text": "Отвечай четко по запросу."},
                {"role": "user", "text": question},
            ]
        )

        for alternative in result:
            return alternative.text.strip()

        return "None"

    except Exception as e:
        print("Ошибка YandexGPT:", e)
        return "None"
