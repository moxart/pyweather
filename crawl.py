import requests, argparse
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"

TBL = PrettyTable(["Day Name", "Status", "Max Temperature °C", "Min Temperature °C"])


def crawl_weather(url):

    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": LANGUAGE
    }

    response = requests.get(url, headers=headers)
    html = bs(response.content, "html.parser")

    result = {
        "region": html.find(id='wob_loc').text,
        "temperature_now": html.find(id='wob_tm').text,
        "date": html.find(id='wob_dts').text,
        "weather_now": html.find(id='wob_dc').text,
        "precipitation": html.find(id='wob_pp').text,
        "humidity": html.find(id='wob_hm').text,
        "wind": html.find(id='wob_ws').text
    }

    next_days = []

    days = html.find("div", id="wob_dp")

    for day in days.find_all("div", attrs={"class": "wob_df"}):
        name = day.find("div", attrs={"class": "vk_lgy"}).attrs['aria-label']
        weather = day.find("img").attrs["alt"]
        temp = day.find_all("span", {"class": "wob_t"})
        max_temp = temp[0].text
        min_temp = temp[2].text

        next_days.append({
            "day_name": name,
            "weather": weather,
            "temp": temp,
            "max_temp": max_temp,
            "min_temp": min_temp,
        })

    result["next_days"] = next_days

    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Scrapping Weather Data From Google Weather")
    parser.add_argument("region", nargs="?", help="""
        Region to get weather for, must be available region.
        Default is your current location determined by your IP Address
    """, default="")

    args = parser.parse_args()
    region = args.region
    URL += region

    data = crawl_weather(URL)

    print("Location: ", data["region"])
    print("Now: ", data["date"])
    print("Temperature now: {}°C ".format(data["temperature_now"]))
    print("Description: ", data["weather_now"])
    print("Precipitation: ", data["precipitation"])
    print("Humidity: ", data["humidity"])
    print("Wind: ", data["wind"])

    for dayweather in data["next_days"]:

        TBL.add_row([
            dayweather["day_name"],
            dayweather["weather"],
            dayweather["max_temp"],
            dayweather["min_temp"]
        ])

    print(TBL)
