import os
import time
import random
import sys
import base64
import json
import requests
import pytz
import cairosvg
from datetime import datetime
from colorama import Fore, Style, init

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class OPNFaucetBot:
    def __init__(self):
        self.url_captcha = "https://faucet.iopn.tech/api/faucet/captcha"
        self.url_claim = "https://faucet.iopn.tech/api/faucet/claim"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://faucet.iopn.tech",
            "referer": "https://faucet.iopn.tech/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
    
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}iOPNFAUCET AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self):
        delay = random.randint(2, 5)
        self.log(f"Delay {delay} seconds...", "INFO")
        time.sleep(delay)

    def load_file(self, filename):
        if not os.path.exists(filename):
            if filename == "proxy.txt":
                return []
            print(f"{Fore.RED}File {filename} not found!{Style.RESET_ALL}")
            sys.exit()
        
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines

    def format_proxy(self, proxy_str):
        if not proxy_str:
            return None
        
        parts = proxy_str.split(':')
        if len(parts) == 4 and "://" not in proxy_str:
            return {
                "http": f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}",
                "https": f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            }

        if "://" not in proxy_str:
            proxy_str = f"http://{proxy_str}"
            
        return {
            "http": proxy_str,
            "https": proxy_str
        }

    def svg_to_base64(self, svg_string):
        try:
            png_data = cairosvg.svg2png(bytestring=svg_string.encode('utf-8'))
            return base64.b64encode(png_data).decode('utf-8')
        except Exception as e:
            self.log(f"SVG Conversion Error: {e}", "ERROR")
            return None

    def solve_2captcha(self, api_key, base64_image):
        url_in = "http://2captcha.com/in.php"
        payload = {
            'key': api_key,
            'method': 'base64',
            'body': base64_image,
            'json': 1,
            'minLength': 5,
            'maxLength': 7
        }

        self.log("Sending captcha to 2captcha...", "INFO")
        try:
            resp = requests.post(url_in, data=payload).json()
            if resp['status'] == 0:
                self.log(f"2captcha Reject: {resp['request']}", "ERROR")
                return None
            task_id = resp['request']
        except Exception as e:
            self.log(f"2captcha Connection Error: {e}", "ERROR")
            return None

        url_res = "http://2captcha.com/res.php"
        self.log("Waiting for answer...", "INFO")
        
        for _ in range(20):
            time.sleep(5)
            try:
                check = requests.get(url_res, params={'key': api_key, 'action': 'get', 'id': task_id, 'json': 1}).json()
                if check['status'] == 1:
                    return check['request']
                elif check['request'] != "CAPCHA_NOT_READY":
                    self.log(f"2captcha Error: {check['request']}", "ERROR")
                    return None
            except:
                pass
        
        self.log("Captcha timeout", "ERROR")
        return None
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def run(self):
        self.print_banner()
        
        api_keys = self.load_file("2captcha.txt")
        if not api_keys:
            self.log("2captcha.txt is empty!", "ERROR")
            sys.exit()
        API_KEY = api_keys[0]
        
        wallets = self.load_file("address.txt")
        proxies = self.load_file("proxy.txt")
        
        choice = self.show_menu()
        
        use_proxy = False
        if choice == '1':
            use_proxy = True
            if not proxies:
                self.log("Proxy file is empty but proxy mode selected!", "ERROR")
                sys.exit()
            self.log("Running with proxy", "INFO")
        else:
            self.log("Running without proxy", "INFO")
        
        self.log(f"Loaded {len(wallets)} accounts", "INFO")
        self.log(f"Loaded {len(proxies)} proxies", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            total_accounts = len(wallets)
            
            for i, wallet in enumerate(wallets):
                self.log(f"Account #{i+1}/{total_accounts}", "INFO")
                
                session = requests.Session()
                session.headers.update(self.headers)
                
                proxy_display = "No Proxy"
                if use_proxy:
                    proxy_raw = proxies[i % len(proxies)]
                    proxy_dict = self.format_proxy(proxy_raw)
                    session.proxies.update(proxy_dict)
                    proxy_display = f"{proxy_raw[:15]}..."
                
                self.log(f"Proxy: {proxy_display}", "INFO")
                self.log(f"Wallet: {wallet[:6]}...{wallet[-4:]}", "INFO")
                
                try:
                    resp = session.get(self.url_captcha, timeout=30)
                    if resp.status_code == 200:
                        data_json = resp.json()
                        captcha_id = data_json.get('captchaId')
                        svg_raw = data_json.get('captcha')
                        
                        if captcha_id and svg_raw:
                            self.log("Captcha received, processing...", "INFO")
                            b64_png = self.svg_to_base64(svg_raw)
                            
                            if b64_png:
                                captcha_text = self.solve_2captcha(API_KEY, b64_png)
                                
                                if captcha_text:
                                    self.log(f"Solved: {captcha_text}", "SUCCESS")
                                    
                                    payload_claim = {
                                        "address": wallet,
                                        "captchaAnswer": captcha_text,
                                        "captchaId": captcha_id
                                    }
                                    
                                    claim_resp = session.post(self.url_claim, json=payload_claim, timeout=30)
                                    result = claim_resp.json()
                                    
                                    if result.get("success") == True:
                                        time_str = self.get_wib_time()
                                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Claim Success! TxHash: {result.get('txHash')}{Style.RESET_ALL}")
                                        success_count += 1
                                    else:
                                        self.log(f"Claim Failed: {result}", "ERROR")
                                else:
                                    self.log("Failed to solve captcha", "ERROR")
                            else:
                                self.log("Failed to convert SVG", "ERROR")
                        else:
                            self.log("Invalid captcha response", "ERROR")
                    else:
                        self.log(f"Failed to get captcha: {resp.status_code}", "ERROR")
                
                except Exception as e:
                    self.log(f"Error: {e}", "ERROR")
                
                session.close()
                
                if i < total_accounts - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 24 * 60 * 60 + random.randint(60, 300)
            self.countdown(wait_time)

if __name__ == "__main__":
    bot = OPNFaucetBot()
    bot.run()
