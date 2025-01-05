import requests
import json
import random
import time

# Token bot Telegram dan chat ID
TELEGRAM_BOT_TOKEN = '7901321743:AAERaXf1QA8yIeuXqVL4PZ6wA2QYWwGZ4MY'  # Ganti dengan token bot Anda
CHAT_ID = '6398762215'  # Ganti dengan chat ID Anda

# Fungsi untuk mengirim pesan ke Telegram dengan parse_mode
def send_message_to_telegram(message, parse_mode='MarkdownV2'):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': parse_mode  # Menambahkan parse_mode
    }
    requests.post(url, data=payload)

# Fungsi untuk menghasilkan email acak
def generate_random_email():
    first_names = [
        "John", "Jane", "Alex", "Emily", "Michael", "Sarah", 
        "David", "Laura", "Daniel", "Sophia", "Chris", "Olivia", 
        "James", "Isabella", "Robert", "Mia", "William", "Ava",
        "Matthew", "Charlotte", "Joshua", "Amelia", "Andrew", "Harper",
        "Ethan", "Ella", "Ryan", "Grace", "Jacob", "Chloe",
        "Samuel", "Lily", "Henry", "Sofia", "Jack", "Zoe",
        "Oliver", "Nora", "Lucas", "Scarlett", "Isaac", "Victoria",
        "Gabriel", "Aria", "Anthony", "Addison", "Dylan", "Aubrey",
        "Leo", "Hannah", "Nathan", "Lillian", "Caleb", "Layla"
    ]
    last_names = [
        "Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", 
        "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", 
        "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor",
        "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis",
        "Robinson", "Walker", "Young", "Allen", "King", "Wright",
        "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green"
    ]
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    username = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}"
    domain = "freesourcecodes.com"
    return f"{username}@{domain}"

# Fungsi untuk membuat akun dan mendapatkan token
def create_account_and_get_token(num_accounts):
    for account_number in range(1, num_accounts + 1):
        # Membuat email acak untuk pembuatan akun
        random_email = generate_random_email()
        password = "Asdu123"  # Gunakan password yang sama

        # Payload untuk pembuatan akun
        payload_create_account = {
            "address": random_email,
            "password": password
        }

        url_create_account = "https://api.mail.tm/accounts"
        headers_create_account = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "content-length": str(len(json.dumps(payload_create_account))),
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://mail.tm",
            "priority": "u=1, i",
            "referer": "https://mail.tm/",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        # Membuat akun
        response_create_account = requests.post(url_create_account, headers=headers_create_account, data=json.dumps(payload_create_account))

        if response_create_account.status_code == 201:
            account_data = response_create_account.json()  # Mendapatkan detail akun
            email = account_data.get("address")
            print(f"Akun berhasil dibuat dengan email : {email}")
            
            # Kirim email ke Telegram dengan nomor urutan
            message = f"Akun ke{account_number} berhasil dibuat dengan email: ` {email.replace('-', '\\-')} `"
            send_message_to_telegram(message=message, parse_mode='MarkdownV2')            
            # Sekarang, buat permintaan untuk mendapatkan token
            payload_token = {
                "address": email,
                "password": password
            }

            # URL untuk mendapatkan token
            url_token = "https://api.mail.tm/token"
            headers_token = {
                "accept": "application/json",
                "accept-encoding": "gzip, deflate, br, zstd",
                "content-length": str(len(json.dumps(payload_token))),
                "content-type": "application/json",
                "dnt": "1",
                "origin": "https://mail.tm",
                "priority": "u=1, i",
                "referer": "https://mail.tm/",
                "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            }

            # Mengirim permintaan untuk mendapatkan token
            response_token = requests.post(url_token, headers=headers_token, data=json.dumps(payload_token))

            # Memeriksa status respons saat mendapatkan token
            if response_token.status_code == 200:
                token_data = response_token.json()  # Data token yang diterima
                token = token_data.get("token")
                if token:
                    print("Token berhasil didapatkan")
                    # Sekarang, interaksi dengan API /me
                    get_me_info(token)
                else:
                    print("Token tidak ditemukan dalam respons.")
            elif response_token.status_code != 429:  # Tambahkan kondisi ini
                print(f"Gagal mendapatkan token. Status Code: {response_token.status_code}")
                print(f"Response: {response_token.text}")
        elif response_create_account.status_code != 429:  # Tambahkan kondisi ini
            print(f"Gagal membuat akun. Status Code: {response_create_account.status_code}")
            print(f"Response: {response_create_account.text}")

        time.sleep(10)  # Jeda 10 detik sebelum membuat akun berikutnya

# Fungsi untuk mengakses informasi akun dari API /me
def get_me_info(token):
    url_me = "https://api.mail.tm/me"
    headers_me = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://mail.tm",
        "referer": "https://mail.tm/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    # Mengirim permintaan untuk mendapatkan informasi akun
    response_me = requests.get(url_me, headers=headers_me)

    if response_me.status_code == 200:
        me_data = response_me.json()  # Data informasi akun
        print("Informasi akun:", me_data)
    else:
        print(f"Gagal mendapatkan informasi akun. Status Code: {response_me.status_code}")
        print(f"Response: {response_me.text}")

# Contoh penggunaan fungsi untuk membuat 10 akun
create_account_and_get_token(1000)
