import cv2
import numpy as np


class Cover:
    def __init__(self, shape, color):
        self._image = np.zeros(shape, np.uint8)
        self._color = color
        self._drawing = False

        self._function = 0
        self._anchor = 0

    @property
    def drawing(self):
        return self._drawing

    @drawing.setter
    def drawing(self, is_drawing):
        self._drawing = is_drawing

    @property
    def image(self):
        return self._image

    @property
    def color(self):
        return self._color

    @property
    def function(self):
        return self._function

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        self._anchor = anchor

    def next_function(self):
        self._function += 1
        self._function %= 3

    @staticmethod
    def draw(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            param.drawing = True

            param.anchor = x
            param.image[:, :] = 0

        elif event == cv2.EVENT_MOUSEMOVE:
            if param.drawing:

                if param.function == 0:
                    param.image[:, :] = param.color
                    param.image[:, x:] = 0

                elif param.function == 1:
                    param.image[:, :] = param.color
                    param.image[:, :x] = 0

                elif param.function == 2:
                    sx = x if x < param.anchor else param.anchor
                    ex = x if x > param.anchor else param.anchor

                    param.image[:, :] = param.color
                    param.image[:, sx:ex] = 0

        elif event == cv2.EVENT_LBUTTONUP:
            param.drawing = False
