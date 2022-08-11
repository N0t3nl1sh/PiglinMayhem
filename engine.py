"""
Version 1.2.2
"""
"""
NOTE: DrawRectObj() func is probably wrong 

"""

"""
ohaaa şu CoolEffect class'ını engine'e ekle

abi çok havalı 
wave x wavey  falan

cos x 
sin y 
için ama ikisi için de kullanılabiliyo

ayrıca mesela:
CoolEffect.wavey = (math.sin(Game.timer/100)*5)
CoolEffect.wavex = (math.cos(Game.timer/100)*5)
size = [sprwidth+CoolEffect.wavex*0.5,sprheight+CoolEffect.wavey*0.5 ]
eng.BlitRotate(Window.gamesurf,pg.transform.scale(Player.spr,size),(Player.x+(Player.spr.get_width()//2),(Player.y+(Player.spr.get_height()//2) ) ),(8,8),Player.rot)

bu arada wavex için de sin kullanmak da güzel 

---
ayrıca mesela sanki bir crt effect varmış gibi 
yapmanın yolunu buldum:
2 surf var screen ve gamesurf
her şeyi gamesurf'a blit edip sonra da gamesurfu 
screena blit ediyorsun ya

screen.blit(gamesurf,(0,0)) yerine
screen.blit(gamesurf,(CoolEffect.x,CoolEffect.y))
bu sanki bir crt ekranı gibi ama o çizgiler yok :(
"""



"""
Player.colrectlist ile collisioncheck yapıp
sonra da bunu bozmayacak şekilde nasıl 
PG1.piglins'de listeden çıkartabiliriz onu bulmaya 
çalış


iterating and removing items from list üzerinde
çalışmam lazımbu ne ya çok karmakarışık saçma bir
işlem olmasına rağmen

"""


import pygame as pg
import math
import random
import json
#from dataclasses import dataclass
#from colorsys import hsv_to_rgb

"""@dataclass #wow i 
class HSVcol:
    h: int
    s: int
    v: int
    
    def ConvertToRGB(self):
        max = self.v

        chroma = self.s * self.v

        #return (self.h+1,self.s+32,255)
        # bu şekilde kendi oluşturduğun dataclass'lardaki 
        # fonksiyonları kullanabilirsin

        pass
"""

"""def ConvertToRGB(h,s,v):
    h /= 255
    s /= 255 
    v /= 255
    return tuple(round(i * 255) for i in hsv_to_rgb(h,s,v)) """
wg = "\ "
wg = wg.strip(" ")

screen = pg.display.set_mode((100,100))

def Clamp2(value,min,max):
    """ 
        limits 2 values of tuple to min/max 
    """
    if value[0] > max:
        value[0] = max
    if value[0] < min:
        value[0] = min

    if value[1] > max:
        value[1] = max
    if value[1] < min:
        value[1] = min
    return value

def Clamp(value,min,max):
    """ 
        limits value to min/max 
    """
    if value > max:
        value = max
    if value < min:
        value = min

    return value

class Cam:
    x = 0
    y = 0
    hsw = 0
    hsh = 0
    def UpdatePos(self,newx,newy,hsw,hsh):
        self.x = newx
        self.y = newy
        self.hsw = hsw
        self.hsh = hsh

class ParticleSystem:
    particles = [ ]
    winddir = pg.math.Vector2(1,1)
    xmultiplier,ymultiplier = 1,1
    obj_list = [ ]

    uirect = pg.rect.Rect(0,0,200,200)
    uicolor = (125,75,100)
    focusedobjid = None

    rbarspr = pg.image.load("enginedata/particle/red bar.png").convert()
    gbarspr = pg.image.load("enginedata/particle/green bar.png").convert()
    bbarspr = pg.image.load("enginedata/particle/blue bar.png").convert()


    def ClearAllObj(self):
        self.obj_list = []
        self.focusedobjid = None
    def GenerateParticles(self,amount,winddir,speed,rect,color,radius,width,needcamerarender = False,autogenerate=False):
        """
            resets particles and generates new ones\n
            winddir is pg.math.vector2 \n
            if autogenerate is on it will dont use amount value and generate based on how big is the rect

            speed should be something between 20 and 60, given speed values will be multiplied by 0.1
        """
        if(winddir.x == 0 and winddir.y == 0):
            winddir.x = 0.9
            winddir.y = 1.65
        winddir = winddir.normalize()
        
        # winddir (0.25,-0.15) gibi değer olucak sonra da bunu speed ve delta ile çarpıp hareket 
        # ettiricez
        


        with open("enginedata/particle/movlist.txt","r" ) as filedata:
            filedata = json.load(filedata)
            randommovlist = filedata


        if autogenerate:
            amount = (rect.width*rect.height) // ((rect.width + rect.height) // 2 )
        plist = [ ]
        offset = 0

        for _ in range(amount):
            plist.append( [random.randint(0,rect.width)  ,  random.randint(0,rect.height) ] )
        self.obj_list.append( [rect,winddir,speed*0.01,plist,needcamerarender,color,radius,width,randommovlist,offset ] )
                               # 0    1      2       3          4          5       6     7        8        9  
        print("entered speed",speed,"actual speed",speed*0.01)
    def Focus_Rect(self,gmp):
        i =0
        found = False
        for obj in self.obj_list:
            if obj[0].collidepoint(gmp):
                self.focusedobjid = i 
                print("focused on rect",self.focusedobjid)
                found = True
                break
            i += 1
        if found == False:
            self.focusedobjid = None
            print("No focused rects")

    def Update(self,dt,gmp,lmbhold):
        """ gmp = game obj mouse pos"""
        if self.focusedobjid != None: #focused obj exists
            rr = self.obj_list[self.focusedobjid][0]
            self.uirect[0],self.uirect[1] = rr[0]+rr[2]+112,rr[1]+85
        
        if self.focusedobjid != None and lmbhold:
            self.obj_list[self.focusedobjid][0].x = gmp[0] - self.obj_list[self.focusedobjid][0].width //2
            self.obj_list[self.focusedobjid][0].y = gmp[1] - self.obj_list[self.focusedobjid][0].width //2


        for obj in self.obj_list:
            i=0
            randommovlist = obj[8]
            windx = obj[1][0]
            windy = obj[1][1]
            speed = obj[2]
            plist = obj[3]

            rmllen = len(randommovlist) #randommovlist len
            offset = random.randint(0,rmllen)
            
            


            for part in plist:
                
                if i+offset >= rmllen:
                    offset = random.randint(0,10)
                
                if i+offset >= rmllen:
                    i -= rmllen

                #part[0] += ((windx + (randommovlist[i+offset][0] *dt )*speed *(dt*0.3) *10) *something
                #)
                
                #part[1] += ((windy + (randommovlist[i+offset][1] *dt) *speed *(dt*0.3) *10) /something
                #)

                part[0] += ( (windx + randommovlist[i+offset][0]) *speed) *dt
                part[1] += ( (windy + randommovlist[i+offset][1]) *speed )*dt


                # (dt*0.25) işe yarıyor sanırım


                # go out of screen
                if part[0] < ( -20 ) or part[0] > ( obj[0].width +20 ):  
                    if obj[1].x > 0:
                        part[0] = -5
                    elif obj[1].x < 0: #sola doğru gidiyor
                        part[0] = obj[0].width + 5
                if part[1] < (-20 ) or part[1] > ((obj[0].height +20 )):
                    if obj[1].y > 0:
                        part[1] = -5
                    elif obj[1].y < 0:
                        part[1] = obj[0].height + 5

                i += 1
            offset += i
        #print(test)


    def Render(self,surf_to_blit,):
        for obj in self.obj_list:
            plist =obj[3]
            if obj[4]: #needcamera render == True
                rectt = obj[0]
                for part in plist:
                    pg.draw.circle(surf_to_blit,obj[5],(part[0]-Cam.x+rectt.x-obj[6]//2 ,part[1]-Cam.y+rectt.y-obj[6]//2 ),obj[6],obj[7])
                    #pg.draw.circle(surf_to_blit,obj[5],(part[0]-Cam.x+rectt.x ,part[1]-Cam.y+rectt.y),obj[6],obj[7])
            else:
                for part in plist:
                    pg.draw.circle(surf_to_blit,obj[5],part,obj[6],obj[8])
        if self.focusedobjid !=  None:
            
            
            DrawRectObj(surf_to_blit,self.uirect,self.uicolor)
            #a = self.obj_list[self.focusedobjid][0]
            #DrawRectObj(surf_to_blit, (a[0]+a[2]//2 -10  ,  a[1]+a[3]//2 -10  ,a[2],a[3]) ,self.obj_list[self.focusedobjid][5],2)
            DrawCircleObj(surf_to_blit,(self.uirect[0],self.uirect[1]-60),(60,60,150),10,0)
            winddir = self.obj_list[self.focusedobjid][1]
            a = [self.uirect[0],self.uirect[1]-60]
            DrawLineObj(surf_to_blit,(255,0,0),(a,[a[0]+winddir.x*20,a[1]+winddir.y*20]  ),2)
            DrawSprObj(surf_to_blit,self.rbarspr,(self.uirect.x-85,self.uirect.y-25))
            DrawSprObj(surf_to_blit,self.gbarspr,(self.uirect.x-85,self.uirect.y-10))
            DrawSprObj(surf_to_blit,self.bbarspr,(self.uirect.x-85,self.uirect.y+5))
            #DrawRectObj(surf_to_blit,(self.uirect[0]+1,self.uirect[1]-25,self.uirect[2]-30,20),(0,255,255))

        #pg.draw.rect(surf_to_blit,self.uicolor,self.uirect)
        
class Text:
    wg = "\ "
    wg = wg.strip(" ")
    t_space = pg.image.load("enginedata" + wg + "font" + wg + "space.png").convert_alpha()
    t_0 = pg.image.load("enginedata" + wg + "font" + wg + "0.png").convert_alpha()
    t_1 = pg.image.load("enginedata" + wg + "font" + wg + "1.png").convert_alpha()
    t_2 = pg.image.load("enginedata" + wg + "font" + wg + "2.png").convert_alpha()
    t_3 = pg.image.load("enginedata" + wg + "font" + wg + "3.png").convert_alpha()
    t_4 = pg.image.load("enginedata" + wg + "font" + wg + "4.png").convert_alpha()
    t_5 = pg.image.load("enginedata" + wg + "font" + wg + "5.png").convert_alpha()
    t_6 = pg.image.load("enginedata" + wg + "font" + wg + "6.png").convert_alpha()
    t_7 = pg.image.load("enginedata" + wg + "font" + wg + "7.png").convert_alpha()
    t_8 = pg.image.load("enginedata" + wg + "font" + wg + "8.png").convert_alpha()
    t_9 = pg.image.load("enginedata" + wg + "font" + wg + "9.png").convert_alpha()
    t_A = pg.image.load("enginedata" + wg + "font" + wg + "A.png").convert_alpha()
    t_B = pg.image.load("enginedata" + wg + "font" + wg + "B.png").convert_alpha()
    t_C = pg.image.load("enginedata" + wg + "font" + wg + "C.png").convert_alpha()
    t_D = pg.image.load("enginedata" + wg + "font" + wg + "D.png").convert_alpha()
    t_E = pg.image.load("enginedata" + wg + "font" + wg + "E.png").convert_alpha()
    t_F = pg.image.load("enginedata" + wg + "font" + wg + "F.png").convert_alpha()
    t_G = pg.image.load("enginedata" + wg + "font" + wg + "G.png").convert_alpha()
    t_H = pg.image.load("enginedata" + wg + "font" + wg + "H.png").convert_alpha()
    t_I = pg.image.load("enginedata" + wg + "font" + wg + "I.png").convert_alpha()
    t_J = pg.image.load("enginedata" + wg + "font" + wg + "J.png").convert_alpha()
    t_K = pg.image.load("enginedata" + wg + "font" + wg + "K.png").convert_alpha()
    t_L = pg.image.load("enginedata" + wg + "font" + wg + "L.png").convert_alpha()
    t_M = pg.image.load("enginedata" + wg + "font" + wg + "M.png").convert_alpha()
    t_N = pg.image.load("enginedata" + wg + "font" + wg + "N.png").convert_alpha()
    t_O = pg.image.load("enginedata" + wg + "font" + wg + "O.png").convert_alpha()
    t_P = pg.image.load("enginedata" + wg + "font" + wg + "P.png").convert_alpha()
    t_Q = pg.image.load("enginedata" + wg + "font" + wg + "Q.png").convert_alpha()
    t_R = pg.image.load("enginedata" + wg + "font" + wg + "R.png").convert_alpha()
    t_S = pg.image.load("enginedata" + wg + "font" + wg + "S.png").convert_alpha()
    t_T = pg.image.load("enginedata" + wg + "font" + wg + "T.png").convert_alpha()
    t_U = pg.image.load("enginedata" + wg + "font" + wg + "U.png").convert_alpha()
    t_V = pg.image.load("enginedata" + wg + "font" + wg + "V.png").convert_alpha()
    t_W = pg.image.load("enginedata" + wg + "font" + wg + "W.png").convert_alpha()
    t_X = pg.image.load("enginedata" + wg + "font" + wg + "X.png").convert_alpha()
    t_Y = pg.image.load("enginedata" + wg + "font" + wg + "Y.png").convert_alpha()
    t_Z = pg.image.load("enginedata" + wg + "font" + wg + "Z.png").convert_alpha()
    t_dot = pg.image.load("enginedata"+wg + "font" + wg + "dot.png").convert_alpha()
    t_lline = pg.image.load("enginedata"+wg+"font"+wg+"little_line.png").convert_alpha()
    t_ddot = pg.image.load("enginedata" + wg + "font" + wg + "ddot.png").convert_alpha()
    t_lbracket = pg.image.load("enginedata" + wg + "font" + wg + "left_bracket.png").convert_alpha()
    t_rbracket = pg.image.load("enginedata" + wg + "font" + wg + "right_bracket.png").convert_alpha()
    t_paranth = pg.image.load("enginedata" + wg + "font" + wg + "parant.png").convert_alpha()
    t_rparanth = pg.image.load("enginedata" + wg + "font" + wg + "rev_parant.png").convert_alpha()
    t_comma = pg.image.load("enginedata" + wg + "font" + wg + "comma.png").convert_alpha()
    t_rth = pg.image.load("enginedata" + wg + "font" + wg + "rthing.png").convert_alpha()
    t_lth = pg.image.load("enginedata" + wg + "font" + wg + "lthing.png").convert_alpha()
    t_qm = pg.image.load("enginedata" + wg + "font" + wg + "questionmark.png").convert_alpha()
    font= { " ":t_space,
    "0":t_0,"1":t_1,"2":t_2,"3":t_3,"4":t_4,"5":t_5,"6":t_6,"7":t_7,"8":t_8, 
    "9":t_9,"A":t_A,"B":t_B,"C":t_C,"D":t_D,"E":t_E,"F":t_F,"G":t_G,"H":t_H,
    "I":t_I,"J":t_J,"K":t_K,"L":t_L,"M":t_M,"N":t_N,"O":t_O,"P":t_P,"Q":t_Q,
    "R":t_R,"S":t_S,"T":t_T,"U":t_U,"V":t_V,"W":t_W,"X":t_X,"Y":t_Y,"Z":t_Z,
    ".":t_dot,"-":t_lline,":":t_ddot,"[":t_lbracket,"]":t_rbracket,"(":t_paranth,")":t_rparanth,",":t_comma ,"<":t_rth,">":t_lth,"?":t_qm
                                                                            }
class Grass:
    sc_chunks = []
    active_chunks = [ ]
    grass_map = [ ]
    

def BlitRotate(surf_to_blit, image, pos, originPos, angle,isdebug = False,needrect = False,needcamerarender = False):
    """ 
        camera render = True means you want the blitted image as a object
        camera render = False means you want the blitted image as ui 
        if camerarender == True then you need to give hsw hsh and camerapos arguments
        NOTE: Dont use needcamerarender
    """
    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pg.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pg.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    if needcamerarender == False:
        surf_to_blit.blit(rotated_image, rotated_image_rect)
    else: 
        surf_to_blit.blit(rotated_image,(rotated_image_rect.x - Cam.x + Cam.hsw - rotated_image.get_width() //2 ,rotated_image_rect.y - Cam.y + Cam.hsh -rotated_image.get_height() //2 ))
        #print((rotated_image_rect.x - Cam.x + Cam.hsw - rotated_image.get_width() //2 ,rotated_image_rect.y - Cam.y + Cam.hsh -rotated_image.get_height() //2) )
    if isdebug == True: # draw rectangle around the image
        pg.draw.rect(surf_to_blit, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)
    if needrect == True:
        return rotated_image_rect

def ColListRender(collist,isdebug,surf_to_blit):
    """
        Collist will contain 2 object types either a circle or rect
        isdebug should be true for it to render
    """ ####OMG OMG this text is actually being shown in there whenever i acces the function from another file
    #isinstance(X, type)
    if isdebug == True:
        for col in collist:
            if isinstance(col, pg.rect.Rect):
                pg.draw.rect(surf_to_blit,(255,255,0),col,1)
            else:
                pg.draw.circle(surf_to_blit,(0,255,25),col,2 )
    return [ ]

def BlitText(text,startpos,surf,centered):
    text = str(text)
    text = text.upper()
    if centered == False:
        pos = startpos
    else: 
        p = TextPxLen(text)
        pos = (startpos[0] - p//2 ,startpos[1])
    text = str(text)
    text = text.upper()
    for char in text:
        spr = Text.font[char]
        surf.blit(spr,pos)
        pos = (pos[0] + spr.get_width(), pos[1])

def TextPxLen(text):
    length = 0
    text = text.upper()
    for char in text:
        spr = Text.font[char]
        length += spr.get_width()
    return length
"""def FontRenderwoFont(fontpath,textcolor,surf_to_blit,text,antialias,backgroundcolor,pos):
    
    font = pg.font.Font(fontpath)
    surf_to_blit.blit(font.render(text,antialias,textcolor,backgroundcolor),pos ) 
"""
pg.font.init()
def FontRenderwithFont(font,textcolor,surf_to_blit,inp_text,antialias,backgroundcolor,pos,iscentered):
    """NOTE: Im pretty sure that in multiple lines vertical centering doesnt exist"""
    pos = [pos[0],pos[1] ]
    
    texts = inp_text.splitlines()
    
    for text in texts:
        if iscentered:
            width = font.render(text,antialias,textcolor,backgroundcolor).get_width()
            pos[0] = pos[0] - width // 2
        
        surf_to_blit.blit(font.render(text,antialias,textcolor,backgroundcolor),pos )
        pos[1] += font.get_height()+3

def Draw_Trans_Rect(trans_surf,color,rect,transparency,surf_to_blit):
    """
        trans_surf is the transparency surf, transparency is between 0 - 255
    """
    pg.draw.rect(trans_surf,color,rect)   #start box
    trans_surf.set_alpha(transparency)
    surf_to_blit.blit(trans_surf,(0,0))
    trans_surf.fill((0,0,0))

def ConvertLevel(level):
    """ 
        returns a converted version of a Tiled map with every line being a list
    """
    newlevel = [ ]
    width = level["layers"][0]["width"]
    for tile in range(level["layers"][0]["height"]):
        newlevel.append( [] )
    y = 0
    x = 0
    for tile in level["layers"][0]["data"]:
        if tile != 0:
            tile -= 1
            
        newlevel[y].append(tile)
        x += 1
        if x == width:
            x = 0
            y += 1

    return newlevel

def RenderMapSurf(surf_to_blit,level,tilheight,tilwidth,tilesetdict):
    """
        tilesetdict is a dict that contains 
    """
    mapheight = len(level * tilheight)
    mapwidth = len(level[0] * tilwidth)
    new_surf = pg.surface.Surface((mapwidth,mapheight))
    y = 0
    for line in level:
        x = 0
        for tile in line:
            spr = pg.image.load(tilesetdict[str(tile)]).convert()
            new_surf.blit(spr,(x*tilwidth,y*tilheight ) )
            x += 1
        y += 1
    return new_surf

def CalculateNewPoints(oldpointlist,time,maxtime,multiplier,crazynessdivider): 
    """
        timer is current time in ms, maxtime is how much time before it resets in ms, 
        multiplier is how much the points will displace/move
        crazynessdivider should be between 100 - 2000 ms, the less value it has more crazy results you get
        if you dont want crazyness set to 0
    """
    if crazynessdivider == 0:
        pass
    else: 
        multiplier += (time % maxtime//crazynessdivider)

    time = time % maxtime #0 - 2000 ms arasını hesaplama için kullanıcaz

    movlist = [ (1*multiplier,-1*multiplier),(0,1*multiplier),(-1*multiplier,0),(0,1*multiplier),(1*multiplier,1*multiplier) ]
    

    div = maxtime // len(movlist )    
    offset = (time // div)

    
    
    
    i = 0 
    t = [ ]
    
    for oldpoint in oldpointlist:
        t.append( [ oldpoint[0],oldpoint[1] ] )
        t[i][0] += movlist[  offset - i ][0] #x
        t[i][1] += movlist[  offset - i ][1] #y
        #oldpoint[0] += movlist[  offset ][0]
        #oldpoint[1] += movlist[  offset ][1]
        i += 1


    #offset += 1
    #if offset == 4:
    #    offset -= 4
    return t
pg.font.init()
def FloatyTextRender(surf_to_blit,font,text,pos,iscentered,time,maxtime,stepamount,color = (255,255,255),needcamerarender = False,fillbackground = False ,backgroundcolor = (0,0,0)):
    """
        if not centered, pos is the center up left a letter can go 
        if centered, x is center and y is the highest 
        stepamount is how many steps it can go in up and down, must be positive
        camerarender = True means an object, false means ui
    """
    text = text.replace(" ","  ")
    movlist = [ ]
    a = range(-stepamount,stepamount + 1 )
    for element in a:
        movlist.append([0,element] )
    a = range(stepamount-1,-stepamount ,-1 )
    for element in a:
        movlist.append([0,element])
    

    i = 0
    time = time % maxtime
    div = maxtime //len(movlist)
    offset = (time // div) 
    pos = [pos[0],pos[1] + stepamount]
    if iscentered:
        pos[0] =  pos[0] - font.render(text,False,color).get_width() //2
    else:
        pass

    
    for letter in text:
        yvalue = pos[1]
        spr = font.render(letter,False,color)

        if i > len(movlist):
            #print("didsomething")
            i = 0
        #print("offset {}     ,i {},     total {}    movlist len {}".format(offset,i,offset-i,len(movlist)))
        
        if (offset -i ) > (len(movlist)-1):
            offset -= len(movlist)
            #print("whaa")

        yvalue = movlist[  offset - i ][1] + pos[1]
        
        

        if needcamerarender:
            if fillbackground:
                pg.draw.rect(surf_to_blit,(backgroundcolor),(pos[0] - Cam.x  - spr.get_width() //2 -1,yvalue - Cam.y  -spr.get_height() //2 -1  ,spr.get_width() + 1,spr.get_height() + 2 ) )
            surf_to_blit.blit(spr,(pos[0] - Cam.x  - spr.get_width() //2 ,yvalue - Cam.y  -spr.get_height() //2 ))
        else:
            if fillbackground:
                pg.draw.rect(surf_to_blit,(backgroundcolor), (pos[0]-1,yvalue-1,spr.get_width() +1,spr.get_height() + 2 ) )
            surf_to_blit.blit(spr, (pos[0],yvalue) )
        

        pos[0] += spr.get_width()


        i += 1 
    
def CameraRender(surf_to_blit,spr,sprpos,needpos = False):
    """ 
        renders stuff based on camera position so things drawn will be gameobjects not ui parts, 
        things rendered are based on camera pos 

        NOTE: create a new function to blit Maps,  the way it will work is that it will get the width and height of the 
        map and use it to blit it in such a way that the (0,0) pos will mean the most up left corner of the map
        using camerarender for blitting mapsurf makes the character spawn at the center tile of the screen
        NOTE: Also add circle and rect draw functions with camera rendering so they behave like objects
        
    """
    pos = (sprpos[0] - Cam.x + Cam.hsw - spr.get_width() //2 ,sprpos[1] - Cam.y + Cam.hsh -spr.get_height() //2 )
    surf_to_blit.blit(spr,pos)

    if needpos:
         
        #pos = [ pos[0] + spr.get_width()//2 , pos[1] ]
        return pos

def BlitMapSurf(surf_to_blit,mapspr,mappos):
    pos = (mappos[0] - Cam.x - mapspr.get_width() //2 ,mappos[1] - Cam.y -mapspr.get_height() //2 )
    surf_to_blit.blit(mapspr,pos)

def Convert_to_Obj(pos,sprwidth = 0,sprheight = 0):
    """ 
        Converts screen pos to gameobject pos
        if you want you can give sprwidth and sprheight too
    """
    pos = (pos[0] - Cam.x - sprwidth ,pos[1] - Cam.y -sprheight )

def Convert_to_UI(pos,sprwidth=0,sprheight=0):
    """
        Convert gameobject pos to screen pos
        optional: give sprwidth and sprheight
    """
    pos = (pos[0] +Cam.x +sprwidth ,pos[1] + Cam.y - sprheight )

def RotCalc(pos1,pos2 ):
    """
        Calculates rot between 2 points and returns the angle between them(doesn't normalize it)
    """
    dis_x,dis_y = pos1[0] - pos2[0],pos1[1] - pos2[1]
    angle = 0
    if dis_x != 0:
        angle = math.atan(dis_y / dis_x)

    if dis_x < 0:
        angle += math.pi

    if dis_y != 0 and dis_x == 0:
        angle = 130
    angle = math.degrees(angle)
    
    return angle

def DrawRectObj(surf_to_blit,rect,color,width = 0,):
    """
        draws an rect as if its an gameobject
    """
    rect = pg.rect.Rect(rect[0],rect[1],rect[2],rect[3] )

    pg.draw.rect(surf_to_blit,color,(rect[0] - Cam.x - (rect.w //2) ,
    rect[1] - Cam.y - (rect.h //2)                                       ,rect[2],rect[3]),width)

def DrawCircleObj(surf_to_blit,pos,color,radius,width=0):
    """
        draws an circle as if its an gameobject
    """

    #pg.draw.circle(surf_to_blit,color,pos,radius,width)

    pos = [ pos[0],pos[1]]
    pos[0] = pos[0] - Cam.x 
    pos[1] = pos[1] - Cam.y 

    pg.draw.circle(surf_to_blit,color,pos,radius,width)

def DrawPolygonObj(surf_to_blit,color,pointlist,width=0):
    """
        Draws an polygon as if it was an gameobj
    """
    for point in pointlist:
        point[0] = point[0] - Cam.x 
        point[1] = point[1] - Cam.y

    pg.draw.polygon(surf_to_blit,color,pointlist,width)

def DrawLineObj(surf_to_blit,color,pointlist,width=1):
    """
        Draws an line as if it was an gameobj
    """
    for point in pointlist:
        point[0] = point[0] - Cam.x 
        point[1] = point[1] - Cam.y
    pg.draw.line(surf_to_blit,color,pointlist[0],pointlist[1],width)

def DrawSprObj(surf_to_blit,spr,pos):
    pos = [pos[0],pos[1]]
    pos[0] = pos[0] - Cam.x
    pos[1] = pos[1] - Cam.y
    surf_to_blit.blit(spr,pos)