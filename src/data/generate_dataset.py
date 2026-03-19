import pandas as pd
import requests
import time
import random
import os
from dotenv import load_dotenv

# Загружаем переменные окружения (для API ключей)
load_dotenv()

# Категории и приоритеты из docs/categories.md
CATEGORIES = ['Payment', 'Technical', 'Delivery', 'Account', 'Other']
PRIORITIES = ['High', 'Medium', 'Low']

# Настройки генерации
TOTAL_TARGET = 500  # Целевое количество строк (минимум 500 по кейсу)
SAMPLES_PER_COMBINATION = TOTAL_TARGET // (len(CATEGORIES) * len(PRIORITIES))  # ~33 на комбинацию


def call_llm_api(prompt):
    """
    Вызывает API нейросети для генерации текста.
    
    TODO: Партнёр должен реализовать эту функцию с реальным API:
    - GigaChat: https://developers.sber.ru/gigachat
    - ChatGPT: https://platform.openai.com/api
    - YandexGPT: https://cloud.yandex.ru/docs/yandexgpt/
    
    Args:
        prompt (str): Промпт для нейросети
    
    Returns:
        list: Список сгенерированных текстов
    """
    
    # ============================================
    # ⚠️ ЗАГЛУШКА (MOCK) — заменить на реальное API
    # ============================================
    
    # Пример для GigaChat (раскомментировать и настроить при наличии ключа):
    """
    GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v2/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GIGACHAT_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(GIGACHAT_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()["choices"][0]["message"]["content"]
    
    # Парсим ответ (предполагаем, что каждый текст с новой строки)
    texts = [line.strip() for line in result.split('\n') if line.strip()]
    return texts
    """
    
    # === ТЕКУЩАЯ ЗАГЛУШКА (для тестирования структуры) ===
    print("   ⚠️ Используется заглушка (mock). Партнёр подключит реальное API.")
    
    # Генерируем фейковые данные для проверки структуры
    templates = {
        'Payment': [
            "У меня не проходит оплата картой",
            "Верните деньги за отменённый заказ",
            "Списание произошло дважды",
            "Карта отклоняется при оплате",
            "Не могу оформить возврат средств"
        ],
        'Technical': [
            "Сайт не открывается",
            "Приложение вылетает при запуске",
            "Ошибка 500 на странице",
            "Не работает кнопка оформления",
            "Сервис тормозит очень сильно"
        ],
        'Delivery': [
            "Где мой заказ?",
            "Курьер не приехал вовремя",
            "Посылка задерживается уже неделю",
            "Не могу отследить доставку",
            "Адрес доставки указан неверно"
        ],
        'Account': [
            "Не могу войти в аккаунт",
            "Забыл пароль от личного кабинета",
            "Нужно сменить email в профиле",
            "Аккаунт заблокирован",
            "Не приходит код подтверждения"
        ],
        'Other': [
            "Спасибо за быстрый ответ",
            "Всё понравилось, буду заказывать ещё",
            "Есть вопрос по условиям сервиса",
            "Хочу оставить отзыв",
            "Где найти информацию о компании?"
        ]
    }
    
    # Добавляем вариативности (опечатки, разные стили)
    texts = []
    for i in range(SAMPLES_PER_COMBINATION):
        base_text = random.choice(templates.get(category, templates['Other']))
        
        # Добавляем немного вариативности
        variations = [
            base_text + "!",
            base_text + ".",
            "Здравствуйте! " + base_text,
            "Помогите! " + base_text,
            base_text + " Уже жду ответа.",
        ]
        
        # 20% шанс добавить опечатку (для реалистичности)
        if random.random() < 0.2:
            text = variations[i % len(variations)]
            # Простая "опечатка" - замена буквы
            if len(text) > 5:
                pos = random.randint(1, len(text) - 2)
                text = text[:pos] + text[pos].lower() + text[pos+1:]
        else:
            text = variations[i % len(variations)]
        
        texts.append(text)
    
    return texts


def generate_batch(category, priority, count=10):
    """
    Генерирует batch примеров для одной категории/приоритета.
    
    Args:
        category (str): Категория обращения
        priority (str): Приоритет (High, Medium, Low)
        count (int): Количество примеров
    
    Returns:
        list: Список текстов обращений
    """
    prompt = f"""
    Сгенерируй {count} примеров обращений клиентов на русском языке.
    Категория: {category}
    Приоритет: {priority}
    
    Требования:
    - Тексты от 5 до 50 слов
    - Добавь 1-2 опечатки в 20% случаев
    - Разный стиль (вежливый, нейтральный, возмущенный)
    
    Верни только текст обращений, каждый с новой строки.
    """
    
    texts = call_llm_api(prompt)
    return texts


def validate_data(df):
    """
    Проверяет качество сгенерированных данных.
    
    Args:
        df (pd.DataFrame): Датасет для проверки
    
    Returns:
        dict: Статистика валидации
    """
    stats = {
        'total_rows': len(df),
        'empty_texts': df['text'].isna().sum(),
        'category_distribution': df['category'].value_counts().to_dict(),
        'priority_distribution': df['priority'].value_counts().to_dict()
    }
    return stats


def main():
    """
    Основная функция генерации датасета.
    """
    print("🚀 Запуск генерации датасета...")
    print(f"📊 Цель: {TOTAL_TARGET} строк")
    print(f"📁 Категории: {CATEGORIES}")
    print(f"⚡ Приоритеты: {PRIORITIES}")
    print("-" * 50)
    
    all_data = []
    
    # Генерируем данные для каждой комбинации категория × приоритет
    for category in CATEGORIES:
        for priority in PRIORITIES:
            print(f"🔄 Генерация для {category} - {priority}...")
            texts = generate_batch(category, priority, count=SAMPLES_PER_COMBINATION)
            
            for text in texts:
                all_data.append({
                    'text': text,
                    'category': category,
                    'priority': priority
                })
            
            # Пауза между запросами (чтобы не заблокировали API)
            time.sleep(0.5)
    
    # Создаём DataFrame
    df = pd.DataFrame(all_data)
    
    # Валидация данных
    stats = validate_data(df)
    print("-" * 50)
    print("📈 Статистика:")
    print(f"   Всего строк: {stats['total_rows']}")
    print(f"   Пустых текстов: {stats['empty_texts']}")
    print(f"   Распределение по категориям: {stats['category_distribution']}")
    print(f"   Распределение по приоритетам: {stats['priority_distribution']}")
    
    # Сохраняем в CSV
    output_path = 'data/raw_dataset.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("-" * 50)
    print(f"✅ Сгенерировано {len(df)} строк!")
    print(f"💾 Сохранено в: {output_path}")
    
    # Проверка на минимальное требование (500 строк по кейсу)
    if len(df) >= 500:
        print("🎯 Требование кейса выполнено (≥500 строк)!")
    else:
        print("⚠️ Внимание: нужно минимум 500 строк для Показа 1!")


if __name__ == '__main__':
    main()