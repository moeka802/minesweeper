import random
import json

class PointOffset:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def rounds():
        return [PointOffset(-1, -1), PointOffset(0, -1), PointOffset(1, -1),
                PointOffset(-1, 0),                    PointOffset(1, 0),
                PointOffset(-1, 1), PointOffset(0, 1), PointOffset(1, 1)]

class Cell:
    def __init__(self, isOpen, isFlag, isMine):
        self.isOpen = isOpen
        self.isFlag = isFlag 
        self.isMine = isMine 
    
    def __repr__(self):
        return json.dumps(self.getPublicInfo())

    def getPublicInfo(self):
        result = {
            'open': int(self.isOpen),
            'flag': int(self.isFlag)
        }
        if self.isOpen:
            result['mine'] = int(self.isMine)
        return result

class Field:
    def __init__(self, width, height, mine):
        self.cells = list()
        self.width = width 
        self.height = height 
        self.mine = mine
        for i in range(self.width * self.height):
            cellMine = True if i < mine else False
            self.cells.append(Cell(False, False, cellMine))
        random.shuffle(self.cells)
    
    def __repr__(self):
        return json.dumps(self.getPublicInfo())
    
    def getPublicInfo(self):
        rest = self.mine
        publicCells = list()
        for i, cell in enumerate(self.cells):
            cellInfo = cell.getPublicInfo()
            # ドカン!
            if cellInfo["open"] == 1 and cellInfo["mine"] == 0:
                cellInfo["number"] = self.roundNum(
                    i % self.width, int(i / self.width)
                )
            # フラグを立てる
            if cellInfo["open"] == 0 and cellInfo["flag"] == 1:
                rest = rest - 1
            publicCells.append(cellInfo)

        status = "continue"
        if self.isOver():
            status = "over"
        elif self.isClear():
            status = "cleared"

        result = {
            "cells": publicCells,
            "width": self.width,
            "height": self.height,
            "mine": self.mine,
            "status": status,
            "rest": rest
        }

        return result

    def cell(self, x, y):
        if 0 > x or 0 > y or self.width <= x or self.height <= y:
            return None
        return self.cells[y * self.width + x]
    
    def open(self, x, y):
        cell = self.cell(x, y)
        if cell is None:
            return 
        # すでに開いているマスなら何もしない
        if cell.isOpen:
            return
        cell.isOpen = True
        if not cell.isMine:
            if self.roundNum(x, y) == 0:
                for offset in PointOffset.rounds():
                    self.open(x + offset.x, y + offset.y)

    def flag(self, x, y, isFlag):
        cell = self.cell(x, y)
        if cell is None:
            return 
        cell.isFlag = isFlag

    def roundNum(self, x, y):
        round = 0
        for offset in PointOffset.rounds():
            if self.isMine(x + offset.x, y + offset.y):
                round += 1
        return round

    # 指定セルが存在してmine状態の場合にTrueを返す