import telebot
import requests

bot_token = "8913794611:AAHccuH3dguaPZ9zp92MyjX0KlWYihiLyfs"
convert_key = "aff4a61cc193542300bcffe8"

bot = telebot.TeleBot(bot_token)


def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{convert_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        rates = data["conversion_rates"]
        if target_currency in rates:
            return rates[target_currency]
        else:
            return None
    else:
        return None


@bot.message_handler(commands=["convert"])
def convert_currency(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "Please write like this: /convert 100 USD KZT")
            return
            
        _, amount, base_currency, target_currency = parts
        amount = float(amount)
        
        exchange_rate = get_exchange_rate(base_currency.upper(), target_currency.upper())
        
        if exchange_rate:
            converted_amount = amount * exchange_rate
            bot.reply_to(message, f"{amount} {base_currency.upper()} is {converted_amount} {target_currency.upper()}")
        else:
            bot.reply_to(message, "Error: no such currency or API error")
            
    except ValueError:
        bot.reply_to(message, "Please write like this: /convert 100 USD KZT")
    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Unknown command. Please use /convert")


if __name__ == "__main__":
    bot.polling()