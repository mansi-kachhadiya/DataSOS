import os
import time
import queue
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from DrissionPage import ChromiumPage, ChromiumOptions
from parsel import Selector

import mytheresa.db_config as db
# message = "Running start for records :30001 to 64000"
#
# db.send_message(message)
# ================= GLOBAL =================
save_path = r"E:\Mansi\pagesave\MYTHERESA\pdp_pagesave\202604"
os.makedirs(save_path, exist_ok=True)

global_status = []
lock = threading.Lock()
BATCH_SIZE = 5

# ================= SAVE FUNCTION =================
def pagesave(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

# ================= SQL BULK UPDATE =================
def update_status():
    global global_status
    try:
        conn, cur = db.connection_()

        if not global_status:
            print("No updates...")
            return
        # Take only BATCH_SIZE records at a time
        batch = global_status[:BATCH_SIZE]
        remaining = global_status[BATCH_SIZE:]
        if not batch:
            return

        # for status, hash_key in global_status:
        query = f"""
            UPDATE {db.unique_pdp_url}
            SET status=%s
            WHERE hash_key_pdp=%s
        """
            # cur.execute(query, (status, hash_key))
        cur.executemany(query, batch)
        conn.commit()
        print(f"Updated {len(global_status)} records")
        # Update global list
        global_status[:] = remaining

    except Exception as e:
        print(f"DB Error: {e}")

# ================= WORKER =================
def worker(browser, tab_id, q):
    tab = browser.new_tab()
    print(f"[Tab {tab_id}] Started")

    while True:
        try:
            url, hash_key = q.get_nowait()
        except queue.Empty:
            print(f"[Tab {tab_id}] Done")
            tab.close()
            return

        print(f"[Tab {tab_id}] Processing: {hash_key}")

        try:
            tab.listen.start()

            tab.get(url)
            time.sleep(random.uniform(8, 10))

            packets_data = []

            while True:
                packets = tab.listen.wait(timeout=5)
                if not packets:
                    break

                if isinstance(packets, list):
                    packets_data.extend(packets)
                else:
                    packets_data.append(packets)

            tab.listen.stop()

            found = False

            for pkg in packets_data:
                if not pkg or not hasattr(pkg, "url"):
                    continue

                if url in pkg.url:
                    text = pkg.response.raw_body
                    sel = Selector(text)

                    raw_json = sel.xpath(
                        "//script[contains(text(),'window.__PRELOADED_STATE__')]//text()"
                    ).get()

                    if raw_json:
                        filename = f"{save_path}\\{hash_key}.html"
                        pagesave(text, filename)

                        with lock:
                            global_status.append(("done", hash_key))

                        print(f"[Tab {tab_id}] ✅ Saved {hash_key}")
                        found = True
                        break

            if not found:
                with lock:
                    global_status.append(("error", hash_key))

                print(f"[Tab {tab_id}] ❌ Data not found")
            if len(global_status) >= BATCH_SIZE:
                update_status()
        except Exception as e:
            print(f"[Tab {tab_id}] Error: {e}")
            with lock:
                global_status.append(("error", hash_key))
            if len(global_status) >= BATCH_SIZE:
                update_status()

        finally:
            q.task_done()

# ================= MAIN =================
def main():
    conn, cur = db.connection_()

    # Fetch pending URLs
    query = f"SELECT product_url, hash_key_pdp FROM {db.unique_pdp_url} WHERE status='pending' and id between 30001 and 66000"
    cur.execute(query)
    records = cur.fetchall()

    if not records:
        print("No data found")
        return

    # Create queue
    q = queue.Queue()

    for row in records:
        q.put((row["product_url"], row["hash_key_pdp"]))

    print(f"Total URLs: {q.qsize()}")

    # ================= BROWSERS =================
    ports = [9969, 9979, 9989, 9999]
    # ports = [9222, 9223, 9224, 9225]
    browsers = []
    for port in ports:
        co = ChromiumOptions().set_local_port(port)
        co.set_argument("--disable-infobars")
        co.set_argument("--no-sandbox")
        browsers.append(ChromiumPage(addr_or_opts=co))

    # ================= THREADS =================
    tabs_per_browser = 2   # safer than 15
    total_workers = len(browsers) * tabs_per_browser

    print(f"Starting {total_workers} workers...")

    start = time.time()

    with ThreadPoolExecutor(max_workers=total_workers) as executor:
        for browser in browsers:
            for i in range(tabs_per_browser):
                executor.submit(worker, browser, i+1, q)

        q.join()

    # ================= UPDATE SQL =================
    if global_status:
        print(f"Final batch update: {len(global_status)} records remaining")
        update_status()
    # update_status()

    print(f"Completed in {time.time() - start:.2f} seconds")


if __name__ == "__main__":
    main()




# from DrissionPage import ChromiumPage, ChromiumOptions
# from parsel import Selector
# import random
# from concurrent.futures import ThreadPoolExecutor
# from queue import Queue
# from parsel import Selector
# import threading ,time ,os ,random
# import mytheresa.db_config as db
# def process_data(port):
#     save_path = fr"G:\pagesave\MYTHERESA\pdp_pagesave\202604"
#     os.makedirs(save_path)
#
#     batch_file = 500
#     lat_id = 0
#     conn , cur = db.connection_()
#     all_packets = []
#     query = f"select * from {db.unique_pdp_url} where status='pending'"
#     cur.execute(query)
#     records = cur.fetchall()
#     co = ChromiumOptions().auto_port()
#     co.set_argument("--disable-infobars")
#     co.set_argument("--no-sandbox")
#     scroll_random_list = random.uniform(800,900)
#     page = ChromiumPage(addr_or_opts=co).latest_tab
#
#     for data in records:
#         page.listen.start()
#         url = data["product_url"]
#         hash_key_pdp = data["hash_key_pdp"]
#         print("Opening page...")
#         page.get(url)
#         time.sleep(random.uniform(8,10))
#
#         while True:
#             try:
#                 packets = page.listen.wait(timeout=2)
#                 if not packets:break
#
#                 if isinstance(packets,list):
#                     all_packets.extend(packets)
#                 else:
#                     all_packets.append(packets)
#             except Exception as e:
#                 print(str(e))
#         page.listen.stop()
#
#         for pkg in all_packets:
#             if not pkg or not hasattr(pkg,"url"):continue
#             if url in pkg.url:
#                 text = pkg.response.raw_body
#                 res = Selector(text)
#                 raw_json = res.xpath("//script[contains(text(), 'window.__PRELOADED_STATE__')]//text()").get()
#                 if raw_json:
#                     with open(fr"{save_path}\{hash_key_pdp}.html", 'w', encoding='utf-8') as f:
#                         f.write(text)
#                     print("Page Saved...")
#                     update_query = f"update {db.unique_pdp_url} set status='done' where hash_key_pdp='{hash_key_pdp}'"
#
# #===============================================================================================
