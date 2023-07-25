import json
import requests
import pytz
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime
from geopy.exc import GeocoderTimedOut
from timezonefinder import TimezoneFinder

class IpBot:
    def __init__(self, bot_token, ipapi_api_key, weather_api_key):
        self.bot_token = bot_token
        self.ipapi_api_key = ipapi_api_key
        self.weather_api_key = weather_api_key
        self.bot = Bot(token=self.bot_token, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot)
        self.markup = InlineKeyboardMarkup(resize_keyboard=True).add(
            InlineKeyboardButton("IP сервера", callback_data="current_ip"),
            InlineKeyboardButton("ввести IP", callback_data="enter_ip"),
            InlineKeyboardButton("хочу собаку", callback_data="want_dog"),
            InlineKeyboardButton("Bitcoin курс", callback_data="bitcoin"),
            InlineKeyboardButton("Ethereum курс", callback_data="ethereum"),
            InlineKeyboardButton("О боте", callback_data="help")
        )
        self.dp.register_message_handler(self.start_command, commands=["start"])
        self.dp.callback_query_handler(lambda query: query.data in ["current_ip", "enter_ip", "want_dog", "bitcoin", "ethereum", "help"])(self.handle_callback_query)
        self.dp.message_handler(content_types=types.ContentType.TEXT)(self.handle_ip_address)
        # настройка ведения журнала ERROR
        self.logger = logging.getLogger("error")
        self.logger.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    async def send_menu(self, chat_id):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(
            types.InlineKeyboardButton("IP сервера", callback_data="current_ip"),
            types.InlineKeyboardButton("ввести IP", callback_data="enter_ip"),
            types.InlineKeyboardButton("хочу собаку", callback_data="want_dog"),
            types.InlineKeyboardButton("Bitcoin курс", callback_data="bitcoin"),
            types.InlineKeyboardButton("Ethereum курс", callback_data="ethereum"),
            types.InlineKeyboardButton("О боте", callback_data="help"),
        )
        await self.bot.send_message(chat_id, "<i>Можете снова выбрать одну из опций:</i>", reply_markup=keyboard)

    async def start_command(self, message: types.Message):
        description = "Привет, " + message.from_user.first_name + "\n" \
                      " Я бот, который может:\n" \
                      "- Показать текущий IP-адрес сервера\n" \
                      "- Получить информацию о местоположении по IP-адресу\n" \
                      "- Показать текущее время в определенном месте\n" \
                      "- Получить информацию о погоде в определенном месте\n" \
                      "- Показать фотографию собаки\n" \
                      "- Показать информацию о курсе Bitcoin и Ethereum\n" \
                      "Выберите одну из опций ниже:"
        await message.answer(description, reply_markup=self.markup)

    async def handle_callback_query(self, callback_query: CallbackQuery):
        symbol = callback_query.data
        if symbol == "enter_ip":
            await self.bot.send_message(callback_query.message.chat.id, "Введите IP-адрес:")
        elif symbol == "current_ip":
            ip_address = self.get_public_ip()
            location_info = self.get_location_info(ip_address)
            if location_info is not None:
                await callback_query.message.answer(f"Текущий IP-адрес: {ip_address}")
                reply_message = self.generate_location_info_reply(location_info)
                await callback_query.message.answer(reply_message)
                await self.send_current_time(callback_query.message.chat.id, location_info["latitude"], location_info["longitude"])
                await self.send_weather_info(callback_query.message.chat.id, location_info["latitude"], location_info["longitude"])
            else:
                await callback_query.message.answer("Не удалось получить информацию о местоположении")
        elif symbol == "want_dog":
            await self.send_dog_picture(callback_query.message.chat.id)
        elif symbol == "bitcoin":
            await self.send_crypto_price(callback_query.message.chat.id, "bitcoin")
        elif symbol == "ethereum":
            await self.send_crypto_price(callback_query.message.chat.id, "ethereum")
        elif symbol == "help":
            await self.send_help_info(callback_query.message.chat.id)
        if symbol != "enter_ip":
            await self.send_menu(callback_query.message.chat.id)
            await callback_query.answer()

    async def handle_ip_address(self, message: types.Message):
        ip_address = message.text
        location_info = self.get_location_info(ip_address)
        if location_info is not None:
            reply_message = self.generate_location_info_reply(location_info)
            await message.answer(reply_message)
            if reply_message != "<b>Введите правильный IP-адрес (например: 1.1.1.1):</b>" and reply_message != "<b>Не удалось получить информацию по IP-адресу</b>":
                await self.send_current_time(message.chat.id, location_info["latitude"], location_info["longitude"])
                await self.send_weather_info(message.chat.id, location_info["latitude"], location_info["longitude"])
        else:
            error_message = f"Не удалось получить информацию о местоположении для указанного IP-адреса: {ip_address}"
            self.logger.error(error_message)
            await message.answer("Не удалось получить информацию о местоположении для указанного IP-адреса")
        await self.send_menu(message.chat.id)

    def get_public_ip(self):
        try:
            response = requests.get("https://api.ipify.org?format=json")
            if response.status_code == 200:
                data = response.json()
                return data["ip"]
        except Exception as e:
            self.error_log_info(str(e))
            self.logger.error(f"Error getting public IP: {e}")
        return None

    def get_location_info(self, ip_address):
        try:
            lang = "ru"
            url = f"http://api.ipapi.com/{ip_address}?access_key={self.ipapi_api_key}&lang={lang}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            self.error_log_info(str(e))
            self.logger.error(str(e))
        return None

    def generate_location_info_reply(self, location_info):
        try:
            continent = location_info["continent_name"]
            country = location_info["country_name"]
            country_wikipedia_url = f"<a href='https://ru.wikipedia.org/wiki/{country}'>{country}</a>"
            region = location_info["region_name"]
            region_wikipedia_url = f"<a href='https://ru.wikipedia.org/wiki/{region}'>{region}</a>"
            city = location_info["city"]
            city_wikipedia_url = f"<a href='https://ru.wikipedia.org/wiki/{city}'>{city}</a>"
            zip_code = location_info["zip"]
            latitude = location_info["latitude"]
            longitude = location_info["longitude"]
            country_code = location_info["country_code"]
            country_flag = location_info["location"]["country_flag"]
            capital = location_info["location"]["capital"]
            capital_wikipedia_url = f"<a href='https://ru.wikipedia.org/wiki/{capital}'>{capital}</a>"
            region_code = location_info["region_code"]
            languages = [f"{lang['native']} ({lang['name']})" for lang in location_info["location"]['languages']]
            reply_message = f"Координаты: {latitude}, {longitude}\n" \
                            f"Континент: {continent}\n" \
                            f"Страна: {country_wikipedia_url}\n" \
                            f"Регион: {region_wikipedia_url}\n" \
                            f"Город: {city_wikipedia_url}\n" \
                            f"Почтовый индекс: {zip_code}\n" \
                            f"Код региона: {region_code}\n" \
                            f"Код страны: {country_code}\n" \
                            f"Флаг страны: {country_flag}\n" \
                            f"Столица: {capital_wikipedia_url}\n" \
                            f"Языки: {', '.join(languages)}"
            return reply_message
        except KeyError:
            return "<b>Введите правильный IP-адрес (например: 1.1.1.1):</b>"
        except TypeError:
            return "<b>Не удалось получить информацию по IP-адресу</b>"

    async def send_current_time(self, chat_id, latitude, longitude):
        try:
            timezone = self.get_timezone(latitude, longitude)
            if timezone:
                current_time = datetime.now(pytz.timezone(timezone))
                await self.bot.send_message(chat_id, f"Текущее время: {current_time} ({timezone})")
            else:
                await self.bot.send_message(chat_id, "Не удалось определить часовой пояс")
        except Exception as e:
            self.error_log_info(str(e))
            self.logger.error(f"Failed to send current time: {e}")

    def get_timezone(self, latitude, longitude):
        try:
            timezone_finder = TimezoneFinder()
            timezone = timezone_finder.timezone_at(lat=latitude, lng=longitude)
            return timezone
        except (KeyError, GeocoderTimedOut) as e:
            self.error_log_info(str(e))
            pass
        except Exception as e:
            self.error_log_info(str(e))
            self.logger.error(str(e))

    async def send_weather_info(self, chat_id, latitude, longitude):
        def convert_timezone(timezone):
            hours = timezone // 3600
            minutes = (timezone % 3600) // 60
            return f"GMT {'+' if hours >= 0 else '-'}{abs(hours):02d}:{abs(minutes):02d}"
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&exclude=hourly,daily&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                first_forecast = weather_data["list"][0]
                temperature = first_forecast["main"]["temp"]
                feels_like = first_forecast["main"]["feels_like"]
                temp_min = first_forecast["main"]["temp_min"]
                temp_max = first_forecast["main"]["temp_max"]
                pressure = first_forecast["main"]["pressure"]
                humidity = first_forecast["main"]["humidity"]
                wind_speed = first_forecast["wind"]["speed"]
                wind_direction = first_forecast["wind"]["deg"]
                clouds = first_forecast["clouds"]
                visibility = first_forecast["visibility"]
                pop = first_forecast["pop"]
                description = first_forecast["weather"][0]["description"]
                city = weather_data["city"]["name"]
                country_code = weather_data["city"]["country"]
                population = weather_data["city"]["population"]
                timezone = weather_data["city"]["timezone"]
                timezone_str = convert_timezone(timezone)
                reply_message = f"Температура: {temperature} °C\n" \
                                f"Ощущается как: {feels_like} °C\n" \
                                f"Минимальная температура: {temp_min} °C\n" \
                                f"Максимальная температура: {temp_max} °C\n" \
                                f"Атмосферное давление: {pressure} гПа\n" \
                                f"Влажность: {humidity}%\n" \
                                f"Описание: {description}\n" \
                                f"Облачность: {clouds}%\n" \
                                f"Скорость ветра: {wind_speed} м/с\n" \
                                f"Направление ветра: {wind_direction}°\n" \
                                f"Видимость: {visibility} м\n" \
                                f"Вероятность осадков: {pop}\n" \
                                f"Город: {city}\n" \
                                f"Страна: {country_code}\n" \
                                f"Население: {population}\n" \
                                f"Временная зона: {timezone_str}\n" \
                                f"(Это прогноз на ближайший период времени для ближайшего города)"
                await self.bot.send_message(chat_id, reply_message)
            else:
                error_message = f"Ошибка при выполнении запроса к OpenWeatherMap API. Код состояния: {response.status_code}"
                self.logger.error(error_message)
                await self.bot.send_message(chat_id, "Не удалось получить данные о погоде")
        except requests.exceptions.RequestException as e:
            self.error_log_info(str(e))
            self.logger.error(f"Failed to send weather info: {e}")

    async def send_dog_picture(self, chat_id):
        try:
            response = requests.get(url="https://api.thedogapi.com/v1/images/search")
            if response.status_code == 200:
                data = response.json()
                await self.bot.send_photo(chat_id, data[0].get("url"))
        except Exception as e:
            self.error_log_info(str(e))
            self.logger.error("Failed to get dog image: {e}")
        return None

    async def send_crypto_price(self, chat_id, cryptocurrency):
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{cryptocurrency}?localization=false&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false"
            response = requests.get(url)
            if response.status_code in [200, 201]:
                json_response = response.json()
                price = json_response["tickers"][0]["converted_last"]["usd"]
                large_image_url = json_response["image"]["large"]
                text = f"Текущий курс {cryptocurrency.capitalize()}: ${price}"
                await self.bot.send_photo(chat_id, large_image_url, caption=text)
        except Exception as e:
            self.logger.error(f"Error sending crypto price: {e}")

    async def send_help_info(self, chat_id):
        try:
            with open("help_info.txt", "r") as file:
                help_info = file.read()
            await self.bot.send_message(chat_id, help_info)
        except Exception as e:
            self.logger.error(f"Error sending help info: {e}")

    def error_log_info(self, error_message):
        with open("error.log", "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] - {error_message}\n"
            file.write(log_message)

    def start(self):
        executor.start_polling(self.dp, skip_updates=True)

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    bot_token = config["bot_token"]
    ipapi_api_key = config["ipapi_api_key"]
    weather_api_key = config["weather_api_key"]
    ip_bot = IpBot(bot_token, ipapi_api_key, weather_api_key)
    ip_bot.start()
