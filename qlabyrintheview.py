from PyQt5 import QtCore

import numpy as np
from PyQt5.QtCore import QLineF
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem, QGraphicsSimpleTextItem, QGraphicsItem
from PyQt5.QtWidgets import QStyleOptionGraphicsItem
from PyQt5.QtWidgets import QWidget, QGraphicsRectItem


class QLabyrintheView(QGraphicsView):
    def __init__(self, grille, debut, fin, chemin, textes, colors, *__args):
        QGraphicsView.__init__(self, *__args)

        n = grille.shape[0]
        p = grille.shape[1]

        self.scene = QGraphicsScene(self)

        self.cases = np.zeros(grille.shape[:2], dtype=object)

        self.setScene(self.scene)

        for i in range(n):
            for j in range(p):
                case = Case(self.scene, i, j, grille[i, j], str((i, j)) + "\n" + str(textes[i, j]), colors[i, j])
                self.cases[i, j] = case

        s = min(self.width() / n, self.height() / p) * 2.5
        self.scale(s, s)

        self.player = Polygon(debut[0], debut[1], 3, "blue", 4)
        self.fin = Polygon(fin[0], fin[1], 3, "green", 8)
        self.scene.addItem(self.fin)
        self.scene.addItem(self.player)

    def move(self, p):
        print(p)
        self.player.move(p[0], p[1])


class Case:
    def __init__(self, scene, x, y, barrieres, text, color):
        self.barrieres = barrieres
        self.text = text

        x *= 10
        y *= 10
        x, y = y, x

        for side in range(4):
            if not barrieres[side]:
                if side == 0:  # haut
                    a, b = x - 5, y - 5
                    c, d = x + 5, y - 5
                elif side == 1:  # droite
                    a, b = x + 5, y - 5
                    c, d = x + 5, y + 5
                elif side == 2:  # bas
                    a, b = x - 5, y + 5
                    c, d = x + 5, y + 5
                else:  # gauche
                    a, b = x - 5, y + 5
                    c, d = x - 5, y - 5
                line = QGraphicsLineItem(QLineF(a, b, c, d))
                line.setPen(QPen(QColor("black"), 0.5))
                scene.addItem(line)

        t = QGraphicsSimpleTextItem(str(text))
        t.setScale(0.1)
        t.setPos(x, y)
        scene.addItem(t)

        rect = QGraphicsRectItem(x - 5, y - 5, 10, 10)
        rect.setBrush(QColor(*color))
        rect.setPen(QPen(QColor(0, 0, 0, 0), 0))
        rect.setZValue(rect.zValue() - 1)
        scene.addItem(rect)


class Polygon(QGraphicsPolygonItem):
    def __init__(self, x, y, size, color, i):
        x *= 10
        y *= 10
        x, y = y, x

        self.position = x, y
        points = []
        for a in range(i):
            p_x = np.sin(2 * a * np.pi / i) * size + x
            p_y = np.cos(2 * a * np.pi / i) * size + y

            points.append(QPointF(p_x, p_y))
        polygon = QPolygonF(points)
        super().__init__(polygon)

        self.setPen(QPen(QColor("black"), 0.25))
        self.setBrush(QColor(color))

    def move(self, x, y):
        x *= 10
        y *= 10
        x, y = y, x

        self.moveBy(x - self.position[0], y - self.position[1])
        self.position = x, y
