import ctypes
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment keys from .env file
load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")

def fetch_nasa_apod():
    """
    Hits the NASA APOD API using an environment-loaded key, parses the data,
    and streams down the daily high-res planetary asset.
    """

    if not NASA_API_KEY:
        print("[-] Configuration Error: 'NASA_API_KEY' not found in environment layers.")
        print("[!] Make sure your local .env file exists and contains your key.")
        return None
    
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    print("[+] Safely loading credentials from .env context...")
    print("[+] Connecting to NASA Planetary API...")

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"[-] API Error: Received status code {response.status_code}")
            return None
        
        data = response.json()

        print(f"\n[ NASA APOD Info ]")
        print(f"Title: {data.get('title')}")
        print(f"Date: {data.get('date')}")
        print(f"Explanation: {data.get('explanation')[:150]}...\n")

        if data.get("media_type") != "image":
            print("[-] Today's payload is a video/article format. Skipping download.")
            return None
        
        img_url = data.get("hdurl") or data.get("url")
        if not img_url:
            print("[-] No valid image vectors mapped inside data asset payload.")
            return None
        
        print(f"[+] Streaming down high-res asset: {img_url}")

        img_response = requests.get(img_url, stream=True, timeout=15)
        if img_response.status_code == 200:
            os.makedirs("wallpapers", exist_ok=True)
            local_filename = "wallpapers/nasa_daily.jpg"

            with open(local_filename, 'wb') as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)
            
            print(f"[+] Download phase successfully closed out: {local_filename}")
            return local_filename
        
    except Exception as e:
        print(f"[-] Critical connection dropout: {e}")
        return None

def set_wallpaper(relative_image_path):
    """
    Forces Windows 11 to execute system background switches.
    """

    absolute_path = os.path.abspath(relative_image_path)

    if not os.path.exists(absolute_path):
        print(f"[-] Error: Target image not found at {absolute_path}.")
        return False
    
    try:
        # Win32 core handles
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 3)
        return bool(result)
    except Exception as e:
        print(f"[-] Call failed critical execution: {e}")
        return False
    
if __name__ == "__main__":

    downloaded_image = fetch_nasa_apod()

    if downloaded_image:
        print("[+] Forwarding resource paths to local Win32 layer...")
        if set_wallpaper(downloaded_image):
            print("[=== SUCCESS ===] Wallpaper updated to today's NASA APOD!")
        else:
            print("[-] Environment applied successfully, but Windows rejected user32 update parameters.")