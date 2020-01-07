import queue

##### Canvas size
NX=200
NY=200
##########



MAXUD=16

#DIRECTION
FaceDOWN=8
FaceLEFT=4
FaceUP=2
FaceRIGHT=1

dirlist = [FaceUP,FaceDOWN,FaceLEFT,FaceRIGHT]


# BID
AIR=0
NOR=1
RFX=2
SPT=3

def counter(x):
    if x==FaceDOWN:
        return FaceUP
    if x==FaceUP:
        return FaceDOWN
    if x==FaceRIGHT:
        return FaceLEFT
    if x==FaceLEFT:
        return FaceRIGHT




def emit(x, y, face, isEmit): #Update Lights in the next block
    while True:
        nx=x
        ny=y
        if face == FaceUP:
            nx -=1
        elif face == FaceDOWN:
            nx +=1
        elif face == FaceLEFT:
            ny -=1
        else:
            ny +=1

        if (nx < 0 or nx >= NX or ny < 0 or ny >= NY): # reach boundarys
            return

        old_state = graph[nx][ny].state
        if (isEmit):
            graph[nx][ny].state |= face
        else:
            graph[nx][ny].state &= 15 - face

        if (graph[nx][ny].state != old_state):  # emission propagation
            if (graph[nx][ny].bid == AIR):
                x=nx
                y=ny
            elif (graph[nx][ny].bid == NOR):
                if (ISQUEUED[nx][ny]<MAXUD):
                    Qupdate.put((nx,ny))
                    ISQUEUED[nx][ny]+=1
            else:
                graph[nx][ny].update()
        else:
            return
    


class Block():
    def __init__(self, ix,iy,ibid):
        self.x=ix
        self.y=iy
        self.face=FaceUP  # outgoing direction running through this block. flags: D L U R
        self.state = 0
        self.bid=ibid

    def update(self): # logic for emission & clearance
        if self.bid == AIR:
            for dface in dirlist:
                emit(self.x,self.y,dface,dface & self.state)
        elif self.bid == NOR:
            emit(self.x,self.y,self.face, not (self.state & (15 - counter(self.face)) ))
            for dface in dirlist:
                if (dface!=self.face):
                    emit(self.x,self.y,dface,False)
        elif self.bid ==RFX:
            if self.face == FaceLEFT or self.face == FaceRIGHT:
                emit(self.x,self.y,FaceRIGHT, FaceDOWN & self.state);
                emit(self.x,self.y,FaceUP, FaceLEFT & self.state);
                emit(self.x,self.y,FaceDOWN  , FaceRIGHT & self.state);
                emit(self.x,self.y,FaceLEFT, FaceUP & self.state);
            else:
                emit(self.x,self.y,FaceRIGHT, FaceUP & self.state);
                emit(self.x,self.y,FaceDOWN, FaceLEFT & self.state);
                emit(self.x,self.y,FaceUP  , FaceRIGHT & self.state);
                emit(self.x,self.y,FaceLEFT, FaceDOWN & self.state);
        elif self.bid ==SPT:
            if self.face == FaceLEFT or self.face == FaceRIGHT:
                emit(self.x,self.y,FaceRIGHT, (FaceDOWN|FaceRIGHT) & self.state);
                emit(self.x,self.y,FaceDOWN, (FaceDOWN|FaceRIGHT) & self.state);
                emit(self.x,self.y,FaceUP  , (FaceLEFT|FaceUP) & self.state);
                emit(self.x,self.y,FaceLEFT, (FaceLEFT|FaceUP) & self.state);
            else:
                emit(self.x,self.y,FaceLEFT, (FaceDOWN|FaceLEFT) & self.state);
                emit(self.x,self.y,FaceDOWN, (FaceDOWN|FaceLEFT) & self.state);
                emit(self.x,self.y,FaceUP  , (FaceRIGHT|FaceUP) & self.state);
                emit(self.x,self.y,FaceRIGHT, (FaceRIGHT|FaceUP) & self.state);


ISQUEUED = [[0 for y in range(NY)] for x in range(NX)]
Qupdate = queue.Queue()


def ChangeBk(x, y, face, bid):
    graph[x][y].face = face
    graph[x][y].bid = bid
    graph[x][y].update()


def CommandA(x,y,dirr,bid):
    global ISQUEUED
    ISQUEUED = [[0 for y in range(NY)] for x in range(NX)]
    if 0<=x and x<NX and 0<=y and y<NY:
        ChangeBk(x,y,dirr,bid)
        while not Qupdate.empty():
            top = Qupdate.get()
            graph[top[0]][top[1]].update()


graph=[[Block(x,y,AIR) for y in range(NY)] for x in range(NX)]


if __name__ == '__main__':
    NX=input()
    NY=input()
    
    while True:
        op = input()
        if op == 'a':
            x=input()
            y=input()
            dirr = input()
            bid=input()
            if dirr =='u' or dirr =='U':
                dirr = FaceUP
            if dirr == 'd' or dirr == 'D':
                dirr = FaceDOWN
            if dirr== 'L' or dirr== 'l':
                dirr = FaceLEFT
            if dirr== 'R' or dirr== 'r':
                dirr = FaceRIGHT
            CommandA(x,y,dirr,bid)
