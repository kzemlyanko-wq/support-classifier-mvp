# Классификатор обращений службы поддержки

## Описание

ML-сервис для автоматической сортировки заявок поддержки по категориям и приоритетам.

Проект разработан в рамках учебного кейса «Классификатор обращений для автоматизации службы поддержки».

## Стек

- **Python 3.10+**
- **FastAPI** (Backend)
- **Scikit-learn** (ML)
- **Pandas, NumPy** (Data Processing)
- **Jupyter** (EDA)

## Установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/kzemlyanko-wq/support-classifier-mvp.git
cd support-classifier-mvp

# 2. Создайте виртуальное окружение
python -m venv venv

# 3. Активируйте окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Установите зависимости
pip install -r requirements.txt

## Структура проекта

support-classifier-mvp/
│
├── data/                      # Датасеты (CSV, JSON)
│   ├── .gitkeep
│   ├── sample_dataset.csv     # Тестовый датасет (10 строк)
│   └── dataset.csv            # Полный датасет (500-1000 строк)
│
├── docs/                      # Документация
│   └── categories.md          # Категории и правила приоритетов
│
├── notebooks/                 # Jupyter ноутбуки (EDA, анализ)
│   └── 01_eda.ipynb           # Разведочный анализ данных
│
├── src/
│   ├── data/                  # Скрипты для работы с данными
│   │   └── generate_prompts.py    # Промпт для генерации данных
│   ├── ml/                    # ML модели и предобработка
│   ├── api/                   # FastAPI код
│   └── frontend/              # Интерфейс (Streamlit / Telegram)
│
├── tests/                     # Тесты
│
├── .gitignore                 # Git ignore правила
├── requirements.txt           # Python зависимости
└── README.md                  # Этот файл

## Команда
- **Землянко Кирилл**
- **Роман Подкопаев**