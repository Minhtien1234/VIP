import requests
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + """
  ███╗░░░███╗████████╗████████╗░█████╗░░█████╗░██╗░░░░░
  ████╗░████║╚══██╔══╝╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
  ██╔████╔██║░░░██║░░░░░░██║░░░██║░░██║██║░░██║██║░░░░░
  ██║╚██╔╝██║░░░██║░░░░░░██║░░░██║░░██║██║░░██║██║░░░░░
  ██║░╚═╝░██║░░░██║░░░░░░██║░░░╚█████╔╝╚█████╔╝███████╗
  ╚═╝░░░░░╚═╝░░░╚═╝░░░░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
     [•] COOKIE + PROXY CHECKER | BY MTTOOL TEAM
    """ + Style.RESET_ALL)

def check_instagram_cookie(cookie):
    try:
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }
        r = requests.get("https://www.instagram.com/api/v1/accounts/current_user/", headers=headers, timeout=10)
        if r.status_code == 200 and '"user"' in r.text:
            print(Fore.GREEN + f"[✓] LIVE INSTAGRAM COOKIE: {cookie[:60]}...")
            with open("cookielive.txt", "a") as f:
                f.write(cookie + "\n")
        else:
            raise Exception("DIE")
    except:
        print(Fore.RED + f"[✗] DIE INSTAGRAM COOKIE: {cookie[:60]}...")
        with open("cookiedie.txt", "a") as f:
            f.write(cookie + "\n")

def check_facebook_cookie(cookie):
    try:
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        if "useragent=" in cookie:
            try:
                parts = cookie.split("useragent=")
                cookie = parts[0].strip()
                ua_raw = parts[1].split(";")[0]
                ua = requests.utils.unquote(ua_raw)
            except:
                pass

        headers = {
            "cookie": cookie,
            "user-agent": ua
        }

        r = requests.get("https://www.facebook.com/", headers=headers, timeout=10)
        if "c_user" in r.text or "home_icon" in r.text or "feed" in r.text:
            print(Fore.GREEN + f"[✓] LIVE FACEBOOK COOKIE: {cookie[:60]}...")
            with open("cookielive.txt", "a") as f:
                f.write(cookie + "\n")
        else:
            raise Exception("DIE")
    except:
        print(Fore.RED + f"[✗] DIE FACEBOOK COOKIE: {cookie[:60]}...")
        with open("cookiedie.txt", "a") as f:
            f.write(cookie + "\n")

def check_proxy(proxy):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
        if r.status_code == 200:
            print(Fore.GREEN + f"[✓] LIVE PROXY: {proxy}")
            with open("proxylive.txt", "a") as f:
                f.write(proxy + "\n")
        else:
            raise Exception("DIE")
    except:
        print(Fore.RED + f"[✗] DIE PROXY: {proxy}")
        with open("proxydie.txt", "a") as f:
            f.write(proxy + "\n")

def main():
    banner()
    print(Fore.YELLOW + "[1] Check Instagram Cookie")
    print("[2] Check Proxy HTTP/S")
    print("[3] Check cả Cookie Instagram + Proxy")
    print("[4] Check Facebook Cookie")
    choice = input(Fore.CYAN + "\n[•] Chọn chế độ (1/2/3/4): ").strip()

    if choice not in ["1", "2", "3", "4"]:
        print(Fore.RED + "[!] Lựa chọn không hợp lệ!")
        return

    print(Fore.MAGENTA + "\n[•] Nhập từng dòng cookie hoặc proxy. Gõ 'exit' để thoát.\n")

    while True:
        user_input = input(Fore.CYAN + "[•] Nhập dữ liệu: ").strip()
        if user_input.lower() == "exit":
            print(Fore.YELLOW + "\n[•] Đã thoát. File kết quả đã được lưu.")
            break

        if choice == "1":
            check_instagram_cookie(user_input)
        elif choice == "2":
            check_proxy(user_input)
        elif choice == "3":
            if "sessionid=" in user_input and "ds_user_id=" in user_input:
                check_instagram_cookie(user_input)
            elif ":" in user_input and "." in user_input:
                check_proxy(user_input)
            else:
                print(Fore.LIGHTYELLOW_EX + "[!] Không nhận diện được cookie/proxy hợp lệ!")
        elif choice == "4":
            check_facebook_cookie(user_input)

if __name__ == "__main__":
    main()
