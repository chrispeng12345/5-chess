# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 19:48:14 2020

@author: ASUS
"""
# TODO: AI
# TODO: STARTPAGESETTINGS
# TODO: RESTRICTED MOVE
import pygame
from pygame import gfxdraw
import random

BLOCK_WIDTH=30      # 一格寬
PIECE_RADIUS=12     # 棋子半徑
OUTSIDE_WIDTH=20    # 棋盤外長
BLOCK_NUM=18        # 格子數(18格就是19個點)
BOARD_WIDTH=BLOCK_WIDTH*BLOCK_NUM  # 棋盤總寬
BLACK=(0,0,0)       
WHITE=(255,255,255)
TEXT_HEIGHT=30
SCREEN_HEIGHT=BOARD_WIDTH+OUTSIDE_WIDTH*2   # 螢幕高
SCREEN_WIDTH=SCREEN_HEIGHT+500           # 螢幕寬
BACKGROUND_COLOR=(222,184,135)              # 被景色(木頭色)

ywz=['(*/ω＼*)','ヾ(•ω•`)o','w(ﾟДﾟ)w','(o-ωｑ)).oO 困','q(≧▽≦q)','(o_ _)ﾉ','( ´･･)ﾉ(._.`)',
'(oﾟvﾟ)ノ','（；´д｀）ゞ','o((>ω< ))o','(ノω<。)ノ))☆.。','♪(´▽｀)','✪ ω ✪',
'ε=ε=ε=(~￣▽￣)~','o(*////▽////*)q','(。・∀・)ノ','( ﾟдﾟ)つ','( ′ 3`) sigh~','(╯‵□′)╯']

def game():         # 主程式
    pygame.init()
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('5-chess')
    toquit=False
    pieces=[]
    black_turn=True
    rounds=1
    ywznum=random.randint(0,18)
    a=ywz[ywznum]+' Round '+str(rounds)
    black_point,white_point=0,0
    b='-----            黑子: '+str(black_point)+'    白子: '+str(white_point)+'          -----'
    wined=False
    MX,MY=0,0
    added_point=True
    while toquit is not True:       # 主循環
        add_piece=False
        piece_already_exists=False
        drawBoard(screen)
        b='-----            黑子: '+str(black_point)+'    白子: '+str(white_point)+'          -----'
        
        add_piece,wined,pieces,black_turn,rounds,a,MX,MY=checkEvents(pygame.event.get(),add_piece,wined,pieces,black_turn,rounds,a,MX,MY,ywznum)
        
        if add_piece and (checkClickPoint(MX,MY) != None) and wined==False:     #下子
            PX,PY=checkClickPoint(MX,MY)
            piece_already_exists,pieces,black_turn=drop(screen,PX,PY,pieces,black_turn,piece_already_exists)
        
        for one_piece in range(len(pieces)):    # 畫棋子
            pieces[one_piece].drawme()
        
        if len(pieces)==(BLOCK_NUM+1)^2:
            wined==True
        if pieces!=[]:      # 判定勝負
            drawCurrentDrop(screen,pieces)
            wined,blackwined=checkwin(pieces,pieces[len(pieces)-1])
            if wined:
                added_point=False
                if blackwined==None:
                    a='搞啥啊你，棋盤滿了都(R to restart)'
                    ywznum=random.randint(0,18)
                if blackwined:
                    a='黑子勝利! (R to restart)'
                    if (not added_point) and (black_point+white_point<rounds):
                        black_point+=1
                        ywznum=random.randint(0,18)
                else:
                    a='白子勝利! (R to restart)'
                    if (not added_point) and (black_point+white_point<rounds):
                        white_point+=1
                        ywznum=random.randint(0,18)
        drawText(screen,b,OUTSIDE_WIDTH+BOARD_WIDTH+30,OUTSIDE_WIDTH)
        drawText(screen,str(a),OUTSIDE_WIDTH+BOARD_WIDTH+30,SCREEN_HEIGHT-50)
        pygame.display.flip()               # 顯示
        #if not black_turn and (AIdrop(screen,pieces) is not None) and wined==False:
        #    SX,SY=AIdrop(screen,pieces)
         #   piece_already_exists,pieces,black_turn=drop(screen,SX,SY,pieces,False,False)
        #print('---')
        #for pss in pieces:
         #   print(pss.place_x,pss.place_y)
                
def checkEvents(events,add_piece,wined,pieces,black_turn,rounds,a,MX,MY,ywznum):
    for event in events:    # 監測退出
        if event.type==pygame.QUIT:
            pygame.quit()
        elif event.type==pygame.MOUSEBUTTONDOWN:    # 判斷點擊
            if event.button==1:
                add_piece=True
                MX,MY=pygame.mouse.get_pos()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r and wined==True:  # 重開
                pieces=[]
                black_turn=True
                wined=False
                rounds+=1
                a=ywz[ywznum]+' 局數：'+str(rounds)
    return add_piece,wined,pieces,black_turn,rounds,a,MX,MY
        
def drop(screen,PX,PY,pieces,black_turn,piece_already_exists):    #下子
    for one_piece in range(len(pieces)):
        if pieces[one_piece].place_x==PX and pieces[one_piece].place_y==PY:
            piece_already_exists=True
    if not(piece_already_exists):
        pieces.append(piece(screen,PX,PY,black_turn))
        black_turn=not black_turn
    return piece_already_exists,pieces,black_turn
         
def checkAround(pieces,P,ce=True):  # 檢查該子周圍
    ps=[]
    for p in pieces:
        if checkDirection(p,P)!='f' and checkDirection(p,P)!='s':
            if p.is_black==P.is_black and ce:
                ps.append(p)
            elif not ce:    # ce=color except 我真是取名鬼才
                ps.append(p)
    return ps
def checkDirection(np,mp):      # 測定該子對於另一子的方向(太長的屑函數
    # check newpiece's direction from mainpiece
    if (mp.place_x-np.place_x,mp.place_y-np.place_y)==(1,1):return 'lu'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(0,1):return 'u'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(-1,1):return 'ru'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(1,0):return 'l'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(0,0):return 's'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(-1,0):return 'r'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(1,-1):return 'ld'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(0,-1):return 'd'
    elif (mp.place_x-np.place_x,mp.place_y-np.place_y)==(-1,-1):return 'rd'
    else:return('f')

def turnDirection(d):       # 轉變方向(同樣長的屑函數
    if d=='lu':return 'rd'
    elif d=='u':return 'd'
    elif d=='ru':return 'ld'
    elif d=='l':return 'r'
    elif d=='r':return 'l'
    elif d=='ld':return 'ru'
    elif d=='d':return 'u'
    elif d=='rd':return 'lu'
    elif d=='s':return 's'
    else:return 'f'
    
def checkwin(pieces,p1):       # 檢查下一步勝負(史上最屑的函數((但是，它做到了!
    if checkAround(pieces,p1)!=[]:
        for p2 in checkAround(pieces,p1):
            for p3 in checkAround(pieces,p2):
                if checkDirection(p3,p2)==checkDirection(p2,p1):
                    for p4 in checkAround(pieces,p3):
                        if checkDirection(p4,p3)==checkDirection(p3,p2):
                            for p5 in checkAround(pieces,p4):
                                if checkDirection(p5,p4)==checkDirection(p4,p3):
                                    return True,p1.is_black
                                else:
                                    for p5 in checkAround(pieces,p1):
                                        if checkDirection(p5,p1)==turnDirection(checkDirection(p2,p1)):
                                            return True,p1.is_black
                        else:
                            for p4 in checkAround(pieces,p1):
                                if checkDirection(p4,p1)==turnDirection(checkDirection(p2,p1)):
                                    for p5 in checkAround(pieces,p4):
                                        if checkDirection(p5,p4)==turnDirection(checkDirection(p2,p1)):
                                            return True,p1.is_black
                else:
                    for p3 in checkAround(pieces,p1):
                        if checkDirection(p3,p1)==turnDirection(checkDirection(p2,p1)):
                            for p4 in checkAround(pieces,p3):
                                if checkDirection(p4,p3)==turnDirection(checkDirection(p2,p1)):
                                    for p5 in checkAround(pieces,p4):
                                        if checkDirection(p5,p4)==turnDirection(checkDirection(p2,p1)):
                                            return True,p1.is_black                            
    return False,None

def checkAroundSpace(pieces,w,b):       
    n=0
    bb=False
    if checkAround(pieces,w,False) !=[]:
        for w2 in checkAround(pieces,w):
                for w3 in checkAround(pieces,w2):
                    if checkDirection(w3,w2)==checkDirection(w2,w):
                        for b4 in checkAround(pieces,w3,False):
                            if checkDirection(b4,w3)==checkDirection(w2,w):
                                n+=5
                                bb=True
                            if bb is not True:
                                n+=10
                                bb=True
            
    else:
        n=0
    return n

def drawCurrentDrop(screen,pieces):
    d=pieces[len(pieces)-1]
    pygame.gfxdraw.aacircle(screen,d.x,d.y,2,(255,0,0))
    pygame.gfxdraw.filled_circle(screen,d.x,d.y,2,(255,0,0))            
    #pygame.draw.rect(screen,(255,0,0),(d.x-PIECE_RADIUS-2,d.y-PIECE_RADIUS-2,PIECE_RADIUS*2+4,PIECE_RADIUS*2+4),2)

def checkClickPoint(x,y):   # 檢定點擊點
    if x<OUTSIDE_WIDTH-PIECE_RADIUS or x>OUTSIDE_WIDTH+BOARD_WIDTH+PIECE_RADIUS:
        return None
    elif y<OUTSIDE_WIDTH-PIECE_RADIUS or y>OUTSIDE_WIDTH+BOARD_WIDTH+PIECE_RADIUS:
        return None
    else:    
        px=int((x-OUTSIDE_WIDTH+PIECE_RADIUS)/BLOCK_WIDTH)+1
        py=int((y-OUTSIDE_WIDTH+PIECE_RADIUS)/BLOCK_WIDTH)+1
        return(px,py)

def drawText(self,text,posx,posy,textHeight=TEXT_HEIGHT,fontColor=(0,0,255),backgroudColor=None):
    fontObj = pygame.font.Font('SourceHanSansOLD-Regular.otf', textHeight)
    textSurfaceObj = fontObj.render(text,True,fontColor,backgroudColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = posx
    textRectObj.top = posy
    self.blit(textSurfaceObj, textRectObj)

def drawBoard(screen):      # 畫背景、棋盤
    x,y,size=0,0,1
    screen.fill(BACKGROUND_COLOR)       # 填背景(棋盤色)
    pygame.draw.rect(screen,BLACK,(OUTSIDE_WIDTH-6,OUTSIDE_WIDTH-6,BOARD_WIDTH+12,BOARD_WIDTH+12),4) # 外框
    for i in range(BLOCK_NUM+1): # 畫棋盤(橫豎)
        pygame.draw.line(screen,BLACK,(OUTSIDE_WIDTH,OUTSIDE_WIDTH+i*BLOCK_WIDTH),(OUTSIDE_WIDTH+BOARD_WIDTH,OUTSIDE_WIDTH+i*BLOCK_WIDTH))
    for j in range(BLOCK_NUM+1):
        pygame.draw.line(screen,BLACK,(OUTSIDE_WIDTH+j*BLOCK_WIDTH,OUTSIDE_WIDTH),(OUTSIDE_WIDTH+j*BLOCK_WIDTH,OUTSIDE_WIDTH+BOARD_WIDTH))
    for k in range(3):  # 加點點ヾ(•ω•`)o
        for l in range(3):
            x=[3,int(BLOCK_NUM/2),BLOCK_NUM-3][k!=0 if k!=2 else 2]
            y=[3,int(BLOCK_NUM/2),BLOCK_NUM-3][l!=0 if l!=2 else 2]  # 畫沒抗鋸齒有點醜...owo (2020/7/17已補上)
            size=int(BLOCK_WIDTH/6.5) if (k==1 and l==1) else int(BLOCK_WIDTH/10)
            #pygame.draw.circle(screen,BLACK,(OUTSIDE_WIDTH+x*BLOCK_WIDTH,OUTSIDE_WIDTH+y*BLOCK_WIDTH),size,0)
            pygame.gfxdraw.aacircle(screen,OUTSIDE_WIDTH+x*BLOCK_WIDTH,OUTSIDE_WIDTH+y*BLOCK_WIDTH,size,BLACK)
            pygame.gfxdraw.filled_circle(screen,OUTSIDE_WIDTH+x*BLOCK_WIDTH,OUTSIDE_WIDTH+y*BLOCK_WIDTH,size,BLACK)            

def AIdrop(screen,pieces):
    for x in range(1,20):
        for y in range(1,20):
            pae=False
            for p in pieces: 
                if p.place_x==x and p.place_y==y:
                    pae=True
            if not pae:
                wined,who_wined=checkwin(pieces,piece(screen,x,y,False))
                if wined:
                    return x,y
                else:
                    wined,who_wined=checkwin(pieces,piece(screen,x,y,True))
                    if wined:
                        return x,y
                    else:
                        wp=piece(screen,x,y,False)
                        bp=piece(screen,x,y,True)
                        

class piece():  # 棋子
    def __init__(self,screen,x,y,is_black):
        self.screen=screen
        self.x=OUTSIDE_WIDTH+(x-1)*30
        self.y=OUTSIDE_WIDTH+(y-1)*30
        self.place_x=x
        self.place_y=y
        self.is_black=is_black
    def drawme(self):
        #pygame.draw.circle(self.screen,[WHITE,BLACK][self.is_black],(self.x,self.y),PIECE_RADIUS,0)
        pygame.gfxdraw.aacircle(self.screen,self.x,self.y,PIECE_RADIUS,[WHITE,BLACK][self.is_black])
        pygame.gfxdraw.filled_circle(self.screen,self.x,self.y,PIECE_RADIUS,[WHITE,BLACK][self.is_black])
game()
