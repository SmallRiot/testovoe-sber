from typing import Dict, Any, List

deposit_db: List[Dict[str, Any]] = [
    {
        "name": "Лучший %",
        "currency": "RUB",
        "rate": 18.0,
        "term_min": 1,
        "term_max": 36,
        "replenishment": False,
        "partial_withdrawal": False,
        "description": (
            "Максимальная ставка при размещении новых денег на 4-5 месяцев "
            "и выплате процентов в конце срока."
        ),
    },
    {
        "name": "Накопительный счёт",
        "currency": "RUB",
        "rate": 18.0,
        "term_min": 0,
        "term_max": 0,
        "replenishment": True,
        "partial_withdrawal": True,
        "description": (
            "Проценты на ежедневный остаток. До 18% годовых при выполнении условий "
            "(СберПрайм, траты, первый раз)."
        ),
    },
    {
        "name": "СберВклад",
        "currency": "RUB",
        "rate": 20.0,
        "term_min": 1,
        "term_max": 36,
        "replenishment": True,
        "partial_withdrawal": False,
        "description": (
            "Максимальная ставка при открытии онлайн, срок 4-5 месяцев, выплаты в конце "
            "срока и надбавки (СберПрайм, зарплата, остатки)."
        ),
    },
]

