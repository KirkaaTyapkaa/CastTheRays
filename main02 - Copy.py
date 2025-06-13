import math

from ClassesCells01 import *
import math as ma
import pygame as pyg
class Grid():
    gridSize = 25  # 5x5 cells
    #global gridMatrix
    def __init__(self,cellSize,Tmargin,pscreen,renderDst):
        self.renderDst = renderDst
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
        #self.assembleGrid()
        self.walls = []
        self.assembleGrid()


    def update(self):
        for wall in self.walls:
            pyg.draw.line(self.screen, (255, 255, 000), wall[0], wall[1], 5)

    def addWall(self,XY1,XY2):
        self.walls.append([XY1,XY2])

        tmpLen = ma.sqrt( (XY1[0]-XY2[0])**2 +  (XY1[1]-XY2[1])**2 )
        tmpSegmentCount = int(tmpLen // (self.cellSize+ self.Tmargin) +1)
        tmpPoints = [XY1,XY2]
        for i in range(1,tmpSegmentCount):
            x1, y1 = XY1
            x2, y2 = XY2
            fifth_x = x1 + (i / tmpSegmentCount) * (x2 - x1)
            fifth_y = y1 + (i / tmpSegmentCount) * (y2 - y1)
            tmpPoints.append([fifth_x,fifth_y])
        print(tmpPoints)
        #return tmpPoints




        for row in self.gridMatrix:
            for cell in row:
                for point in tmpPoints:
                    if cell.rect.collidepoint(point):
                        cell.walls.append(len(self.walls) - 1)
                        cell.curColour = (150, 0, 0)


                 #
        #pyg.draw.line(self.screen, (255, 255, 255), XY1, XY2, 3)


    def doLinesIntersectGPT(sellf,line1_start, line1_end, line2_start, line2_end):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

        return intersect(line1_start, line1_end, line2_start, line2_end)

    def findIntersectionGPT(self,line1_start, line1_end, line2_start, line2_end):
        x1, y1 = line1_start
        x2, y2 = line1_end
        x3, y3 = line2_start
        x4, y4 = line2_end

        # Координаты точки пересечения
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        return px, py
    def distance(self,point1, point2):
        return ma.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    def checkCollisions(self,xy1,xy2):
        dst = []
        compDst = self.renderDst # сравнительная дальность
        dstTmp = self.renderDst
        for wall in self.walls:
            if self.doLinesIntersectGPT(wall[0],wall[1],xy1,xy2):
                tgtXY = self.findIntersectionGPT(wall[0],wall[1],xy1,xy2)

                dstTmp = self.distance(xy1,tgtXY)
                pyg.draw.circle(self.screen, (255, 0, 255), tgtXY, 5, )
            if dstTmp < compDst:
                compDst = dstTmp
        dst.append(compDst)
           #     cords.append(xy2)
        #print("cords ",cords)
        return dst

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

    def __init__(self,pscreen,pgrid,renderDist):
        self.grid = pgrid
        self.screen = pscreen
        self.x = 50
        self.y = 50
        self.len = renderDist
        self.walkSpd = 1
        self.angle = 0
        self.rotateSpd = 0.05
        self.raysCount = 40
        self.rayStep = 5

    def calcWalkPos(self, dir, parallel= False):
        if not parallel:
            self.x  = self.x + self.walkSpd * ma.cos(self.angle) * dir
            self.y = self.y + self.walkSpd * ma.sin(self.angle) * dir
        else:
            self.x = self.x + self.walkSpd * ma.cos(self.angle + math.pi/2) * dir
            self.y = self.y + self.walkSpd * ma.sin(self.angle + math.pi/2) * dir

        #return (finx, finy)
    def rotate(self,arr):
        if arr[0]:
            self.angle -= self.rotateSpd
        if arr[1]:
            self.angle += self.rotateSpd
    def move(self,arr):
        if arr[0]:
            self.calcWalkPos(1)
        if arr[1]:
            self.calcWalkPos(-1)
        if arr[2]:
            self.calcWalkPos(1, True)
        if arr[3]:
            self.calcWalkPos(-1, True)

    def distance(self,point1, point2):
        return ma.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def calcRotPos(self, offset = 0):
        finx = self.x + self.len * ma.cos(self.angle+offset)
        finy = self.y + self.len * ma.sin(self.angle+offset)
        return (finx,finy)

    def update(self):
        wallsArr = []
        count = 0
        og = -self.raysCount
        for offset in range(-self.raysCount,self.raysCount+1,1):
            og += 1
            if offset != 0:
           # print(abs(offset)/self.raysCount, "offest")
               # print(abs(offset) / og, "offest")
              #  print(ma.log(abs(offset/og),ma.e), "fin")
              #  logCoef = ma.log(abs(offset/og),ma.e)
                logCoef = ma.log(abs(offset*0.023)/self.raysCount, ma.e) * (abs(offset)/offset) * (offset*0.023)
            else:
                logCoef = 0
            xy2 = self.calcRotPos(offset*0.023)
            pyg.draw.line(self.screen, (255, 255, 255), (self.x, self.y), xy2, 5)
            tmpArr =self.grid.checkCollisions(((self.x, self.y)), xy2)
            #print(tmpArr)
            for collision in tmpArr:
                #dst = self.distance((self.x,self.y),collision)
                wallsArr.append([count,collision])

            count += 1
        #print("walls ", wallsArr)
        return wallsArr


        #for i in range(-3,3,1):
         #   pyg.draw.line(self.screen, (255,255,255), (self.x,self.y), self.calcEndPos(i*0.1),5)

class PlayScreen():

    def __init__(self,pscreen,renderDist):
        self.bigScreen = pscreen
        self.scrWidth = 500
        self.scrHeight = self.scrWidth* (9 / 16)

        self.maxDst = renderDist # TEMP
        self.rectsWidth = 5

        self.screen = self.bigScreen.subsurface((250,250, self.scrWidth,self.scrHeight ))


    def update(self,wallArr):
        self.updateScreen()
        startX = 10 # TEMP
        dx = 0
        for i in range(len(wallArr)):
            dx = startX + self.rectsWidth*wallArr[i][0]
            #for j in range(len(wallArr[i])):
            dstPerc =(wallArr[i][1]/self.maxDst) # ma.log(5,ma.e)
            heightD = dstPerc *  200
            #tmpRect = pyg.Rect(startX+dx, heightD/2, self.rectsWidth, self.scrHeight - heightD)
            tmpRect = pyg.Rect(startX + dx, heightD / 2, self.rectsWidth, self.scrHeight - heightD)
           # dx += self.rectsWidth
            pyg.draw.rect(self.screen, (((dstPerc-1)**2)*255,((dstPerc-1)**2)*255,((dstPerc-1)**2)*255), tmpRect)



    def updateScreen(self):
        self.screen.fill((70, 50, 50))

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
    renderDst = 500
    grid = Grid(40,5,screen,renderDst)
    clockSpeed = 60
    TPS = pyg.time.Clock()

    plr = Player(screen,grid,renderDst)
    cameraDir = [False,False]
    moveDir = [False,False,False,False]
    playScreen = PlayScreen(screen,renderDst)
    print(1/0.0000000050)

    grid.addWall((100, 100), (200, 300))
    grid.addWall((550, 100), (100, 500))
    grid.addWall((300, 200), (600, 300))
    grid.addWall((100, 200), (600, 50))
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
                    if event.key == pyg.K_e:
                        moveDir[2] = True
                    if event.key == pyg.K_q:
                        moveDir[3] = True
                case pyg.KEYUP:
                    if event.key == pyg.K_a:
                        cameraDir[0] = False
                    if event.key == pyg.K_d:
                        cameraDir[1] = False
                    if event.key == pyg.K_w:
                        moveDir[0] = False
                    if event.key == pyg.K_s:
                        moveDir[1] = False
                    if event.key == pyg.K_e:
                        moveDir[2] = False
                    if event.key == pyg.K_q:
                        moveDir[3] = False

        screen.fill((50, 50, 50))
        #grid.gridUpd(0,0)
        grid.update()
        plr.move(moveDir)
        plr.rotate(cameraDir)

        wallArr = plr.update()
        #print(wallArr)
        playScreen.update(wallArr)


        TPS.tick(clockSpeed)  # it should not be here?
        pyg.display.update()



main()