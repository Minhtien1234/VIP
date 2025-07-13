import os
import json
import time
import uuid
import cloudscraper
import random
import re
import requests

# === CONFIG ===
COOKIE_FILE_TXT = "mycookie.txt"
COOKIE_FILE_JSON = "ig_cookie.json"

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1"
]

def print_logo():
    logo = r'''
[i] ███╗   ███╗████████╗████████╗ ██████╗  ██████╗ ██╗     ██╗
[i] ████╗ ████║╚══██╔══╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║
[i] ██╔████╔██║   ██║      ██║   ██║   ██║██║   ██║██║     ██║
[i] ██║╚██╔╝██║   ██║      ██║   ██║   ██║██║   ██║██║     ██║
[i] ██║ ╚═╝ ██║   ██║      ██║   ╚██████╔╝╚██████╔╝███████╗███████╗
[i] ╚═╝     ╚═╝   ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
    '''
    print("\033[1;34m" + logo + "\033[0m")

# ===================== NEW FEATURE: Facebook Login via TK+MK =====================
def login_facebook(username, password):
    session = requests.Session()
    headers = {
        "User-Agent": USER_AGENTS[0],
        "Referer": "https://mbasic.facebook.com/login",
    }
    session.headers.update(headers)

    login_url = "https://mbasic.facebook.com/login"
    r = session.get(login_url)
    lsd = re.search(r'name=\"lsd\" value=\"(.*?)\"', r.text)
    jazoest = re.search(r'name=\"jazoest\" value=\"(.*?)\"', r.text)

    if not lsd or not jazoest:
        return False, "[!] Không lấy được token đăng nhập"

    payload = {
        "lsd": lsd.group(1),
        "jazoest": jazoest.group(1),
        "email": username,
        "pass": password,
        "login": "Đăng nhập"
    }

    res = session.post("https://mbasic.facebook.com/login", data=payload)

    if "c_user" in session.cookies.get_dict():
        cookie_str = "; ".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()])
        return True, cookie_str
    elif "checkpoint" in res.url:
        return False, "[WARN] Checkpoint! Cần xác minh."
    else:
        return False, "[✗] Sai tài khoản hoặc mật khẩu."

# ===================== Check Cookie Live =====================
def check_cookie_live(cookie_str):
    session = requests.Session()
    headers = {
        "User-Agent": USER_AGENTS[0],
        "Cookie": cookie_str,
        "Referer": "https://www.facebook.com/",
    }
    session.headers.update(headers)

    try:
        res = session.get("https://www.facebook.com/settings", allow_redirects=False)
        if res.status_code == 200 and "c_user" in cookie_str:
            return True
        return False
    except:
        return False

# ===================== Convert Cookie Basic to Cookie Xịn =====================
def upgrade_cookie_string(cookie_str, platform="fb"):
    if not check_cookie_live(cookie_str):
        return "[✗] Cookie không hợp lệ hoặc đã hết hạn."

    session = requests.Session()
    headers = {
        "User-Agent": USER_AGENTS[0],
        "Cookie": cookie_str,
        "Referer": "https://www.facebook.com/",
    }
    session.headers.update(headers)

    try:
        res = session.get("https://www.facebook.com/")
        cookie_dict = session.cookies.get_dict()
        cookie_str_updated = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
        extras = {
            "ps_l": "1",
            "ps_n": "1",
            "wd": "750x1334",
            "ig_nrcb": "1",
            "useragent": USER_AGENTS[0],
            "_uafec": USER_AGENTS[0].replace(" ", "%20")
        }
        return cookie_str_updated + "; " + "; ".join([f"{k}={v}" for k, v in extras.items()])
    except Exception as e:
        return f"[!] Lỗi khi nâng cấp cookie: {str(e)}"

# ===================== CLI Menu Update =====================
def cli_mode():
    while True:
        print_logo()
        print("[i] Instagram & Facebook Cookie Tool (CLI Mode)")
        try:
            print("[1] Lấy cookie Instagram")
            print("[2] Kiểm tra cookie IG sống/chết")
            print("[3] Kiểm tra cookie Facebook sống/chết")
            print("[4] Kiểm tra proxy")
            print("[5] Lấy cookie Facebook từ tài khoản mật khẩu")
            print("[6] Nâng cấp cookie thường ➜ cookie xịn (thực tế)*)")
            opt = input("[i] Chọn chức năng: ").strip()

            if opt == "1":
                print("[!] Chức năng này hiện chưa có trong bản này!")

            elif opt == "2":
                print("[!] Chức năng này hiện chưa có trong bản này!")

            elif opt == "3":
                raw = input("[i] Nhập cookie Facebook: ")
                if check_cookie_live(raw):
                    print("[✓] Cookie LIVE!")
                else:
                    print("[✗] Cookie DIE hoặc không hợp lệ!")

            elif opt == "4":
                print("[!] Chức năng này hiện chưa có trong bản này!")

            elif opt == "5":
                username = input("[i] Email/Username FB: ").strip()
                password = input("[i] Password FB: ").strip()
                success, cookie = login_facebook(username, password)
                if success:
                    print("[✓] Login Facebook thành công!")
                    print(cookie)
                else:
                    print(cookie)

            elif opt == "6":
                raw = input("[i] Nhập cookie thường: ")
                result = upgrade_cookie_string(raw)
                print("[✓] Cookie nâng cấp xịn:")
                print(result)

            else:
                print("[!] Lựa chọn không hợp lệ!")
        except KeyboardInterrupt:
            print("\n[!] Đã thoát.")
            break

        print("\n[i] Quay lại menu sau 5 giây...")
        time.sleep(5)

if __name__ == '__main__':
    cli_mode()
