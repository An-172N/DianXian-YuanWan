# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议

import heapq
import math
import json
import os

import pygame


def vector(current, target, step):
    cx, cy = current
    tx, ty = target
    dx, dy = tx - cx, ty - cy
    dist_sq = dx * dx + dy * dy

    if not dist_sq:
        return (tx, ty)

    distance = math.sqrt(dist_sq)
    dx, dy = dx / distance, dy / distance

    if dist_sq < step * step:
        return (tx, ty)
    return (cx + dx * step, cy + dy * step)


def rotate(point, angle, center):
    cx, cy = center
    dx, dy = point[0] - cx, point[1] - cy
    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)

    return (cx + dx * cos - dy * sin, cy + dx * sin + dy * cos)


def coordinate(position, angle, length):
    radians = math.radians(angle)
    x = position[0] + length * math.cos(radians)
    y = position[1] + length * math.sin(radians)

    return (x, y)


def clamp(value, minimum, maximum):
    if minimum > maximum:
        maximum, minimum = minimum, maximum

    if value > maximum:
        return maximum
    elif value < minimum:
        return minimum
    else:
        return value


def bearing(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b

    return math.degrees(math.atan2(bx - ax, by - ay)) % 360


def carry(former, latter, start, final):
    if latter >= final:
        former += 1
        latter = start
    else:
        latter += 1

    return (former, latter)


def one_shot(condition, power, critical):
    if not condition and power >= critical:
        condition = True
        power -= critical

    return (condition, power)


def draw_rectangle(size, border, color, radius=(-1, -1, -1, -1)):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surface, color, surface.get_rect(), border, -1, *radius)

    return surface


def draw_circle(xy_size, border, color):
    surface = pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, color, xy_size, border)

    return surface


def blit_text(text, font, color, fixed_char_width=8):
    height = font.get_height()
    width = len(text) * fixed_char_width
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i, char in enumerate(text):
        char_surface = font.render(char, False, color)
        surface.blit(char_surface, (i * fixed_char_width, 0))

    return surface


class Base(pygame.sprite.Sprite):
    def __init__(self, original_image, group=None, turn_image=None, angle=0, pos=(0, 0), radius=None, rotate=False, form=None):
        super().__init__(group) if group is not None else super().__init__()
        self.original_image = original_image
        self.turn_image = turn_image
        if turn_image is not None:
            self.turn_image_flipped = pygame.transform.flip(turn_image, True, False)
        self.image = self.original_image if not rotate else pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=pos)
        self.angle = angle
        if radius:
            self.radius = radius
        if form is not None:
            self.type = form
        self._x, self._y = pos

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.centerx = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.centery = self._y

    def swivel(self, flip, turn):
        if flip:
            self.image = self.turn_image_flipped
        elif turn:
            self.image = self.turn_image
        else:
            self.image = self.original_image


class Invinc:
    def __init__(self, end_time, blink_interval, func=lambda: None, *func_args):
        self.end = end_time
        self.blink_interval = blink_interval
        self.func = func
        self.func_args = func_args
        self.condition = False
        self.visitable = True
        self.timer = 0

    def update(self):
        if self.condition:
            self.timer += 1
            if self.timer >= self.end:
                self.func(*self.func_args)
                self.timer = 0
                self.visitable = True
                self.condition = False
            else:
                self.visitable = (self.timer // self.blink_interval) % 2 == 1


class Menu:
    def __init__(self, font, surface, screen, font_color, surface_colors, pos):
        self.font = font
        self.surface = surface
        self.screen = screen
        self.font_color = font_color
        self.surface_colors = surface_colors
        self.pos = pos
        self.timer = 0
        self._count = 0

    def draw_menu(self, sound, *texts, interval=(0, 30, 60), subsurface=None, shortly=False):
        group = []
        if subsurface:
            surface = self.surface.subsurface(subsurface)
        else:
            surface = self.surface
        if self.timer < interval[len(interval) - 1] + 1 or shortly:
            if self.timer == interval[len(interval) - 1]:
                sound.play()
            for text in texts:
                sub_group = []
                for i in range(len(text[0])):
                    sub_group.append((self.font.render(text[0][i], False, self.font_color), (text[1], text[2] + text[3] * i), text[4]))
                group.append(sub_group)
            self._pop_animate(interval, group, shortly)
            self.timer += 1
        self.screen.blit(surface, self.pos)

    def reset_timer(self):
        self.timer = 0
        self._count = 0

    def _pop_animate(self, interval, group, shortly):
        if not shortly:
            if self.timer in interval:
                self.surface.fill(self.surface_colors[self._count])
                self._count += 1
                for i in range(len(group)):
                    if self.timer >= interval[i]:
                        self._bilt_text(group[i])
        else:
            color = self.surface_colors[len(self.surface_colors) - 1]
            self.surface.fill(color)
            for i in range(len(group)):
                self._bilt_text(group[i])

    def _bilt_text(self, group):
        for text_surface, pos, is_right in group:
            if is_right:
                rect = text_surface.get_rect(topright=(self.surface.get_rect().right - pos[0], pos[1]))
                self.surface.blit(text_surface, rect)
            else:
                self.surface.blit(text_surface, pos)


class Talk:
    def __init__(self, content):
        self.text = json.loads(content)
        self.part = 1
        self.number = 1

    def get_content(self, index=2, title="char"):
        text = self.text[f"{self.part}"][f"{self.number}"]
        human = text[title]
        content = tuple(text[f"{i + 1}"] for i in range(index) if f"{i + 1}" in text)

        return (human, content)

    def set_part(self, index=1, one_by_one=True):
        if one_by_one:
            self.part += index
        else:
            self.part = index

    def set_number(self, index=1, one_by_one=True):
        if one_by_one:
            self.number += index
        else:
            self.number = index


class Log:
    def __init__(self, folder, extension='.dx00', reverse=True, count=8):
        self.folder = folder
        self.extension = extension
        try:
            with os.scandir(self.folder) as f:
                def file_iter():
                    for file in f:
                        if file.is_file() and file.name.endswith(extension):
                            yield (file.stat().st_mtime, file.path)

                if reverse:
                    top = heapq.nlargest(count, file_iter(), key=lambda x: x[0])
                else:
                    top = heapq.nsmallest(count, file_iter(), key=lambda x: x[0])
                self.files = [path for _, path in top]
        except:
            self.files = []
        self.log = None
        self.name = ''
        self.index = 0
        self.total_files = len(self.files)

    def record_log(self, file, content, encode='utf-8'):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        with open(f'{self.folder}/{file}{self.extension}', 'w', encoding=encode) as f:
            f.write(content)

    def load_log(self, max_char=128, max_cut=7, cut=','):
        with open(self.files[self.index], 'r', encoding='utf-8') as f:
            self.log = f.readline(max_char).split(cut, max_cut)

    def delete_log(self):
        os.remove(self.files[self.index])
        self.files.pop(self.index)
        self.total_files = len(self.files)
        if self.index > self.total_files - 1:
            self.index = self.total_files - 1

    def input_name(self, input_char, max_char=8):
        self.name = (self.name + input_char)[:max_char]

    def backspace_name(self):
        self.name = self.name[:-1]

    def get_page(self):
        return f"{self.total_files - self.index} / {self.total_files}"

    def turn_page(self, action):
        if action == "down":
            if self.index > 0:
                self.index -= 1
            else:
                self.index = self.total_files - 1
        else:
            if self.index < self.total_files - 1:
                self.index += 1
            else:
                self.index = 0