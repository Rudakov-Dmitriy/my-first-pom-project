# My First POM Project

[![Run UI Tests](https://github.com/Rudakov-Dmitriy/my-first-pom-project/actions/workflows/run_tests.yml/badge.svg)](https://github.com/Rudakov-Dmitriy/my-first-pom-project/actions/workflows/run_tests.yml)

Автоматизированное тестирование с использованием **Playwright + Pytest + Page Object Model**.

## 🚀 Стек

- Python 3.13
- Playwright 1.61
- Pytest 9.1
- Allure Reports
- Flake8 (PEP 8)
- pytest-xdist (параллельный запуск)
- pytest-rerunfailures (автоперезапуск упавших тестов)
- GitHub Actions (CI/CD)
- Docker

## 📂 Структура проекта
```
my_first_pom_project/
├── .github/
│ └── workflows/
│ └── run_tests.yml # CI/CD
├── pages/ # Page Object Model
│ ├── base_page.py # Базовые методы
│ ├── login_page.py # Страница логина
│ ├── products_page.py # Страница товаров
│ ├── cart_page.py # Страница корзины
│ └── checkout_page.py # Страница оформления
├── tests/ # Тесты
│ ├── conftest.py # Фикстуры и хуки
│ ├── test_login.py # Тесты логина (6)
│ ├── test_cart.py # Тесты корзины (4)
│ └── test_checkout.py # Тесты оформления (4)
├── utils/ # Утилиты
│ └── api_auth.py # API-логин
├── data/ # Тестовые данные
├── Dockerfile # Docker-образ
├── docker-compose.yml # Docker-конфигурация
├── .dockerignore # Исключения для Docker
├── .flake8 # Конфиг линтера
├── config.py # Конфигурация
├── pytest.ini # Настройки pytest
├── requirements.txt # Зависимости
└── README.md
```
## 📊 Тестовые данные

Тестовые данные хранятся в папке `data/` в формате JSON.

Пример `data/users.json`:
```json
{
  "standard_user": {
    "username": "standard_user",
    "password": "secret_sauce",
    "description": "Стандартный пользователь для позитивных тестов"
  }
}
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

# 6. Создаём .env файл из примера
cp .env.example .env
# Заполни своими данными или оставь для SauceDemo

# 7. Запускаем тесты
pytest -v -s

# 8. Запускаем тесты параллельно (быстрее в 2-3 раза)
pytest -v -n auto
```
## 🐳 Docker

```powershell
docker compose build
docker compose up
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

