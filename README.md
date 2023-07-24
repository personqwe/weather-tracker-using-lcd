## 프로젝트 정보

[](https://git.huconn.com/topst-project/weather-tracker-using-lcd)

[The trusted source for IP address data, leading IP data provider - IPinfo.io](http://ipinfo.io/)

[Weather API](https://api.openweathermap.org/)

[ipinfo.io](http://ipinfo.io/) API를 사용하여 IP의 위도와 경도 값을 받아왔습니다.

받아온 위도와 경도를 이용하여 해당 지역의 이름, 날씨, 온도를 가져오기 위해 Weather API를 사용합니다. Weather API 홈페이지에 접속하여 회원 가입 후 API키를 발급 받아야 합니다.

GND = GND pin

VCC - 5V pin

SDA = GPIO SDA I2C pin

SCL = GPIO SCL I2C pin

VSCode 설치 방법:

1. 다음 명령어를 실행하세요: wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
2. packages.microsoft.gpg 파일을 /etc/apt/trusted.gpg.d/ 디렉토리에 복사합니다: sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
3. 다음 명령어를 실행하여 /etc/apt/sources.list.d/vscode.list 파일을 만듭니다: sudo sh -c 'echo "deb [arch=arm64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
4. 패키지 목록을 업데이트합니다: sudo apt update
5. VSCode를 설치합니다: sudo apt install code
6. 

실행 방법:

다음 명령어를 입력하세요:
code --no-sandbox --user-data-dir=/path/to/alternate/user/data/dir

진행 방법:

- pip을 설치하려면 다음 명령을 실행하십시오.

```
sudo apt install python3-pip

```

- I2C 통신을 위해 smbus를 설치하십시오.

```jsx
pip install smbus
```

- http통신을 위한 requests와 LCD제어를 위한 RPLCD를 설치하십시오

```jsx
pip install requests
pip install RPLCD
```

```python
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
```

# **Weather fields in API response**

If you do not see some of the parameters in your API response it means that these weather phenomena are just not happened for the time of measurement for the city or location chosen. Only really measured or calculated data is displayed in API response.

# **JSON**

```
Example of API response
```

                          `
{
  "coord": {
    "lon": 10.99,
    "lat": 44.34
  },
  "weather": [
    {
      "id": 501,
      "main": "Rain",
      "description": "moderate rain",
      "icon": "10d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 298.48,
    "feels_like": 298.74,
    "temp_min": 297.56,
    "temp_max": 300.05,
    "pressure": 1015,
    "humidity": 64,
    "sea_level": 1015,
    "grnd_level": 933
  },
  "visibility": 10000,
  "wind": {
    "speed": 0.62,
    "deg": 349,
    "gust": 1.18
  },
  "rain": {
    "1h": 3.16
  },
  "clouds": {
    "all": 100
  },
  "dt": 1661870592,
  "sys": {
    "type": 2,
    "id": 2075663,
    "country": "IT",
    "sunrise": 1661834187,
    "sunset": 1661882248
  },
  "timezone": 7200,
  "id": 3163858,
  "name": "Zocca",
  "cod": 200
}`

**Fields in API response**

- `coord`
    - `coord.lon`
        
        Longitude of the location
        
    - `coord.lat`
        
        Latitude of the location
        
- `weather`
    
    (more info Weather condition codes)
    
    - `weather.id`
        
        Weather condition id
        
    - `weather.main`
        
        Group of weather parameters (Rain, Snow, Extreme etc.)
        
    - `weather.description`
        
        Weather condition within the group. You can get the output in your language. [Learn more](https://openweathermap.org/current#multi)
        
    - `weather.icon`
        
        Weather icon id
        
- `base`
    
    Internal parameter
    
- `main`
    - `main.temp`
        
        Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
        
    - `main.feels_like`
        
        Temperature. This temperature parameter accounts for the human perception of weather. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
        
    - `main.pressure`
        
        Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa
        
    - `main.humidity`
        
        Humidity, %
        
    - `main.temp_min`
        
        Minimum temperature at the moment. This is minimal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
        
    - `main.temp_max`
        
        Maximum temperature at the moment. This is maximal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
        
    - `main.sea_level`
        
        Atmospheric pressure on the sea level, hPa
        
    - `main.grnd_level`
        
        Atmospheric pressure on the ground level, hPa
        
- `visibility`
    
    Visibility, meter. The maximum value of the visibility is 10km
    
- `wind`
    - `wind.speed`
        
        Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour.
        
    - `wind.deg`
        
        Wind direction, degrees (meteorological)
        
    - `wind.gust`
        
        Wind gust. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour
        
- `clouds`
    - `clouds.all`
        
        Cloudiness, %
        
- `rain`
    - `rain.1h`
        
        (where available) Rain volume for the last 1 hour, mm. Please note that only mm as units of measurement are available for this parameter.
        
    - `rain.3h`
        
        (where available) Rain volume for the last 3 hours, mm. PPlease note that only mm as units of measurement are available for this parameter.
        
- `snow`
    - `snow.1h`
        
        (where available) Snow volume for the last 1 hour, mm. Please note that only mm as units of measurement are available for this parameter.
        
    - `snow.3h`
        
        (where available)Snow volume for the last 3 hours, mm. Please note that only mm as units of measurement are available for this parameter.
        
- `dt`
    
    Time of data calculation, unix, UTC
    
- `sys`
    - `sys.type`
        
        Internal parameter
        
    - `sys.id`
        
        Internal parameter
        
    - `sys.message`
        
        Internal parameter
        
    - `sys.country`
        
        Country code (GB, JP etc.)
        
    - `sys.sunrise`
        
        Sunrise time, unix, UTC
        
    - `sys.sunset`
        
        Sunset time, unix, UTC
        
- `timezone`
    
    Shift in seconds from UTC
    
- `id` City ID. Please note that built-in geocoder functionality has been deprecated. Learn more [here](https://openweathermap.org/current#builtin).
- `name` City name. Please note that built-in geocoder functionality has been deprecated. Learn more [here](https://openweathermap.org/current#builtin).
- `cod`
    
    Internal parameter
    
![Alt text](image.png)