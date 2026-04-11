from groq import Groq
from config import GROQ_KEY

client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
Ты — помощник поддержки TUMO Astana.
Отвечай только на вопросы связанные с TUMO Astana.
Отвечай на том языке на котором пишет пользователь.
Будь кратким и дружелюбным.

ОБЩЕЕ:
- TUMO — бесплатный центр для подростков 12–18 лет
- Astana Hub, павильон 4.6
- Сайт: https://astana.tumo.kz
- Email: info.astana@tumo.kz

ЗАПИСЬ:
- Через https://astana.tumo.kz/enroll-now/
- Нужен HubID на astanahub.com
- Регистрация не гарантирует зачисление

РАСПИСАНИЕ:
- 2 раза в неделю: Пн/Чт или Вт/Пт
- Слоты: 10:30, 14:30, 16:30

ДОКУМЕНТЫ:
- Удостоверение родителя + свидетельство о рождении ребёнка
"""

conversation_history: dict[int, list] = {}


def get_ai_response(user_id: int, user_message: str) -> str:
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })

    history = conversation_history[user_id][-10:]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
        max_tokens=500,
        temperature=0.7
    )

    answer = response.choices[0].message.content

    conversation_history[user_id].append({
        "role": "assistant",
        "content": answer
    })

    return answer