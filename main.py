from ClassesCells02 import *
import math as ma
import pygame as pyg
class Grid():
    gridSize = 25  # 5x5 cells
    #global gridMatrix
    def __init__(self,cellSize,Tmargin,pscreen):
        self.screen = pscreen
        #screen = self.screen  # thats absolute rubbish, but just let it be, im too lazy
        self.dispLength ,self.dispHeight =  self.screen.get_size()

        self.gridMatrix = []
        self.cellSize = cellSize
        self.Tmargin = Tmargin  # DONT USE, HAVE NO IDEA HOW AND WHY ITS EXISCVTS
        #self.dx = 0 # i thnik they used only in camera move, should mean something like "difference in X"
        #self.dy = 0

        self.selCol = 0  # selected columng and row,
        self.selRow = 0
        self.dx = 0
        self.dy = 0
        self.assembleGrid()


        for y in range(len(self.gridMatrix)-1):
            self.gridMatrix[y][3] = Wall(self.gridMatrix[y][3].getBase())
        for x in range(len(self.gridMatrix)-1):
            self.gridMatrix[6][x] = Wall(self.gridMatrix[6][x].getBase())
        for x in range(5,len(self.gridMatrix)-1):
            self.gridMatrix[3][x] = Wall(self.gridMatrix[3][x].getBase())
        self.gridMatrix[6][7] = Floor(self.gridMatrix[6][7].getBase())

    def getCell(self,cords):
        self.getColRow(cords)
        if self.selRow < self.gridSize and self.selRow > 0 and self.selCol < self.gridSize and self.selCol > 0:
            return  self.gridMatrix[self.selRow][self.selCol]
        return Cell()


    def assembleGrid(self):
        self._x = 0  # _ для одноразовых
        self._y = 0
        self._x2 = self._x
        for i in range(self.gridSize):  # i = rows
            self.gridMatrix.append([])
            for j in range(self.gridSize):  # j = columns
                self.gridMatrix[i].append(Floor((self._x2, self._y, j, i, screen, self.cellSize,self
                                                ),))  # px,py,pcol,prow, pPlace,psize,pnearRoad,pgridOBJ,pmood

                self._x2 += self.cellSize + self.Tmargin
            self._y += self.cellSize + self.Tmargin
            self._x2 = self._x
        self._x = 0  # _ для одноразовых
        self._y = 0
    def getColRow(self,cords): # get Column and Row of grid на которых вот счас нажали
        xMouse, yMouse = cords #pyg.mouse.get_pos() #
        self.selCol = int((xMouse + self.dx - self._x) // (self.cellSize + self.Tmargin))  # selected column # бялт что это иксы с нижним подчеркивание, откуда они, пиздец
        #print((xMouse + self.dx - self._x))
        self.selRow = int((yMouse + self.dy - self._y) // (self.cellSize + self.Tmargin))
        #print("Sel Col,Row",self.selCol,self.selRow)
        return self.selCol,self.selRow
    def gridUpd(self, _dx, _dy): # I think used only in cameraMove # could use dictionary to определять шо счас делать
        for row in self.gridMatrix:
            for cell in row:
                cell.move(_dx, _dy)

class Player():

    def __init__(self,pscreen):
        self.screen = pscreen
        self.x = 50
        self.y = 50
        self.len = 50
        self.walkSpd = 2
        self.angle = 0
        self.rotateSpd = 0.01


        self.rayStep = 5

    def calcStepPos(self, dir):
        finx = self.x + self.walkSpd * ma.cos(self.angle) * dir
        finy = self.y + self.walkSpd * ma.sin(self.angle) * dir
        self.x = finx
        self.y = finy
        #return (finx, finy)

    def rotate(self,arr):
        if arr[0]:
            self.angle -= self.rotateSpd
        if arr[1]:
            self.angle += self.rotateSpd
    def move(self,arr):
        if arr[0]:
            self.calcStepPos(1)
        if arr[1]:
            self.calcStepPos(-1)

    def distance(self,point1, point2):
        return ma.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    def checkColision(self,matrix):
        dstArr = []
        for j in range(-80,81,1):
        #for j in range(0, 1, 1):
            x = self.x
            y = self.y
            for i in range(100):
                finx = x + self.rayStep * ma.cos(self.angle+j*0.005)
                finy = y + self.rayStep * ma.sin(self.angle+j*0.005)
                x = finx
                y = finy
                if  matrix.getCell((finx,finy)).type == "wall":
                    dstArr.append(self.distance((self.x,self.y),(finx,finy)))
                    #print(dstArr)
                    pyg.draw.circle(self.screen, (255,255,255), (x,y),5,)
                    break
                elif i == 99:
                    dstArr.append(500)
        return dstArr

    def calcEndPos(self, offset = 0):
        finx = self.x + self.len * ma.cos(self.angle+offset)
        finy = self.y + self.len * ma.sin(self.angle+offset)
        return (finx,finy)

    def update(self):
        pyg.draw.line(self.screen, (255, 255, 255), (self.x, self.y), self.calcEndPos(), 5)
        #for i in range(-3,3,1):
         #   pyg.draw.line(self.screen, (255,255,255), (self.x,self.y), self.calcEndPos(i*0.1),5)

class PlayScreen():

    def __init__(self,pscreen):
        self.bigScreen = pscreen
        self.scrWidth = 500
        self.scrHeight = self.scrWidth* (9 / 16)

        self.maxDst = 500 # TEMP
        self.rectsWidth = 3

        self.screen = self.bigScreen.subsurface((250,250, self.scrWidth,self.scrHeight ))


    def update(self,wallArr):
        self.updateScreen()
        startX = 10 # TEMP
        dx = 0
        for i in range(len(wallArr)):
            dstPerc = wallArr[i]/self.maxDst
            heightD = dstPerc *  100
            #tmpRect = pyg.Rect(startX+dx, heightD/2, self.rectsWidth, self.scrHeight - heightD)
            tmpRect = pyg.Rect(startX + dx, heightD / 2, self.rectsWidth, self.scrHeight - heightD)
            dx += self.rectsWidth
            pyg.draw.rect(self.screen, (255- dstPerc*255,255-dstPerc*255,255-dstPerc*255), tmpRect)



    def updateScreen(self):
        self.screen.fill((50, 50, 50))

def main():
    pyg.init()
    baseFont = pyg.font.Font(None, 12)
    # load and set the logo
    #logo = pyg.image.load("logo32x32.png")
    #pyg.display.set_icon(logo)
    pyg.display.set_caption("minimal program")
    # create a surface on screen that has the size of 240 x 180
    global dispLength, dispHeight
    dispLength = 1024
    dispHeight = dispLength * (9 / 16)
    global screen
    screen = pyg.display.set_mode((dispLength, dispHeight))
    screen.fill((50, 50, 50))
    grid = Grid(40,5,screen)
    clockSpeed = 60
    TPS = pyg.time.Clock()
    plr = Player(screen)
    cameraDir = [False,False]
    moveDir = [False,False]
    playScreen = PlayScreen(screen)
    print(1/0.0000000050)


#    debRect =
    while True:
        for event in pyg.event.get():
            match event.type:
                case pyg.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                    pyg.quit()
                case pyg.KEYDOWN:
                    if event.key == pyg.K_a:
                        cameraDir[0] = True
                    if event.key == pyg.K_d:
                        cameraDir[1] = True
                    if event.key == pyg.K_w:
                        moveDir[0] = True
                    if event.key == pyg.K_s:
                        moveDir[1] = True
                case pyg.KEYUP:
                    if event.key == pyg.K_a:
                        cameraDir[0] = False
                    if event.key == pyg.K_d:
                        cameraDir[1] = False
                    if event.key == pyg.K_w:
                        moveDir[0] = False
                    if event.key == pyg.K_s:
                        moveDir[1] = False

        screen.fill((50, 50, 50))
        grid.gridUpd(0,0)
        plr.move(moveDir)
        plr.rotate(cameraDir)
        wallArr = plr.checkColision(grid)
       # print(wallArr)
        plr.update()
        playScreen.update(wallArr)
        #plr.angle += 0.01

        TPS.tick(clockSpeed)  # it should not be here?
        pyg.display.update()



main()