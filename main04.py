import math

from ClassesCells01 import *
import math as ma
import pygame as pyg
class Grid():
    gridSize = 25  # 5x5 cells
    #global gridMatrix
    def __init__(self,cellSize,Tmargin,pscreen,renderDst,plr= None):
        self.renderDst = renderDst
        self.screen = pscreen
        self.plr = plr
        self.visibleWalls =[]
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
            pyg.draw.line(self.screen, wall[2], wall[0], wall[1], 5)

    def addWall(self,XY1,XY2,col):
        self.walls.append([XY1,XY2,col])

        tmpLen = ma.sqrt( (XY1[0]-XY2[0])**2 +  (XY1[1]-XY2[1])**2 )
        tmpSegmentCount = int(tmpLen // (self.cellSize+ self.Tmargin) +1)
        tmpPoints = [XY1,XY2]
        for i in range(1,tmpSegmentCount):
            x1, y1 = XY1
            x2, y2 = XY2
            fifth_x = x1 + (i / tmpSegmentCount) * (x2 - x1)
            fifth_y = y1 + (i / tmpSegmentCount) * (y2 - y1)
            tmpPoints.append([fifth_x,fifth_y])
        #print(tmpPoints)
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
            #precision -
            if  (C[1] - A[1]) * (B[0] - A[0]) > ((B[1] - A[1]) * (C[0] - A[0])  ) or (C[1] - A[1]) * (B[0] - A[0]) > ((B[1] - A[1]) * (C[0] - A[0]) ):
                return True # эта 10 это десятка и если её убрать всё начент мигать,

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

    def getAngleFromPlr(self,point):
        pass

    def checkVisibleWalls(self,triangle):

        visibleWallsArr = []

        костыль = 0
        for wall in self.walls:
            visiblePoints = []

           # visiblePoints = self.checkCollisionsV2(triangle[0],triangle[1],wall,visiblePoints,50, triangle )
           # visiblePoints = self.checkCollisionsV2(triangle[1], triangle[2], wall,visiblePoints,50,triangle )
           # visiblePoints = self.checkCollisionsV2(triangle[0], triangle[2], wall,visiblePoints,50, triangle )
            visiblePoints = self.checkCollisionsV3(triangle,wall,visiblePoints)

            visiblePoints = self.isPointInTrig(wall[0],triangle,visiblePoints)
            visiblePoints = self.isPointInTrig(wall[1], triangle,visiblePoints)

            if len(visiblePoints) == 2:
                visiblePoints.append(костыль)
                visibleWallsArr.append(visiblePoints)
            elif len(visiblePoints) == 3:
                print("yes")
            elif len(visiblePoints) == 1:
                print("len 1")
            костыль += 1

        self.visibleWalls = visibleWallsArr
       # print(visibleWallsArr)
        #self.drawVisibleWallsDeb()
        self.sortVisibleWallsV2(triangle)
        self.drawVisibleWallsDeb()
        print(self.visibleWalls, len(self.visibleWalls))
        #self.sortVisibleWalls()
        #print(visibleWallsArr, "this hsit is visivble walls")
        for wallInd in range(len(self.visibleWalls)):
            wall = self.visibleWalls[wallInd]
            dstTmp = self.distance(triangle[0],wall[0])
            angle = self.angle_between_lines((triangle[0],triangle[1]),( triangle[0],wall[0]))
            wall[0] = (angle,dstTmp)

            dstTmp = self.distance(triangle[0], wall[1])
            angle = self.angle_between_lines((triangle[0], triangle[1]), ( triangle[0],wall[1]))
            wall[1] = (angle,dstTmp)


            self.visibleWalls[wallInd] = wall
        print(self.visibleWalls, len(self.visibleWalls), "углы растояния")
        return self.visibleWalls
    def sortVisibleWallsV2(self,triangle):
        sortedWalls = []
        startXY = (self.plr.x, self.plr.y)

        for curWall in self.visibleWalls:
            pyg.draw.line(self.screen, (0, 0, 255), (self.plr.x, self.plr.y), curWall[0], 5)
            pyg.draw.line(self.screen, (0, 100, 255), (self.plr.x, self.plr.y), curWall[1], 5)

            middleXY1 = curWall[0]
            middleXY2 = curWall[1]

            angleTmp = self.angle_between_lines(((self.plr.x, self.plr.y), curWall[0]),((self.plr.x, self.plr.y),triangle[1]))
            хуйПодзалупногоТворожка = self.plr.calcRotPos(-self.plr.fov + angleTmp)  # -self.plr.fov
            endXY1 =  хуйПодзалупногоТворожка

            angleTmp = self.angle_between_lines(((self.plr.x, self.plr.y), curWall[1]),   ((self.plr.x, self.plr.y), triangle[1]))
            хуйПодзалупногоТворожка = self.plr.calcRotPos(-self.plr.fov + angleTmp)  # -self.plr.fov
            endXY2 = хуйПодзалупногоТворожка

            pyg.draw.line(self.screen, (255, 0, 255), middleXY1, endXY1, 5)

            pyg.draw.line(self.screen, (255, 200, 255), middleXY2, endXY2, 5)

            selWall = curWall

            # всё выше просто шоб найти лучи до и после каря стены

            noWallsInFront = True
            allWallsInFrontSorted = True
            curWallInsertionInd = 0
            foundWalls = []
            for checkWall in self.visibleWalls:  # для стен перед выбранной стеной
                if checkWall != selWall:
                    if self.doLinesIntersectGPT(startXY,middleXY1,checkWall[0],checkWall[1]): # проверяем левый луч
                        noWallsInFront = False
                        foundWalls.append(checkWall)
                        try:
                            sortedWalls.index(checkWall)
                        except:  # если стены нету в осторитивравнном массиве то просто добавляем
                            allWallsInFrontSorted = False
                            sortedWalls.append(checkWall)
                    elif self.doLinesIntersectGPT(startXY, middleXY2, checkWall[0], checkWall[1]):
                        noWallsInFront = False
                        foundWalls.append(checkWall)
                        try:
                            sortedWalls.index(checkWall)
                        except:
                            allWallsInFrontSorted = False
                            sortedWalls.append(checkWall)

            # добавляем текущию стену, или не добавляем
            if selWall in sortedWalls:

                for foundWall in foundWalls:
                    if foundWall in sortedWalls:
                        foundWallInd = sortedWalls.index(foundWall)
                        selWallInd = sortedWalls.index(selWall)
                        if foundWallInd > selWallInd:
                            tmpWall = sortedWalls[foundWallInd]
                            sortedWalls[foundWallInd] = sortedWalls[selWallInd]
                            sortedWalls[selWallInd] = tmpWall

                for foundWall in foundWalls:
                    if foundWall in sortedWalls == False:
                        foundWallInd = sortedWalls.index(foundWall)
                        sortedWalls.insert(foundWallInd+1,foundWall)


            else:
                if noWallsInFront: # если стен перед этой не обнаружено, то пихаем в начало
                # if len(foundWalls) == 0
                    sortedWalls.insert(0,selWall)
                elif allWallsInFrontSorted:

                    insInd = 0
                    for foundWall in foundWalls:
                        if sortedWalls.index(foundWall) > insInd:
                            insInd = sortedWalls.index(foundWall)
                    sortedWalls.insert(insInd+1,selWall)

                else:
                    sortedWalls.append(selWall)



            selWallInd = sortedWalls.index(selWall)
            for checkWall in self.visibleWalls:  # для стен после выбранной стеной
                if checkWall != selWall:
                    if self.doLinesIntersectGPT(middleXY1,endXY1,checkWall[0],checkWall[1]): # проверяем левый луч
                        if checkWall in sortedWalls:
                            checkWallInd = sortedWalls.index(checkWall)
                            if checkWallInd  < selWallInd:
                                tmpWall = sortedWalls[checkWallInd]
                                sortedWalls[checkWallInd] = sortedWalls[selWallInd]
                                sortedWalls[selWallInd] = tmpWall

                        else:
                            sortedWalls.insert(selWallInd+1,checkWall)

        self.visibleWalls = sortedWalls





    # for curWall in self.visibleWalls:


    def sortVisibleWalls(self):
        visibleWallsArr = self.visibleWalls
        #self.drawVisibleWallsDeb()
        ind = 0
        for wall in visibleWallsArr: # стену которую сейчас чекаем
            print(wall)
            pyg.draw.line(self.screen, (0, 0, 255), (self.plr.x, self.plr.y), wall[0], 5)
            pyg.draw.line(self.screen, (255, 0, 255), (self.plr.x, self.plr.y), wall[1], 5)
            wallTmp = visibleWallsArr[0]

            tmpSucces = False
            ind2 = 0
            for checkWall in visibleWallsArr: # с какими стенами чекаем
                firstRay = False
                secRay = False
                tmpSucces = False
                if wall != checkWall:
                    if self.doLinesIntersectGPT((self.plr.x, self.plr.y), wall[1], checkWall[0], checkWall[1]):
                        firstRay = True
                        wallInd = 1
                        crossPoint = self.findIntersectionGPT((self.plr.x, self.plr.y), wall[1], checkWall[0],checkWall[1])
                        pyg.draw.circle(self.screen, (255, 0, 255), crossPoint, 7, )
                        tmp = checkWall
                        visibleWallsArr[ind2] = wall
                        visibleWallsArr[ind] = tmp


                    if self.doLinesIntersectGPT((self.plr.x, self.plr.y), wall[0], checkWall[0], checkWall[1]):
                        wallInd = 0
                        secRay = True
                        crossPoint = self.findIntersectionGPT((self.plr.x, self.plr.y), wall[0], checkWall[0],checkWall[1])

                        pyg.draw.circle(self.screen, (0, 0, 255), crossPoint, 12, )
                        tmp = checkWall
                        visibleWallsArr[ind2] = wall
                        visibleWallsArr[ind] = tmp
                  #  if firstRay and secRay :
                        #visibleWallsArr.pop(ind)
                #        pass
                #    else:
                #        tmp = checkWall
                #        visibleWallsArr[ind2] = wall
                #        visibleWallsArr[ind] = tmp

                ind2 += 1

            ind += 1

        self.visibleWalls = visibleWallsArr



        #



    def isPointInTrig(self,point,triangle,visibleArr):

        mainTrig = self.getTriangleArea(triangle[0],triangle[1],triangle[2])
        tmpTrig1 = self.getTriangleArea(point,triangle[1],triangle[2])
        tmpTrig2 = self.getTriangleArea(triangle[0], point, triangle[2])
        tmpTrig3 = self.getTriangleArea(triangle[0], triangle[1], point)
        tmpTotalArea = tmpTrig1 + tmpTrig2 + tmpTrig3
        diff = abs(mainTrig - tmpTotalArea)

        if diff < 5:
            pyg.draw.circle(self.screen, (255 , 0, 0 ), point, 5, )
            visibleArr.append(point)

            angle = self.angle_between_lines((triangle[0], triangle[1]), (triangle[0], point))

        return visibleArr

    def drawVisibleWallsDeb(self):

        max = len(self.visibleWalls)
        count = 0
        for wall in self.visibleWalls:
            pyg.draw.line(self.screen, (0, 255* (count/max), 0), wall[0], wall[1], 5)
            count += 1


    def getTriangleArea(self,a,b,c):
        return abs((a[0] - c[0]) * (b[1] - c[1]) + (b[0] - c[0]) * (c[1] - a[1]))

    def checkCollisionsV4(self,trig,wall,visibleArr):
        if self.doLinesIntersectGPT(wall[0], wall[1], trig[sideInd], trig[secSide]):
            tgtXY = self.findIntersectionGPT(wall[0], wall[1], trig[sideInd], trig[secSide])

    def checkCollisionsV3(self,trig,wall,visibleArr):
        angle = 0

        #pyg.draw.circle(self.screen, (255, 0, 255), trig[1], 5, )
       # print(trig)
        for sideInd in range(3):
            secSide = (sideInd + 1)%3
            if self.doLinesIntersectGPT(wall[0], wall[1], trig[sideInd], trig[secSide]):

                tgtXY = self.findIntersectionGPT(wall[0], wall[1], trig[sideInd], trig[secSide])

                if sideInd == 1:
                    angle = self.angle_between_lines((trig[0],trig[1]),(trig[0],tgtXY))
                pyg.draw.circle(self.screen, (255, 0, 255), tgtXY, 5, )
                visibleArr.append(tgtXY)
        return visibleArr


    def checkCollisionsV2(self,xy1,xy2,wall,visibleArr,colour, trig):
        wall = wall[:2]
        maxColNum = 200
        colour += maxColNum / 2
        colNow = colour / maxColNum

        if self.doLinesIntersectGPT(wall[0], wall[1], xy1, xy2):
            tgtXY = self.findIntersectionGPT(wall[0], wall[1], xy1, xy2)
            dstTmp = self.distance(xy1, tgtXY)
            pyg.draw.circle(self.screen, (255 * colNow, 0, 255 * colNow), tgtXY, 5, )
            visibleArr.append(tgtXY)


        return visibleArr

    def angle_between_lines(self,line1,line2): # gpt

        xy1, xy2 = line1
        xy3, xy4 = line2

        x1, y1 = xy1
        x2, y2 = xy2
        x3, y3 = xy3
        x4, y4 = xy4
        # Найдите векторы
        vec_ab = (x2 - x1, y2 - y1)
        vec_cd = (x4 - x3, y4 - y3)

        # Вычислите скалярное произведение векторов
        dot_product = vec_ab[0] * vec_cd[0] + vec_ab[1] * vec_cd[1]

        # Найдите длины векторов
        length_ab = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        length_cd = math.sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)

        # Найдите угол между векторами
        tmpSmthingIdk = (length_ab * length_cd)
        precision = 1000
        thisThing =  ma.floor((dot_product / (length_ab * length_cd)) * precision) /precision

        angle_rad = math.acos(thisThing)


        lineTmp = self.plr.calcRotPos(-self.plr.fov+angle_rad)#-self.plr.fov
        #pyg.draw.line(self.screen, (255, 255, 255),(self.plr.x,self.plr.y ), (lineTmp[0],lineTmp[1]), 5)

        #debug rays
        #pyg.draw.line(self.screen, (0, 255, 255), (self.plr.x, self.plr.y), (lineTmp[0], lineTmp[1]), 5)

        # Преобразуйте угол из радиан в градусы
        #angle_deg = math.degrees(angle_rad)

        return angle_rad

    def checkCollisions(self,xy1,xy2,colour):
        dst = []
        maxColNum = 200
        colour += maxColNum /2
        colNow = colour/maxColNum
        compDst = self.renderDst # сравнительная дальность
        dstTmp = self.renderDst
        for wall in self.walls:
            if self.doLinesIntersectGPT(wall[0],wall[1],xy1,xy2):
                tgtXY = self.findIntersectionGPT(wall[0],wall[1],xy1,xy2)
                dstTmp = self.distance(xy1,tgtXY)
                pyg.draw.circle(self.screen, (255*colNow, 0, 255*colNow), tgtXY, 5, )
            if dstTmp < compDst:
                compDst = dstTmp
        dst.append(compDst)
           #     cords.append(xy2)

        return compDst

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

    def __init__(self,pscreen,pgrid,renderDist,rays):
        self.grid = pgrid
        self.screen = pscreen
        self.x = 50
        self.y = 50
        self.len = renderDist
        self.walkSpd = 2
        self.angle = 0
        self.fov = ma.pi/4

        self.rotateSpd = 0.05
        self.raysCount = rays//2
        self.angleStep = self.fov / self.raysCount
        self.rayStep = 5
        self.update()

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

    def update(self,moveArr=(False,False,False,False),rotArr=(False,False)):
        self.rotate(rotArr)
        self.move(moveArr)
       # wallsArr = []
        #count = 0

        xy = (self.x,self.y)
        #angles = [-self.fov,self.fov]
        cords = [self.calcRotPos(-self.fov),self.calcRotPos(self.fov)]
        triangle = [[xy,cords[0]],[xy,cords[1]],[cords[0],cords[1]]]
        self.triangle = triangle
        for line in triangle:
            pyg.draw.line(self.screen, (255, 255, 255), line[0], line[1], 5)
            #self.grid.checkCollisions(line[0], line[1], 50)
        triangle = [xy, cords[0], cords[1]]
        return triangle
        #print(cords)
     #   for xyTmp in angles:
      #      xy = self.calcRotPos(xyTmp)
      #      pyg.draw.line(self.screen, (255, 255, 255), (self.x, self.y), xy, 5)
            #self.grid.checkCollisions((self.x, self.y), xy, 50)
        #
        #self.grid.checkCollisions(self.calcRotPos(angles[0]), self.calcRotPos(angles[-1]), 50)

class PlayScreen():

    def __init__(self,pscreen,renderDist,raysNum,plr):
        self.plr = plr
        self.bigScreen = pscreen
        self.scrWidth = 500
        self.scrHeight = self.scrWidth* (9 / 16)
        self.raysCount = raysNum
        self.maxDst = renderDist # TEMP
        self.maxDst = 380
        self.rectsWidth = 500 // raysNum
        self.fishEyeCoef = 1.3

        self.screen = self.bigScreen.subsurface((250,250, self.scrWidth,self.scrHeight ))
    def distance(self,point1, point2):
        return ma.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def update(self,wallArr,triangle):
        self.updateScreen()
        startX = 10 # TEMP
        dx = 0
        maxDst = self.plr.len
       # maxDst = 500
        maxAngle = self.plr.fov *2
        width = 500
        middle = 150
        maxHeight = 250
        wallArr.reverse()

        forwardRayLen =  ma.sqrt((self.distance(triangle[0],triangle[1])**2) - ((self.distance(triangle[1],triangle[2])/2)**2 ))
        print(forwardRayLen)

        angleCoefMax = maxDst / forwardRayLen -1
       # angleCoefMax = 0.4
       # angleCoefMax = forwardRayLen/maxDst
        print(angleCoefMax)

        colCoefMax = len(wallArr)
        #for wallInd in range(len(wallArr)):
        count = 0
        for wallInd in wallArr:
            wall = wallInd
            x1 = wall[0][0]/maxAngle * width

            y1AngleCoef = (1 -abs(wall[0][0] - self.plr.fov)/self.plr.fov) * angleCoefMax +1  # чёт там умное чситает я ебу, шоб стены за стенам и не видно было
            y1AngleCoef = ma.cos(abs(wall[0][0] - self.plr.fov)) * angleCoefMax + 1
            y1AngleCoef = ma.cos(abs(wall[0][0] - self.plr.fov))
            if y1AngleCoef < 0 :
                print("oh no")

            y1 = (1 -(wall[0][1]*y1AngleCoef)/(maxDst ))
            if y1 <0:
                y1 = 0
            y1 = y1 * maxHeight


            x2 = wall[1][0]/maxAngle * width

            y2AngleCoef = (1 - abs(wall[1][0] - self.plr.fov) / self.plr.fov) * angleCoefMax + 1
          #  y2AngleCoef = ma.cos(abs(wall[1][0] - self.plr.fov)) * angleCoefMax + 1
            y2AngleCoef = ma.cos(abs(wall[1][0] - self.plr.fov))
            y2 = (1- (wall[1][1]*y2AngleCoef) / (maxDst) )
            if y2 <0:
                y2 = 0
            y2 = y2 * maxHeight

            colDebCoef = count/colCoefMax
            count += 1
            pyg.draw.polygon(self.screen,(255*colDebCoef*0,255*colDebCoef,255*colDebCoef*0),((x2,y2+middle),(x2,middle-y2),(x1,middle-y1),(x1,middle+y1)))






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
    renderDst = 550
    grid = Grid(40,5,screen,renderDst)
    clockSpeed = 30
    TPS = pyg.time.Clock()
    raysNum = 80
    plr = Player(screen,grid,renderDst,raysNum)
    grid.plr = plr
    cameraDir = [False,False]
    moveDir = [False,False,False,False]
    playScreen = PlayScreen(screen,renderDst,raysNum,plr)
    print(1/0.0000000050)

    #grid.addWall((100, 100), (200, 300),(255,255,0))
   # grid.addWall((550, 100), (100, 500),(255,255,0))
    grid.addWall((300, 200), (600, 300),(255,255,0))
    grid.addWall((320, 100), (600, 50),(255,255,0))
  #  grid.addWall((200, 200), (300, 250), (255, 255, 0))
    grid.addWall((150, 50), (450, 550), (255, 255, 0))
    grid.addWall((250, 150), (300, 200), (255, 255, 0))
    #grid.addWall((350, 150), (300, 200), (255, 255, 0))
    #grid.addWall((200, 200), (300, 250), (255, 255, 0))
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
        #plr.move(moveDir)
       # plr.rotate(cameraDir)


        visionTriangle = plr.update(moveDir,cameraDir)
        visbleWalls = grid.checkVisibleWalls(visionTriangle)
        #print(wallArr)
        playScreen.update(visbleWalls,visionTriangle)


        TPS.tick(clockSpeed)  # it should not be here?
        pyg.display.update()



main()