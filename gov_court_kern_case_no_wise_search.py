import random
import time
import os
import pymysql
from DrissionPage import ChromiumPage, ChromiumOptions
import tempfile
from DrissionPage.errors import ContextLostError
from slack_info import *

message= f"running proces start.. file no 1\n time : {datetime.now().strftime('%H:%M:%S')}\ncc: <@U0ARB6NF1S7>"
send_message(message)
def get_connection()    :
    conn = pymysql.connect(host="localhost",user="root",database="protal_kern_BGC",cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    return conn, cur

def update_status(case_no,table_name,conn,cur):
    query = f"update {table_name} set status='done' where case_no= %s"
    cur.execute(query,(case_no,))
    conn.commit()
conn, cur = get_connection()
# table_name = "case_no_table_traffic"
table_name = "case_no_table_last_name"
query = f"select * from {table_name} where status='pending' and id between 1 and 14000"
cur.execute(query,)
data = cur.fetchall()
print(len(data))

def random_wait(a=5, b=10):
    t = random.uniform(a, b)
    time.sleep(t)

os.makedirs(fr"D:\Mansi\pagesave\portal_gov\202603_last_name",exist_ok=True)
def save_page(case_no,html):
    with open(fr"D:\Mansi\pagesave\portal_gov\202603_last_name\lastname_{case_no}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(fr"D:\Mansi\pagesave\portal_gov\202603_last_name\last_name_{case_no}.html saved successfully")
try:
    # Create temp profile (acts like incognito)
    temp_dir = tempfile.mkdtemp()
    co = ChromiumOptions()
    co.set_user_data_path(temp_dir)
    co.set_local_port(9222)
    # fresh profile = no cookies
    co.headless(False)
    # wait for page load
    page = ChromiumPage(co)
    page.run_js("document.title='demo_1'")
    time.sleep(5)
    page.get("https://portal.kern.courts.ca.gov/")
    time.sleep(25)
    page.ele('text:Login').click()
    time.sleep(5)
    # ✅ fill email
    page.ele('#edit-name').input('kristi.reed@genuinedataservices.com')
    time.sleep(1)
    # ✅ fill password
    page.ele('#edit-pass').input('D@t@GDS2025!!')
    # input("Press Enter to close...")
    print("port is :",9222)
    print("👉 Fill CAPTCHA manually now... you have 15 seconds")
    time.sleep(20)

    page.ele('#edit-submit').click()
    time.sleep(2)
    page.ele('xpath://a[contains(text(),"Case Search")]').click()
    time.sleep(2)
    #search case no wise this use
    # case_input = page.ele('xpath://div//label[contains(text(),"Case Number")]/following-sibling::div/input')
    # case_input.scroll.to_see()
    # case_no = "26BIN00001"
    # case_input.input(case_no)
    # #first name wise searching
    case_input = page.ele('xpath://div//label[contains(text(),"First Name")]/following-sibling::div/input')
    case_input.scroll.to_see()
    case_no = "**"
    case_input.input(case_no)  # <-- your case number
    #last name wise searching
    case_input = page.ele('xpath://div//label[contains(text(),"Last Name")]/following-sibling::div/input')
    case_input.scroll.to_see()
    case_no = "Last"
    case_input.input(case_no)  # <-- your case number
    time.sleep(15)
    page.ele('#edit-submit').click()
    time.sleep(5)
    # ✅ save to file
    # html = page.html
    # save_page(case_no,html)
    # try:
    #     update_status(case_no, table_name, conn, cur)
    #     random_wait(a=2, b=3)
    # except Exception as e:
    #     print("issue in update record..",e)
    print(f"{case_no}.html saved successfully")
    print(f"file 1 running ......")
    # #========================try if data present else skip==============================
    # rows = page.ele('xpath://div[@class="search-result-page-tag"]//table//tbody//tr')
    # for data in rows:
    #     link = data.ele("tag:a")
    #     case_no = link.text.strip()
    #     print("case no :", case_no)
    #     link.click()
    #     page.wait.load_complete()
    #     random_wait(a=5, b=6)
    #     save_page(case_no)
    #     random_wait(a=2, b=4)


    # ===========================================================================
    # lst = ["26FLB00761","26FLR00060","26FLS00046","26CSB00326"]
    # lst = [f"25FLB{str(i).zfill(5)}" for i in range(853, 854)]
    # for i in lst:
    for i in data:
        case_no = i["case_no"]
        # case_input = page.ele('xpath://div//label[contains(text(),"Case Number")]/following-sibling::div/input')
        # case_input.scroll.to_see()
        # case_input.clear()
        # case_input.clear()
        # case_input.input(case_no)  # <-- your case number
        # random_wait(a=3, b=4)
        # #first name wise searching
        case_input = page.ele('xpath://div//label[contains(text(),"First Name")]/following-sibling::div/input')
        case_input.scroll.to_see()
        case_input.clear()
        case_no = "**"
        case_input.input(case_no)  # <-- your case number
        # last name wise searching
        case_input = page.ele('xpath://div//label[contains(text(),"Last Name")]/following-sibling::div/input')
        case_input.scroll.to_see()
        case_input.clear()
        case_input.clear()
        case_input.input(case_no)  # <-- your case number
        random_wait(a=3, b=4)
        page.ele('#edit-submit').click()
        # if captcha then need to solve it.
        try:
            while True:
                iframe = page.ele('xpath://iframe[contains(@src,"recaptcha")]')
                frame = page.get_frame(iframe)
                captch_element = frame.ele('xpath://div[@class="recaptcha-checkbox-checkmark"]')
                if captch_element:
                    checked = frame.ele('xpath://span[@aria-checked="true"]', timeout=1)
                    if checked:
                        break
                    else:
                        print("solve captcha for further process.....")
                        time.sleep(5)
                        continue
        except Exception as e:
            print(e)
        random_wait(a=6, b=7)
        page.wait.doc_loaded()
        for _ in range(3):
            try:
                html = page.html
                if html:break
            except ContextLostError:
                print("please wait page is refreshing...")
                time.sleep(2)

        html = page.html
        save_page(case_no, html)
        try:
            update_status(case_no, table_name, conn, cur)
            random_wait(a=0, b=1)
        except Exception as e:
            print("issue in update record..", e)
        random_wait(a=1, b=2)
except Exception as e:
    message = f"issue in file : file 1\n time : {datetime.now().strftime('%H:%M:%S')}\ncc: <@U0ARB6NF1S7>"
    send_message(message)

message = f"stop running : file 1\n time : {datetime.now().strftime('%H:%M:%S')}\ncc: <@U0ARB6NF1S7>"
send_message(message)
# from playwright.sync_api import sync_playwright
# import time
# import random
#
# def human_delay(a=1.0, b=3.0):
#     time.sleep(random.uniform(a, b))
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(
#         headless=False,  # IMPORTANT: keep visible
#         args=[
#             "--start-maximized",
#             "--disable-blink-features=AutomationControlled"
#         ]
#     )
#
#     context = browser.new_context(
#         viewport=None,
#         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                    "AppleWebKit/537.36 (KHTML, like Gecko) "
#                    "Chrome/120.0.0.0 Safari/537.36"
#     )
#
#     page = context.new_page()
#
#     # Go to site
#     page.goto("https://portal.kern.courts.ca.gov/", timeout=60000)
#
#     # wait like a human
#     human_delay(15, 25)
#
#     # Example interaction
#     # page.click("text=Search")  # adjust selector
#
#     # Keep browser open
#     input("Press ENTER to close...")
#     browser.close()


# import time
#
# from DrissionPage import ChromiumPage, ChromiumOptions
#
# co = ChromiumOptions()
# co.headless(False)
# co.set_user_agent(
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#     '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# )
# page = ChromiumPage(co)
# page.get('https://portal.kern.courts.ca.gov/')
#
# time.sleep(15)


# from selenium import webdriver
# import undetected_chromedriver as uc
#
# from selenium.webdriver.common.by import By
# import time
#
# driver = webdriver.Chrome()
# options = uc.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--ignore-ssl-errors")
# options.add_argument("--allow-insecure-localhost")
# options.add_argument("--disable-web-security")
# driver.get("https://portal.kern.courts.ca.gov/")
#
# time.sleep(10)
#
# # Example: click "Smart Search" (inspect karke selector lena padega)
# # driver.find_element(By.XPATH, "//span[text()='Smart Search']").click()
