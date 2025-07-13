import os
import json
import time
import uuid
import cloudscraper
import re

# === CONFIG ===
COOKIE_FILE_TXT = "mycookie.txt"
COOKIE_FILE_JSON = "ig_cookie.json"

def build_cookie_string(session, user_agent):
    cookie_dict = session.cookies.get_dict()
    cookie_dict.update({
        "ig_nrcb": "1",
        "ps_l": "1",
        "ps_n": "1",
        "wd": "1920x1080",
        "useragent": user_agent,
        "_uafec": cloudscraper.requests.utils.quote(user_agent),
    })
    return "; ".join(f"{k}={v}" for k, v in cookie_dict.items())

def save_cookies(cookie_str, cookie_dict):
    with open(COOKIE_FILE_TXT, "a", encoding="utf-8") as f:
        f.write(cookie_str + "\n\n\n")
    with open(COOKIE_FILE_JSON, "w", encoding="utf-8") as f:
        json.dump(cookie_dict, f, indent=2)

def handle_challenge(scraper, challenge_url):
    print("[!] Phát hiện checkpoint hoặc 2FA")
    full_url = "https://www.instagram.com" + challenge_url
    try:
        json_api_url = full_url.replace("/challenge/", "/challenge/api/")
        response = scraper.get(json_api_url)

        try:
            j = response.json()
        except ValueError:
            print("[!] Instagram không trả về JSON hợp lệ, có thể bị redirect hoặc chặn!")
            print("[i] Response text (rút gọn):", response.text[:300])
            return False

        step_name = j.get("step_name", "unknown")

        if step_name == "whatsapp":
            print("[!] Xác minh WhatsApp được yêu cầu, đang chuyển sang xác minh bằng số điện thoại...")
            change_resp = scraper.post(json_api_url, data={"choice": 1})
            if not change_resp.ok:
                print("[!] Không thể chuyển sang xác minh bằng số điện thoại!")
                return False

        print(f"[!] Loại xác minh: {step_name.capitalize()}")

        code = input("Nhập mã xác minh được gửi tới ở trên: ").strip()
        data = {'security_code': code}
        scraper.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        verify = scraper.post(full_url, data=data)
        return verify.ok
    except Exception as e:
        print(f"[!] Lỗi khi xử lý checkpoint: {e}")
        return False

def login_instagram(username, password):
    scraper = cloudscraper.create_scraper(browser={"custom": "Chrome/138.0.0.0"})
    user_agent = scraper.headers['User-Agent']

    scraper.headers.update({
        "Referer": "https://www.instagram.com/accounts/login/",
        "Origin": "https://www.instagram.com"
    })

    try:
        scraper.get("https://www.instagram.com/accounts/login/")
        csrf = scraper.cookies.get("csrftoken")
        x_ajax = uuid.uuid4().hex[:12]
    except Exception as e:
        return False, f"Không thể kết nối: {e}"

    scraper.headers.update({
        "X-CSRFToken": csrf,
        "X-Requested-With": "XMLHttpRequest",
        "X-Instagram-Ajax": x_ajax,
        "X-IG-App-ID": "936619743392459",
        "X-ASBD-ID": "198387",
        "X-IG-WWW-Claim": "0",
        "Content-Type": "application/x-www-form-urlencoded",
    })

    enc_pw = f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}"
    data = {
        "username": username,
        "enc_password": enc_pw,
        "queryParams": "{}",
        "optIntoOneTap": "false",
        "stopDeletionNonce": "",
        "trustedDeviceRecords": "{}"
    }

    try:
        res = scraper.post("https://www.instagram.com/accounts/login/ajax/", data=data)
        j = res.json()
    except Exception as e:
        return False, f"Không thể gửi login: {e}"

    if j.get("authenticated"):
        cookie_str = build_cookie_string(scraper, user_agent)
        save_cookies(cookie_str, scraper.cookies.get_dict())
        return True, cookie_str
    elif j.get("message") == "checkpoint_required":
        challenge_url = j.get("checkpoint_url")
        if handle_challenge(scraper, challenge_url):
            cookie_str = build_cookie_string(scraper, user_agent)
            save_cookies(cookie_str, scraper.cookies.get_dict())
            return True, cookie_str
        else:
            return False, "Không thể vượt qua xác minh!"
    else:
        return False, json.dumps(j, indent=2)

# === CLI MODE ===
def cli_mode():
    print("\n[+] Instagram Cookie Tool (CLI Mode)")
    try:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        success, result = login_instagram(username, password)
        if success:
            print("\n[✓] Login thành công! Cookie:")
            print(result)
            time.sleep(5)  # Đợi 5 giây sau khi in cookie
        else:
            print("\n[✗] Login thất bại:")
            print(result)
    except KeyboardInterrupt:
        print("\n[!] Đã hủy.")

# === Main launcher ===
def main():
    cli_mode()

if __name__ == '__main__':
    main()
