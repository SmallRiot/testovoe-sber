from langchain.tools import tool
from deposit_db import deposit_db
from rag import rag_qa

@tool
def list_deposit_names() -> str:
    """Возвращает названия всех вкладов через запятую."""
    # Лог в консоль для отладки
    print("\033[92mCalled list_deposit_names()\033[0m")
    return ", ".join([d["name"] for d in deposit_db])

@tool
def recommend_deposits(
    currency: str,
    term_months: int,
    need_replenishment: bool,
    need_partial_withdrawal: bool,
) -> str:
    """
    Подбирает до трёх наиболее подходящих вкладов по параметрам.

    Args:
        currency (str): Валюта ('RUB', 'USD', ...)
        term_months (int): Срок вклада в месяцах.
        need_replenishment (bool): Нужно ли пополнение.
        need_partial_withdrawal (bool): Нужно ли частичное снятие.
    """
    print(f"\033[92mCalled recommend_deposits({currency}, {term_months}, "
          f"{need_replenishment}, {need_partial_withdrawal})\033[0m")
    scored = []
    for d in deposit_db:
        if d["currency"] != currency.upper():
            continue
        # Проверка срока
        if not (d["term_min"] <= term_months <= d["term_max"]):
            continue
        # Начальный вес — ставка
        score = d["rate"]
        # Бонусы за соответствие потребностям
        if d["replenishment"] == need_replenishment:
            score += 1
        if d["partial_withdrawal"] == need_partial_withdrawal:
            score += 1
        scored.append((score, d))

    scored.sort(reverse=True, key=lambda x: x[0])
    if not scored:
        return "К сожалению, подходящих вкладов не найдено."

    lines = ["Рекомендованные вклады:"]
    for _, d in scored[:3]:
        lines.append(
            f"- {d['name']} — {d['rate']}% годовых, "
            f"{'с' if d['replenishment'] else 'без'} пополнения, "
            f"{d['term_min']}-{d['term_max']} мес."
        )
    return "\n".join(lines)

@tool
def calculate_final_amount(
    initial_amount: float,
    rate: float,
    term_months: int
) -> str:
    """
    Рассчитывает сумму на счёте к концу срока (без капитализации).

    Args:
        initial_amount (float): Начальная сумма.
        rate (float): Годовая ставка.
        term_months (int): Срок вклада.
    """
    print(f"\033[92mCalled calculate_final_amount({initial_amount}, {rate}, {term_months})\033[0m")
    final = initial_amount + (initial_amount * rate / 100 * term_months / 12)
    return f"Через {term_months} мес. на счёте будет: {final:.2f} руб."

@tool
def ask_rag_about_deposits(query: str) -> str:
    """
    Возвращает подробную информацию о вкладе по названию через RAG.

    Args:
        query (str): Название вклада или вопрос.
    """
    print(f"\033[92mCalled ask_rag_about_deposits({query})\033[0m")
    return rag_qa.invoke(query)
