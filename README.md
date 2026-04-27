# Sprint_7

API tests for Yandex Scooter service using `pytest`, `requests`, and `allure`.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Tests

```bash
pytest
```

Allure raw results are saved to `target/allure-results` by `pytest.ini`.

## Build Allure Report

```bash
allure generate target/allure-results -o target/allure-report --clean
```

Open report:

```bash
allure open target/allure-report
```
