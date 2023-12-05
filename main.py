import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import time
from threading import Thread
import winsound
from plyer import notification

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")

        self.load_settings()
        self.setup_gui()
        self.running = False
        self.session_count = 0
        self.current_time = 0
        self.timer_thread = None
        self.settings_changed = False

    def load_settings(self):
        try:
            with open('settings.json', 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {
                "work_duration": 1500,
                "rest_duration": 300,
                "long_rest_duration": 900,
                "long_rest_interval": 4
            }

    def save_settings(self):
        with open('settings.json', 'w') as file:
            json.dump(self.settings, file)

    def setup_gui(self):
        self.timer_label = tk.Label(self.master, text=self.format_time(self.settings["work_duration"]), font=("Arial", 48))
        self.timer_label.pack()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_timer)
        self.stop_button.pack()

        self.work_duration_label = tk.Label(self.master, text=f"작업 시간: {self.format_time(self.settings['work_duration'])}")
        self.work_duration_label.pack()

        self.rest_duration_label = tk.Label(self.master, text=f"휴식 시간: {self.format_time(self.settings['rest_duration'])}")
        self.rest_duration_label.pack()

        self.long_rest_duration_label = tk.Label(self.master, text=f"긴 휴식 시간: {self.format_time(self.settings['long_rest_duration'])}")
        self.long_rest_duration_label.pack()

        self.long_rest_interval_label = tk.Label(self.master, text=f"긴 휴식 간격: {self.settings['long_rest_interval']}")
        self.long_rest_interval_label.pack()

        self.settings_button = tk.Button(self.master, text="Settings", command=self.open_settings_window)
        self.settings_button.pack()

    def open_settings_window(self):
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")
        # 부모 창 비활성화
        self.settings_window.grab_set()

        # 스타일 설정
        self.settings_window.configure(bg='lightgray')

        # 작업 시간 설정
        tk.Label(self.settings_window, text="작업 시간 (분:초):", bg='lightgray').grid(row=0, column=0, sticky='w')
        self.work_duration_minutes_entry = tk.Entry(self.settings_window, width=3)
        self.work_duration_seconds_entry = tk.Entry(self.settings_window, width=3)
        self.work_duration_minutes_entry.insert(0, self.settings["work_duration"] // 60)
        self.work_duration_seconds_entry.insert(0, self.settings["work_duration"] % 60)
        self.work_duration_minutes_entry.grid(row=0, column=1)
        tk.Label(self.settings_window, text=":", bg='lightgray').grid(row=0, column=2)
        self.work_duration_seconds_entry.grid(row=0, column=3)

        # 휴식 시간 설정
        tk.Label(self.settings_window, text="휴식 시간 (분:초):", bg='lightgray').grid(row=1, column=0, sticky='w')
        self.rest_duration_minutes_entry = tk.Entry(self.settings_window, width=3)
        self.rest_duration_seconds_entry = tk.Entry(self.settings_window, width=3)
        self.rest_duration_minutes_entry.insert(0, self.settings["rest_duration"] // 60)
        self.rest_duration_seconds_entry.insert(0, self.settings["rest_duration"] % 60)
        self.rest_duration_minutes_entry.grid(row=1, column=1)
        tk.Label(self.settings_window, text=":", bg='lightgray').grid(row=1, column=2)
        self.rest_duration_seconds_entry.grid(row=1, column=3)

        # 긴 휴식 시간 설정
        tk.Label(self.settings_window, text="긴 휴식 시간 (분:초):", bg='lightgray').grid(row=2, column=0, sticky='w')
        self.long_rest_duration_minutes_entry = tk.Entry(self.settings_window, width=3)
        self.long_rest_duration_seconds_entry = tk.Entry(self.settings_window, width=3)
        self.long_rest_duration_minutes_entry.insert(0, self.settings["long_rest_duration"] // 60)
        self.long_rest_duration_seconds_entry.insert(0, self.settings["long_rest_duration"] % 60)
        self.long_rest_duration_minutes_entry.grid(row=2, column=1)
        tk.Label(self.settings_window, text=":", bg='lightgray').grid(row=2, column=2)
        self.long_rest_duration_seconds_entry.grid(row=2, column=3)

        # 긴 휴식 간격 설정
        tk.Label(self.settings_window, text="긴 휴식 간격:", bg='lightgray').grid(row=3, column=0, sticky='w')
        self.long_rest_interval_entry = tk.Entry(self.settings_window)
        self.long_rest_interval_entry.insert(0, self.settings["long_rest_interval"])
        self.long_rest_interval_entry.grid(row=3, column=1, columnspan=3)

        # 설정 저장 버튼
        save_button = tk.Button(self.settings_window, text="Save Settings", command=self.save_new_settings, bg='blue',
                                fg='white')
        save_button.grid(row=4, column=0, columnspan=4, pady=10)

    def save_new_settings(self):
        try:
            # 작업 시간, 휴식 시간, 긴 휴식 시간, 긴 휴식 간격 설정값을 가져옵니다.
            new_work_duration = int(self.work_duration_minutes_entry.get()) * 60 + int(
                self.work_duration_seconds_entry.get())
            new_rest_duration = int(self.rest_duration_minutes_entry.get()) * 60 + int(
                self.rest_duration_seconds_entry.get())
            new_long_rest_duration = int(self.long_rest_duration_minutes_entry.get()) * 60 + int(
                self.long_rest_duration_seconds_entry.get())
            new_long_rest_interval = int(self.long_rest_interval_entry.get())

            # 설정값을 업데이트합니다.
            self.settings = {
                "work_duration": new_work_duration,
                "rest_duration": new_rest_duration,
                "long_rest_duration": new_long_rest_duration,
                "long_rest_interval": new_long_rest_interval
            }

            # 설정을 저장합니다.
            self.save_settings()

            # 레이블을 새로운 설정값으로 업데이트합니다.
            self.work_duration_label.config(text=f"작업 시간: {self.format_time(new_work_duration)}")
            self.rest_duration_label.config(text=f"휴식 시간: {self.format_time(new_rest_duration)}")
            self.long_rest_duration_label.config(text=f"긴 휴식 시간: {self.format_time(new_long_rest_duration)}")
            self.long_rest_interval_label.config(text=f"긴 휴식 간격: {new_long_rest_interval}")

            # 변경 사항 저장 플래그를 리셋합니다.
            self.settings_changed = False

            # 레이블 업데이트
            self.timer_label.config(text=self.format_time(new_work_duration))
            self.update_labels(new_work_duration, new_rest_duration, new_long_rest_duration, new_long_rest_interval)

            messagebox.showinfo("Settings Saved", "세팅 저장완료")
            # 설정 창 닫기
            self.settings_window.destroy()
            self.settings_changed = False
        except ValueError:
            messagebox.showerror("Error", "유효한 숫자를 입력해주세요.")

    def update_labels(self, work_duration, rest_duration, long_rest_duration, long_rest_interval):
        self.work_duration_label.config(text=f"작업 시간: {self.format_time(work_duration)}")
        self.rest_duration_label.config(text=f"휴식 시간: {self.format_time(rest_duration)}")
        self.long_rest_duration_label.config(text=f"긴 휴식 시간: {self.format_time(long_rest_duration)}")
        self.long_rest_interval_label.config(text=f"긴 휴식 간격: {long_rest_interval}")

    def start_timer(self):
        if not self.running:
            self.running = True
            self.session_count = 0
            self.timer_thread = Thread(target=self.run_timer)
            self.timer_thread.start()

    def stop_timer(self):
        self.running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()

    def run_timer(self):
        try:
            while self.running:
                # 작업 시간 타이머
                self.current_time = self.settings["work_duration"]
                self.session_count += 1

                self.show_message("작업 시간 시작", "집중해서 작업할 시간입니다!")
                while self.current_time > 0 and self.running:
                    self.update_timer()

                if self.running:
                    # 휴식 시간 타이머
                    if self.session_count % self.settings["long_rest_interval"] == 0:
                        self.current_time = self.settings["long_rest_duration"]
                        self.show_message("긴 휴식 시간 시작", "긴 휴식 시간입니다! 잠시 쉬어 가세요.")
                    else:
                        self.current_time = self.settings["rest_duration"]
                        self.show_message("휴식 시간 시작", "휴식 시간입니다! 잠시 쉬어 가세요.")

                    while self.current_time > 0 and self.running:
                        self.update_timer()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.running = False

    def update_timer(self):
        self.current_time -= 1
        mins, secs = divmod(self.current_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.update_label(time_format)
        time.sleep(1)

    def update_label(self, time_format):
        self.timer_label.config(text=time_format)
        self.timer_label.update()

    def show_message(self, title, message):
        notification.notify(title=title, message=message, app_name='Pomodoro Timer', timeout=10)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins}분 {secs}초"

    def check_unsaved_changes(self):
        if self.settings_changed:
            if messagebox.askyesno("변경사항 저장", "변경사항을 저장하시겠습니까?"):
                self.save_settings()
                self.settings_changed = False

    def close_app(self):
        self.check_unsaved_changes()
        self.running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        self.save_settings()
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = PomodoroApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
