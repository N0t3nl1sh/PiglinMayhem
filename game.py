import pygame as pg
import engine as eng
from sys import exit
import random
import math

wg = "\ "
wg = wg.strip(" ")

class Input:
    m_movement = [0,0]
    w_prs = False
    a_prs = False
    s_prs = False
    d_prs = False
    lmbhold = False
    movex = False
    movey = False
    def Keydown(self,key):
        if key == "w":
            self.w_prs = True
            self.s_prs = False
        if key == "a":
            self.a_prs = True
            self.d_prs = False
        if key == "s":
            self.s_prs = True
            self.w_prs = False
        if key == "d":
            self.d_prs = True
            self.a_prs = False
    def Keyup(self,key):
        if key == "w":
            self.w_prs = False
        if key == "a":
            self.a_prs = False
        if key == "s":
            self.s_prs = False
        if key == "d":
            self.d_prs = False
    def Calc(self):
        if self.d_prs == True and self.a_prs == False:
            self.movex = 1
        if self.d_prs == False and self.a_prs == True:
            self.movex = -1
        if self.d_prs == False and self.a_prs == False:
            self.movex = 0
        
        if self.w_prs == True and self.s_prs == False:
            self.movey = -1
        if self.w_prs == False and self.s_prs == True:
            self.movey = 1
        if self.w_prs == False and self.s_prs == False:
            self.movey = 0
pg.mixer.init()

class Window:
    sc_size = (900,700)
    screen = pg.display.set_mode(sc_size)
    gamesurf = pg.surface.Surface((450,350))
    trns_surf = pg.surface.Surface((450,350))
    trns_surf.set_colorkey((230,230,230))
    hsw = gamesurf.get_width()//2
    hsh = gamesurf.get_height()//2

class Game:
    clock = pg.time.Clock()
    fps = 60
    timer = 600
    dt = 0
    debugmode = False

    mode = "alive"
    deadtimer = 0
    uideadbox = pg.rect.Rect((50,50,350,200))
    restart = pg.rect.Rect((66,150,315,80))
    rshold = 0

    difficulty = 1
    highscore = 0
    score = 0

    ui_mpos = (0,0)
    game_mpos = (0,0)

class Camera:
    """
        pos is centered on the screen 
    """
    x = Window.hsw
    y = Window.hsh

class TestObj:
    points = [(10,25),(55,45),(255,90),(90,15)]
    rect = pg.rect.Rect(200,200,100,100)
    circle = (255,45)

def Logic():
    Input.Calc(Input)

    Player.Move(Player,Input.movex,Input.movey)

#ÖNEMMMM !!!
""" 
    Nasıl yapılacağını buldum
    Player.colrectlist'e yakınımızdaki düşmanların rectlerini eklerken şunu yapıcaz:
    i = 0
    for pig in PG1.piglins:
        for chunk in chunklist:
            if pig["chunk"] == chunk:
                #rect is near us
                Player.colrectlist.append({"rect":pig["rect"] ,"id":pig["id"] } )

    daha sonra rect collision:
    for rect in Player.colrectlist:
        if rect["rect"].colliderect(Player.rect)
            PG0.piglins.pop[rect["id"]]
    sanırım bu olur 
    fakat ileride PG0.piglins mesela  60 61 62 diye id'si başlayıp gidiyorsa onda da hem .sort() kullanıp en düşük
    id'den en yükseğine gitmesi sağlanmalı aynı zamanda gidip şey dememiz lazım .pop(ilk elementin id'si - çıkarıcağımız elemementn idsi) 
    ilk 
"""
pg.mouse.set_visible(False)

class PG1:
    spr = pg.image.load("data/piglin1.png").convert_alpha()
    piglins = [ ]
    timer = 100
    idcount = 0

    def Add(self,dt):
        self.timer -= (dt/16)
        if self.timer <= 0:
            self.timer = 17

            pos = [0,0]
            if Player.x >= 175:
                pos[0] = random.randint(0,100)
            else:
                pos[0] = random.randint(200,440)
            if Player.y >= 175:
                pos[1] = random.randint(0,100)
            else:
                pos[1] = random.randint(200,340)

            self.piglins.append({"id":self.idcount,"pos":pos,"rot":0 ,"speed":random.randint(7,17)*0.1,
            "rect": pg.rect.Rect(pos[0],pos[1],16,16),"chunk":[0,0],"active":False } )
            self.idcount += 1
    def Update(self,dt):
        for piglin in self.piglins:
            dir = pg.math.Vector2((Player.x - piglin["pos"][0]),(Player.y - piglin["pos"][1]))
            dir = dir.normalize()
            xmov = dir.x * piglin["speed"] *(dt*0.05)
            ymov = dir.y * piglin["speed"] *(dt*0.05)
            piglin["pos"][0] += xmov
            piglin["pos"][1] += ymov
            piglin["rect"][0] = piglin["pos"][0] -8
            piglin["rect"][1] = piglin["pos"][1] -8
            piglin["chunk"] = [piglin["pos"][0]//50,piglin["pos"][1]//50]
            movement = [dir[0],dir[1] ]
            piglin["rot"] = math.degrees(math.atan2(-movement[1], movement[0]))  #+ (self.rot*0.1) 
            #self.rot = math.degrees(math.atan2(-Input.m_movement[1], Input.m_movement[0])) + (self.rot*0.1)
            piglin["rot"] += 90
            
            
            """list = [ [Player.xchunk,Player.ychunk],[Player.xchunk-1,Player.ychunk-1],[Player.xchunk,Player.ychunk-1]
            ,[Player.xchunk+1,Player.ychunk-1],[Player.xchunk-1,Player.ychunk],[Player.xchunk+1,Player.ychunk],
            [Player.xchunk-1,Player.ychunk+1],[Player.xchunk,Player.ychunk+1],[Player.xchunk+1,Player.ychunk+1],
            ]
            
            for chunk in list:
                if piglin["chunk"] == chunk: 
                    #pg.draw.rect(surf,(255,0,0),piglin["rect"],1 )
                    piglin["active"] = True
                    print("aaaaaaaaaaaaaaa")
                    #Player.colrects.append(  { "rect":piglin["rect"],"id":"PG1"}  )
                else:
                    piglin["active"] = False"""



    def Render(self,surf):
        i = 0
        for piglin in self.piglins:
            size = [16+CoolEffect.wavex*0.5,16+CoolEffect.wavey*0.5 ]
            eng.BlitRotate(surf,pg.transform.scale(self.spr,size),piglin["pos"],(8,8),piglin["rot"])
            i += 1

class PG2:
    spr = pg.image.load("data/piglin2.png").convert_alpha()
    spr2 = pg.image.load("data/piglin21.png").convert_alpha()
    piglins = [ ]
    timer = 100
    idcount = 0

    def Add(self,dt):
        self.timer -= (dt/16)
        if self.timer <= 0:
            self.timer = random.randint(350,475)

            pos = [0,0]
            if Player.x >= 175:
                pos[0] = random.randint(0,100)
            else:
                pos[0] = random.randint(200,440)
            if Player.y >= 175:
                pos[1] = random.randint(0,100)
            else:
                pos[1] = random.randint(200,340)

            self.piglins.append({"id":self.idcount,"pos":pos,"rot":0 ,"speed":random.randint(7,17)*0.1,
            "rect": pg.rect.Rect(pos[0],pos[1],16,16),"chunk":[0,0],"timer":None } )
            self.idcount += 1
    def Update(self,dt):
        i = 0
        for piglin in self.piglins:
            dist = pg.math.Vector2((Player.x - piglin["pos"][0]),(Player.y - piglin["pos"][1]))
            if dist.length() <= 65 and piglin["timer"] == None :
                piglin["timer"] =0
            if piglin["timer"] != None:
                piglin["timer"] += dt/16
                if piglin["timer"] >= 60:
                    piglin["timer"] = -100
                    try:
                        PG2.piglins.pop(i)
                    except IndexError:
                        pass
                    
                    i = 0
                    length = len( PG1.piglins)
                    while i < length:
                        dist = (abs(PG1.piglins[i]["pos"][0] - piglin["pos"][0])+
                                abs(PG1.piglins[i]["pos"][1] - piglin["pos"][1]))
                        if dist < 100:
                            PG1.piglins.remove(PG1.piglins[i])
                            i -= 1
                            length -= 1
                        i += 1
                    i = 0
                    length = len( PG3.piglins)
                    while i < length:
                        dist = (abs(PG3.piglins[i]["pos"][0] - piglin["pos"][0])+
                                abs(PG3.piglins[i]["pos"][1] - piglin["pos"][1]))
                        if dist < 100:
                            PG3.piglins.remove(PG3.piglins[i])
                            i -= 1
                            length -= 1
                        
                        i += 1

            else:
                dir = dist.normalize()
                xmov = dir.x * piglin["speed"] *(dt*0.05)
                ymov = dir.y * piglin["speed"] *(dt*0.05)
                piglin["pos"][0] += xmov
                piglin["pos"][1] += ymov
                piglin["rect"][0] = piglin["pos"][0] -8
                piglin["rect"][1] = piglin["pos"][1] -8
                piglin["chunk"] = [piglin["pos"][0]//50,piglin["pos"][1]//50]
                movement = [dir[0],dir[1] ]
                piglin["rot"] = math.degrees(math.atan2(-movement[1], movement[0]))  #+ (self.rot*0.1) 
                #self.rot = math.degrees(math.atan2(-Input.m_movement[1], Input.m_movement[0])) + (self.rot*0.1)
                piglin["rot"] -= 90
            i += 1
            
            

    def Render(self,surf):
        for piglin in self.piglins:
            size = [16+CoolEffect.wavex*0.5,16+CoolEffect.wavey*0.5 ]
            if piglin["timer"] == None:
                eng.BlitRotate(surf,pg.transform.scale(self.spr,size),piglin["pos"],(8,8),piglin["rot"])
            else:
                if piglin["timer"] %30 >= 15:
                    eng.BlitRotate(surf,pg.transform.scale(self.spr,size),piglin["pos"],(8,8),piglin["rot"])
                else: 
                    eng.BlitRotate(surf,pg.transform.scale(self.spr2,size),piglin["pos"],(8,8),piglin["rot"])

class PG3:
    spr = pg.image.load("data/piglin3.png").convert_alpha()
    piglins = [ ]
    timer = 100
    idcount = 0

    def Add(self,dt):
        self.timer -= (dt/16)
        if self.timer <= 0:
            self.timer = 100

            pos = [0,0]
            if Player.x >= 175:
                pos[0] = random.randint(0,100)
            else:
                pos[0] = random.randint(200,440)
            if Player.y >= 175:
                pos[1] = random.randint(0,100)
            else:
                pos[1] = random.randint(200,340)

            self.piglins.append({"id":self.idcount,"pos":pos,"rot":0 ,"speed":random.randint(50,70)*0.1,
            "rect": pg.rect.Rect(pos[0],pos[1],16,16),"chunk":[0,0],"timer":0,"state":"look","dir":(0,0) } )
            self.idcount += 1
    def Update(self,dt):
        for piglin in self.piglins:
            piglin["timer"] += dt/16
            if piglin["state"] == "look":
                dir = pg.math.Vector2((Player.x - piglin["pos"][0]),(Player.y - piglin["pos"][1]))
                dir = dir.normalize()
                movement = [dir[0],dir[1] ]
                piglin["dir"] = dir 
                piglin["rot"] = math.degrees(math.atan2(-movement[1], movement[0])) 
                piglin["rot"] += 90

            if piglin["timer"] >= 120:
                piglin["timer"] = 0
                if piglin["state"] == "look":
                    piglin["state"] = "move"
                else: 
                    piglin["state"] = "look"


            if piglin["state"] == "move":
                xmov = piglin["dir"].x * piglin["speed"] *(dt*0.05)
                ymov = piglin["dir"].y * piglin["speed"] *(dt*0.05)
                piglin["pos"][0] += xmov
                piglin["pos"][1] += ymov
                piglin["rect"][0] = piglin["pos"][0] -8
                piglin["rect"][1] = piglin["pos"][1] -8
                piglin["chunk"] = [piglin["pos"][0]//50,piglin["pos"][1]//50]
                piglin["pos"][0] = eng.Clamp(piglin["pos"][0],-3,454)
                piglin["pos"][1] = eng.Clamp(piglin["pos"][1],-3,344)

            



    def Render(self,surf):
        i = 0
        for piglin in self.piglins:
            size = [16+CoolEffect.wavex*0.5,16+CoolEffect.wavey*0.5 ]
            eng.BlitRotate(surf,pg.transform.scale(self.spr,size),piglin["pos"],(8,8),piglin["rot"])
            #eng.FontRenderwithFont(Fonts.testfont,(255,255,255),(Window.gamesurf),str(i),False,(0,0,0),piglin["pos"],False)
            i += 1

class Ammo:
    spr = pg.image.load("data/bullet.png").convert()
    bullets = [ ]
    timer = 0
    speed = 0.1
    bullettimer = 45
    def Add(self,dt):
        self.timer += dt/16
        if Player.guntype == "shotgun":
            self.bullettimer = 60
        if self.timer >= self.bullettimer:
            self.timer = 0
            pos = [Player.x+8,Player.y+8]
            aaa = pg.math.Vector2(Input.m_movement[0],Input.m_movement[1])
            
            if aaa.length() != 0:
                aaa = aaa.normalize()
            if Player.guntype == "pistol":
                Sounds.pistol.play()
                self.bullets.append({"pos":pos,"dir":[-aaa[0],-aaa[1]],"rot":Player.rot,
                "rect":pg.rect.Rect(pos[0],pos[1],6,6),"speed":1.5,"type":"pistol" })
            elif Player.guntype == "sniper":
                arot = math.floor(Player.rot)
                rotlist = [ ]
                for i in range(arot-2,arot+2): 
                    rotlist.append(i)
                for rot in rotlist:
                    rot -= 90
                    rot = math.radians(rot)
                    aaa = [math.cos(rot),-math.sin(rot)]
                    aaa = pg.math.Vector2(aaa[0],aaa[1])
                    aaa.normalize()
                    self.bullets.append({"pos":pos,"dir":[-aaa[0],-aaa[1]],"rot":rot,
                    "rect":pg.rect.Rect(pos[0],pos[1],6,6),"speed":1,"type":"sniper" })
            elif Player.guntype == "shotgun":
                Sounds.sniper.play()
                arot = math.floor(Player.rot)
                rotlist = [ ]
                for i in range(arot-20,arot+20): 
                    rotlist.append(i)

                arot -= 90
                apos = pos

                arot = math.radians(arot)
                aaa = [math.cos(arot),-math.sin(arot)]
                aaa = pg.math.Vector2(aaa[0],aaa[1])
                aaa = aaa.normalize()
                
                
                self.bullets.append({"pos":pos,"dir":[-aaa[0],-aaa[1]],"rot":arot,
                "rect":pg.rect.Rect(apos[0],apos[1],6,6),"speed":5,"type":"shotgun" })


    def Update(self,dt):
        a = 0
        for b in self.bullets:
            b["pos"][0] += b["dir"][0] * b["speed"]*(dt/16)
            b["pos"][1] += b["dir"][1] * b["speed"]*(dt/16)
            b["rect"].topleft = b["pos"][0]-4,b["pos"][1] -4
            
            aa = False
            if b["pos"][0] > 450:
                aa = True
            if b["pos"][0] < 0:
                aa = True
            if b["pos"][1] > 350:
                aa = True
            if b["pos"][1] < 0:
                aa = True
            if aa == None:
                try:
                    self.bullets.pop(a)
                except IndexError:
                    pass
            
            i = 0
            length = len( PG1.piglins)
            while i < length:
                if b["rect"].colliderect(PG1.piglins[i]["rect"]):
                    PG1.piglins.remove(PG1.piglins[i])
                    i -= 1
                    length -= 1
                    try:
                        if self.bullets[a]["type"] != "shotgun":
                            try:
                                self.bullets.pop(a)
                            except IndexError:
                                pass
                    except IndexError:
                        pass
                        
                        
                i += 1
            i = 0
            length = len( PG3.piglins)
            while i < length:
                if b["rect"].colliderect(PG3.piglins[i]["rect"]):
                    PG3.piglins.remove(PG3.piglins[i])
                    i -= 1
                    length -= 1
                    try:
                        if self.bullets[a]["type"] != "shotgun":
                            try:
                                self.bullets.pop(a)
                            except IndexError:
                                pass
                    except IndexError:
                        pass
                i += 1

            a += 1
    def Render(self,surf):
        for b in self.bullets:
            eng.BlitRotate(surf,self.spr,b["pos"],(3,3),b["rot"])

class CoolEffect:
    y = 0 
    x = 0
    qy = 0 #quartery
    wavey = 0
    wavex = 0

class Player:
    spr = pg.image.load("data/player.png").convert_alpha()
    hp = 120
    x = 0
    y = 0
    rot = 0
    xchunk = 0
    ychunk = 0
    rect = pg.rect.Rect(0,0,14,14)
    colrects = [ ]
    
    guntype = "pistol"
    pistol = pg.image.load("data/pistol.png").convert_alpha()
    shotgun = pg.image.load("data/ui_sniper.png").convert_alpha()

    def Move(self):
        self.x,self.y = (Game.ui_mpos[0]//2) -self.spr.get_width()//2 ,(Game.ui_mpos[1] //2)-self.spr.get_height()//2
        self.xchunk,self.ychunk = self.x//50,self.y//50
        self.rect.topleft = (self.x+1,self.y+1)
        #rot = math.degrees(math.atan2(self.y-next.y, next.x-previous.x))
        if Input.m_movement[0] != 0 or Input.m_movement[1] != 0:
            self.rot = math.degrees(math.atan2(-Input.m_movement[1], Input.m_movement[0])) + (self.rot*0.1)
            
            self.rot += 90
    def ColCheck(self):
        i = 0
        for pig in PG1.piglins:
            if self.rect.colliderect(pig["rect"]):
                self.hp -= 5
                PG1.piglins.pop(i) 
            i += 1
        
        i = 0
        length = len( PG3.piglins)
        while i < length:
            if PG3.piglins[i]["rect"].colliderect(Player.rect):
                PG3.piglins.remove(PG3.piglins[i])
                i -= 1
                length -= 1
                self.hp -= 3
            i += 1
        if Player.hp <= 0:
            print("player ded :(")
            Game.mode = "dead"
            if Game.highscore < Game.score:
                Game.highscore = Game.score


class Sounds:
    pistol = pg.mixer.Sound("data/pistol2.wav")
    pistol.set_volume(0.5)
    sniper_equip = pg.mixer.Sound("data/sniper equip.wav")
    sniper = pg.mixer.Sound("data/sniper.wav")

def DeadRender():
    pg.draw.rect(Window.gamesurf,(200,200,200),(Game.uideadbox.x,Game.uideadbox.y+CoolEffect.wavey,
     Game.uideadbox.w,Game.uideadbox.h))
    pos = [70,70+CoolEffect.wavey]
    text = "Cool! \nYour Highscore is: "
    color = (77, 77, 255)

    eng.FontRenderwithFont(Fonts.testfont,color,Window.gamesurf,text,False,(200,200,200),pos,False)
    eng.FontRenderwithFont(Fonts.testfont,(255,68,204),Window.gamesurf,str(int(Game.highscore)),False,
     (200,200,200),(pos[0]+200,pos[1]+25),False)
    Game.restart = pg.rect.Rect(Game.restart[0],150+CoolEffect.wavey,
    Game.restart[2],Game.restart[3])
    pg.draw.rect(Window.gamesurf,(57,255,20),Game.restart)

    pg.draw.rect(Window.gamesurf,(255,57,20),(Game.restart[0],Game.restart[1],Game.rshold,Game.restart[3]))
    
    
    eng.FontRenderwithFont(Fonts.bigfont,(255,255,255),Window.trns_surf,"RESTART",False,
     (230,230,230),(Game.restart[0]+12,Game.restart[1]+8),False)


def Render():
    #Window.gamesurf.blit(Player.spr,(Player.x,Player.y))
    PG1.Render(PG1,Window.gamesurf)
    PG2.Render(PG2,Window.gamesurf)
    PG3.Render(PG3,Window.gamesurf)
    Stuff.Render(Stuff,Window.trns_surf)
    Ammo.Render(Ammo,Window.gamesurf)

    size = [16+CoolEffect.wavex*0.5,16+CoolEffect.wavey*0.5 ]
    eng.BlitRotate(Window.gamesurf,pg.transform.scale(Player.spr,size),(Player.x+(Player.spr.get_width()//2),(Player.y+(Player.spr.get_height()//2) ) ),(8,8),Player.rot)

    dir = [Window.hsw,Window.hsh]
    pg.draw.line(Window.gamesurf,(255,0,0),(Player.x+8,Player.y+8),dir)

    pg.draw.rect(Window.gamesurf,(eng.Clamp(125-Player.hp,0,255),eng.Clamp(55+Player.hp*2,0,255),eng.Clamp(25,0,255)),(10, #health bar
    10 + #CoolEffect.qy +
    CoolEffect.wavey
    ,Player.hp*1.5,20))
    # math.acos()
    eng.FontRenderwithFont(Fonts.testfont,(0,0,0),Window.trns_surf,str(math.floor(Game.score)),False,(230,230,230),(390,10 +CoolEffect.wavey),False)
    #eng.FontRenderwithFont(Fonts.testfont,(0,0,0),Window.gamesurf,str(Game.difficulty),False,(230,230,230),(290,10 +CoolEffect.wavey),False)
    #eng.FontRenderwithFont(Fonts.testfont,(0,0,0),Window.trns_surf,str((Game.timer)//1000),False,(230,230,230),(290,40 +CoolEffect.wavey),False)


    if Player.guntype == "pistol":
        Window.gamesurf.blit(Player.pistol,(240,5+CoolEffect.wavey))
    if Player.guntype == "shotgun":
        Window.gamesurf.blit(Player.shotgun,(240,10+CoolEffect.wavey))



class Stuff:
    sprs = [pg.image.load("data/healthbox.png").convert(),pg.image.load("data/sniper.png").convert(), ]
    objlist = [ ]
    timer = 400
    shtimer = 5400 #60000 
    gaveshotgun = False
    idcount = 0
    def Add(self,dt):
        self.timer -= (dt/16)
        self.shtimer -= dt/16
        if self.shtimer <= 0 and Player.guntype == "pistol" and self.gaveshotgun == False:
            print("shotgun given")
            self.gaveshotgun = True
            pos = [0,0]
            pos[0] = random.randint(0,434)
            pos[1] = random.randint(30,334)
            self.objlist.append({"id":self.idcount,"pos":pos,
            "rect": pg.rect.Rect(pos[0],pos[1],16,16), "type":"shotgun"} )
            self.idcount += 1
        if self.timer <= 0:
            self.timer = 1000
            pos = [0,0 ]
            pos[0] = random.randint(0,434)
            pos[1] = random.randint(30,334)
            
            self.objlist.append({"id":self.idcount,"pos":pos,
            "rect": pg.rect.Rect(pos[0]-9,pos[1]-9,16,16), "type":"health"} )
            self.idcount += 1
    def Update(self):
        i = 0
        for stuff in self.objlist:
            stuff["rect"].y = (stuff["pos"][1]+CoolEffect.wavey*2)-8
            if Player.rect.colliderect(stuff["rect"]):
                if stuff["type"] == "health":
                    Player.hp += 30
                    Player.hp = eng.Clamp(Player.hp,0,120)
                    self.objlist.pop(i)
                if stuff["type"] == "shotgun":
                    Sounds.sniper_equip.play()
                    Player.guntype = "shotgun"
                    try:
                        self.objlist.pop(i)
                    except IndexError:
                        pass
            i+= 1

    def Render(self,surf):
        for stuff in self.objlist:
            if stuff["type"] == "health":
                eng.BlitRotate(surf,self.sprs[0],(stuff["pos"][0],stuff["pos"][1]+(CoolEffect.wavey*2)),(9,9),(Game.timer%720)//2 )
            elif stuff["type"] == "shotgun":
                eng.BlitRotate(surf,self.sprs[1],(stuff["pos"][0],stuff["pos"][1]+(CoolEffect.wavey*2)),(8,8),(Game.timer%720)//2 )
                
def DeadLogic():
    ttt =  pg.rect.Rect(Game.restart[0],Game.restart[1],Game.restart[2],Game.restart[3])
    #pg.draw.rect(Window.gamesurf,(125,255,125),ttt)
    mpos = pg.mouse.get_pos()
    mpos = [((mpos[0]-CoolEffect.x)//2),((mpos[1]-CoolEffect.y)//2) ]
    if ttt.collidepoint(mpos):
        Game.rshold += (Game.dt /6)
    else:
        Game.rshold = 0
    if Game.rshold >= Game.restart.w:
        print("game restarted")
        Game.score = 0
        Player.hp = 120
        PG1.piglins = [ ]
        PG2.piglins = [ ]
        PG3.piglins = [ ]
        Stuff.objlist = [ ]
        Ammo.bullets = []
        Game.timer = 0
        Game.deadtimer = 0
        Game.difficulty = 1
        Game.mode = "alive"
        Game.rshold = 0
        Player.guntype = "pistol"


def Logic():
    
    Game.score += Game.dt/16*0.05
    Player.Move(Player)

    PG1.Add(PG1,Game.dt*Game.difficulty)
    PG1.Update(PG1,Game.dt)
    
    PG2.Add(PG2,Game.dt)
    PG2.Update(PG2,Game.dt)
    
    PG3.Add(PG3,Game.dt*Game.difficulty)
    PG3.Update(PG3,Game.dt)

    Stuff.Add(Stuff,Game.dt)
    Stuff.Update(Stuff)

    Ammo.Add(Ammo,Game.dt)
    Ammo.Update(Ammo,Game.dt)
    
    Player.ColCheck(Player)

    # chunks to look for
    list = [ (Player.xchunk,Player.ychunk),(Player.xchunk-1,Player.ychunk-1),(Player.xchunk,Player.ychunk-1)
    ,(Player.xchunk+1,Player.ychunk-1),(Player.xchunk-1,Player.ychunk),(Player.xchunk+1,Player.ychunk),
    (Player.xchunk-1,Player.ychunk+1),(Player.xchunk,Player.ychunk+1),(Player.xchunk+1,Player.ychunk+1),]
    #for chunk in list:
    #    pg.draw.rect(Window.gamesurf,(125,125,0),(chunk[0]*50,chunk[1]*50,50,50 ),2 )
    if Game.debugmode:
        pg.draw.rect(Window.gamesurf,(0,255,0),Player.rect,2)

    Player.colrects = [ ]

def main( ):
    running = True
    while running:
        Game.dt = Game.clock.tick(Game.fps)
        Game.timer += Game.dt
        if Game.mode == "dead":
            Game.deadtimer += Game.dt
        Game.difficulty += (Game.dt/16)*0.0001 
        Game.difficulty = eng.Clamp(Game.difficulty,1,2.2)
        Window.trns_surf.fill((230,230,230))
        Window.gamesurf.fill((230,230,230))
        Window.screen.fill((200,200,200))
        eng.Cam.UpdatePos(eng.Cam,Camera.x,Camera.y,Window.hsw,Window.hsh)

        Game.ui_mpos = pg.mouse.get_pos()[0]-CoolEffect.x,pg.mouse.get_pos()[1]-CoolEffect.y
        Game.game_mpos = (Game.ui_mpos[0] +Camera.x,Game.ui_mpos[1]+Camera.y)
        if Game.ui_mpos[0] != pg.mouse.get_pos()[0] or Game.ui_mpos[1] != pg.mouse.get_pos()[1]:
            if (abs(Game.ui_mpos[0] - pg.mouse.get_pos()[0]) + abs(Game.ui_mpos[1] - pg.mouse.get_pos()[1]) )  >= 2:
                Input.m_movement = [ Game.ui_mpos[0] - pg.mouse.get_pos()[0],Game.ui_mpos[1] - pg.mouse.get_pos()[1] ]

        
        CoolEffect.wavey = (math.sin(Game.timer/100)*5)
        CoolEffect.wavex = (math.cos(Game.timer/100)*5)
        if Game.ui_mpos[1] != 0: 
            CoolEffect.y = math.sin((Game.ui_mpos[1]/(Window.hsh*2))-1  )*-40
        if Game.ui_mpos[0] != 0: 
            CoolEffect.x = math.sin((Game.ui_mpos[0]/(Window.hsw*2))-1  )*-40
        CoolEffect.qy = CoolEffect.y //4

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                exit() #from sys
        
        
        if Game.mode == "alive":
            Logic()
            pg.mouse.set_visible(False)
        elif Game.mode == "dead":
            pg.mouse.set_visible(True)
        Render()
        if Game.mode == "dead":
            DeadLogic()
            DeadRender()
            

        Window.gamesurf.blit(Window.trns_surf,(0,0))
        Window.screen.blit(pg.transform.scale(Window.gamesurf,Window.sc_size),(CoolEffect.x,CoolEffect.y))
        pg.display.flip()




class Fonts:
    testfont = pg.font.Font("enginedata/fontfile/FFFFORWA.ttf",16)
    bigfont = pg.font.Font("enginedata/fontfile/FFFFORWA.ttf",48)

if __name__ == '__main__':
    main()
