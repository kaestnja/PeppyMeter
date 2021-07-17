# Copyright 2016-2018 PeppyMeter peppy.player@gmail.com
# 
# This file is part of PeppyMeter.
# 
# PeppyMeter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PeppyMeter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PeppyMeter. If not, see <http://www.gnu.org/licenses/>.

import math
import pygame as pg
from configfileparser import *

class NeedleFactory(object):
    """ Factory to prepare needle sprites for circular animator """
    
    def __init__(self, name, image, config, needle_cache, mono_rect_cache, left_rect_cache, right_rect_cache):
        """ Initializer
        
        :param image: base needle image
        :param config: configuration dictionary
        :param needle_cache: dictionary where key - meter name, value - list of needle sprites
        :param mono_rect_cache: dictionary where key - meter name, value - list of mono needle sprite rectangles
        :param left_rect_cache: dictionary where key - meter name, value - list of left needle sprite rectangles
        :param right_rect_cache: dictionary where key - meter name, value - list of right needle sprite rectangles
        """
        self.image = image
        self.config = config
        self.needle_sprites = self.get_cached_object(name, needle_cache)
        self.mono_needle_rects = self.get_cached_object(name, mono_rect_cache)
        self.left_needle_rects = self.get_cached_object(name, left_rect_cache)
        self.right_needle_rects = self.get_cached_object(name, right_rect_cache)
        self.angle_range = abs(self.config[STOP_ANGLE] - self.config[START_ANGLE])
        
        if len(self.needle_sprites) != 0:
            return

        if config[CHANNELS] == 1:
            self.create_needle_sprites(self.needle_sprites, self.mono_needle_rects, self.config[DISTANCE], self.config[MONO_ORIGIN_X] + self.config[METER_X], self.config[MONO_ORIGIN_Y] + self.config[METER_Y])
            needle_cache[name] = self.needle_sprites
            mono_rect_cache[name] = self.mono_needle_rects
        elif config[CHANNELS] == 2:
            self.create_needle_sprites(self.needle_sprites, self.left_needle_rects, self.config[DISTANCE], self.config[LEFT_ORIGIN_X] + self.config[METER_X], self.config[LEFT_ORIGIN_Y] + self.config[METER_Y])
            self.create_needle_sprites(None, self.right_needle_rects, self.config[DISTANCE], self.config[RIGHT_ORIGIN_X] + self.config[METER_X], self.config[RIGHT_ORIGIN_Y] + self.config[METER_Y])
            needle_cache[name] = self.needle_sprites
            left_rect_cache[name] = self.left_needle_rects
            right_rect_cache[name] = self.right_needle_rects

    def get_cached_object(self, name, cache):
        """ Get cached object

        :param name: object name
        :param cache: object cache

        :return: object from cache or empty list otherwise
        """
        cached_object = list()

        try:
            cached_object = cache[name]
        except:
            pass

        return cached_object

    def create_needle_sprites(self, needle_sprites, needle_rects, d, o_x, o_y):
        """ Create needle sprites
        
        :param needle_sprites: list for image sprites
        :param needle_rects: list for sprite bounding boxes
        :param d: the distance beteen image center and rotation origin
        :param o_x: x coordinate of the rotation origin
        :param o_y: y coordinate of the rotation origin 
        """
        img = pg.transform.rotozoom(self.image, self.config[START_ANGLE], 1)
        self.initial_angle = self.config[START_ANGLE]
        start_angle = math.atan2(img.get_rect().h/2, -img.get_rect().w/2) - math.radians(self.config[START_ANGLE])
 
        for _ in range(self.angle_range * self.config[STEPS_PER_DEGREE]):
            self.initial_angle = (self.initial_angle - 1/self.config[STEPS_PER_DEGREE]) % 360
            new_angle = math.radians(self.initial_angle) + start_angle
            new_center = (o_x + d * math.cos(new_angle), o_y - d * math.sin(new_angle))            
            img = pg.transform.rotozoom(self.image, self.initial_angle, 1)
            r = img.get_rect()
            img = img.subsurface((r.x, r.y, r.w, r.h))
            rect = img.get_rect(center=new_center)
            if needle_sprites != None:
                needle_sprites.append(img)
            needle_rects.append(rect)     
