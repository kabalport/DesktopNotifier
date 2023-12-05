pip install -r requirements.txt


pyinstaller --onefile --windowed --hidden-import=plyer.platforms.win.notification main.py
