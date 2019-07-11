import random
class Card:
    cardlist=["0解除","1跳过","2反转","3攻击","4侦察","5洗牌","6抽底","7乞讨","8自爆","9炸弹"]
    def __init__(self,num,pile=False):
        self.num=num
        if(pile):
            self.lst=[random.randint(0,8) for ovo in range(self.num-1)]+[9]*(pile-1)+[7]*pile
            random.shuffle(self.lst)
        else:
            self.lst=[0]+[random.randint(1,8) for ovo in range(self.num-1)]
    def _showlist(self):
        for i in self.lst:
            print(self.cardlist[i],end=" ")
        print()
    def delwhere(self,where):
        del self.lst[where]
    def delwhat(self,what):
        loc=self.lst.index(what)
        del self.lst[loc]
    def foreseelist(self,where):
        print("你看到了：",end="")
        if(where>=len(self.lst)):
            where=len(self.lst)-1
        for i in range(where-1):
            print(self.cardlist[self.lst[i]],end=",")
        print(self.cardlist[self.lst[where]],end="！\n")
    def shufflelist(self):
        random.shuffle(self.lst)
    def takeone(self,up=True):
        if(up):
            cardtaken=self.lst[0]
            del self.lst[0]
        else:
            cardtaken=self.lst[-1]
            del self.lst[-1]
        return cardtaken
    def addone(self,crd):
        self.lst.append(crd)
    def addwhere(self,crd,where):
        self.lst.insert(where,crd)
    def locate9(self):
        return self.lst.index(9)
    def locatewhat(self,what):
        try:
            return self.lst.index(what)
        except:
            return False
    def takewhere(self,where):
        cardtaken=self.lst[where]
        del self.lst[where]
        return cardtaken
    def __str__(self):
        res=""
        for i in self.lst:
            res+=self.cardlist[i]+" "
        return res

class Player:
    num=0
    #There are some bugs in AI part. If you need to play with AI, change "ai=False" to "ai=True"
    def __init__(self,ai=False):
        self.num=Player.num
        Player.num+=1
        self.card=Card(5)
        self.alive=True
        self.times=0
        self.ai=ai
    def __str__(self):
        return str(self.num)+";"+str(self.card)+";"+str(self.alive)+";"+str(self.times)
    def isalive(self):
        return self.alive
    def isai(self):
        return self.ai
        
class GameCtrl:
    def __init__(self,playernum):
        self.playernum=playernum
        self.pile=Card(playernum*7,pile=playernum)
        self.playerlst=[]
        self.alivelst=[]
        self.runing=True
        self.winner=""
        self.r=False
        for i in range(self.playernum-1):
            self.playerlst.append(Player())
        self.playerlst.append(Player(ai=False))
        self.alivelst=self.playerlst.copy()
        self.turn=random.randint(0,playernum-1)
    def _showall(self):
        print("self.playernum:",self.playernum)
        print("self.pile:",self.pile)
        for i in self.playerlst:
            print("self.player:",i)
    def showbasicinfo(self):
        print(r"牌堆还有{0}张牌，抽中炸弹的几率为{1}%；".format(len(self.pile.lst),int((100*(len(self.alivelst)-1))/len(self.pile.lst))),end="")
        for i in self.alivelst:
            print(i.num,"号玩家还有",len(i.card.lst),"张牌；",sep="",end="")
        print()
    def nextturn(self):
        print("-"*10)
        alives=0
        for i in self.playerlst:
            if(i.isalive()):
                self.winner=i.num
                alives+=1
        if(alives==1):
            self.runing=False
        if(self.r):
            for ovo in range(self.playernum):
                if(self.turn<self.playernum-1):
                    self.turn+=1
                else:
                    self.turn=self.turn+1-self.playernum
                try:
                    if(self.playerlst[self.turn].isalive()):
                        break
                except:
                    self.turn=0
        else:
            for ovo in range(self.playernum):
                if(self.turn>0):
                    self.turn-=1
                else:
                    self.turn=self.turn-1+self.playernum
                
                try:
                    if(self.playerlst[self.turn].isalive()):
                        break
                except:
                    self.turn=self.playernum
    def dointurn(self):
        self.playerlst[self.turn].times+=1
        def aidointurn():
            def aitakeone():
                self.playerlst[self.turn].times-=1
                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)牌堆摸了一张牌！")
                tko=self.pile.takeone()
                if(tko==9):
                    print(str(self.playerlst[self.turn].num)+"号玩家(BOT)摸到了炸弹！")
                    if "0" in str(self.playerlst[self.turn].card):
                        self.playerlst[self.turn].card.delwhat(0)
                        wh=random.randint(0,len(self.pile.lst)-1)
                        self.pile.addwhere(9,wh)
                        return False
                    else:
                        self.playerlst[self.turn].alive=False
                        del self.alivelst[self.alivelst.index(self.playerlst[self.turn])]
                        print(str(self.playerlst[self.turn].num)+"号玩家(BOT)阵亡！")
                        return True
                else:
                    self.playerlst[self.turn].card.addone(tko)                
            while self.playerlst[self.turn].times>0:
                atkus=False
                if(self.pile.locate9()-1>self.playerlst[self.turn].times):
                    if(self.playerlst[self.turn].card.locatewhat(8)):
                        if(random.randint(1,100)%4!=1):
                            self.playerlst[self.turn].card.delwhat(8)
                            print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[自爆]！")
                            self.playerlst[self.turn].times+=2
                    if(aitakeone()):
                        break
                    else:
                        continue
                else:
                    if(self.playerlst[self.turn].card.locatewhat(4)):
                        print(str(self.playerlst[self.turn].num)+"号玩家(BOT)使用了[侦察]！")
                        self.playerlst[self.turn].card.delwhat(4)
                    if(self.pile.locate9()>1):
                        if(random.randint(1,100)%2==1):
                            if(aitakeone()):
                                break
                            else:
                                continue
                        if(random.randint(1,100)%2==1):
                            if(aitakeone()):
                                break
                            else:
                                continue
                    if(self.playerlst[self.turn].times):
                        seed=random.randint(1,100)
                        if(seed%2==0):
                            if(self.playerlst[self.turn].card.locatewhat(1)):
                                self.playerlst[self.turn].card.delwhat(1)
                                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[跳过]！")
                                self.playerlst[self.turn].times-=1
                                continue
                        if(seed%2==1):
                            if(self.playerlst[self.turn].card.locatewhat(2)):
                                self.playerlst[self.turn].card.delwhat(2)
                                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[反转]！")
                                self.r=not(self.r)
                                self.playerlst[self.turn].times-=1
                                continue
                        if(seed%2==1):
                            if(self.playerlst[self.turn].card.locatewhat(5)):
                                self.playerlst[self.turn].card.delwhat(5)
                                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[洗牌]！")
                                self.pile.shufflelist()
                                continue
                        if(seed%2==0):
                            if(self.playerlst[self.turn].card.locatewhat(6)):
                                if(self.pile.lst[-1]!=9):
                                    self.playerlst[self.turn].card.delwhat(6)
                                    print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[抽底]！")
                                    crd=self.pile.takeone(up=False)
                                    if(crd!=9):
                                        self.playerlst[self.turn].card.addone(crd)
                                        self.playerlst[self.turn].times-=1
                                        continue
                                    else:
                                        if "0" in str(self.playerlst[self.turn].card):
                                            self.playerlst[self.turn].card.delwhat(0)
                                            wh=random.randint(0,len(self.pile.lst)-1)
                                            self.pile.addwhere(9,wh)
                                            continue
                                        else:
                                            self.playerlst[self.turn].alive=False
                                            del self.alivelst[self.alivelst.index(self.playerlst[self.turn])]
                                            print(str(self.playerlst[self.turn].num)+"号玩家(BOT)阵亡！")
                                            break
                        if(seed%5!=4):
                            if(self.playerlst[self.turn].card.locatewhat(7)):
                                self.playerlst[self.turn].card.delwhat(7)
                                qt=self.alivelst[random.randint(1,100)%len(self.alivelst)]
                                while(qt==self.playerlst[self.turn]):
                                    qt=self.alivelst[random.randint(1,100)%len(self.alivelst)]
                                qt=qt.num
                                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)向"+str(qt)+"号玩家打出[乞讨]！")
                                self.playerlst[self.turn].card.addone(self.playerlst[qt].card.takewhere(-1))
                                continue
                        while(self.pile.locate9()<=1):
                            a=self.playerlst[self.turn].card.locatewhat(1)
                            b=self.playerlst[self.turn].card.locatewhat(2)
                            c=self.playerlst[self.turn].card.locatewhat(3)
                            if(a and b):
                                self.playerlst[self.turn].card.delwhat(1)
                                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[跳过]！")
                                atkus=True
                                self.playerlst[self.turn].times-=1
                                break
                            elif(a):
                                self.playerlst[self.turn].card.delwhat(1)
                                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[跳过]！")
                                atkus=True
                                self.playerlst[self.turn].times-=1
                                break
                            elif(b):
                                self.playerlst[self.turn].card.delwhat(2)
                                print(str(self.playerlst[self.turn].num)+"号玩家(BOT)打出[反转]！")
                                atkus=True
                                self.r=not(self.r)
                                self.playerlst[self.turn].times-=1
                                break
                            else:
                                if(c):
                                    self.playerlst[self.turn].card.delwhat(3)
                                    atk=self.alivelst[random.randint(1,100)%len(self.alivelst)]
                                    while(atk==self.playerlst[self.turn]):
                                        atk=self.alivelst[random.randint(1,100)%len(self.alivelst)]
                                    atk=atk.num
                                    atkus=True
                                    tmp=self.playerlst[self.turn].times
                                    self.playerlst[self.turn].times=0
                                    self.playerlst[atk].times=tmp+2
                                    self.turn=atk
                                    break                                
                    if(atkus):
                        continue
                    else:
                        if(aitakeone()):
                            break
                        else:
                            continue                                         
        if(self.playerlst[self.turn].isai()):
            aidointurn()
        else:
            self.showbasicinfo()
            while self.playerlst[self.turn].times>0:
                usecard=input("你是"+str(self.turn)+"号玩家("+str(self.playerlst[self.turn].times)+"次)，手牌有："+str(self.playerlst[self.turn].card)+"\n你要使用：")
                if(usecard=="" or (int(usecard) in self.playerlst[self.turn].card.lst)):
                    if(usecard=="0"):
                        print("解除不可主动打出！")
                    if(usecard=="1"):
                        self.playerlst[self.turn].card.delwhat(1)
                        self.playerlst[self.turn].times-=1
                    if(usecard=="2"):
                        self.playerlst[self.turn].card.delwhat(2)
                        self.r=not(self.r)
                        self.playerlst[self.turn].times-=1
                    if(usecard=="3"):
                        self.playerlst[self.turn].card.delwhat(3)
                        atk=input("你要攻击0-"+str(self.playernum-1)+"号玩家：")
                        try:
                            if(self.playerlst[int(atk)].alive):
                                tmp=self.playerlst[self.turn].times
                                self.playerlst[self.turn].times=0
                                self.playerlst[int(atk)].times=tmp+2
                                self.turn=int(atk)
                                self.dointurn()
                        except:
                            print("玩家无效！")
                            continue
                    if(usecard=="4"):
                        self.playerlst[self.turn].card.delwhat(4)
                        self.pile.foreseelist(3)
                    if(usecard=="5"):
                        self.playerlst[self.turn].card.delwhat(5)
                        self.pile.shufflelist()
                    if(usecard=="6"):
                        self.playerlst[self.turn].card.delwhat(6)
                        crd=self.pile.takeone(up=False)
                        if(crd!=9):
                            self.playerlst[self.turn].card.addone(crd)
                            self.playerlst[self.turn].times-=1
                            continue
                        else:
                            if "0" in str(self.playerlst[self.turn].card):
                                self.playerlst[self.turn].card.delwhat(0)
                                wh=input("BOOM！你要把炸弹放在第0-"+str(len(self.pile.lst)-1)+"张：")
                                try:
                                    self.pile.addwhere(9,int(wh))
                                except:
                                    self.pile.addwhere(9,0)
                                continue
                            else:
                                self.playerlst[self.turn].alive=False
                                print("你("+str(self.turn)+"号玩家)摸到炸弹阵亡了！")
                                del self.alivelst[self.alivelst.index(self.playerlst[self.turn])]
                                break
                                
                        self.playerlst[self.turn].times-=1
                    if(usecard=="7"):
                        self.playerlst[self.turn].card.delwhat(7)
                        #
                        qt=input("你要向0-"+str(self.playernum-1)+"号玩家乞讨：")
                        try:
                            if(self.playerlst[int(qt)].alive):
                                self.playerlst[self.turn].card.addone(self.playerlst[int(qt)].card.takewhere(-1))
                        except:
                            print("玩家无效！")
                            continue
                    if(usecard=="8"):
                        self.playerlst[self.turn].card.delwhat(8)
                        self.playerlst[self.turn].times+=2
                    if(usecard==""):
                        self.playerlst[self.turn].times-=1
                        tko=self.pile.takeone()
                        if(tko==9):
                            if "0" in str(self.playerlst[self.turn].card):
                                self.playerlst[self.turn].card.delwhat(0)
                                wh=input("BOOM！你要把炸弹放在第0-"+str(len(self.pile.lst)-1)+"张：")
                                try:
                                    self.pile.addwhere(9,int(wh))
                                except:
                                    self.pile.addwhere(9,0)
                                continue
                            else:
                                self.playerlst[self.turn].alive=False
                                print("你("+str(self.turn)+"号玩家)摸到炸弹阵亡了！")
                                del self.alivelst[self.alivelst.index(self.playerlst[self.turn])]
                                break
                        else:
                            self.playerlst[self.turn].card.addone(tko)                                 
                else:
                    print("此卡不存在！")
                    continue
            

gc=GameCtrl(4)
while(gc.runing):
    #gc._showall()
    gc.dointurn()
    gc.nextturn()

print("游戏结束！获胜的是",gc.winner,"号玩家。",sep="")
