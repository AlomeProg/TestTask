# SQL Privilege SELECT Test Plan (Firebird 5.0)

## Описание
Тестовое задание: составить план тестирования SQL-привилегии **SELECT** для работы с таблицами в Firebird 5.0 и реализовать один тесткейс в виде автотеста с использованием [firebird-qa](https://pypi.org/project/firebird-qa/).

## Зависимости
- Python 3.10+
- Firebird 5.0
- Установленные пакеты из `requirements.txt`

## Запуск

``` bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
pytest -v ./tests
```
