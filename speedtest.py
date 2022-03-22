import time
import wget
import socket
import threading
import os
import datetime

final_value = 0
count = 0


def scan_func(timer) -> float:
    global final_value, count

    for file in os.scandir('123'):
        file_size_speedtest = os.path.getsize(file)
        timer_after = datetime.datetime.now()
        real_timer = timer_after - timer
        real_timer = real_timer.seconds + real_timer.microseconds / 1000000
        file_mg = file_size_speedtest / 1024 / 1024
        megabiter = file_mg / real_timer
        megabitter = file_mg / real_timer * 8

        count += 1
        final_value += megabitter

        print('\r')
        print('speedtest: ', 'file/mb: \033[034m', file_mg, '\033[0mdown sec: \033[034m', real_timer, '\033[0m\n',
              'speedtest: ', 'MB/s: \033[034m', megabiter, '\033[0mMbit/s: \033[034m', megabitter, '\033[0m\n')
    return final_value / count


def download(url, file_name) -> None:
    """downloading file here"""
    os.mkdir('123')
    wget.download(url, out=file_name)
    os.remove(file_name)
    os.rmdir('123')


def main_speed_test_func() -> None:
    print('date: ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('ip: ', socket.gethostbyname_ex(socket.gethostname()))

    try:
        if os.path.exists('123'):
            [os.remove(_) for _ in os.scandir('123')]
            os.rmdir('123')
    except Exception as E3:
        print('E3:', E3, '\nIt\'s ok')

    timer = datetime.datetime.now()

    """start thread here - 28.3 mg file"""
    speedtest = threading.Thread(target=download,
                                 args=('http://mapbasic.ru/soft/mapbasic_12.zip', '123/mapbasic_12.zip',))
    speedtest.start()
    time.sleep(0.1)

    """watch on dependence between size file and time"""
    while os.path.exists('123'):
        time.sleep(1)
        try:
            megabitter_for_print = scan_func(timer)
        except Exception as E1:
            print(E1, '\nOk, we done successfully!')

    os.system(f"osascript -e 'say \"Download speed: {megabitter_for_print:.0f} megabits in sec\"'; "
              f"osascript -e 'display alert \"Download speed: \" "
              f"message \"{megabitter_for_print:.0f} megabits in sec\"'; ")


if __name__ == '__main__':
    main_speed_test_func()
