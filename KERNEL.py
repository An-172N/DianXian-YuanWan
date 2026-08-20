# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议

import sys
import os
from datetime import datetime
from random import randint, choice, uniform
from math import sin, cos, radians, hypot

import pygame as pg
from pygame.sprite import Group

from PRELOAD import *
from LOGIC import *


class One:
    def __init__(oc):
        oc.plane_group = Group()
        oc.bullet_group = Group()
        oc.brick_group = Group()
        oc.item_group = Group()
        oc.barrage_group = Group()
        oc.particle_group = Group()
        oc.menu = Menu(font, picture[5], screen, color_dict[8], (color_dict[8], color_dict[9], color_dict[10]), (120, 0))
        oc.is_pause = False
        oc.is_summary = False
        oc.is_talk = False
        oc.is_save = False
        oc.is_check = False
        oc.is_level_load = False
        oc.is_exit = False
        oc.char: Basic = None
        oc.talk: Talk = None
        oc.win = 0


class Two:
    def __init__(oc):
        oc.is_run = False
        oc.score = 0
        oc.flashed = 0
        oc.win = 0
        oc.lose = 0
        oc.stage = 1
        oc.wait_load_timer = 0


class Basic(Base):
    def __init__(oc, image, turn_image, barrage_group, particle_group, brick_group):
        super().__init__(image, brick_group, turn_image, pos=(300, 60))
        oc.barrage_group = barrage_group
        oc.particle_group = particle_group
        oc.can_shoot = False
        oc.choice = None
        oc.down_timer = 9000
        oc.timer = 0
        oc.bullets = 0
        oc.index = 0
        oc.locate = (0, 0)
        oc.target_pos = (300, 60)

    def reset_state(oc):
        oc.bullets = 0
        oc.timer = 0
        oc.interval_locate = oc.locate
        oc.can_shoot = True
        oc.choice = oc.sd[oc.index]
        oc.index = (oc.index + 1) if oc.index < len(oc.sd) - 1 else 0

    def spawn_particles(oc, radius, speed):
        particle_image = particle_cache[(2, color_dict[8])]
        for _ in range(32):
            pos = oc.x + randint(-radius, radius), oc.y + randint(-radius, radius)
            angle = bearing((oc.x, oc.y), pos)
            Barrage(effective, speed, angle, pos, particle_image, oc.particle_group)
        sound_cache["charge"].play()

class Cle(Basic):
    def __init__(oc, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((24, 0, 12, 26)), subsurface((36, 0, 12, 26)), *group)
        oc.bullet_image = barrage_cache[(0, color_dict[8])]
        oc.goal = 131072
        oc.sd = (oc.d1, oc.d1, oc.d2, oc.d3)

    def d1(oc):
        if oc.bullets < 12:
            speed = 4.5
            for i in range(6):
                delay_angle = oc.bullets * i
                pos = [coordinate(oc.rect.center, i, 256) for i in (-20 - delay_angle, -40 - delay_angle, -140 + delay_angle, -160 + delay_angle)]
                for p in pos:
                    p = vector(oc.rect.center, p, 28 * oc.bullets)
                    angle = bearing((oc.locate[0], oc.locate[1] - 128), p)
                    Barrage(effective, speed, angle, p, oc.bullet_image, oc.barrage_group, 2, True)
                speed -= 0.5
            oc.bullets += 1
            if oc.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(48 if oc.bullets < 12 else 0))

    def d2(oc):
        if oc.bullets < 12:
            speed = 4.5
            pos = [coordinate(oc.rect.center, i, 256) for i in (60, 120)]
            for _ in range(6):
                for i in range(-60, 61, 120):
                    for p in pos:
                        p = vector(p, oc.rect.center, 24 * oc.bullets)
                        angle = bearing(oc.locate, p) + i
                        Barrage(effective, speed, angle, p, oc.bullet_image, oc.barrage_group, 2, True)
                speed -= 0.5
            oc.bullets += 1
            if oc.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(48 if oc.bullets < 12 else 0))

    def d3(oc):
        if oc.bullets < 10:
            cp = oc.rect.center
            for p in (window.topleft, window.topright):
                pos = vector(p, cp, hypot(cp[0] - p[0], cp[1] - p[1]) / 12 * oc.bullets)
                speed = 5
                for _ in range(4):
                    for i in range(-30, 31, 30):
                        angle = bearing(oc.locate, pos) + i
                        Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 2, True)
                    speed -= 1
            oc.bullets += 1
            if oc.bullets % 5 == 0:
                sound_cache["fire"].play(maxtime=(84 if oc.bullets < 10 else 0))

    def update(oc):
        oc.timer += 1
        oc.down_timer -= 1
        if oc.timer % 130 == 0:
            if oc.index == 0:
                oc.target_pos = coordinate((300, 60), 120, 96)
            elif oc.index == 1:
                oc.target_pos = (300, 60)
            else:
                oc.target_pos = coordinate((300, 60), 60, 96)
            oc.reset_state()
        if oc.timer % 105 == 0 and oc.timer % 130 >= 105:
            oc.spawn_particles(48, 3)
        pg.sprite.spritecollide(oc, oc.particle_group, True)
        if oc.can_shoot:
            oc.choice()
        delay = oc.x
        oc.x, oc.y = vector((oc.x, oc.y), oc.target_pos, 4)
        oc.swivel(oc.x < delay, oc.x > delay)


class Xsu(Basic):
    def __init__(oc, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((48, 0, 12, 26)), subsurface((60, 0, 12, 26)), *group)
        oc.bullet_image = barrage_cache[(2, color_dict[8])]
        oc.goal = 98304
        oc.sd = (oc.d1, oc.d4, oc.d2, oc.d3, oc.d5, oc.d6)

    def d1(oc):
        if oc.bullets < 16:
            delay_angle = 30 * oc.bullets
            delay_angle2 = bearing(oc.interval_locate, oc.rect.center)
            for i in (-1, 1):
                pos = coordinate(oc.rect.center, delay_angle * i, 64)
                for j in range(0, 360, 60):
                    Barrage(effective, 3, j + delay_angle2, pos, oc.bullet_image, oc.barrage_group, 2)
            oc.bullets += 1
            if oc.bullets % 4 == 0:
                sound_cache["fire"].play(maxtime=(67 if oc.bullets < 16 else 0))

    def d2(oc):
        if oc.timer == 0:
            speed = 5
            for _ in range(8):
                for p in (window.bottomleft, window.bottomright, window.topleft, window.topright):
                    angle = bearing((oc.locate[0], oc.locate[1]), p)
                    for i in range(0, 360, 15):
                        Barrage(effective, speed, i + angle, p, oc.bullet_image, oc.barrage_group, 2)
                speed -= 0.5
            sound_cache["fire"].play()

    def d3(oc):
        if oc.timer % 6 == 0 and oc.bullets < 6:
            pos = oc.rect.center
            speed = 4.5
            for _ in range(4):
                for i in range(-30, 31, 10):
                    angle = bearing(oc.interval_locate, pos) + i + oc.bullets * 60
                    Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 2)
                speed -= 1
            oc.bullets += 1
            sound_cache["fire"].play(maxtime=(98 if oc.bullets < 3 else 0))

    def d4(oc):
        if oc.bullets < 16:
            delay_angle = 22.5 * oc.bullets
            for i in (-1, 1):
                pos = coordinate(oc.rect.center, delay_angle * i, 64)
                for j in range(30, 330, 50):
                    Barrage(effective, 2.5, j + oc.bullets * 8, pos, oc.bullet_image, oc.barrage_group, 2)
            oc.bullets += 1
            if oc.bullets % 4 == 0:
                sound_cache["fire"].play(maxtime=(67 if oc.bullets < 16 else 0))

    def d5(oc):
        if oc.timer % 3 == 0 and oc.bullets < 12:
            angle = bearing(oc.interval_locate, oc.rect.center)
            pos = coordinate(oc.rect.center, angle - 120 + oc.bullets * 20, 32)
            for i in range(0, 360, 15):
                Barrage(effective, 3.5, angle + i, pos, oc.bullet_image, oc.barrage_group, 2)
            oc.bullets += 1
            sound_cache["fire"].play(maxtime=(51 if oc.bullets < 12 else 0))

    def d6(oc):
        if oc.timer % 2 == 0 and oc.bullets < 12:
            pos = coordinate(oc.rect.center, oc.bullets * 30, oc.bullets * 12)
            for i in range(0 + oc.bullets * 4, 360 + oc.bullets * 4, 15):
                angle = bearing(oc.interval_locate, oc.rect.center) + i
                Barrage(effective, 3, angle, pos, oc.bullet_image, oc.barrage_group, 2)
            oc.bullets += 1
            if oc.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(67 if oc.bullets < 12 else 0))

    def update(oc):
        oc.timer += 1
        oc.down_timer -= 1
        if oc.timer % 140 == 0:
            oc.target_pos = coordinate((300, 120), 60 * oc.index, 32)
            oc.reset_state()
        if oc.timer % 110 == 0 and oc.timer % 140 >= 110:
            oc.spawn_particles(48, 3)
        pg.sprite.spritecollide(oc, oc.particle_group, True)
        if oc.can_shoot:
            oc.choice()
        delay = oc.x
        oc.x, oc.y = vector((oc.x, oc.y), oc.target_pos, 4)
        oc.swivel(oc.x < delay, oc.x > delay)


class Wyv(Basic):
    def __init__(oc, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((72, 0, 12, 26)), subsurface((84, 0, 12, 26)), *group)
        oc.traingle_bullet_image = barrage_cache[(0, color_dict[8])]
        oc.circle_bullet_image = barrage_cache[(2, color_dict[8])]
        oc.goal = 393216
        oc.sd = (oc.d1, oc.d2, oc.d3, oc.d4, oc.d5, oc.d6, oc.d7, oc.d8)

    def triangle(oc, func, is_delay, sprite_size, side_length, *args):
        p = oc.rect.center
        height_factor = math.sqrt(3) / 2
        if is_delay:
            heigth = (side_length - 1) * sprite_size * height_factor
            center_offset_y = 2 * heigth / 3
        for row in range(side_length):
            num_in_row = row + 1
            for col in range(num_in_row):
                offset_x = (col - row / 2) * sprite_size
                offset_y = row * sprite_size * height_factor - (center_offset_y if is_delay else 0)
                func(offset_x, offset_y, p, *args)

            yield

    def d1(oc):
        if oc.timer % 3 == 0 and oc.bullets < 12:
            for i in range(0, 360, 10):
                p = oc.rect.center
                angle = i + bearing((oc.locate[0], oc.locate[1] - 128), p)
                rad = radians(angle) + oc.timer * 2
                speed = 4 * (1 + 0.2 * cos(3 * rad))
                Barrage(effective, speed, angle, p, oc.traingle_bullet_image, oc.barrage_group, 2, True)
            oc.bullets += 1
            sound_cache["fire"].play(maxtime=(51 if oc.bullets < 8 else 0))

    def d2(oc):
        if oc.timer % 3 == 0 and oc.bullets < 16:
            p = oc.rect.center
            for i in range(0, 360, 12):
                angle = bearing(oc.interval_locate, p) + i
                if oc.bullets >= 11:
                    angle -= 2 * (oc.bullets - 10)
                elif oc.bullets >= 6:
                    angle += 2 * (oc.bullets - 5)
                image = oc.traingle_bullet_image if oc.bullets >= 6 else oc.circle_bullet_image
                rotate = True if oc.bullets >= 6 else False
                Barrage(effective, 4, angle, p, image, oc.barrage_group, 2, rotate)
            oc.bullets += 1
            sound_cache["fire"].play(maxtime=(51 if oc.bullets < 16 else 0))

    def d3(oc):
        if oc.timer == 0:
            def spwan_barrage(offset_x, offset_y, p, delay):
                pos = rotate((p[0] + offset_x, p[1] + offset_y), delay, p)
                angle = bearing(p, pos) + delay
                Barrage(effective, speed, angle, pos, oc.traingle_bullet_image, oc.barrage_group, 2, True)

            speed = 5
            for i in range(0, 360, 45):
                for _ in oc.triangle(spwan_barrage, True, 16, 8, i):
                    pass
                speed -= 0.5
            sound_cache["fire"].play()

    def d4(oc):
        if oc.bullets < 24:
            def spwan_barrage(offset_x, offset_y, p):
                angle = oc.bullets * 15
                pos = rotate((p[0] + offset_x, p[1] + offset_y), angle, p)
                Barrage(effective, speed, angle, pos, oc.traingle_bullet_image, oc.barrage_group, 2, True)

            speed = 5
            for _ in oc.triangle(spwan_barrage, False, 9, 9):
                speed -= 0.3
            oc.bullets += 1
            if oc.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(51 if oc.bullets < 12 else 0))

    def d5(oc):
        if oc.bullets < 20:
            speed1 = 5
            original_angle = bearing(oc.interval_locate, oc.rect.center)
            base = 30 + oc.bullets * 7.625
            for _ in range(8):
                for i in (1, -1):
                    angle = (original_angle + i * base) % 360
                    Barrage(effective, speed1, angle, oc.rect.center, oc.circle_bullet_image, oc.barrage_group, 2)
                speed1 -= 0.5
            if oc.bullets == 0:
                speed2 = 6
                for _ in range(8):
                    for i in range(-30, 31, 15):
                        angle = original_angle + i
                        Barrage(effective, speed2, angle, oc.rect.center, oc.traingle_bullet_image, oc.barrage_group, 2, True)
                    speed2 -= 0.5
            oc.bullets += 1
            if oc.bullets % 4 == 0:
                sound_cache["fire"].play(maxtime=(67 if oc.bullets < 20 else 0))

    def d6(oc):
        if oc.bullets < 8:
            for i in range(6):
                pos = coordinate(oc.rect.center, 60 * i, oc.bullets * 16)
                for j in range(0, 360, 60):
                    angle = bearing(oc.rect.center, pos) + j + oc.bullets * 6 + bearing(oc.locate, pos)
                    Barrage(effective, 3, angle, pos, oc.traingle_bullet_image, oc.barrage_group, 2, True)
            oc.bullets += 1
            if oc.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(34 if oc.bullets < 8 else 0))

    def d7(oc):
        if oc.timer % 2 == 0 and oc.bullets < 16:
            angle = bearing(oc.interval_locate, oc.rect.center)
            for i in range(0, 360, 115):
                for j in range(-15 - oc.bullets * 10, 15 + oc.bullets * 10 + 1, 15):
                    Barrage(effective, 5, angle + i + j, oc.rect.center, oc.traingle_bullet_image, oc.barrage_group, 2, True)
            oc.bullets += 1
            if oc.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(67 if oc.bullets < 16 else 0))

    def d8(oc):
        if oc.timer % 2 == 0 and oc.bullets < 16:
            angle = bearing(oc.interval_locate, oc.rect.center)
            for i in range(-15 - oc.bullets * 20, 15 + oc.bullets * 20 + 1, 45):
                for j in range(3):
                    pos = coordinate(oc.rect.center, oc.bullets * 20 + 120 * j, 32)
                    Barrage(effective, 4, angle + i, pos, oc.traingle_bullet_image, oc.barrage_group, 2, True)
            oc.bullets += 1
            if oc.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(67 if oc.bullets < 16 else 0))

    def update(oc):
        oc.timer += 1
        oc.down_timer -= 1
        if oc.timer % 120 == 0:
            if oc.index < 2 or oc.index >= 4:
                oc.target_pos = (300, 60)
            else:
                if oc.index == 2:
                    oc.target_pos = coordinate((300, 60), 180, 128)
                elif oc.index == 3:
                    oc.target_pos = coordinate((300, 60), 90, 128)
            oc.reset_state()
        if oc.down_timer == 1800 and oc.goal > 65536:
            oc.sd = (oc.d4, oc.d7, oc.d5, oc.d6)
            oc.index = 0
        if oc.timer % 99 == 0 and oc.timer % 120 >= 99:
            oc.spawn_particles(72, 5.5)
        pg.sprite.spritecollide(oc, oc.particle_group, True)
        if oc.can_shoot:
            oc.choice()
        delay = oc.x
        oc.x, oc.y = vector((oc.x, oc.y), oc.target_pos, 4)
        oc.swivel(oc.x < delay, oc.x > delay)


class Flo(Basic):
    def __init__(oc, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((96, 0, 12, 26)), subsurface((108, 0, 12, 26)), *group)
        oc.bullet_image = barrage_cache[(1, color_dict[8])]
        oc.goal = 262144
        oc.sd = (oc.d1, oc.d2, oc.d3, oc.d4, oc.d5, oc.d6, oc.d7, oc.d8, oc.d9, oc.d10)

    def diagonal(oc, delay=48):
        tl, tr = (oc.x - delay, oc.y - delay), (oc.x + delay, oc.y - delay)
        bl, br = (oc.x - delay, oc.y + delay), (oc.x + delay, oc.y + delay)

        return  (
            (tl, tr),
            (tr, br),
            (br, bl),
            (bl, tl)
        )

    def d1(oc):
        if oc.bullets < 12:
            speed = 6
            for _ in range(10):
                angle = bearing(window.bottomright, window.topleft)
                for i in (-1, 1):
                    x = 300 - 180 * i
                    start_y = 180 - 180 * i
                    end_y = 180 + 180 * i
                    p = vector((x, start_y), (x, end_y), 30 * oc.bullets)
                    angle += i * 180
                    Barrage(effective, speed, angle, p, oc.bullet_image, oc.barrage_group, 2, True)
                speed -= 0.5
            oc.bullets += 1
            if oc.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(48 if oc.bullets < 12 else 0))

    def d2(oc):
        if oc.timer % 4 == 0 and oc.bullets < 12:
            for p in (((window.left, oc.y), (window.right, oc.y)), ((window.right, oc.y), (window.left, oc.y))):
                pos = vector(p[0], p[1], 30 * oc.bullets)
                speed = 5
                for _ in range(6):
                    for i in range(0, 360, 90):
                        angle = bearing(oc.locate, pos) + i
                        sprite = Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 3, True)
                        if major.rub_range.colliderect(sprite.rect):
                            sprite.kill()
                    speed -= 0.5
            oc.bullets += 1
            sound_cache["fire"].play(maxtime=(67 if oc.bullets < 12 else 0))

    def d3(oc):
        if oc.bullets < 30:
            speed = 5
            for _ in range(6):
                angle = 180
                for i in (-1, 1):
                    start_x = 300 - 180 * i
                    end_x = 300 + 180 * i
                    p = vector((start_x, oc.y), (end_x, oc.y), 12 * oc.bullets)
                    angle += i * 180 + oc.bullets * 8
                    Barrage(effective, speed, angle, p, oc.bullet_image, oc.barrage_group, 2, True)
                speed -= 0.5
            oc.bullets += 1
            if oc.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(67 if oc.bullets < 16 else 0))

    def d4(oc):
        if oc.timer == 0:
            for i in range(8):
                for start, end in oc.diagonal():
                    speed = 5
                    for _ in range(8):
                        pos = vector(start, end, 16 * i)
                        angle = bearing(oc.rect.center, pos) + i * 30
                        Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 2, True)
                        speed -= 0.5
                speed -= 0.5
            sound_cache["fire"].play()

    def d5(oc):
        if oc.timer == 0:
            for i in range(12):
                for start, end in oc.diagonal():
                    speed = 5
                    for j in range(8):
                        pos = vector(start, end, 16 * i)
                        angle = bearing(oc.rect.center, pos) + i * 30 + j * 6
                        Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 2, True)
                        speed -= 0.5
            sound_cache["fire"].play()

    def d6(oc):
        if oc.timer % 4 == 0 and oc.bullets < 8:
            for j in range(4):
                tl, tr = window.topleft, window.topright
                bl, br = window.bottomleft, window.bottomright
                delay = j * 30
                pos_pairs = (
                    ((tl[0] + delay, tl[1] + delay), (tr[0] - delay, tr[1] + delay)),
                    ((tr[0] - delay, tr[1] + delay), (br[0] - delay, br[1] - delay)),
                    ((br[0] - delay, br[1] - delay), (bl[0] + delay, bl[1] - delay)),
                    ((bl[0] + delay, bl[1] - delay), (tl[0] + delay, tl[1] + delay))
                )
                for start, end in pos_pairs:
                    pos = vector(start, end, 45 * oc.bullets)
                    angle = bearing(window.center, pos) + oc.bullets * 12
                    sprite = Barrage(effective, 2, angle, pos, oc.bullet_image, oc.barrage_group, 3, True)
                    if major.rub_range.colliderect(sprite.rect):
                        sprite.kill()
            oc.bullets += 1
            sound_cache["fire"].play(maxtime=(67 if oc.bullets < 8 else 0))

    def d7(oc):
        if oc.timer == 0:
            for i in range(8):
                for start, end in oc.diagonal():
                    speed = 5
                    for j in range(8):
                        pos = vector(start, end, 16 * i)
                        angle = bearing(oc.rect.center, pos) + j * 15
                        Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 2, True)
                        speed -= 0.5
            sound_cache["fire"].play()

    def d8(oc):
        if oc.bullets < 8:
            for start, end in oc.diagonal():
                speed = 5
                for _ in range(6):
                    for k in (-30, 31, 60):
                        pos = vector(start, end, 16 * oc.bullets)
                        angle = bearing(oc.rect.center, pos) + k
                        Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 2, True)
                    speed -= 0.5
            oc.bullets += 1
            if oc.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(34 if oc.bullets < 8 else 0))

    def d9(oc):
        if oc.bullets < 24:
            speed = 6
            for _ in range(8):
                for i in range(0, 360, 90):
                    angle = bearing(oc.locate, oc.rect.center) + i + oc.bullets ** 2
                    Barrage(effective, speed, angle, oc.rect.center, oc.bullet_image, oc.barrage_group, 3, True)
                speed -= 0.5
            oc.bullets += 1
            if oc.bullets % 4 == 0:
                sound_cache["fire"].play(maxtime=(51 if oc.bullets < 12 else 0))

    def d10(oc):
        if oc.timer == 0:
            for h in range(4):
                for i in range(8):
                    for start, end in oc.diagonal():
                        speed = 5
                        for j in range(8):
                            pos = vector(start, end, 16 * i)
                            angle = bearing(oc.rect.center, pos) + i * 30 + h * 32 + j
                            Barrage(effective, speed, angle, pos, oc.bullet_image, oc.barrage_group, 2, True)
                            speed -= 0.5
                    speed -= 0.5
            sound_cache["fire"].play()

    def update(oc):
        oc.timer += 1
        oc.down_timer -= 1
        if oc.timer % 120 == 0:
            oc.target_pos = (300, 60)
            oc.reset_state()
        if oc.timer % 99 == 0 and oc.timer % 120 >= 99:
            oc.spawn_particles(64, 4.6)
        pg.sprite.spritecollide(oc, oc.particle_group, True)
        if oc.can_shoot:
            oc.choice()


class Ewa(Basic):
    def __init__(oc, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((120, 0, 12, 26)), subsurface((132, 0, 12, 26)), *group)
        oc.bullet_image = barrage_cache[(1, color_dict[8])]
        oc.down_timer = 4500
        oc.goal = 229376

    def d1(oc):
        if oc.timer == 0:
            rands = choice(((12, 30), (18, 20), (15, 24), (16, 22.5)))
            for i in range(rands[0]):
                speed = 6
                for _ in range(10):
                    angle = 270
                    for j in (-1, 1):
                        x = 300 - 180 * j
                        start_y = 180 - 180 * j
                        end_y = 180 + 180 * j
                        p = vector((x, start_y), (x, end_y), rands[1] * i)
                        angle += j * 180
                        Barrage(effective, speed, angle, p, oc.bullet_image, oc.barrage_group, 2, False)
                    speed -= 0.5
            sound_cache["fire"].play()

    def update(oc):
        oc.timer += 1
        oc.down_timer -= 1
        if oc.timer % 120 == 0:
            oc.index += 1
            oc.target_pos = ((300, 60), (360, 60), (420, 60))[oc.index % 3]
            oc.timer = 0
            oc.can_shoot = True
            oc.choice = oc.d1
        if oc.timer % 99 == 0 and oc.timer % 120 >= 99:
            oc.spawn_particles(36, 3)
        pg.sprite.spritecollide(oc, oc.particle_group, True)
        if oc.can_shoot:
            oc.choice()
        delay = oc.x
        oc.x, oc.y = vector((oc.x, oc.y), oc.target_pos, 4)
        oc.swivel(oc.x < delay, oc.x > delay)


class Hro(Base):
    def __init__(oc, plane_group):
        subsurface = char_image.subsurface
        super().__init__(subsurface((0, 0, 12, 26)), plane_group, subsurface((12, 0, 12, 26)), pos=(300, 346), radius=1)
        oc.flash = 0
        oc.max_flash = 48
        oc.max_power = 24
        oc.max_collect_counter = 72
        oc.color = color_dict[6]
        oc.collided = Invinc(210, 6)
        oc.divided = Invinc(120, 4)
        oc.rub_range = oc.image.get_rect().inflate(16, 2)
        oc.collect_counter = 0
        oc.power = 0
        oc.is_fast = False

    def get_speed(oc):
        return 4, 2

    def add_power(oc):
        oc.flash, oc.collect_counter = carry(oc.flash, oc.collect_counter, 0, oc.max_collect_counter - 1)
        oc.flash = clamp(oc.flash, -oc.max_flash, oc.max_flash)

    def tired(oc, barrage_group, item_group):
        if oc.divided.condition:
            if oc.divided.timer == 0:
                for barrage in barrage_group:
                    Item(2.5, barrage.rect.center, item_group)
                    barrage.kill()
            oc.divided.update()

    def use_tired(oc):
        if oc.power >= oc.max_power:
            oc.divided.condition = True
            oc.power -= oc.max_power
            sound_cache["charge"].play()

    def reset_invinc(oc):
        oc.collided = Invinc(210, 6)
        oc.divided = Invinc(120, 4)

    def update(oc):
        oc.collided.update()
        keys = pg.key.get_pressed()
        speed = oc.get_speed()
        x = oc.x
        if keys[pg.K_LEFT]:
            oc.x -= speed[1] if oc.is_fast else speed[0]
        if keys[pg.K_RIGHT]:
            oc.x += speed[1] if oc.is_fast else speed[0]
        if keys[pg.K_UP]:
            oc.y -= speed[1] if oc.is_fast else speed[0]
        if keys[pg.K_DOWN]:
            oc.y += speed[1] if oc.is_fast else speed[0]
        oc.is_fast = True if keys[pg.K_z] else False
        oc.swivel(oc.x > x, oc.x < x)
        oc.x = clamp(oc.x, window.left, window.right)
        oc.y = clamp(oc.y, window.top, window.bottom)
        oc.rub_range.center = oc.rect.center


def score_summary(win, power, max_power):
    return win * 16384 + int(power / max_power * 8192)


def stage_loader(stage, barrage_group, particle_group, brick_group):
    one.char = choose_human(stage, barrage_group, particle_group, brick_group)
    one.talk = Talk(asset(f"ASSET/JSON/{stage}.json").decode('utf-8'))
    one.is_talk = True


def choose_human(stage, barrage_group, particle_group, brick_group):
    return {
        1: Cle,
        2: Xsu,
        3: Wyv,
        4: Flo,
    }[stage](barrage_group, particle_group, brick_group)


def close_summary():
    two.wait_load_timer = 0
    one.is_level_load = True
    one.menu.reset_timer()
    one.is_talk = True


def fade_surface(alpha, timer, is_exit, surface, screen):
    if is_exit:
        if timer % 30 == 0 and alpha < 255:
            alpha += 85
        timer -= 1
        surface.set_alpha(alpha)
        screen.blit(surface)
        if timer <= -30:
            sys.exit()
    elif alpha > 0 and not is_exit:
        if timer % 30 == 0 and alpha > 0:
            alpha -= 85
        timer += 1
        surface.set_alpha(alpha)
        screen.blit(surface)

    return alpha, timer


def save_file(name, score, flashed, power, win, lose):
    name = name.translate(str.maketrans('!<>:"/\\|?*,', '___________'))
    time = (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H-%M-%S'))
    content = f"{name},{score},{flashed},{win},{lose},{power},{time[0]}"
    logs.record_log(f'{name}_{time[0]}_{time[1]}', content)


class Barrage(Base):
    def __init__(oc, effective, speed, angle, pos, image, group, radius=0, rotate=False):
        super().__init__(image, group, None, angle, pos, radius=radius, rotate=rotate)
        oc.effective = effective
        oc.is_rubbed = False
        oc.speed = speed

    def update(oc):
        rad = radians(oc.angle)
        sin_, cos_ = sin(rad), cos(rad)
        oc.x, oc.y = oc.x - (sin_ * oc.speed), oc.y - (cos_ * oc.speed)
        if not oc.effective.collidepoint(oc.rect.center):
            oc.kill()


class Item(Base):
    def __init__(oc, speed, pos, group):
        super().__init__(item_cache, group, pos=pos)
        oc.speed = speed

    def update(oc, locate):
        oc.speed -= 0.1
        if oc.speed <= 0:
            oc.rect.center = vector(oc.rect.center, locate, 12)
        else:
            oc.y -= oc.speed


def spawn_particles(group, size, pos, speeds, color1, color2=None):
    rands = randint(0, 60)
    for i in range(0 + rands, 360 + rands, 60):
        color = color1 if color2 is None else choice([color1, color2])
        speed = uniform(speeds[0], speeds[1])
        image = particle_cache[(size, color)]
        Barrage(window, speed, i, pos, image, group)


def reset():
    one.__init__()
    two.__init__()
    logs.__init__(f'{os.path.expanduser("~")}/Saved Games/DX01', '.dx01')
    major.__init__(one.plane_group)


def situation(clock):
    for info in (
        (f"{two.score:9d}", (39, 25)),
        (f"{(one.char.goal if one.char is not None else 0):9d}", (39, 50)),
        (f"{(one.char.down_timer if one.char is not None else 0):9d}", (39, 75)),
        (f"{major.flash:9d}", (39, 125)),
        (f"{major.power:9d}", (39, 150)),
        (f"{int(clock.get_fps()):9d}", (39, 200))
    ):
        screen.blit(blit_text(info[0], font, color_dict[8]), info[1])


def pause_menu():
    title = "休息ing"
    text = ("Esc 休息好了", "Del 不玩了") if one.menu.timer >= 60 else ("", "")
    half_menu(title, text)


def load_menu():
    current = stage_title[two.stage - 1].split(",")
    title = current[0]
    text = (current[1], "START!!!!")
    half_menu(title, text)


def talk_menu():
    try:
        half_menu(*one.talk.get_content(), (0, 6, 12))
    except KeyError:
        one.is_talk = False


def summary_menu():
    hit = 'Hit Z Key.' if one.menu.timer >= 60 else ''
    stage = f"Stage {get_stage(two.stage)} Clear! {hit}"
    win = one.win
    max_flash = major.max_flash
    flash = major.flash
    text = (
        f"输赢 {win} * 16384 = {win * 16384}",
        f"形闪 {flash} / {max_flash} * 8192 = {int(flash / max_flash * 8192)}"
    )
    half_menu(stage, text)


def start_menu(version, title):
    other = "(C)opyright 2026 An_172N"
    text = ('', '', '', '', f"Ver {version}")
    key = ("Q 回家", "C 日志" if logs.total_files > 0 else "C 木鱼", "Z 开玩")
    full_menu(title, text, key, other)


def save_menu():
    title = "玩耍日志"
    name = f"{f'由 {logs.name} 当裁判' if one.menu.timer >= 60 else ''}"
    date = datetime.now().strftime('%Y-%m-%d')
    text = get_logs(date, two.score, two.flashed, major.flash, two.win, two.lose)
    key = ("Esc 算了", "Ent 记录")
    keys = pg.key.get_pressed()
    shortly = one.menu.timer == 60 or (one.menu.timer >= 60 and any(keys[i] for i in range(len(keys))))
    full_menu(title, text, key, name, shortly=shortly)


def check_menu():
    try:
        if one.menu.timer == 0:
            logs.load_log()
        log = logs.log
        title = f"玩耍日志簿第 {logs.get_page()} 页"
        text = get_logs(log[6], log[1], log[2], log[5], log[3], log[4])
        key = ("Esc 合上", "Del 丢掉", "<-> 翻页")
        full_menu(title, text, key, f"由 {log[0]} 当裁判")
    except:
        one.is_check = False


def full_menu(title, text, key, other, shortly=False):
    right = True
    one.menu.draw_menu(
        sound_cache["pick"],
        ((title, other), 8, 10, 325, right), (text, 8, 210, 25, right), (key, 8, 60, 25, right),
        shortly=shortly
    )


def half_menu(title, text, interval=(0, 30, 60)):
    right = True
    one.menu.draw_menu(
        sound_cache["pick"],
        ((title,), 8, 10, 0, right), *[((text[i],), 8, 60 + 25 * i, 0, right) for i in range(len(text))],
        subsurface=(0, 0, 360, 110),
        interval=interval
    )


def summary_logic():
    def level_logic():
        one.__init__()
        major.reset_invinc()
        one.plane_group.add(major)
        two.stage += 1

    total_max_power = major.max_flash
    total_power = major.flash
    two.score += score_summary(one.win, total_power, total_max_power)
    one.is_summary = False
    one.menu.reset_timer()
    if two.stage == 4:
        one.is_save = True
    else:
        level_logic()


def talk_logic():
    if one.char.down_timer == 0 and not one.is_talk:
        def win():
            two.win += 1
            one.win += 1

        def lose():
            two.lose += 1
            one.win -= 1

        def stage3(first, second):
            if one.char.sd == (one.char.d4, one.char.d7, one.char.d5, one.char.d6):
                one.talk.set_part(first)
            else:
                one.talk.set_part(second)

        if one.talk.part == 1:
            if isinstance(one.char, (Cle, Xsu, Flo)):
                if one.char.goal > 0:
                    one.talk.set_part(2)
                    lose()
                else:
                    one.talk.set_part()
                    win()
            else:
                if one.char.goal > 0:
                    stage3(4, 3)
                    lose()
                else:
                    stage3(2, 1)
                    win()
        elif isinstance(one.char, Ewa):
            if one.char.goal > 0:
                one.talk.set_part(3)
                lose()
            else:
                one.talk.set_part(2)
                win()
        one.talk.set_number(1, False)
        one.is_talk = True
        if isinstance(one.char, Flo) and one.char.goal <= 0:
            if major.flash >= 36:
                one.char.kill()
                one.char = Ewa(one.barrage_group, one.particle_group, one.brick_group)
            else:
                one.talk.set_part(4)
                one.is_summary = True
        else:
            one.is_summary = True

def key_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if one.menu.timer >= 60:
                if one.is_check and event.key in keydown_check_dict:
                    keydown_check_dict[event.key]()
                    sound_cache["pick"].play()
                    one.menu.reset_timer()
                elif not two.is_run and not one.is_check and not one.is_exit and event.key in keydown_start_dict:
                    sound_cache["pick"].play()
                    keydown_start_dict[event.key]()
                elif one.is_save:
                    if event.key in keydown_over_dict:
                        keydown_over_dict[event.key]()
                    else:
                        logs.input_name(event.unicode)
                    sound_cache["pick"].play()
                elif one.is_pause and event.key in keydown_pause_dict:
                    keydown_pause_dict[event.key]()
                    sound_cache["pick"].play()
                elif one.is_summary and event.key == pg.K_z:
                    summary_logic()
                    sound_cache["pick"].play()
            elif one.is_talk and not one.is_pause and event.key in keydown_talk_dict and one.menu.timer >= 12:
                keydown_talk_dict[event.key]()
                sound_cache["pick"].play()
                one.menu.reset_timer()
            elif one.is_level_load and event.key in keydown_game_dict and not (one.is_summary or one.is_talk or one.is_pause):
                keydown_game_dict[event.key]()


def item_collide():
    for item in pg.sprite.spritecollide(major, one.item_group, False):
        sound_cache["pick"].play()
        major.add_power()
        two.score += 64
        one.char.goal -= 64
        item.kill()


def barrage_collide():
    pos = major.rect.center
    for barrage in one.barrage_group:
        invinc_condition = not major.collided.condition and not major.divided.condition
        if pg.sprite.collide_circle(major, barrage):
            if invinc_condition:
                major.collided.condition = True
                major.flash = clamp(major.flash - 8, -major.max_flash, major.max_flash)
                two.flashed += 1
                one.char.goal += 4096
                for _ in range(8):
                    spawn_particles(one.particle_group, 2, pos, (6, 12), major.color, color_dict[8])
                sound_cache["fire"].play()
            barrage.kill()
        if major.rub_range.colliderect(barrage.rect) and not barrage.is_rubbed and invinc_condition:
            major.power = clamp(major.power + 1, 0, major.max_power)
            sound_cache['tick'].play(maxtime=24)
            barrage.is_rubbed = True


def display(clock, version, title):
    if two.is_run:
        screen.blit(picture[two.stage], (120, 0))
        one.brick_group.draw(screen)
        if major.collided.visitable and major.divided.visitable:
            one.plane_group.draw(screen)
        one.item_group.draw(screen)
        one.particle_group.draw(screen)
        one.barrage_group.draw(screen)
    if one.is_check: check_menu()
    elif not two.is_run: start_menu(version, title)
    elif one.is_pause: pause_menu()
    elif not one.is_level_load: load_menu()
    elif one.is_talk: talk_menu()
    elif one.is_summary: summary_menu()
    elif one.is_save: save_menu()
    screen.blit(picture[6])
    situation(clock)


def update(clock, stage, version, title):
    two.stage = clamp(stage, 1, 4)
    alpha = 255
    timer = 0
    for info in (
        ("分", (9, 25)),
        ("剩", (9, 50)),
        ("时", (9, 75)),
        ('闪', (9, 125)),
        ('形', (9, 150)),
        ("刷", (9, 200))
    ):
        picture[6].blit(font.render(info[0], False, color_dict[8]), info[1])
    while True:
        key_event()
        if two.is_run and not one.is_save and not one.is_pause:
            if not one.is_summary and not one.is_talk and one.is_level_load:
                one.char.locate = major.rect.center
                one.plane_group.update()
                one.barrage_group.update()
                one.item_group.update(major.rect.center)
                one.particle_group.update()
                one.brick_group.update()
                barrage_collide()
                item_collide()
                major.tired(one.barrage_group, one.item_group)
                talk_logic()
            if not one.is_level_load:
                if two.wait_load_timer <= 90:
                    if two.wait_load_timer == 0:
                        stage_loader(two.stage, one.barrage_group, one.particle_group, one.brick_group)
                    two.wait_load_timer += 1
                else:
                    close_summary()
        display(clock, version, title)
        alpha, timer = fade_surface(alpha, timer, one.is_exit, picture[7], screen)
        pg.display.flip()
        clock.tick(60)


one = One()
two = Two()
logs = Log(f'{os.path.expanduser("~")}/Saved Games/DX01', '.dx01')
major = Hro(one.plane_group)


keydown_game_dict = {
    pg.K_SPACE: lambda: major.use_tired(),
    pg.K_ESCAPE: lambda: (setattr(one, "is_pause", True), one.menu.reset_timer(), sound_cache["pick"].play())
}


keydown_talk_dict = {
    pg.K_z: lambda: one.talk.set_number(),
    pg.K_x: lambda: (setattr(one, "is_talk", False))
}


keydown_pause_dict = {
    pg.K_ESCAPE: lambda: (setattr(one, "is_pause", False), one.menu.reset_timer()),
    pg.K_DELETE: lambda: reset()
}


keydown_start_dict = {
    pg.K_z: lambda: (setattr(two, "is_run", True), one.menu.reset_timer()),
    pg.K_q: lambda: setattr(one, "is_exit", True),
    pg.K_c: lambda: (setattr(one, "is_check", True), one.menu.reset_timer()) if logs.total_files > 0 else None
}


keydown_over_dict = {
    pg.K_RETURN: lambda: (save_file(logs.name, two.score, two.flashed, major.flash, two.win, two.lose), reset()),
    pg.K_ESCAPE: lambda: reset(),
    pg.K_BACKSPACE: lambda: logs.backspace_name()
}


keydown_check_dict = {
    pg.K_DELETE: lambda: logs.delete_log(),
    pg.K_ESCAPE: lambda: reset(),
    pg.K_LEFT: lambda: logs.turn_page("down"),
    pg.K_RIGHT: lambda: logs.turn_page("up")
}