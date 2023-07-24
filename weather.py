import requests
import smbus
import time
from RPLCD.i2c import CharLCD

API_key = "###############################"

def get_gps_coordinates():
    try:
        # IP Geolocation API를 통해 위치 정보를 가져옴
        response = requests.get("http://ipinfo.io/json")
        data = response.json()

        # 위도와 경도 추출
        if "loc" in data:
            latitude, longitude = data["loc"].split(",")
            return float(latitude), float(longitude)
        else:
            return None, None

    except Exception as e:
        print("Error occurred:", e)
        return None, None

def get_weather(lat, lon):
    # openweathermap API를 통해 날씨 정보를 가져옴
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"
    response = requests.get(url)
    data = response.json()
    weather = data["weather"][0]["main"]
    temperature = data["main"]["temp"] - 273.15
    city = data["name"]

    return city, weather, temperature

def display_weather_on_lcd(lat, lon):
    # I2C 인터페이스 설정 (I2C 버스 번호는 Raspberry Pi 모델에 따라 다를 수 있습니다)
    bus = smbus.SMBus(1)

    # LCD 초기화 (0x27은 대부분의 16x2 I2C LCD 모듈에서 기본 주소이며, 주소가 0x3F인 경우도 있습니다.)
    lcd = CharLCD('PCF8574', 0x3F)

    try:
        city, weather, temperature = get_weather(lat, lon)

        # 메시지 롤링
        message = f"City: {city}  Weather: {weather}  Temp: {temperature:.2f}°C"
        while True:
            for i in range(len(message) - 15):
                lcd.clear()
                lcd.write_string(message[i:i+16])
                time.sleep(0.5)

    except Exception as e:
        # 오류 처리: API 호출 중에 문제가 발생한 경우 예외 처리
        lcd.clear()
        lcd.write_string("Weather Error")

if __name__ == "__main__":
    latitude, longitude = get_gps_coordinates()
    if latitude is not None and longitude is not None:
        print("현재 위도: ", latitude)
        print("현재 경도: ", longitude)
    else:
        print("위치 정보를 찾을 수 없습니다.")

    display_weather_on_lcd(latitude, longitude)
