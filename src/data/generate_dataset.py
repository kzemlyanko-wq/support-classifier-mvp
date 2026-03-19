import pandas as pd
import requests
import time
import random
import os
import math
from dotenv import load_dotenv
from pathlib import Path
from prompts import PROMPT_GENERATE_TEXT

# Загружаем переменные окружения (для API ключей)
load_dotenv()

# Категории и приоритеты из docs/categories.md
CATEGORIES = ['Payment', 'Technical', 'Delivery', 'Account', 'Other']
PRIORITIES = ['High', 'Medium', 'Low']

# Настройки генерации
TOTAL_TARGET = 500  # Целевое количество строк (минимум 500 по кейсу)
SAMPLES_PER_COMBINATION = math.ceil(TOTAL_TARGET / (len(CATEGORIES) * len(PRIORITIES)))


def call_llm_api(prompt, category, priority):
    """
    Вызывает API нейросети для генерации текста.
    
    TODO: Партнёр должен реализовать эту функцию с реальным API:
    - GigaChat: https://developers.sber.ru/gigachat
    - ChatGPT: https://platform.openai.com/api
    - YandexGPT: https://cloud.yandex.ru/docs/yandexgpt/
    
    Args:
        prompt (str): Промпт для нейросети
        category (str): Категория обращения (для заглушки)
        priority (str): Приоритет (для заглушки)
    
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
        "messages": [
            {"role": "system", "content": "Ты полезный ассистент для генерации данных."},
            {"role": "user", "content": prompt}
        ],
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
    
    # Используем category и priority из параметров
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
    
    # Добавляем ключевые слова по приоритетам
    priority_keywords = {
        'High': ['срочно', 'немедленно', 'быстро', 'ужас', 'катастрофа'],
        'Medium': ['подскажите', 'вопрос', 'помогите', 'не понимаю'],
        'Low': ['спасибо', 'интересно', 'всё хорошо', 'благодарю']
    }
    
    # Добавляем вариативности (опечатки, разные стили)
    texts = []
    for i in range(SAMPLES_PER_COMBINATION):
        base_text = random.choice(templates.get(category, templates['Other']))
        
        # Добавляем ключевые слова по приоритету (20% случаев)
        if random.random() < 0.2:
            keyword = random.choice(priority_keywords.get(priority, []))
            base_text = f"{base_text}, {keyword}!"
        
        # Добавляем немного вариативности
        variations = [
            base_text + "!",
            base_text + ".",
            "Здравствуйте! " + base_text,
            "Помогите! " + base_text,
            base_text + " Уже жду ответа.",
            "Добрый день, " + base_text.lower(),
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
    # Используем промпт из prompts.py
    prompt = PROMPT_GENERATE_TEXT.format(count=count)
    
    # Передаём category и priority в call_llm_api
    texts = call_llm_api(prompt, category, priority)
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
        'empty_texts_percent': (df['text'].isna().sum() / len(df) * 100) if len(df) > 0 else 0,
        'category_distribution': df['category'].value_counts().to_dict(),
        'priority_distribution': df['priority'].value_counts().to_dict(),
        'avg_text_length': df['text'].str.len().mean()
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
    print(f"📈 Строк на комбинацию: {SAMPLES_PER_COMBINATION}")
    print(f"📈 Итого строк: {SAMPLES_PER_COMBINATION * len(CATEGORIES) * len(PRIORITIES)}")
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
    print(f"   Пустых текстов: {stats['empty_texts']} ({stats['empty_texts_percent']:.1f}%)")
    print(f"   Средняя длина текста: {stats['avg_text_length']:.0f} символов")
    print(f"   Распределение по категориям: {stats['category_distribution']}")
    print(f"   Распределение по приоритетам: {stats['priority_distribution']}")
    
    # Используем Path для надёжного пути
    output_path = Path('data/raw_dataset.csv')
    
    # Создаём папку data, если её нет
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем в CSV
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("-" * 50)
    print(f"✅ Сгенерировано {len(df)} строк!")
    print(f"💾 Сохранено в: {output_path.absolute()}")
    
    # Проверка на минимальное требование (500 строк по кейсу)
    if len(df) >= 500:
        print("🎯 Требование кейса выполнено (≥500 строк)!")
    else:
        print("⚠️ Внимание: нужно минимум 500 строк для Показа 1!")
    
    # Проверка на сбалансированность классов (требование из кейса)
    min_category = min(stats['category_distribution'].values())
    max_category = max(stats['category_distribution'].values())
    if max_category / min_category < 1.2:
        print("✅ Классы сбалансированы!")
    else:
        print("⚠️ Внимание: классы несбалансированы!")


if __name__ == '__main__':
    main()