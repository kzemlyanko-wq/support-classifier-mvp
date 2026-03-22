# Классификатор обращений службы поддержки

## Команда
- **Землянко Кирилл**
- **Роман Подкопаев**

## Описание

ML-сервис для автоматической сортировки заявок поддержки по категориям и приоритетам.

Проект разработан в рамках учебного кейса «Классификатор обращений для автоматизации службы поддержки».

## Стек

- **Python 3.10+**
- **FastAPI** (Backend)
- **Scikit-learn** (ML)
- **Pandas, NumPy** (Data Processing)
- **Jupyter** (EDA)

## Структура проекта

```
support-classifier-mvp/
│
├── .env.example                # Шаблон, который нужно переименовать в .env и положить свои ключи
├── .gitignore                  # Правила игнорирования
├── README.md                   # Документация проекта
├── requirements.txt            # Python зависимости
│
├── data/                       # Датасеты
│   ├── .gitkeep                # Заглушка для Git
│   ├── sample_dataset.csv      # Тестовый (10 строк)
│   └── raw_dataset.csv         # Основной (510 строк)
│
├── docs/                       # Документация
│   └── categories.md           # Категории и приоритеты
│
├── notebooks/                  # Jupyter ноутбуки (EDA)
│   └── (пока пусто)            # Будет 01_eda.ipynb
│
├── src/                        # Исходный код
│   │
│   ├── data/                   # Скрипты для работы с данными
│   │   ├── prompts.py          # Промпты
│   │   ├── generate_dataset.py # Скрипт генерации
│   │
│   ├── ml/                     # ML модели
│   │   └── (пока пусто)        # train_baseline.py
│   │
│   ├── api/                    # FastAPI код
│   │   └── (пока пусто)        # Будет main.py
│   │
│   └── frontend/               # Интерфейс
│       └── (пока пусто)        # Будет Streamlit/Telegram
│
├── tests/                      # Тесты
│   └── (пока пусто)            # Будут тесты API
│
└── venv/                       # Виртуальное окружение (НЕ в Git)
```

## Установка

## 1. Клонируйте репозиторий
git clone https://github.com/kzemlyanko-wq/support-classifier-mvp.git

cd support-classifier-mvp

## 2. Создайте виртуальное окружение
python -m venv venv

## 3. Активируйте окружение
## Windows:
venv\Scripts\activate
## Linux/Mac:
source venv/bin/activate

## 4. Установите зависимости
pip install -r requirements.txt
