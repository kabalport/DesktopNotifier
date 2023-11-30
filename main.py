from notifier import send_notification
import schedule
import time

def send_rest_notification():
    # 사용자에게 휴식을 취할 시간임을 알리는 메시지를 보냅니다.
    send_notification("휴식 시간", "잠시 쉬는 시간을 가져보세요!")

if __name__ == '__main__':
    # 매 1시간마다 휴식 알림 설정
    schedule.every(1).hours.do(send_rest_notification)

    # 테스트용: 매 10초마다 알림 설정
    schedule.every(10).seconds.do(lambda: send_notification("테스트 알림", "10초마다 오는 테스트 메시지입니다."))

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("프로그램이 사용자에 의해 중지되었습니다.")
