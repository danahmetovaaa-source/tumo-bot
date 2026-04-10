from faq import FAQ


def score_message(text: str) -> dict[str, int]:
    """
    Score each intent by keyword hits.
    Returns {intent_key: score}, sorted descending.
    """
    normalized = text.lower().strip()
    scores: dict[str, int] = {}

    for intent_key, data in FAQ.items():
        if intent_key == "__fallback__":
            continue
        count = sum(1 for kw in data["keywords"] if kw in normalized)
        if count > 0:
            scores[intent_key] = count * data.get("priority", 1)

    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


def get_best_answer(text: str) -> tuple[str, str]:
    """
    Returns (intent_key, answer_text).
    Falls back to __fallback__ if no match.
    """
    scores = score_message(text)

    if not scores:
        return "__fallback__", FAQ["__fallback__"]["answer"]

    best_intent = next(iter(scores))
    return best_intent, FAQ[best_intent]["answer"]


def get_top_answers(text: str, top_n: int = 3) -> list[tuple[str, str, int]]:
    """
    Returns top N (intent_key, answer, score) for debug/logging.
    """
    scores = score_message(text)
    result = []
    for key, score in list(scores.items())[:top_n]:
        result.append((key, FAQ[key]["answer"], score))
    return result


# ── Quick smoke test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        "как записаться в TUMO?",
        "сколько стоит обучение?",
        "какие документы нужны?",
        "когда проходит презентация?",
        "где находится центр?",
        "сколько лет должно быть ребёнку?",
        "как восстановить пароль hubid",
        "что-то непонятное",
    ]

    for msg in tests:
        intent, answer = get_best_answer(msg)
        first_line = answer.split("\n")[0]
        print(f"Q: {msg!r:45s}  →  [{intent}]  {first_line[:60]}")
