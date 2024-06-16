import requests


def creat_game(class_user, topic):
    prompt = {
        "messages": [
            {
                "text": f"Придумай задачу по теме {topic} для {class_user} класса и напиши ответ число",
                "role": "user"
            }
        ],
        "completionOptions": {
            "stream": False
        },
        "modelUri": "gpt://b1g8h2nqmho77l0cmm7v/yandexgpt-lite"
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN07ueKMUw4VyOKZIbVudE8xaEU6mlGUfXLtMQ"
    }
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()["result"]["alternatives"][0]["message"]["text"].split("\n\n**")
    task = " ".join(result[0].split("\n\n"))
    response_task = "".join("".join(result[1].split(" ")[1].split("**")).split("\n\n"))
    return [task, response_task]
