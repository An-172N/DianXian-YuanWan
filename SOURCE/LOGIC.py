# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


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
        return (tx, ty), (0.0, 0.0)

    distance = math.sqrt(dist_sq)
    dx, dy = dx / distance, dy / distance

    if dist_sq < step * step:
        return (tx, ty), (dx, dy)
    return (cx + dx * step, cy + dy * step), (dx, dy)


def rotate(point, angle, center):
    cx, cy = center
    dx, dy = point[0] - cx, point[1] - cy
    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)

    return cx + dx * cos - dy * sin, cy + dx * sin + dy * cos


def coordinate(position, angle, length):
    radians = math.radians(angle)
    x = position[0] + length * math.cos(radians)
    y = position[1] + length * math.sin(radians)

    return x, y


def clamp(value, minimum, maximum):
    if value > maximum:
        return maximum
    elif value < minimum:
        return minimum
    else:
        return value


def fibonacci(former: float, latter: float, frequency: int):
    for _ in range(0, frequency + 1):
        former, latter = latter, former + latter

    return former


def bearing(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b

    return math.degrees(math.atan2(bx - ax, by - ay)) % 360


def record(folder, file, content, encoding='utf-8'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    dump = [content[0]]
    dump.append(content[1])

    with open(f'{folder}/{file}', 'w', encoding=encoding) as f:
        return json.dump(dump, f, indent=4)


def get(folder, extension='.json', reverse=True):
    try:
        files = []
        for file in os.listdir(folder):
            if file.endswith(extension) and os.path.isfile(path := os.path.join(folder, file)):
                time = os.path.getmtime(path)
                files.append((time, path))
        files.sort(key=lambda x: x[0], reverse=reverse)

        return [path for _, path in files]
    except:
        return []


def rectangle(size, border, color, radius=(-1, -1, -1, -1)):
    return (
        surface := pygame.Surface(size, pygame.SRCALPHA),
        pygame.draw.rect(surface, color, surface.get_rect(), border, -1, *radius)
    )[0]


def circle(xy_size, border, color):
    return (
        surface := pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA),
        pygame.draw.ellipse(surface, color, xy_size, border)
    )[0]


class Base(pygame.sprite.Sprite):
    def __init__(oc, original_image, group=None, turn_image=None, form=None, angle=0, pos=(0, 0), mask=False, radius=None, rotate=False):
        super().__init__(group) if group is not None else super().__init__()
        oc.original_image = original_image
        oc.turn_image = turn_image
        if turn_image is not None:
            oc.turn_image_flipped = pygame.transform.flip(turn_image, True, False)
        oc.image = oc.original_image if not rotate else pygame.transform.rotate(oc.original_image, angle)
        oc.rect = oc.image.get_rect(center=pos)
        oc.angle = angle
        if radius:
            oc.radius = radius
        if mask:
            oc.mask = pygame.mask.from_surface(oc.image)
        if form is not None:
            oc.type = form
        oc._x, oc._y = pos

    @property
    def x(oc):
        return oc._x

    @x.setter
    def x(oc, value):
        oc._x = value
        oc.rect.centerx = oc._x

    @property
    def y(oc):
        return oc._y

    @y.setter
    def y(oc, value):
        oc._y = value
        oc.rect.centery = oc._y

    def swivel(oc, flip, turn):
        if flip:
            oc.image = oc.turn_image_flipped
        elif turn:
            oc.image = oc.turn_image
        else:
            oc.image = oc.original_image


class Invinc:
    def __init__(oc, end, blink_interval, func=lambda: None, *func_args):
        oc.end = end
        oc.blink_interval = blink_interval
        oc.func = func
        oc.func_args = func_args

        oc.condition = False
        oc.visitable = True
        oc.timer = 0

    def update(oc):
        if oc.condition:
            oc.timer += 1
            if oc.timer >= oc.end:
                oc.func(*oc.func_args)
                oc.timer = 0
                oc.visitable = True
                oc.condition = False
            else:
                oc.visitable = (oc.timer // oc.blink_interval) % 2 == 1


def carry(former, latter, start, final):
    if latter >= final:
        former += 1
        latter = start
    else:
        latter += 1

    return former, latter


def one_shot(condition, power, critical):
    if not condition and power >= critical:
        condition = True
        power -= critical

    return condition, power