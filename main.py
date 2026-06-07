import ctypes
import os
import sys

def set_wallpaper(relative_image_path):
    """
    Force Windows 11 to immediately update the desktop wallpaper to the specified image.
    """

    absolute_path = os.path.abspath(relative_image_path)

    if not os.path.exists(absolute_path):
        print(f"[-] Error: Target image not found at {absolute_path}.")
        return
    
    print(f"[+] Found image. Target absolute path: {absolute_path}")
    print("[+] Sending system update commands to Windows User32 system...")

    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02

    try:
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            absolute_path,
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
        )

        if result:
            print("[+] Success! Wallpaper updated successfully.")
            return True
        else:
            print("[-] Windows rejected the parameter update call.")
            return False
    except Exception as e:
        print(f"[-] Call failed critical execution: {e}")
        return False
    
if __name__ == "__main__":
    print("=== Phase 1: Local System Wallpaper Test ===")

    test_image = "wallpapers/default.jpg"

    set_wallpaper(test_image)