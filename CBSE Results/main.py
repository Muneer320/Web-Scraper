import requests
from lxml import html
from threading import Thread
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import re
import os

NAME_INITIALS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_marks(roll_no, school_no, admit_id):
    data = {
        "regno": str(roll_no),
        "sch": str(school_no),
        "admid": admit_id,
        "B2": "Submit",
        "as_sfid": ["AAAAAAW2KHzrqU6ovtFyNJfql3blC6L0ci1MGbdufq2S-nfJrzWEvZdZPO_fqcL-1UP1EqzQgQhMlng5yzmD1s0e7Ph5x4oHzIBBwp27HTNVXzafIOKgpUdMzXD2zeO4ywfgDqw=", "AAAAAAWOyNUww0f-KakO_D4QDHBUxRfRXmfJXY1fn-E3GwOJz5qWbdvtHCjR1-mWMG4nr_ETJs3rHSuMrJbTuZbIZAvYvzlJsMVvNytSnM_HG8m2mHzaZMgOw26b-KF-KHymO-0="],
        "as_fid": ["f914448d28d08fb83ead1c1ced699372b7de6e51", "218520f49f375ef87e6d64848742f8d82195e9f7"]
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Length": "439",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Host": "testservices.nic.in",
        "Origin": "https://testservices.nic.in",
        "Referer": "https://testservices.nic.in/cbseresults/class_xii_a_2024/ClassTwelfth_c_2024.htm",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "TE": "trailers",
        "Upgrade-Insecure-Requests": "1"
    }
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
        # method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    res = session.post("https://testservices.nic.in/cbseresults/class_xii_a_2024/ClassTwelfth_c_2024.asp", data=data, headers=headers, timeout=10)
    if str(roll_no) not in res.text:
        return False
    tree = html.fromstring(res.text)
    result = {"NAME": tree.xpath("/html/body/div/table[1]/tr[2]/td[2]/font/b/text()")[0]}
    marks = []
    for x in range(2, 20):
        row = tree.xpath(f"/html/body/div/div/center/table/tr[{x}]/td/font/text()")
        if len(row) == 6:
            mark = extract_numerical_part(row[4])
            result[row[1]] = mark
            marks.append(mark)
    result["AVG"] = sum(marks) / len(marks)
    return result

def save_to_csv(data, filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename, index_col='NAME')
    else:
        df = pd.DataFrame()
    new_df = pd.DataFrame([data]).set_index('NAME')
    df = pd.concat([df, new_df])
    df = df.sort_values(by='AVG', ascending=False).drop_duplicates()
    df.to_csv(filename)

def extract_numerical_part(s):
    match = re.match(r'^\d+', s)
    if match:
        return int(match.group())
    else:
        return 'nil'

def search(roll_no, school_no):
    for i in NAME_INITIALS:
        for j in NAME_INITIALS:
            admit_id = f'{i}{j}{str(roll_no)[-3:-1]}2590'
            try:
                result = get_marks(roll_no, school_no, admit_id)
            except:
                continue
            if result:
                print(result)
                save_to_csv(result, 'results.csv')
                return

def main(roll_no, school_no, n_records=200):
# def main(roll_no, school_no, n_records=2):
    threads = []
    for n in range(n_records):
        threads.append(Thread(target=search, args=(roll_no+n, school_no)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main(14629090, 25224)
    # main(int(input("Roll No.: ")), 25224)
