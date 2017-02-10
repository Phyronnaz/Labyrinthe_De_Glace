import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem, QGraphicsSimpleTextItem


class Labyrinthe(QGraphicsView):
    def __init__(self, board, first, finx, finy, chemin, T, *__args):
        QGraphicsView.__init__(self, *__args)
        self.scene = QGraphicsScene(self)
        self.scale = 75

        self.setScene(self.scene)

        for i in range(len(board)):
            for j in range(len(board)):
                for k in range(4):
                    item = QLine(i, j, self.scale, k, board[i][j][k])
                    self.scene.addItem(item)
                    # t = QGraphicsSimpleTextItem(str(i) + ", " + str(j))
                    # t.setScale(1)
                    # t.setPos(j * self.scale, i * self.scale - 10)
                    # self.scene.addItem(t)
                    # t = QGraphicsSimpleTextItem(str(T[i, j]))
                    # t.setScale(1)
                    # t.setPos(j * self.scale, i * self.scale + 10)
                    # self.scene.addItem(t)

        self.player = Hexagon(first[0], first[1], 25* self.scale / 60, (255, 0, 0, 128), self.scale)
        self.scene.addItem(self.player)
        self.fin = Hexagon(finx, finy, 25 * self.scale / 60, (0, 0, 255, 128), self.scale)
        self.scene.addItem(self.fin)
        for p in chemin:
            self.fin = Hexagon(p[0], p[1], 10 * self.scale / 50, (0, 255, 0, 128), self.scale)
            self.scene.addItem(self.fin)

    def move(self, x, y):
        print(x, y)
        self.player.move(x, y, self.scale)


class QLine(QGraphicsPolygonItem):
    def __init__(self, x, y, scale, side, value):
        x, y = y, x
        if value:
            super().__init__(None)
        else:
            if side == 0:  # haut
                a, b = x - 0.5, y - 0.5
                c, d = x + 0.5, y - 0.5
            elif side == 1:  # bas
                a, b = x - 0.5, y + 0.5
                c, d = x + 0.5, y + 0.5
            elif side == 2:  # gauche
                a, b = x - 0.5, y + 0.5
                c, d = x - 0.5, y - 0.5
            else:  # droite
                a, b = x + 0.5, y + 0.5
                c, d = x + 0.5, y - 0.5
            p1 = QPointF(a * scale, b * scale)
            p2 = QPointF(c * scale, d * scale)

            super().__init__(QPolygonF([p1, p2]))
            self.setPen(QPen(QColor("black"), 5))
            self.setBrush(QColor("black"))


class Hexagon(QGraphicsPolygonItem):
    def __init__(self, x, y, size, color, scale):
        x, y = y, x
        self.position = x * scale, y * scale
        points = []
        for a in range(4):
            p_x = np.sin(a * np.pi / 2) * size + x * scale
            p_y = np.cos(a * np.pi / 2) * size + y * scale

            points.append(QPointF(p_x, p_y))
        polygon = QPolygonF(points)
        super().__init__(polygon)
        self.setPen(QPen(QColor("black"), 1))
        self.setBrush(QColor(*color))

    def setColor(self, color):
        self.setBrush(QColor(color))

    def setColorRGB(self, r, g, b, a):
        self.setBrush(QColor(r, g, b, a))

    def move(self, x, y, scale):
        x, y = y, x
        self.moveBy(x * scale - self.position[0], y * scale - self.position[1])
        self.position = x * scale, y * scale
