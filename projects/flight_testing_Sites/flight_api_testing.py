"""
step1 :this file has scrpit for fetching flight detail with automation .. saving page
site url : https://www.aerlingus.com/html/en-GB/home.html
from and to at one time
only so don't forget to change it for one destination all price scrape
loke from = london
to = new york
"""

import asyncio
import json

from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta

import random
from playwright_stealth import Stealth

def date_fetch(page,main_count):
    #ittration on date
    page.wait_for_selector('//swiper-container[@class="barchart__list"]')
    slides = page.locator('swiper-slide[data-test-id^="test_barchart_column"]')
    count = slides.count()

    for i in range(count):
        slide = slides.nth(i)
        # Click each date (if clickable)
        button = slide.locator('button')
        if button.is_visible():
            page.wait_for_timeout(500)
            human_mouse(page)
            button.click()
        # Wait a bit for potential network request to fire
        page.wait_for_timeout(500)
    main_count +=1
    with open(fr"E:\Mansi\pagesave\pagesave_flight_api\{from_.replace(' ','_')}_{to_.replace(' ','_')}\flights_{from_.replace(' ','_')}_{to_.replace(' ','_')}_{main_count}.json", "w") as f:
        json.dump(captured_requests, f, indent=4)

def generate_dates(start_date: str, num_days: int):
    """
    Generate a list of dates in format: 'Wed 11 Mar'

    :param start_date: starting date in 'YYYY-MM-DD' format
    :param num_days: number of consecutive days to generate
    :return: list of strings
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    dates = []
    for i in range(num_days):
        current = start + timedelta(days=i)
        formatted = current.strftime("%a %d %b")  # e.g., Wed 11 Mar
        dates.append(formatted)
    return dates

def handle_route(route, request):
    # if "flights/fixed?origin" in request.url:
    #     captured_requests.append({
    #         "url": request.url,
    #         "method": request.method,
    #         "headers": dict(request.headers),
    #         "post_data": request.post_data,
    #         "cookies": context.cookies()
    #     })
    route.continue_()
def handle_request(request):
    if "flights/fixed?origin" in request.url:
        print("REQUEST FOUND:", request.url)

def handle_response(response):
    if "flights/fixed?origin" in response.url:
        try:
            response_json = response.json()  # Capture JSON body
        except Exception:
            response_json = None

        captured_requests.append({
            "url": response.url,
            "method": response.request.method,
            "headers": dict(response.request.headers),
            "post_data": response.request.post_data,
            "cookies": context.cookies(),
            "status": response.status,
            "response_json": response_json
        })
        print(f"Captured: {response.url}")

def human_mouse(page):
    x1 = random.randint(200,600)
    y1 = random.randint(200,600)
    x2 = random.randint(400,900)
    y2 = random.randint(200,700)

    page.mouse.move(x1,y1,steps=random.randint(10,30))
    page.mouse.move(x2,y2,steps=random.randint(10,30))

with sync_playwright() as p:
    device = p.devices["iPhone 13"]

    browser = p.chromium.launch(
        headless=False,args=[    "--start-maximized","--disable-blink-features=AutomationControlled", "--disable-infobars","--disable-dev-shm-usage",  "--no-sandbox"]
    )
    context = browser.new_context()
    page = context.new_page()
    captured_requests = []

    Stealth().apply_stealth_sync(page)

    page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """)
    page.route("**/*", handle_route)
    context.on("request", handle_request)
    context.on("response", handle_response)
    page.goto("https://www.aerlingus.com/html/en-GB/home.html", timeout=60000)
    page.wait_for_load_state("networkidle")
    human_mouse(page)
    page.locator('[id="onetrust-accept-btn-handler"]').click()
    human_mouse(page)
    page.locator('[data-test-id="update-button"]').click()
    #origin
    page.wait_for_selector("//input[@aria-label='Departure Airport']", timeout=10000)
    from_ = "london"
    to_ = "new york"
    human_mouse(page)
    human_mouse(page)
    page.locator("//input[@aria-label='Departure Airport']").first.click()
    human_mouse(page)
    page.locator("//input[@aria-label='Departure Airport']").first.type(from_,delay=random.randint(120,200))
    page.wait_for_selector("(//ul[@class='dropdown-scroll custom-scroll']//li)[1]")
    human_mouse(page)
    page.locator("(//ul[@class='dropdown-scroll custom-scroll']//li)[1]").click()


    #destination
    human_mouse(page)
    page.locator("//input[@aria-label='Arrival Airport']").first.click()
    human_mouse(page)
    page.locator("//input[@aria-label='Arrival Airport']").first.type(to_, delay=random.randint(120, 200))
    page.wait_for_selector("(//ul[@class='dropdown-scroll custom-scroll']//li)[1]")
    human_mouse(page)
    page.locator("(//ul[@class='dropdown-scroll custom-scroll']//li)[1]").click()
    human_mouse(page)
    # --
    # date selection
    # page.locator("#destinationInput-menu li").first.click()
    # page.locator("[class*='_today']").click()
    human_mouse(page)
    page.wait_for_selector('//div[@input-placeholder="Departure Date"]')
    page.locator('//div[@input-placeholder="Departure Date"]').click()
    human_mouse(page)
    page.wait_for_selector('//td[contains(@class,"ui-datepicker-today")]//a[contains(@class,"ui-state-active")]')
    page.locator('//td[contains(@class,"ui-datepicker-today")]//a[contains(@class,"ui-state-active")]').first.click()

    #search
    page.wait_for_selector('[data-test-id="test_booker_search"]')

    human_mouse(page)
    page.locator('[data-test-id="test_booker_search"]').click()

    #next page after click on search
    page_content =  page.text_content('body')
    main_count = 1
    # page.reload()

    date_fetch(page, main_count)

    while page.locator('[data-test-id="test_barcharts_go_next"]').count() > 0:
        human_mouse(page)
        page.locator('[data-test-id="test_barcharts_go_next"]').click()
        human_mouse(page)
        page.wait_for_timeout(9000)
        date_fetch(page, main_count)
        main_count+=1
        page.wait_for_timeout(9000)

    page.wait_for_timeout(80000)
    context.close()

    # if "All flights are sold out for this date" in page_content:
    #     page.wait_for_selector('//span[@data-test-id="test_barchart_column_date"][contains(text()," Wed 11 Mar ")]')
    #     page.locator('//span[@data-test-id="test_barchart_column_date"][contains(text()," Wed 11 Mar ")]').click()
    #
    #     page.reload()
        #goto next data section
        # page.wait_for_selector('[data-test-id="test_barcharts_go_next"]')
        # page.locator('[data-test-id="test_barcharts_go_next"]').click()

#priveous code
    # page.wait_for_selector("[data-testid='desktop-travellerselector']")
    # apply_btn = page.get_by_test_id("traveller-selector-apply-button")
    # apply_btn.scroll_into_view_if_needed()
    # apply_btn.click(force=True)
    # page.wait_for_selector("[data-testid='desktop-cta']")
    #
    # # click search
    #
    # human_mouse(page)
    # page.get_by_test_id("desktop-cta").click(force=True)
    # page.wait_for_timeout(3000)
    # page.reload()

#target url




#
# from curl_cffi import requests
# import json
# import urllib.parse
# import uuid
# API_KEY = "876484b6eb084b818e74e53e26d5e519302cbab8e78"
#
# url = "https://www.skyscanner.co.in/g/radar/api/v2/web-unified-search/"
# view_id = str(uuid.uuid4())
#
# payload = {
#     "cabinClass": "ECONOMY",
#     "childAges": [],
#     "adults": 1,
#     "legs": [
#         {
#             "legOrigin": {"@type": "entity", "entityId": "27544008"},
#             "legDestination": {"@type": "entity", "entityId": "27537542"},
#             "dates": {"@type": "date", "year": "2026", "month": "03", "day": "10"},
#             "placeOfStay": "27537542"
#         }
#     ]
# }
#
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "User-Agent": "Mozilla/5.0",
#     "X-Skyscanner-Traveller-Context": str(uuid.uuid4()),
#     "X-Skyscanner-TrustedFunnelId": view_id,
#     "X-Skyscanner-ViewId": view_id,
#     "X-Skyscanner-Market": "IN",
#     "X-Skyscanner-Currency": "INR",
#     "X-Skyscanner-Locale": "en-GB"
# }
#
# proxies = {
#     "http": f"http://{API_KEY}:@proxy.scraper.do:8080",
#     "https": f"http://{API_KEY}:@proxy.scraper.do:8080"
# }
#
# response = requests.post(
#     url,
#     headers=headers,
#     json=payload,
#     proxies=proxies,
#     impersonate="chrome131",http_version="v2",
#     timeout=600,verify=False
# )
#
# print("Status:", response.status_code)
# print(response.text)





# from curl_cffi import requests
# cookies = {
#     'reese84': '3:gBVdZ+NNmDRvXWz1R1U1vQ==:iYjzHPgcjwISNr8AuiVd/Pe2uOAFP4P/CiO+DyyxY+aIHgrqQ1y6WaQ2KUf4KmM+FaGq6QRoLk3zvRZm1gvFFeYfc9HfrYWg8Usw0s/MPox+Cx2qa+wIkUCxucu0Ea8TG2tvVxUNFY4HjCMfW6bAfy8qi0iPtu8Yva4kQHerdIapHd54sHZB6U/0t4gXbD5Mi7GGp6VmfW40REt0avM4x+Vd3f070NKw75uj03OVd3OkETx5IhXxJb3WTLmE1RprUG/rUBe07gRdtZoXCGDJ+cc2B/SWYKzuuwiMO6UayB0Vuphp4mnLnLoscncESAkWwvODxDKI9N0TNhjNk/6H0TrIDMou5l4ORCB8NZZlnRMx4GT0x5PP4kPQDIu9Y9aIeUp6PQpKbxqGCMiAk8y7ySESVAn/J/mg7lzIGjTd2La+ELmXWFWWyrH7mhGI5cjnC58Xyipf2puSv7KS1dcYqK98joaUE5JmAy0qNpMxSsg=:XAS4h7hmk22Z8h1r0QHNBBmVwRLnpuOANnpG5NjlyJI=',
#     'ei_userId': '"1655887061:1773139510252"',
#     'OptanonAlertBoxClosed': '2026-03-10T10:45:16.882Z',
#     'ei_consent_activegroups': '%2CC0001%2C',
#     'preffered_home_airport': 'BOS',
#     'ei_locale_data': '%7B%22language%22%3A%22en%22%2C%22origin%22%3A%22bos%22%2C%22country%22%3A%22us%22%7D',
#     'ei_redirect': 'en-US',
#     'latest_search': '%7B%22fareType%22%3A%7B%22val%22%3A%22ECONOMY%22%2C%22labelLh%22%3A%22module.booker.option.economy%22%2C%22labelSh%22%3A%22module.booker.option.economy%22%2C%22label%22%3A%22module.booker.option.economy%22%7D%2C%22fareCategory%22%3A%22ECONOMY%22%2C%22type%22%3A%22ROUND%22%2C%22flightJourneySearches%22%3A%5B%7B%22sourceAirportCode%22%3A%22LON%22%2C%22sourceAirportLabel%22%3A%22London%20England%20Area%20(LON)%2C%20England%2C%20UK%22%2C%22sourceAirportShortLabel%22%3A%22Boston%20(BOS)%22%2C%22sourceAirportCountry%22%3A%22GB%22%2C%22destinationAirportCode%22%3A%22JFK%22%2C%22destinationAirportLabel%22%3A%22New%20York%20(JFK)%2C%20New%20York%2C%20USA%22%2C%22destinationAirportShortLabel%22%3A%22New%20York%20(JFK)%22%2C%22destinationCountry%22%3A%22US%22%2C%22departureDate%22%3A1773167400000%2C%22arrivalDate%22%3A1773167400000%7D%5D%2C%22passengersCount%22%3A%7B%22adultsCount%22%3A1%2C%22youngAdultsCount%22%3A0%2C%22childrenCount%22%3A0%2C%22infantsCount%22%3A0%7D%7D',
#     'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Mar+10+2026+16%3A18%3A01+GMT%2B0530+(India+Standard+Time)&version=202411.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f3dbcddf-5855-44f9-8458-ea1c5c6d1082&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0005%3A0%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&intType=6&geolocation=IN%3BGJ&AwaitingReconsent=false',
#     'requestObj': '%7B%22origin%22%3A%22LON%2CJFK%22%2C%22destination%22%3A%22JFK%2CLON%22%2C%22departureDate%22%3A%2211%2F03%2F2026%22%2C%22returnDate%22%3A%2211%2F03%2F2026%22%2C%22numYouths%22%3A0%2C%22numAdults%22%3A1%2C%22numChildren%22%3A0%2C%22numInfants%22%3A0%2C%22fare%22%3A%22low%22%7D',
# }
#
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'en-US,en;q=0.9',
#     'priority': 'u=1, i',
#     'referer': 'https://www.aerlingus.com/app/make/flight-search-result?fareType=RETURN&fareCategory=ECONOMY&sourceAirportCode_0=LON&destinationAirportCode_0=JFK&departureDate_0=2026-03-11&sourceAirportCode_1=JFK&destinationAirportCode_1=LON&departureDate_1=2026-03-11&numAdults=1&numYoungAdults=0&numChildren=0&numInfants=0&promoCode=&groupBooking=false',
#     'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
#     'x-correlation-id': 'null',
#     # 'cookie': 'reese84=3:gBVdZ+NNmDRvXWz1R1U1vQ==:iYjzHPgcjwISNr8AuiVd/Pe2uOAFP4P/CiO+DyyxY+aIHgrqQ1y6WaQ2KUf4KmM+FaGq6QRoLk3zvRZm1gvFFeYfc9HfrYWg8Usw0s/MPox+Cx2qa+wIkUCxucu0Ea8TG2tvVxUNFY4HjCMfW6bAfy8qi0iPtu8Yva4kQHerdIapHd54sHZB6U/0t4gXbD5Mi7GGp6VmfW40REt0avM4x+Vd3f070NKw75uj03OVd3OkETx5IhXxJb3WTLmE1RprUG/rUBe07gRdtZoXCGDJ+cc2B/SWYKzuuwiMO6UayB0Vuphp4mnLnLoscncESAkWwvODxDKI9N0TNhjNk/6H0TrIDMou5l4ORCB8NZZlnRMx4GT0x5PP4kPQDIu9Y9aIeUp6PQpKbxqGCMiAk8y7ySESVAn/J/mg7lzIGjTd2La+ELmXWFWWyrH7mhGI5cjnC58Xyipf2puSv7KS1dcYqK98joaUE5JmAy0qNpMxSsg=:XAS4h7hmk22Z8h1r0QHNBBmVwRLnpuOANnpG5NjlyJI=; ei_userId="1655887061:1773139510252"; OptanonAlertBoxClosed=2026-03-10T10:45:16.882Z; ei_consent_activegroups=%2CC0001%2C; preffered_home_airport=BOS; ei_locale_data=%7B%22language%22%3A%22en%22%2C%22origin%22%3A%22bos%22%2C%22country%22%3A%22us%22%7D; ei_redirect=en-US; latest_search=%7B%22fareType%22%3A%7B%22val%22%3A%22ECONOMY%22%2C%22labelLh%22%3A%22module.booker.option.economy%22%2C%22labelSh%22%3A%22module.booker.option.economy%22%2C%22label%22%3A%22module.booker.option.economy%22%7D%2C%22fareCategory%22%3A%22ECONOMY%22%2C%22type%22%3A%22ROUND%22%2C%22flightJourneySearches%22%3A%5B%7B%22sourceAirportCode%22%3A%22LON%22%2C%22sourceAirportLabel%22%3A%22London%20England%20Area%20(LON)%2C%20England%2C%20UK%22%2C%22sourceAirportShortLabel%22%3A%22Boston%20(BOS)%22%2C%22sourceAirportCountry%22%3A%22GB%22%2C%22destinationAirportCode%22%3A%22JFK%22%2C%22destinationAirportLabel%22%3A%22New%20York%20(JFK)%2C%20New%20York%2C%20USA%22%2C%22destinationAirportShortLabel%22%3A%22New%20York%20(JFK)%22%2C%22destinationCountry%22%3A%22US%22%2C%22departureDate%22%3A1773167400000%2C%22arrivalDate%22%3A1773167400000%7D%5D%2C%22passengersCount%22%3A%7B%22adultsCount%22%3A1%2C%22youngAdultsCount%22%3A0%2C%22childrenCount%22%3A0%2C%22infantsCount%22%3A0%7D%7D; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Mar+10+2026+16%3A18%3A01+GMT%2B0530+(India+Standard+Time)&version=202411.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f3dbcddf-5855-44f9-8458-ea1c5c6d1082&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0005%3A0%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&intType=6&geolocation=IN%3BGJ&AwaitingReconsent=false; requestObj=%7B%22origin%22%3A%22LON%2CJFK%22%2C%22destination%22%3A%22JFK%2CLON%22%2C%22departureDate%22%3A%2211%2F03%2F2026%22%2C%22returnDate%22%3A%2211%2F03%2F2026%22%2C%22numYouths%22%3A0%2C%22numAdults%22%3A1%2C%22numChildren%22%3A0%2C%22numInfants%22%3A0%2C%22fare%22%3A%22low%22%7D',
# }
# session = requests.Session()
# response = session.get(
#     'https://www.aerlingus.com/api/v2/flights/fixed?origin=LON,JFK&destination=JFK,LON&departureDate=11/03/2026&returnDate=11/03/2026&numYouths=0&numAdults=1&numChildren=0&numInfants=0&fare=low',
#     cookies=cookies,
#     headers=headers,impersonate="chrome101"
# )
# session.close()
#
#
#
# if response.status_code == 200:
#     print(response.json)
#
# else:
#     print(response.text)
#
#
# print(response.status_code)