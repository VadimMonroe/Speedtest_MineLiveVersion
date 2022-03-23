import time
import socket
import threading
import os
import datetime

import pygame
import wget

final_value = 0
count = 0

megabyter = 0
megabiter = 0
screen = False

ping = os.popen('ping -c 3 google.com').readlines()[-1].split('/')[4]


def scan_file_size_func(timer) -> float:
    """watch on size file every sec"""

    global final_value, count, megabyter, megabiter
    if os.path.exists('123'):
        for file in os.scandir('123'):
            file_size_speedtest = os.path.getsize(file)
            timer_after = datetime.datetime.now()
            real_timer = timer_after - timer
            real_timer = real_timer.seconds + real_timer.microseconds / 1000000
            file_mg = file_size_speedtest / 1024 / 1024
            megabyter = file_mg / real_timer
            megabiter = file_mg / real_timer * 8

            count += 1
            final_value += megabiter

            print('\r')
            print(' speedtest: ', 'file/mb: \033[034m', file_mg, '\033[0mdown sec: \033[034m', real_timer, '\033[0m\n',
                  'speedtest: ', 'MB/s: \033[034m', megabyter, '\033[0mMbit/s: \033[034m', megabiter, '\033[0m\n')
    if count != 0:
        return final_value / count


def download_file(url: str, file_name: str) -> None:
    """download file(29 mb) from internet"""
    os.mkdir('123')
    wget.download(url, out=file_name)
    os.remove(file_name)
    os.rmdir('123')


def main_speed_test_func() -> None:
    print('date: ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('ip: ', socket.gethostbyname_ex(socket.gethostname()))
    timer = datetime.datetime.now()

    try:
        if os.path.exists('123'):
            [os.remove(_) for _ in os.scandir('123')]
            os.rmdir('123')
    except Exception as E3:
        print('E3:', E3, '\nIt\'s ok')

    """start thread here - 28.3 mg file"""
    speedtest = threading.Thread(target=download_file,
                                 args=('http://mapbasic.ru/soft/mapbasic_12.zip', '123/mapbasic_12.zip',),
                                 daemon=True)
    speedtest.start()
    time.sleep(0.1)

    if screen:
        pygame_screen_func()
    else:
        """watch on dependence between size file and time"""
        while os.path.exists('123'):
            time.sleep(1)
            try:
                megabiter_for_print = scan_file_size_func(timer)
            except Exception as E1:
                print(E1, '\nOk, we done successfully!')

        print(speedtest.getName(), speedtest.is_alive(), speedtest.ident)
        os.system(f"osascript -e 'say \"Download speed: {megabiter_for_print:.0f} megabits in sec "
                  f"and ping: {float(ping):.0f}\"';"
                  f"osascript -e 'display alert \"Download speed: \""
                  f"message \"{megabiter_for_print:.0f} megabits in sec and ping: {float(ping):.0f}\"';")


def pygame_screen_func() -> None:
    """if wonna watch online speed test on screen (screen=True)"""
    fps = 60
    display_w, display_h = 640, 480  # ширина/высота
    red, black = (255, 0, 0), (255, 255, 255)
    pygame.init()
    pygame_screen = pygame.display.set_mode((display_w, display_h / 2))
    display = pygame.Surface((display_w, display_h / 2))
    display_rect = display.get_rect()
    display_rect.center = pygame_screen.get_rect().center
    pygame.display.set_caption("speed test")
    clock = pygame.time.Clock()
    font_name3 = pygame.font.match_font('verdana')

    def draw_text(text: str, size: int, x: float, y: float, colour=(255, 255, 255), shadow=True,
                  shadow_colour=(70, 70, 70), font=font_name3, offset=1, text_rect_center=True) -> None:

        font = pygame.font.Font(font, size)

        if shadow:
            text_surface = font.render(text, True, shadow_colour)
            text_rect = text_surface.get_rect()

            if text_rect_center:
                text_rect.center = (x, y)
            else:
                text_rect = (x, y)

            dropshadow_offset = offset + (size // 15)
            display.blit(text_surface, (text_rect.x + dropshadow_offset, text_rect.y + dropshadow_offset))

        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()

        if text_rect_center:
            text_rect.center = (x, y)
        else:
            text_rect = (x, y)

        display.blit(text_surface, text_rect)

    def redraw_window() -> None:
        pygame_screen.fill(black)
        display.fill(red)
        draw_text(f'PING: {ping}', 20, display.get_width() / 2, display.get_height() / 2 - 15)
        draw_text(f'DOWNLOAD: mg sec: {megabyter:.2f}, mегаbит sec: {megabiter:.2f}', 20, display.get_width() / 2,
                  display.get_height() / 2 + 15)
        pygame_screen.blit(display, display_rect)
        pygame.display.flip()

    timer = datetime.datetime.now()

    pygame_run_cycle = True
    while pygame_run_cycle:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame_run_cycle = False

        scan_file_size_func(timer)
        redraw_window()
    pygame.quit()


if __name__ == '__main__':
    screen = True
    main_speed_test_func()
