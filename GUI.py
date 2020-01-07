from tkinter import *
from core import *
import time
import os

FaceDOWN=8
FaceLEFT=4
FaceUP=2
FaceRIGHT=1

## Scaling 

len_sq = 20
len_bdr= 4
len_cir = len_sq//5

##
root = Tk()

# sby = Scrollbar(root)
# sby.pack(side=RIGHT,fill=Y)
# sbx = Scrollbar(root,orient=HORIZONTAL)
# sbx.pack(side=BOTTOM,fill=X,)

#width = min(NY*(len_sq+len_bdr),500) , height = min( NX*(len_sq+len_bdr)/2),500

cv = Canvas(root, background = 'white')
# cv.config(xscrollcommand= sbx.set,yscrollcommand=sby.set)
# sby.config(command = cv.yview)
# sbx.config(command = cv.xview)

cv_Tool = Canvas(root, background = 'white', width =len_sq*12 , height = len_sq*2)

cv_Tool.pack(side=BOTTOM)
cv.pack(expand=True,fill=BOTH)

cv_Tool.create_rectangle(len_sq/4,len_sq/4,len_sq*12-len_sq/4,len_sq*2-len_sq/4, outline='black', fill = None, width=1)
cv_Tool_offsetx = len_bdr*1.5
cv_Tool_offsety = len_bdr*1.5
cv_Tool_selected_id = -1
cv_Tool_VIS_selected_handle = -1

def init_canvas():
    for y in range(NX-1):
        cv.create_line(0, (y+1)*(len_sq+len_bdr) + len_bdr/2 ,NY*(len_sq+len_bdr),(y+1)*(len_sq+len_bdr) + len_bdr/2,fill='lightgrey')
    for x in range(NY-1):
        cv.create_line((x+1)*(len_sq+len_bdr) + len_bdr/2, 0 ,(x+1)*(len_sq+len_bdr) + len_bdr/2, NX*(len_sq+len_bdr), fill = 'lightgrey')


ToolFace=[FaceUP,FaceDOWN,FaceLEFT,FaceRIGHT,FaceUP,FaceLEFT,FaceUP,FaceLEFT,FaceLEFT]
ToolBID=[NOR,NOR,NOR,NOR,RFX,RFX,SPT,SPT,AIR]
def init_cv_Tool():
    DrawNOR(cv_Tool,0,0,FaceUP,cv_Tool_offsetx,cv_Tool_offsety)
    DrawNOR(cv_Tool,1,0,FaceDOWN,cv_Tool_offsetx,cv_Tool_offsety)
    DrawNOR(cv_Tool,2,0,FaceLEFT,cv_Tool_offsetx,cv_Tool_offsety)
    DrawNOR(cv_Tool,3,0,FaceRIGHT,cv_Tool_offsetx,cv_Tool_offsety)
    DrawRFX(cv_Tool,4,0,FaceUP,0,cv_Tool_offsetx,cv_Tool_offsety)
    DrawRFX(cv_Tool,5,0,FaceLEFT,0,cv_Tool_offsetx,cv_Tool_offsety)
    DrawSPT(cv_Tool,6,0,FaceUP,0,cv_Tool_offsetx,cv_Tool_offsety)
    DrawSPT(cv_Tool,7,0,FaceLEFT,0,cv_Tool_offsetx,cv_Tool_offsety)
    DrawLight(cv_Tool,8,0,3,cv_Tool_offsetx,cv_Tool_offsety)

def VIS_deselect_cv_Tool():
    global cv_Tool_VIS_selected_handle
    if (cv_Tool_VIS_selected_handle != -1):
        cv_Tool.delete(cv_Tool_VIS_selected_handle)

def VIS_select_cv_tool():
    global cv_Tool_VIS_selected_handle
    if (cv_Tool_selected_id == -1):
        return
    x1,y1,x2,y2 = corr(cv_Tool_selected_id,0)
    cv_Tool_VIS_selected_handle = cv_Tool.create_rectangle(x1-len_bdr/2+cv_Tool_offsetx, y1-len_bdr/2 +cv_Tool_offsety, x2+len_bdr/2+cv_Tool_offsetx, y2+len_bdr/2+cv_Tool_offsety, outline = 'red')
    


def keydown(event):
    global cv_Tool_selected_id
    if event.keycode>=ord('1') and event.keycode<=ord('9'):
        nselection = int(event.char)-1
        if (nselection == cv_Tool_selected_id):
            cv_Tool_selected_id=8
        else:
            cv_Tool_selected_id = nselection
        VIS_deselect_cv_Tool()
        VIS_select_cv_tool()
    if event.char == 'o':
        InputHandler()
    if event.char == 's':
        SavingHandler()
    if event.char == ' ':
        cv.xview_moveto(0)
        cv.yview_moveto(0)
    if event.char == 'c':
        CopyHandler()
        print("Copyed!")
    if event.char == 'm':
        MoveHandler()
        print("Moved!")
    if event.char == 'd':
        DeleteHandler()
        print("Deleted!")

def wheel(event):
    # Maybe Different for different systems!
    # DEBUG

    if event.state:
        # Horizonal "x"
        cv.xview_scroll(-event.delta,'units')
    else:
        # Vertical "y"
        cv.yview_scroll(-event.delta,'units')
    

def tool_clk(event):
    global cv_Tool_selected_id
    x = event.x - cv_Tool_offsetx
    y = event.y - cv_Tool_offsety
    #decoding
    xid = (x - len_bdr) // (len_sq+len_bdr)
    xid = int(xid)
    x1,y1,x2,y2=corr(xid,0)
    if x1<=x and x<= x2 and y1<=y and y<=y2 and xid<9:
        cv_Tool_selected_id = xid
        VIS_deselect_cv_Tool()
        VIS_select_cv_tool()
    else:
        cv_Tool_selected_id = -1
        VIS_deselect_cv_Tool()

QueMvCp = []

def canvas_clk(event):
    x = int(cv.canvasx(event.x))
    y = int(cv.canvasy(event.y))
    #decoding
    xid = (x - len_bdr)//(len_sq+len_bdr)
    yid = (y - len_bdr)//(len_sq+len_bdr)
    xid = int(xid)
    yid = int(yid)
    x1,y1,x2,y2=corr(xid,yid)

    if x1<=x and x<= x2 and y1<=y and y<=y2 and yid >= 0 and yid < NX and xid >= 0 and xid < NY:
        print("Click on (%d,%d)"%(yid,xid))
        if len(QueMvCp)==3:
            del(QueMvCp[0])
        QueMvCp.append((yid,xid))
        print(QueMvCp)
        if cv_Tool_selected_id!=-1:
            CommandA(yid,xid,ToolFace[cv_Tool_selected_id],ToolBID[cv_Tool_selected_id])
            NaiveGUIUpdate()


def corr(x, y):
    return x*len_sq+(x+1)*len_bdr, y*len_sq+(y+1)*len_bdr, (x+1)*(len_sq+len_bdr), (y+1)*(len_sq+len_bdr)

def DrawNOR(cvobj, x, y ,face, offsetx=0, offsety=0):
    x1,y1,x2,y2=corr(x,y)
    u=cvobj.create_rectangle(x1+offsetx,y1+offsety,x2+offsetx,y2+offsety, outline='blue', fill = None, width=1)
    cvBdItem[x][y].append(u)
    if face == FaceRIGHT:
        x1,y1,x2,y2 = x2- len_cir*2, (y1+y2)/2 - len_cir, x2, (y1+y2)/2 + len_cir
    if face == FaceUP:
        x1,y1,x2,y2 = (x1+x2)/2- len_cir, y1, (x1+x2)/2+ len_cir, y1+ len_cir*2
    if face == FaceLEFT:
        x1,y1,x2,y2 = x1, (y1+y2)/2 - len_cir, x1 + len_cir*2, (y1+y2)/2 + len_cir
    if face == FaceDOWN:
        x1,y1,x2,y2 = (x1+x2)/2- len_cir, y2 - len_cir*2, (x1+x2)/2+ len_cir, y2
    u=cvobj.create_oval(x1+offsetx,y1+offsety,x2+offsetx,y2+offsety,outline='blue', fill = None, width=1)
    cvBdItem[x][y].append(u)

def DrawRFX(cvobj,x,y,face,state, offsetx=0, offsety=0):
    x1,y1,x2,y2 = corr(x,y)
    if face == FaceUP or face == FaceDOWN:
        x1,y1,x2,y2 = x2,y1,x1,y2
    u=cvobj.create_line(x1+offsetx,y1+offsety,x2+offsetx,y2+offsety, fill = None, width=1)
    cvBdItem[x][y].append(u)

    halfstate = 0
    if face == FaceUP or face == FaceDOWN:
        if state & (FaceDOWN + FaceRIGHT):
            halfstate |= (FaceLEFT + FaceUP)
        if state & (FaceUP + FaceLEFT):
            halfstate |= (FaceRIGHT+FaceDOWN)
    if face == FaceLEFT or face == FaceRIGHT:
        if state & (FaceDOWN + FaceLEFT):
            halfstate |= (FaceUP + FaceRIGHT)
        if state & (FaceUP + FaceRIGHT):
            halfstate |= (FaceDOWN + FaceLEFT)
    DrawHalfLight(cvobj, x, y, halfstate, offsetx, offsety)

def DrawSPT(cvobj,x,y,face,state, offsetx=0, offsety=0):
    x1,y1,x2,y2 = corr(x,y)
    midx = (x1+x2)/2
    midy = (y1+y2)/2
    u=cvobj.create_oval(midx - len_cir + offsetx, midy - len_cir +offsety, midx + len_cir + offsetx, midy + len_cir+offsety, outline='blue', fill = None, width=1)
    cvBdItem[x][y].append(u)
    if face == FaceUP or face == FaceDOWN:
        x1,y1,x2,y2 = x2,y1,x1,y2
    u=cvobj.create_line(x1+offsetx,y1+offsety,x2+offsetx,y2+offsety, fill = None, width=1)
    cvBdItem[x][y].append(u)

    halfstate = 0
    if face == FaceUP or face == FaceDOWN:
        if state & FaceLEFT:
            halfstate |= FaceLEFT+FaceDOWN+FaceRIGHT
        if state & FaceRIGHT:
            halfstate |= FaceLEFT+FaceRIGHT+FaceUP
        if state & FaceUP:
            halfstate |= FaceUP+FaceDOWN+FaceRIGHT
        if state & FaceDOWN:
            halfstate |= FaceUP+FaceDOWN+FaceLEFT
    if face == FaceLEFT or face == FaceRIGHT:
        if state & FaceLEFT:
            halfstate |= FaceLEFT+FaceRIGHT+FaceUP
        if state & FaceRIGHT:
            halfstate |= FaceLEFT+FaceRIGHT+FaceDOWN
        if state & FaceUP:
            halfstate |= FaceUP+FaceDOWN+FaceLEFT
        if state & FaceDOWN:
            halfstate |= FaceUP+FaceDOWN+FaceRIGHT
    DrawHalfLight(cvobj, x, y, halfstate, offsetx, offsety)


def DrawHalfLight(cvobj, x, y, state, offsetx=0 , offsety=0):
    x1,y1,x2,y2 = corr(x,y)
    midx = (x1+x2)/2
    midy = (y1+y2)/2
    if state & FaceUP:
        u=cvobj.create_line(midx+offsetx, y1 - len_bdr/2 +offsety , midx+offsetx, midy- len_bdr/2+offsety)
        cvBdItem[x][y].append(u)
    if state & FaceDOWN:
        u=cvobj.create_line(midx+offsetx, midy + len_bdr/2 +offsety , midx+offsetx, y2 + len_bdr/2+offsety)
        cvBdItem[x][y].append(u)
    if state & FaceLEFT:
        u=cvobj.create_line(x1- len_bdr/2 +offsetx, midy +offsety , midx-len_bdr/2 +offsetx, midy + offsety)
        cvBdItem[x][y].append(u)
    if state & FaceRIGHT:
        u=cvobj.create_line(midx + len_bdr/2 +offsetx, midy +offsety , x2 + len_bdr/2 +offsetx, midy + offsety)
        cvBdItem[x][y].append(u)


def DrawLight(cvobj, x,y,state, offsetx=0, offsety=0):
    x1,y1,x2,y2 = corr(x,y)
    midx = (x1+x2)/2
    midy = (y1+y2)/2
    if state & (FaceLEFT+ FaceRIGHT):
        u=cvobj.create_line(x1 - len_bdr/2 +offsetx,midy+offsety,x2 + len_bdr/2+offsetx ,midy+offsety)
        cvBdItem[x][y].append(u)
    if state & (FaceUP + FaceDOWN):
        u=cvobj.create_line(midx+offsetx, y1 - len_bdr/2+offsety ,midx+offsetx, y2 + len_bdr/2+offsety )
        cvBdItem[x][y].append(u)

def InputHandler():
    url = input("Enter dgn file location:")
    if ('.dgn' not in url) and ('.txt' not in url):
        url+='.dgn'
    s=open(url,'r').read()
    

    # Control Variables
    counter = 0
    ofx = 0
    ofy = 0
    labellist = []
    condition = False

    #Parsing
    u = s.split('\n')
    i = 0
    while i < len(u):
        try:
            if u[i]=='' or u[i][0]=='/':
                i+=1
                continue
            else:
                ilist = u[i].strip().split(' ')
                if ilist[0]=='a':
                    # Command Type a
                    x=int(ilist[1])+ofx
                    y=int(ilist[2])+ofy
                    if ilist[3] in ['u', 'U']:
                        face = FaceUP
                    elif ilist[3] in ['r','R']:
                        face = FaceRIGHT
                    elif ilist[3] in ['d','D']:
                        face = FaceDOWN
                    elif ilist[3] in ['l','L']:
                        face = FaceLEFT
                    else:
                        raise BaseException
                    bid = int(ilist[4])
                    if bid>=0 and bid<=3:
                        CommandA(x,y,face,bid)
                    else:
                        raise BaseException

                elif ilist[0]=='.':
                    # Configuration
                    if ilist[1] == 'offsetx':
                        ofx = int(ilist[2])
                    elif ilist[1] == 'offsety':
                        ofy = int(ilist[2])
                    elif ilist[1] == 'counter':
                        counter = int(ilist[2])

                    elif ilist[1] == 'label':
                        labellist.append([i+1,ilist[2]])
                    elif ilist[1] == 'jump':
                        if condition:
                            found = False
                            ToLabel = ilist[2]
                            for Line, Label in labellist:
                                if ToLabel == Label:
                                    i = Line
                                    found = True
                                    break
                            if not found:
                                raise BaseException
                            else:
                                continue
                    elif ilist[1] == 'condition':
                        if ilist[2] in ['<', 'less']:
                            condition = counter < int(ilist[3])
                        elif ilist[2] in ['==', 'equal']:
                            condition = counter == int(ilist[3])
                        elif ilist[2] in ['>', 'greater']:
                            condition = counter > int(ilist[3])
                        else:
                            raise BaseException
                    elif ilist[1] == 'add':
                        if ilist[2] == 'offsetx':
                            ofx += int(ilist[3])
                        elif ilist[2] == 'offsety':
                            ofy += int(ilist[3]) 
                        elif ilist[2] == 'counter':
                            counter += int(ilist[3])
                        else:
                            raise BaseException
                    else:
                        raise BaseException
                i+=1
        except BaseException as e:
            print("error parsing. line :" ,i+1, u[i])
            i+=1
    print("Done loading file ", url)
    NaiveGUIUpdate()

def SavingHandler():
    url = input("saving file name: ")
    if '.dgn' not in url:
        url += '.dgn'

    with open(url,'w') as fd:
        for x in range(NX):
            for y in range(NY):
                if graph[x][y].bid !=AIR:
                    if graph[x][y].face == FaceUP:
                        face = 'u'
                    elif graph[x][y].face == FaceDOWN:
                        face = 'd'
                    elif graph[x][y].face == FaceLEFT:
                        face = 'l'
                    elif graph[x][y].face == FaceRIGHT:
                        face = 'r'
                    fd.write('a %d %d %c %d\n' % (x,y, face, graph[x][y].bid))
    print("Save complete: ",url)

def CopyHandler():
    global QueMvCp
    if len(QueMvCp)<3:
        return
    clist = []
    for x in range(QueMvCp[0][0], QueMvCp[1][0]+1):
        for y in range(QueMvCp[0][1], QueMvCp[1][1]+1):
            if graph[x][y].bid !=AIR:
                clist.append((x-QueMvCp[0][0]+QueMvCp[2][0],y-QueMvCp[0][1]+QueMvCp[2][1],graph[x][y].face, graph[x][y].bid))
    for item in clist:
        CommandA(*item)
    QueMvCp = []
    NaiveGUIUpdate()

def DeleteHandler():
    if len(QueMvCp)<2:
        return
    for x in range(QueMvCp[-2][0], QueMvCp[-1][0]+1):
        for y in range(QueMvCp[-2][1], QueMvCp[-1][1]+1):
            if graph[x][y].bid !=AIR:
                CommandA(x,y,FaceUP,AIR)
    NaiveGUIUpdate()

def MoveHandler():
    global QueMvCp
    if len(QueMvCp)<3:
        return
    clist = []
    for x in range(QueMvCp[0][0], QueMvCp[1][0]+1):
        for y in range(QueMvCp[0][1], QueMvCp[1][1]+1):
            if graph[x][y].bid !=AIR:
                clist.append((x-QueMvCp[0][0]+QueMvCp[2][0],y-QueMvCp[0][1]+QueMvCp[2][1],graph[x][y].face, graph[x][y].bid))
                CommandA(x,y,FaceUP,AIR)
    for item in clist:
        CommandA(*item)
    QueMvCp = []
    NaiveGUIUpdate()
    

cvBdItem = [[ [] for y in range(NX)] for x in range(NY)]

def NaiveGUIUpdate():
    for item in cv.find_all():
        cv.delete(item)
    init_canvas()
    for x in range(NX):
        for y in range(NY):
            if graph[x][y].bid == AIR:
                DrawLight(cv,y,x,graph[x][y].state)
            elif graph[x][y].bid == NOR:
                DrawNOR(cv,y,x, graph[x][y].face)
            elif graph[x][y].bid == RFX:
                DrawRFX(cv,y,x, graph[x][y].face, graph[x][y].state)
            else:
                DrawSPT(cv,y,x, graph[x][y].face,graph[x][y].state)

init_canvas()
init_cv_Tool()
cv_Tool.bind('<Button-1>',tool_clk)
root.bind('<Key>', keydown)
cv.bind('<Button-1>',canvas_clk)
cv.bind('<MouseWheel>',wheel)

root.mainloop()
