import tkinter as tk
import math
import random

canvas = None

SQUARE_LENGTH = 100
RADIUS = SQUARE_LENGTH / 2 - 5
POSITION = {"x": 8, "y": 8}
BORDER_WIDTH = 8
NUMBER = 4
LENGTH = SQUARE_LENGTH * NUMBER + BORDER_WIDTH * NUMBER
CELL_COLOR = '#cbbeb5'
BORDER_COLOR = '#b2a698'
gameCells = []


class Cell:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num


def initialBoard():
    global gameCells
    gameCells.clear()
    for i in range(4):
        for j in range(4):
            gameCells.append(Cell(j, i, ""))


def decideLocation():
    firstNum = 2
    while firstNum > 0:
        randomX = random.randint(0, 3)
        randomY = random.randint(0, 3)
        if gameCells[4 * randomY + randomX].num == "":
            gameCells[4 * randomY +
                      randomX] = Cell(randomX, randomY, firstSet())
            firstNum -= 1


def firstSet():
    randomNumber = random.randint(0, 4)
    if randomNumber == 4:
        return "4"
    else:
        return "2"


def set_field():
    canvas.create_rectangle(POSITION["x"], POSITION["y"], LENGTH + POSITION["x"],
                            LENGTH + POSITION["y"], fill='#cbbeb5', width=BORDER_WIDTH, outline=BORDER_COLOR)

    for i in range(NUMBER - 1):
        x = POSITION["x"] + SQUARE_LENGTH * \
            (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
        y = POSITION["y"] + SQUARE_LENGTH * \
            (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
        canvas.create_line(
            x, POSITION["y"], x, LENGTH + POSITION["y"], width=BORDER_WIDTH, fill=BORDER_COLOR)
        canvas.create_line(
            POSITION["x"], y, LENGTH + POSITION["x"], y, width=BORDER_WIDTH, fill=BORDER_COLOR)


def create_canvas():
    root = tk.Tk()
    root.geometry(
        f"""{LENGTH + POSITION["x"] * 2}x{LENGTH + POSITION["y"] * 2}""")
    root.title("2048")
    canvas = tk.Canvas(root, width=(
        LENGTH + POSITION["x"]), height=(LENGTH + POSITION["y"]))
    canvas.place(x=0, y=0)

    return root, canvas


def set_number(num, x, y):
    center_x = POSITION["x"] + BORDER_WIDTH * x + \
        BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
    center_y = POSITION["y"] + BORDER_WIDTH * y + \
        BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2
    canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2,
                            center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill=CELL_COLOR, width=0)
    canvas.create_text(center_x, center_y, text=num,
                       justify="center", font=("", 50), tag="count_text")


def setNum(col, colList):
    for row in range(4):
        gameCells[4 * col + row].num = colList[row]


def changeBlocks(colList, direction):
    for row in range(4):
        if colList[row] != "" and not checkFillList(colList) and row > int(findEmpty(colList, direction)):
            colList[row], colList[findEmpty(colList, direction)] = colList[findEmpty(
                colList, direction)], colList[row]


def moveNumber(direction):
    for col in range(4):
        colList = []
        for row in range(4):
            colList.append(gameCells[4 * col + row].num)
            changeBlocks(colList, direction)
            addNumber(colList, direction)
            setNum(col, colList)


def operate(event):
    print(event.keysym)
    if event.keysym == "Left":
        for col in range(4):
            colList = []
            for row in range(4):
                colList.append(gameCells[4 * col + row].num)
            print(colList)
            for row in range(4):
                if colList[row] != "":
                    if not checkFillList(colList):
                        emptyBlockNumber = int(findEmpty(colList, "Left"))
                        if row > emptyBlockNumber:
                            colList[row], colList[emptyBlockNumber] = colList[emptyBlockNumber], colList[row]
            print(colList)
            addNumber(colList, "Left")
            # initialBoard()
            for row in range(4):
                gameCells[4 * col + row].num = colList[row]
    if event.keysym == "Right":
        for col in range(4):
            colList = []
            for row in range(4):
                colList.append(gameCells[4 * col + row].num)
            print(colList)
            for row in range(4):
                if colList[3-row] != "":
                    if not checkFillList(colList):
                        emptyBlockNumber = int(findEmpty(colList, "Right"))
                        if 3-row < emptyBlockNumber:
                            colList[3-row], colList[emptyBlockNumber] = colList[emptyBlockNumber], colList[3-row]
            print(colList)
            addNumber(colList, "Right")
            # initialBoard()
            for row in range(4):
                gameCells[4 * col + row].num = colList[row]
    if event.keysym == "Up":
        for row in range(4):
            rowList = []
            for col in range(4):
                rowList.append(gameCells[4 * col + row].num)
            print(rowList)
            for col in range(4):
                if rowList[col] != "":
                    if not checkFillList(rowList):
                        emptyBlockNumber = int(findEmpty(rowList, "Up"))
                        if col > emptyBlockNumber:
                            rowList[col], rowList[emptyBlockNumber] = rowList[emptyBlockNumber], rowList[col]
            print(rowList)
            addNumber(rowList, "Up")
            # initialBoard()
            for col in range(4):
                gameCells[4 * col + row].num = rowList[col]
    if event.keysym == "Down":
        for row in range(4):
            rowList = []
            for col in range(4):
                rowList.append(gameCells[4 * col + row].num)
            print(rowList)
            for col in range(4):
                if rowList[3-col] != "":
                    if not checkFillList(rowList):
                        emptyBlockNumber = int(findEmpty(rowList, "Down"))
                        if 3-col < emptyBlockNumber:
                            rowList[3-col], rowList[emptyBlockNumber] = rowList[emptyBlockNumber], rowList[3-col]
            print(rowList)
            addNumber(rowList, "Down")
            # initialBoard()
            for col in range(4):
                gameCells[4 * col + row].num = rowList[col]
    fillNumber()
    for gameCell in gameCells:
        set_number(gameCell.num, gameCell.x, gameCell.y)


def checkFillList(checkList):
    for ele in checkList:
        if ele == "":
            return False
            break
    return True


def addNumber(cellList, direction):
    if direction == "Left" or direction == "Up":
        for row in range(3):
            if cellList[row] == cellList[row + 1] and cellList[row] != "":
                print("-------")
                addNum = int(cellList[row]) * 2
                cellList[row] = str(addNum)
                cellList[row + 1] = ""
                putAside(cellList, row + 1, direction)
                print("数字が足し算されました")
                break
    if direction == "Right" or direction == "Down":
        for row in range(3):
            if cellList[3 - row] == cellList[2-row] and cellList[3 - row] != "":
                addNum = int(cellList[3 - row]) * 2
                cellList[3 - row] = str(addNum)
                cellList[2 - row] = ""
                putAside(cellList, 2 - row, direction)
                print("数字が足し算されました")
                break


def putAside(cellList, number, direction):
    if direction == "Left" or direction == "Up":
        for num in range(number, len(cellList) - 1):
            cellList[num], cellList[num + 1] = cellList[num + 1], cellList[num]
    if direction == "Right" or direction == "Down":
        for num in range(number, 1):
            cellList[num], cellList[num - 1] = cellList[num - 1], cellList[num]


def findEmpty(list, direction):
    if direction == "Left" or direction == "Up":
        for i in range(4):
            if list[i] == "":
                return i
    elif direction == "Right" or direction == "Down":
        for i in range(4):
            if list[3-i] == "":
                return 3-i


def fillNumber():
    while True:
        newRandom = random.randint(0, 4)
        if newRandom == 4:
            newNumber = 4
        else:
            newNumber = 2
        fillX = random.randint(0, 3)
        fillY = random.randint(0, 3)
        if gameCells[fillX + 4 * fillY].num == "":
            gameCells[fillX + 4 * fillY].num = str(newNumber)
            break


def play():
    global canvas
    root, canvas = create_canvas()
    set_field()
    initialBoard()
    decideLocation()
    for gameCell in gameCells:
        set_number(gameCell.num, gameCell.x, gameCell.y)
    print(gameCells)
    root.bind("<Key>", lambda event: operate(event))
    root.mainloop()


play()
