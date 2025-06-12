import time
from rebrowser_playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, timezone, timedelta
import json
import os

# URL of the live timing page
URL = "https://www.f1academy.com/livetiming/index.html"
PAGE_TIMEOUT = 60000
PAGE_LOADING_TIME = 5


def download_live_timing(page):
    """Opens the target webpage, waits a set amount of time for it to load, and return HTML of that page.

    Args:
        page (Page): rebrowser playwright page object

    Returns:
        HTML: HTML of loaded page
    """
    # Navigate to the URL and wait until the network is idle
    # (This helps ensure the JavaScript has finished loading data.)
    page.goto(URL, wait_until="commit", timeout=PAGE_TIMEOUT)
    # Optionally, wait for a specific element:
    time.sleep(PAGE_LOADING_TIME)
    # Get the rendered HTML content
    html = page.content()
    return html


def parse_driver_data(html):
    """Take HTML data and parse into an array of dictionaries

    Args:
        html (HTML): HTML of live timing page

    Returns:
        Dictionary: A dictionary of all drivers with relevant data fields
    """
    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.find_all("tbody")
    if not tbody:
        print("Error: Could not find the <tbody> element in the rendered HTML.")
        return []
    utc_now = datetime.now(timezone.utc)

    drivers = []
    for section in tbody[1].find_all("tr"):
        tds = section.find_all("td")
        sector1 = section.find("td", class_="sector1-time ng-binding").get_text(
            strip=True
        )
        sector2 = section.find("td", class_="sector2-time ng-binding").get_text(
            strip=True
        )
        sector3 = section.find("td", class_="sector3-time ng-binding").get_text(
            strip=True
        )

        # Parse into timedeltas
        s1_td = parse_sector_time(sector1)
        s2_td = parse_sector_time(sector2)
        s3_td = parse_sector_time(sector3)

        # Conditionally calculate latest_lap_time
        if all([s1_td, s2_td, s3_td]):
            total = s1_td + s2_td + s3_td
            latest_lap_time = (
                f"{int(total.total_seconds() // 60)}:{total.total_seconds() % 60:06.3f}"
            )
        else:
            latest_lap_time = ""

        driver_info = {
            "position": section.find("td", class_="position ng-binding").get_text(
                strip=True
            ),
            "driver_short_name": section.find(
                "td", class_="driver-short-name ng-binding"
            ).get_text(strip=True),
            "gap": section.find("td", class_="gap ng-binding").get_text(strip=True),
            "interval": section.find("td", class_="interval ng-binding").get_text(
                strip=True
            ),
            "best_lap": section.find("td", class_="best-lap ng-binding").get_text(
                strip=True
            ),
            "sector1_time": section.find(
                "td", class_="sector1-time ng-binding"
            ).get_text(strip=True),
            "sector2_time": section.find(
                "td", class_="sector2-time ng-binding"
            ).get_text(strip=True),
            "sector3_time": section.find(
                "td", class_="sector3-time ng-binding"
            ).get_text(strip=True),
            "latest_lap_time": latest_lap_time,
            "timestamp": utc_now.strftime("%H:%M:%S"),
        }
        drivers.append(driver_info)

    return drivers


def parse_sector_time(sector_string):
    """Converts string to timedelta object with sector time split in to minutes and seconds

    Args:
        sector_string (string): Sector time in string format ex. 12.345

    Returns:
        timedelta: Timedelta object with sector time split in to minutes and seconds
    """
    try:
        minutes, seconds = sector_string.split(":")
        return timedelta(minutes=int(minutes), seconds=float(seconds))
    except (ValueError, AttributeError):
        return None


def main():
    """Creates parameters for a Chrome window to open the live timing page.
    Create file for storing driver data in jsonl format.
    Loop and call logic that opens the page and gathers the html.
    Dump the returned dictionary to the create jsonl file.
    """
    with sync_playwright() as playwright:
        # Launch headless Chromium
        browser = playwright.chromium.launch(
            headless=False, args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1,
        )
        page = context.new_page()
        utc_fileName = datetime.now(timezone.utc)
        filename = utc_fileName.strftime("f1aData_%Y_%m_%d_%H_%M_%S.jsonl")
        while True:
            try:
                html = download_live_timing(page)
                # htmlFile = open("f1av2.html", "r", encoding="utf-8")
                # html = htmlFile.read()
                drivers = parse_driver_data(html)

                print("=== Driver Data ===")
                if drivers:
                    with open(filename, "a", encoding="utf-8") as f:
                        json.dump(drivers, f)
                        f.write("\n")
                    for driver in drivers:
                        print(driver)
                else:
                    print("No driver data found.")

            except Exception as e:
                print("An error occurred:", e)
                break
        browser.close()


if __name__ == "__main__":
    main()
