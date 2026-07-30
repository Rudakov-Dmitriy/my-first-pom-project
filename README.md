# My First POM Project

[![Run UI Tests](https://github.com/Rudakov-Dmitriy/my-first-pom-project/actions/workflows/run_tests.yml/badge.svg)](https://github.com/Rudakov-Dmitriy/my-first-pom-project/actions/workflows/run_tests.yml)

Автоматизированное тестирование с использованием **Playwright + Pytest + Page Object Model**.

## 🚀 Стек

- Python 3.13
- Playwright 1.61
- Pytest 9.1
- Allure Reports
- Flake8 (PEP 8)
- GitHub Actions (CI/CD)

## 📂 Структура проекта
```
my_first_pom_project/
├── pages/ # Page Object Model
│ ├── base_page.py # Базовые методы (click, fill, ожидания)
│ ├── login_page.py # Страница логина SauceDemo
│ └── products_page.py # Страница товаров
├── tests/ # Тесты
│ ├── conftest.py # Фикстуры и хук скриншотов
│ └── test_login.py # Тесты логина (6 тестов)
├── utils/ # Утилиты (API-хелперы)
├── data/ # Тестовые данные
├── config.py # Конфигурация (из .env)
├── pytest.ini # Настройки pytest
└── requirements.txt # Зависимости
```
## ⚙️ Быстрый старт

```powershell
# 1. Клонируем репозиторий
git clone https://github.com/Rudakov-Dmitriy/my-first-pom-project.git
cd my-first-pom-project

# 2. Создаём виртуальное окружение
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Проверяем качество кода
flake8 .

# 5. Устанавливаем браузеры
playwright install

# 6. Создаём .env файл
# Добавь свои LOGIN, PASSWORD, BASE_URL

# 7. Запускаем тесты
pytest -v -s
```

## 📊 Allure-отчёт

📊 [Открыть отчёт](https://rudakov-dmitriy.github.io/my-first-pom-project/)

```powershell
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## 🔄 CI/CD
Тесты автоматически запускаются при каждом пуше в main через GitHub Actions.

Статус последнего запуска показан выше в бейдже.

## 📸 Скриншоты
При падении теста автоматически создаётся скриншот в папке `screenshots/` и прикрепляется к Allure-отчёту.

