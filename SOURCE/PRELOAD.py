# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from io import BytesIO
from pkgutil import get_data


import pygame as pg


from LOGIC import *


window = pg.Rect(120, 0, 360, 360)
effective = window.inflate(30, 30)


color_dict = {
    6: (0, 255, 0),
    8: (255, 255, 255),
    9: (128, 128, 128),
    10: (0, 0, 0)
}


stage_title = (
    "热敏灰女孩,~ Coral Red",
    "起床决斗,~ Squid Cakes",
    "原始二进制,~ Would you like some CDs?",
    "海胆道馆,~ Flower and Entertain"
)


asset = lambda path: get_data(__name__, path)
get_stage = lambda stage: stage if stage < 4 else 'Final'
get_logs = lambda date, score, flashed, power, win, lose: (
    f"今天是 {date}",
    f"得到了 {score} 分",
    f"输赢各为 {lose} 跟 {win}",
    f"使用了 {flashed} 次形闪",
    f"最终形力为 {power} 点"
)[::-1]
screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN|pygame.SCALED)
font = pg.font.Font(BytesIO(asset('ASSET/FONT/UNI3500.otf')), 15)
icon = pg.display.set_icon(pg.image.load(BytesIO(asset('ASSET/IMAGE/ICON.png'))))


sound_cache = {
    'pick': pg.mixer.Sound(BytesIO(asset('ASSET/FLAC/PICK.flac'))),
    'fire': pg.mixer.Sound(BytesIO(asset('ASSET/FLAC/FIRE.flac'))),
    'charge': pg.mixer.Sound(BytesIO(asset('ASSET/FLAC/CHARGE.flac'))),
    'tick': pg.mixer.Sound(BytesIO(asset('ASSET/FLAC/TICK.flac')))
}


char_image = pg.image.load(BytesIO(asset('ASSET/IMAGE/CHAR.png'))).convert()
basic_image = pg.image.load(BytesIO(asset('ASSET/IMAGE/BASIC.png'))).convert()
white_rect = rectangle((8, 8), 0, color_dict[8]).convert_alpha()
char_image.set_colorkey(color_dict[10])
basic_image.set_colorkey(color_dict[10])
picture = {
    1: pg.image.load(BytesIO(asset('ASSET/IMAGE/STAGE1BG.png'))).convert(),
    2: pg.image.load(BytesIO(asset('ASSET/IMAGE/STAGE2BG.png'))).convert(),
    3: pg.image.load(BytesIO(asset('ASSET/IMAGE/STAGE3BG.png'))).convert(),
    4: pg.image.load(BytesIO(asset('ASSET/IMAGE/STAGE4BG.png'))).convert(),
    5: pg.Surface((360, 360)).convert(),
    6: pg.image.load(BytesIO(asset('ASSET/IMAGE/GAMEBG.png'))).convert(),
    7: pg.Surface((480, 360)).convert()
}


barrage_cache = {
    (2, color_dict[8]): circle((0, 0, 8, 8), 0, color_dict[8]),
    (1, color_dict[8]): white_rect,
    (0, color_dict[8]): basic_image
}


item_cache = rectangle((9, 9), 2, color_dict[6]).convert()


particle_cache = {
    (2, color_dict[6]): white_rect.subsurface((0, 0, 2, 2)),
    (2, color_dict[8]): rectangle((2, 2), 0, color_dict[8]).convert(),
}