import cv2
import numpy as np
import pyautogui
import time
import os
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from datetime import datetime

import keyboard
  
BASE = os.path.join(os.getcwd(), "IMG")

def load(name):
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        log(f"[LỖI] Không tìm thấy ảnh: {path}", "error")
        return None
    return cv2.imread(path, 0)

img_dua_hau = load("mua_dua_hau.png")
img_bi_ngo = load("mua_bi_ngo.png")
img_plus = load("plus.png")
img_thanhtoan = load("thanhtoan.png")
img_hat_dua_hau = load("hat_dua_hau.png")
img_hat_bi_ngo = load("hat_bi_ngo.png")

# ========== GIAO DIỆN ==========
root = tk.Tk()
root.title("TOOL GAME AUTO VIP - Alex Nguyen")
root.geometry("700x600")
root.configure(bg="#1F1F1F")

running = False
emergency_stop = False

count_dua = 0
count_bi = 0


log_box = scrolledtext.ScrolledText(root, width=80, height=20, bg="#111", fg="white", font=("Consolas", 10))
log_box.pack(pady=10)

def log(text, type="info"):
    log_colors = {
        "info": "white",
        "success": "lightgreen",
        "error": "red",
        "warn": "yellow"
    }
    log_box.insert(tk.END, text + "\n", type)
    log_box.tag_config(type, foreground=log_colors.get(type, "white"))
    log_box.see(tk.END)

def start_bot():
    global running, emergency_stop
    running = True
    emergency_stop = False
    log("🔵 BOT ĐÃ BẬT!", "success")
    threading.Thread(target=bot_loop, daemon=True).start()

def stop_bot():
    global running
    running = False
    log("🟡 BOT ĐÃ TẠM DỪNG", "warn")

def panic_stop():
    global running, emergency_stop
    running = False
    emergency_stop = True
    log("🔴 KHẨN CẤP! BOT DỪNG NGAY LẬP TỨC!", "error")

top_frame = tk.Frame(root, bg="#1F1F1F")
top_frame.pack(pady=10)

tk.Button(top_frame, text="ON", width=12, bg="#28A745", fg="white", font=("Arial", 12, "bold"), command=start_bot).grid(row=0, column=0, padx=10)
tk.Button(top_frame, text="OFF", width=12, bg="#FFC107", fg="black", font=("Arial", 12, "bold"), command=stop_bot).grid(row=0, column=1, padx=10)
tk.Button(top_frame, text="STOP NGAY!", width=12, bg="#DC3545", fg="white", font=("Arial", 12, "bold"), command=panic_stop).grid(row=0, column=2, padx=10)


count_label = tk.Label(root, text="Dưa hấu: 0    |    Bí ngô: 0", fg="cyan", bg="#1F1F1F", font=("Consolas", 14))
count_label.pack(pady=5)

def update_count():
    count_label.config(text=f"Dưa hấu: {count_dua}    |    Bí ngô: {count_bi}")


def click_if_found(template, threshold=0.72, delay=0.1):
    if template is None:
        return False

    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        x = max_loc[0] + template.shape[1] // 2
        y = max_loc[1] + template.shape[0] // 2
        pyautogui.click(x, y)
        time.sleep(delay)
        return True

    return False

def bot_loop():
    global running, emergency_stop, count_dua, count_bi
    last_switch = 0
    current_tab = "dua"

    log("🔁 BOT BẮT ĐẦU CHẠY...", "info")

    while running and not emergency_stop:
        now = time.time()
        
        if click_if_found(img_dua_hau):
            count_dua += 1
            update_count()
            log("🛒 Mua dưa hấu!", "success")
            continue

        if click_if_found(img_bi_ngo):
            count_bi += 1
            update_count()
            log("🛒 Mua bí ngô!", "success")
            continue

        if click_if_found(img_plus):
            log("➕ Bấm +", "info")
            continue

        if click_if_found(img_thanhtoan):
            log("💳 Thanh toán!", "success")
            continue

        if now - last_switch >= 10:
            if current_tab == "dua":
                if click_if_found(img_hat_bi_ngo):
                    log("🔄 Chuyển sang tab Bí Ngô", "info")
                    current_tab = "bi"
            else:
                if click_if_found(img_hat_dua_hau):
                    log("🔄 Chuyển sang tab Dưa Hấu", "info")
                    current_tab = "dua"

            last_switch = now

        time.sleep(0.2)

    log("⛔ BOT ĐÃ DỪNG!", "warn")


clock_label = tk.Label(root, text="", fg="white", bg="#1F1F1F", font=("Consolas", 12))
clock_label.pack()

def update_clock():
    now = datetime.now().strftime("%H:%M:%S  -  %d/%m/%Y")
    clock_label.config(text=now)
    root.after(500, update_clock)

update_clock()

footer = tk.Label(root, text="Tool được viết bởi Alex Nguyen", fg="#888", bg="#1F1F1F", font=("Arial", 10))
footer.pack(pady=10)


# ============================================================
#                    🔥 BỔ SUNG HOTKEY
# ============================================================
def hotkey_listener():
    while True:
        if keyboard.is_pressed("1"):
            start_bot()
            time.sleep(0.3)

        if keyboard.is_pressed("2"):
            stop_bot()
            time.sleep(0.3)

        if keyboard.is_pressed("space"):
            panic_stop()
            time.sleep(0.3)

threading.Thread(target=hotkey_listener, daemon=True).start()

root.mainloop()

