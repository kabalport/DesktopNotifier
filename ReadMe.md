pip install -r requirements.txt


pyinstaller --onefile --windowed --hidden-import=plyer.platforms.win.notification --add-data "bbomologo.png;." --add-data "desktopnotifier.ico;." --name 뽀모도로타이머 --icon=desktopnotifier.ico main.py

