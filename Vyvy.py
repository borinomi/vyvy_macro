import pyautogui
import pyperclip
import time
import os
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import keyboard
import threading

# --- Cài đặt cơ bản ---
TIME_TO_WAIT_BEFORE_START = 3

# 스크립트 기준 절대 경로
try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()

VYVY_IMG = BASE_DIR / 'vyvy.png'
DANG_IMG = BASE_DIR / 'dang.png'
VYVY_TXT = BASE_DIR / 'vyvy.txt'

# --- 함수 정의 ---
running = True

def stop_macro():
    """매크로를 중지하는 함수"""
    global running
    running = False
    print("Hoàn thành", "Macro đã bị dừng bởi người dùng.")

def run_macro(repeat_count, gui_root, start_btn, entry_widget):
    """실제 매크로 작업을 수행하는 함수"""
    keyboard.add_hotkey('ctrl+esc', stop_macro)
    
    missing = []
    for p in [VYVY_IMG, DANG_IMG, VYVY_TXT]:
        if not p.exists():
            missing.append(str(p))

    if missing:
        print("[Error]", f"Không tìm thấy tệp/thư mục sau:\n" + "\n".join(missing))
        keyboard.remove_hotkey('ctrl+esc')
        gui_root.after(10, lambda: start_btn.config(state=tk.NORMAL))
        gui_root.after(10, lambda: entry_widget.config(state=tk.NORMAL))
        return

    print(f"Macro sẽ bắt đầu sau {TIME_TO_WAIT_BEFORE_START} giây. Di chuyển chuột đến vị trí mong muốn.")
    time.sleep(TIME_TO_WAIT_BEFORE_START)

    global running
    try:
        for i in range(repeat_count):
            if not running:
                break
            
            print(f"--- Vòng lặp {i + 1}/{repeat_count} ---")
            
            # 1) Tìm nút vyvy.png
            try:
                button_location = pyautogui.locateCenterOnScreen(str(VYVY_IMG), confidence=0.8)
                pyautogui.click(button_location)
                print("Nhấn nút thành công!")
                time.sleep(1)
            except pyautogui.ImageNotFoundException:
                print("Không tìm thấy hình ảnh nút, chuyển sang bước tiếp theo.")
                time.sleep(1)
                continue

            # 2) Dán nội dung của vyvy.txt
            if not running: break
            text_to_paste = VYVY_TXT.read_text(encoding='utf-8')
            pyperclip.copy(text_to_paste)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v')
            print("Đã dán văn bản xong.")
            time.sleep(1)

            # 5) Chuyển tab bằng cách nhấn Alt+Tab 두 번
            if not running: break
            pyautogui.keyDown('alt')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.keyUp('alt')
            print("Chuyển tab bằng Alt+Tab 2 lần xong.")
            time.sleep(0.5)

            # 2. Sao chép tệp (Ctrl+C)
            if not running: break
            print("Đang sao chép tệp đã chọn (Ctrl+C)...")
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.5)
            pyautogui.hotkey('alt', 'tab')
            time.sleep(1)

            # 3) Dán ảnh từ thư mục PHOTO
            if not running: break
            print("Đang dán tệp (Ctrl+V)...")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            print("Đã dán ảnh xong")

            # 4) Tìm nút DANG.jpg
            if not running: break
            try:
                dang_button_location = pyautogui.locateCenterOnScreen(str(DANG_IMG), confidence=0.8)
                pyautogui.click(dang_button_location)
                print("Nhấn nút DANG thành công!")
                time.sleep(1)
            except pyautogui.ImageNotFoundException:
                print("Không tìm thấy hình ảnh nút DANG, chuyển sang bước tiếp theo.")
                time.sleep(1)
                continue

            # 6) Thời gian chờ giữa các vòng lặp
            if not running: break
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(1)
            pyautogui.keyDown('alt')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.keyUp('alt')
            print("Chuyển tab bằng Alt+Tab 2 lần xong.")
            time.sleep(1)
            
    except Exception as e:
        print("[Error]", f"Lỗi không mong muốn đã xảy ra: {e}")
        time.sleep(5)
    
    keyboard.remove_hotkey('ctrl+esc')
    if running:
        print("Hoàn thành", "Đã hoàn tất macro!")
    else:
        print("Hoàn thành", "Macro đã bị dừng bởi người dùng.")

    # 매크로가 끝난 후 GUI 위젯을 다시 활성화합니다.
    gui_root.after(10, lambda: start_btn.config(state=tk.NORMAL))
    gui_root.after(10, lambda: entry_widget.config(state=tk.NORMAL))


# --- Code giao diện (GUI) ---

class TextRedirector(object):
    """stdout을 Tkinter 위젯으로 리디렉션하는 클래스"""
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
    
    def flush(self):
        pass

def start_macro():
    """매크로 시작 버튼 클릭 시 호출되는 함수"""
    global running
    running = True
    try:
        repeat_count = int(entry.get())
        if repeat_count <= 0:
            print("[Error]", "Vui lòng nhập một số nguyên dương.")
            return
        
        start_button.config(state=tk.DISABLED)
        entry.config(state=tk.DISABLED)
        
        log_text.insert(tk.END, f"Macro sẽ bắt đầu {repeat_count} lần.\n")
        log_text.insert(tk.END, "-" * 30 + "\n")
        
        root.update()
        
        # 매크로를 스레드에서 실행
        macro_thread = threading.Thread(target=run_macro, args=(repeat_count, root, start_button, entry), daemon=True)
        macro_thread.start()

    except ValueError:
        print("[Error]", "Vui lòng nhập một số hợp lệ.")

root = tk.Tk()
root.title("Cài đặt Macro")
root.geometry("450x300")

label = tk.Label(root, text="Nhập số lần lặp:")
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

start_button = tk.Button(root, text="Bắt đầu", command=start_macro)
start_button.pack(pady=5)

log_text = ScrolledText(root, wrap=tk.WORD)
log_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

sys.stdout = TextRedirector(log_text)

root.mainloop()