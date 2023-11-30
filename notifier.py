from win10toast import ToastNotifier

toaster = ToastNotifier()

def send_notification(title, message):
    toaster.show_toast(title, message, duration=10)
