# Telegram-ukassa-bot

Это пример интеграции telegram bot + [Юкасса](https://yookassa.ru/docs) + [Юкасса SDK](https://github.com/yoomoney/yookassa-sdk-python)


## Настройка ukassa
1. Создать тестовый магазин
2. В bot settings -> payments у BotFather настроить **LIVE** Юкассу, указав `shopId` тестового магазина
3. При тестировании бота использовать эти [карты](https://yookassa.ru/developers/using-api/testing#test-bank-card-success). После оплаты транзакция появится в личном кабинете.
4. 



## Запуск бота локально

### 1. Создать .env файл
```dotenv
# telegram
TELEGRAM_TOKEN=<bot_token>

# ukassa
PROVIDER_TOKEN=<provider_token> # можно взять у BotFather, bot settings
UKASSA_SECRET_KEY=<secret_key> # в админке Юкассы
SHOP_ID=<shop_id> # в админке Юкассы
```

### 2. 
```bash
python run_pooling.py
```
