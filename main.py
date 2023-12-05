import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import time
from threading import Thread
from winsound import Beep

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")

        self.load_settings()
        self.setup_gui()
        self.running = False
        self.session_count = 0
        self.current_time = 0

    def load_settings(self):
        try:
            with open('settings.json', 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {
                "work_duration": 1500,  # 25 minutes
                "rest_duration": 300,   # 5 minutes
                "long_rest_duration": 900,  # 15 minutes
                "long_rest_interval": 4
            }

    def save_settings(self):
        with open('settings.json', 'w') as file:
            json.dump(self.settings, file)

    def setup_gui(self):
        self.timer_label = tk.Label(self.master, text="25:00", font=("Arial", 48))
        self.timer_label.pack()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.settings_button = tk.Button(self.master, text="Settings", command=self.open_settings)
        self.settings_button.pack()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.session_count = 0
            Thread(target=self.run_timer).start()

    def run_timer(self):
        while self.running:
            self.current_time = self.settings["work_duration"]
            self.session_count += 1

            self.show_message("작업 시간 시작", "집중해서 작업할 시간입니다!")
            while self.current_time > 0 and self.running:
                self.update_timer()

            if self.running:
                self.play_sound()
                self.show_message("휴식 시간 시작", "휴식 시간입니다! 잠시 쉬어 가세요.")

                if self.session_count % self.settings["long_rest_interval"] == 0:
                    self.current_time = self.settings["long_rest_duration"]
                else:
                    self.current_time = self.settings["rest_duration"]

                while self.current_time > 0 and self.running:
                    self.update_timer()

                if self.running:
                    self.play_sound()

    def update_timer(self):
        mins, secs = divmod(self.current_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.update_label(time_format)
        time.sleep(1)
        self.current_time -= 1

    def update_label(self, time_format):
        self.timer_label.config(text=time_format)
        self.timer_label.update()

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def open_settings(self):
        new_work_duration = simpledialog.askinteger("Settings", "Work Duration (seconds)",
                                                    initialvalue=self.settings["work_duration"])
        new_rest_duration = simpledialog.askinteger("Settings", "Rest Duration (seconds)",
                                                    initialvalue=self.settings["rest_duration"])
        new_long_rest_duration = simpledialog.askinteger("Settings", "Long Rest Duration (seconds)",
                                                         initialvalue=self.settings["long_rest_duration"])
        new_long_rest_interval = simpledialog.askinteger("Settings", "Long Rest Interval (sessions)",
                                                         initialvalue=self.settings["long_rest_interval"])

        if new_work_duration and new_rest_duration and new_long_rest_duration and new_long_rest_interval:
            self.settings = {
                "work_duration": new_work_duration,
                "rest_duration": new_rest_duration,
                "long_rest_duration": new_long_rest_duration,
                "long_rest_interval": new_long_rest_interval
            }
            self.save_settings()

    def play_sound(self):
        Beep(2500, 1000)  # Beep at 2500 Hz for 1000 ms

if __name__ == '__main__':
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
