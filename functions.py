# zed je "  ", start je colors.bg.black+"  "+colors.reset, cil je colors.bg.green+"  "+colors.reset
import random
import sys
import keyboard
import time
import cursor
import queue
from playsound import playsound


def maze_minigame(sirka, vyska, view_distance, pocet_otazek, cas, npc = False):
    # vytvori level, ktery nasledne uzivatel hraje
    kopie_view_distance = view_distance
    skore = 0
    bludiste, pozice_otazek = complete_bludiste(sirka, vyska, pocet_otazek)

    file_otazky = open("/".join(sys.argv[0].split("\\")[:-1])+"otazky.txt", "r", encoding="utf-8")
    otazky = [x[:-1].split("=") for x in file_otazky]
    file_otazky.close()
    kopie_otazky = otazky.copy()
    x, y = start_pozice(bludiste)
    baterka = False
    pozice_cil = False

    typer("Pro zahajeni hry stisknete enter", 10)
    keyboard.wait("enter")
    start_time = time.time()
    cursor.hide()

    sys.stdout.write(colors.line_home+colors.screen_clear)
    optimized_tisk_bludiste(bludiste,x,y,view_distance,"full")
    sys.stdout.write(f"Tvoje skore je {skore}/{pocet_otazek}. Potrebne skore je {pocet_otazek//2}\n")
    if npc:
        pepa = NPC("poskok1", 100, bludiste)
        pepa2 = NPC("poskok2", 10, bludiste)

    while True:
        if keyboard.is_pressed("a") and keyboard.is_pressed("b") and keyboard.is_pressed("c"):
            sys.stdout.write("Prohral jsi!!")
            break

        if not pozice_cil:
            if bludiste[y-1][x-1] == colors.bg.green+"  "+colors.reset:
                pozice_cil = True
                if skore >= pocet_otazek // 2:
                    end_time = time.time()
                    sys.stdout.write(f"Vyhral jsi!!! Trvalo ti to {round(end_time-start_time,1)} sekund")
                    break
                else:
                    sys.stdout.write("Jeste nemas dost bodu!")

        
        if keyboard.is_pressed("r"):
            cursor.hide()
            start_time = time.time()
            x = start_pozice(bludiste)[0]
            y = start_pozice(bludiste)[1]
            for i in pozice_otazek:
                bludiste[i[1]-1][i[0]-1] = colors.bg.yellow+"  "+colors.reset
            skore = 0
            otazky = kopie_otazky
            sys.stdout.write("\033[H\033[J")
            optimized_tisk_bludiste(bludiste,x,y,view_distance,"full")
            sys.stdout.write(f"Tvoje skore je {skore}/{pocet_otazek}. Potrebne skore je {pocet_otazek//2}\n")
        
        if keyboard.is_pressed("f5"):
            cursor.hide()
            sys.stdout.write("\033[H\033[J")
            optimized_tisk_bludiste(bludiste,x,y,view_distance,"full")
            sys.stdout.write(f"Tvoje skore je {skore}/{pocet_otazek}. Potrebne skore je {pocet_otazek//2}\n")

        if keyboard.is_pressed("ctrl"):
            time.sleep(.1)
            if not baterka:
                view_distance = max(vyska, sirka)
                sys.stdout.write("\033[H")
                optimized_tisk_bludiste(bludiste,x,y,view_distance,"full")
                sys.stdout.write(colors.line_down)
                baterka = True
            else:
                view_distance = kopie_view_distance
                sys.stdout.write("\033[H")
                optimized_tisk_bludiste(bludiste,x,y,view_distance,"full")
                sys.stdout.write(colors.line_down)
                baterka = False

        yy = y
        xx = x
        if keyboard.is_pressed("up arrow") or keyboard.is_pressed("w"):
            yy = yy - 1
            if keyboard.is_pressed("0"):
                yy -= 1
        elif keyboard.is_pressed("down arrow") or keyboard.is_pressed("s"):
            yy = yy + 1
            if keyboard.is_pressed("0"):
                yy += 1
        elif keyboard.is_pressed("left arrow") or keyboard.is_pressed("a"):
            xx = xx - 1
            if keyboard.is_pressed("0"):
                xx -= 1
        elif keyboard.is_pressed("right arrow") or keyboard.is_pressed("d"):
            xx = xx + 1
            if keyboard.is_pressed("0"):
                xx += 1
        
        if xx != x or yy != y:
            if not bludiste_zed(xx, yy, bludiste):
                optimized_tisk_bludiste(bludiste,x,y,view_distance,"update",xx,yy)
                move(2,vyska+3)
                if pozice_cil:
                    sys.stdout.write(colors.line_clear)
                    pozice_cil = False
                x = xx
                y = yy
                
                for each in NPC.npcs:
                    each.npc_move(x-1, y-1)
                time.sleep(0.05)
                move(2,vyska+3)

        if bludiste[y-1][x-1] == colors.bg.yellow+"  "+colors.reset:
            if otazka_odpoved(otazky, cas):
                skore += 1
            sys.stdout.write("\nPro navraceni do pohybu po bludisiti stisknete enter")
            time.sleep(.1)
            keyboard.wait("enter")
            sys.stdout.write((colors.line_clear+colors.line_up)*4+colors.line_clear+"\n"+colors.line_clear+colors.line_up)
            bludiste[y-1][x-1] = "  "
            sys.stdout.write(colors.line_up+"Tvoje skore je "+str(skore)+"/"+str(pocet_otazek)+"\n")


def optimized_tisk_bludiste(bludiste, x, y, view_distance, mode, xx = 0, yy = 0):
    x -= 1
    y -= 1
    yy -= 1
    xx -= 1
        
    if mode == "full":
        for i, radek in enumerate(bludiste):
            for j, char in enumerate(radek):
                if abs(i - y) <= view_distance and abs(j - x) <= view_distance:
                    if i == y and j == x:
                        sys.stdout.write(colors.bg.red+"  "+colors.reset)
                    elif j+1 != len(radek):
                        sys.stdout.write(char)
                    else:
                        sys.stdout.write(char+"\n")
                elif j+1 != len(radek):
                    sys.stdout.write(colors.bg.blue+"  "+colors.reset)
                else:
                    sys.stdout.write(colors.bg.blue+"  "+colors.reset+"\n")
    elif mode == "update":
        if yy != -1 and xx != -1:
            if xx > x:
                move((x+1)*2,y+2)
                sys.stdout.write(bludiste[y][x])
                move((xx+1)*2, yy+2)
                sys.stdout.write(colors.bg.red+"  "+colors.reset)

                for yyy in range(yy - view_distance + 2,yy + view_distance + 3):
                    if x-view_distance in range (0,len(bludiste[0])) and yyy - 2 in range(0,len(bludiste)):
                        move((x-view_distance+1)*2,yyy)
                        sys.stdout.write(colors.bg.blue+"  "+colors.reset)
                    if xx+view_distance in range (0,len(bludiste[0])) and yyy - 2 in range(0,len(bludiste)):
                        move((xx+view_distance+1)*2,yyy)
                        sys.stdout.write(bludiste[yyy-2][xx+view_distance])

            if yy > y:
                move((x+1)*2,y + 2)
                sys.stdout.write(bludiste[y][x])
                move((xx+1)*2,yy + 2)
                sys.stdout.write(colors.bg.red+"  "+colors.reset)
                
                for xxx in range(xx - view_distance + 1, xx + view_distance + 2):
                    if y - view_distance in range (0,len(bludiste)) and xxx in range(1, len(bludiste[0])+1):
                        move(xxx*2,y-view_distance + 2)
                        sys.stdout.write(colors.bg.blue+"  "+colors.reset)
                    if yy + view_distance in range (0,len(bludiste)) and xxx in range(1, len(bludiste[0])+1):
                        move(xxx*2, yy+view_distance + 2)
                        sys.stdout.write(bludiste[yy + view_distance][xxx - 1])

            if xx < x:
                move((xx + 1)*2,yy + 2)
                sys.stdout.write(colors.bg.red+"  "+colors.reset)
                move((x+1)*2, y + 2)
                sys.stdout.write(bludiste[y][x])
                
                for yyy in range(yy - view_distance + 2,yy + view_distance + 3):
                    if x+view_distance in range (0,len(bludiste[0])) and yyy - 2 in range(0,len(bludiste)):
                        move((x+view_distance+1)*2,yyy)
                        sys.stdout.write(colors.bg.blue+"  "+colors.reset)
                    if xx-view_distance in range (0,len(bludiste[0])) and yyy -2 in range(0,len(bludiste)):
                        move((xx-view_distance+1)*2,yyy)
                        sys.stdout.write(bludiste[yyy-2][xx-view_distance])
            if yy < y:
                move((x+1)*2,y + 2)
                sys.stdout.write(bludiste[y][x])
                move((xx+1)*2,yy + 2)
                sys.stdout.write(colors.bg.red+"  "+colors.reset)
                
                for xxx in range(xx - view_distance + 1, xx + view_distance + 2):
                    if y + view_distance in range (0,len(bludiste)) and xxx in range(1, len(bludiste[0])+1):
                        move(xxx*2,y+view_distance + 2)
                        sys.stdout.write(colors.bg.blue+"  "+colors.reset)
                    if yy - view_distance in range (0,len(bludiste)) and xxx in range(1, len(bludiste[0])+1):
                        move(xxx*2, yy-view_distance + 2)
                        sys.stdout.write(bludiste[yy - view_distance][xxx - 1])
        else:
            raise ValueError("xx and yy not given")
    else:
        raise ValueError("Invalid mode")


def pridej_otazky(bludiste, pocet):
    pozice=list()
    for i in range(pocet):
        y = random.randint(1, len(bludiste) - 2)
        x = random.randint(1, len(bludiste[0]) - 2)
        while bludiste[y][x] != "  ":
            y = random.randint(1, len(bludiste) - 2)
            x = random.randint(1, len(bludiste[0]) - 2)
        bludiste[y][x] = colors.bg.yellow+"  "+colors.reset
        pozice.append([x + 1, y + 1])
    return pozice

def pridej_start_cil(bludiste):
    x = 1
    y = random.randint(1, len(bludiste) - 2)
    while bludiste[y][x]==colors.bg.lightgrey+"  "+colors.reset:
        y = random.randint(1, len(bludiste) - 2)
    bludiste[y][x] = colors.bg.black+"  "+colors.reset
    x = len(bludiste[0]) - 2
    y = random.randint(1, len(bludiste) - 2)
    while bludiste[y][x]==colors.bg.lightgrey+"  "+colors.reset:
        y = random.randint(1, len(bludiste) - 2)
    bludiste[y][x] = colors.bg.green+"  "+colors.reset

def start_pozice(bludiste):
    for y, char in enumerate(bludiste):
        try:
            x = char.index(colors.bg.black+"  "+colors.reset)
        except:
            pass
        else:
            return x + 1, y + 1

class Player:
    zivoty = 3
    skore = 0
    
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

def graficke_predelani(generovane_bludiste):
    for sloupec in range (len(generovane_bludiste)):
        for char in range (len(generovane_bludiste[0])):
            if generovane_bludiste[sloupec][char] == "z":
                generovane_bludiste[sloupec][char] = colors.bg.lightgrey+"  "+colors.reset
            elif generovane_bludiste[sloupec][char] == "S":
                generovane_bludiste[sloupec][char] = colors.bg.black+"  "+colors.reset
            elif generovane_bludiste[sloupec][char] == "C":
                generovane_bludiste[sloupec][char] = colors.bg.green+"  "+colors.reset
            elif generovane_bludiste[sloupec][char] == "o":
                generovane_bludiste[sloupec][char] = colors.bg.yellow+"  "+colors.reset
            else:
                generovane_bludiste[sloupec][char]="  "

def graficke_oddelani(bludiste):
    for sloupec in range (len(bludiste)):
        for char in range (len(bludiste[0])):
            if bludiste[sloupec][char] == colors.bg.lightgrey+"  "+colors.reset:
                bludiste[sloupec][char] = "z"
            elif bludiste[sloupec][char] == colors.bg.black+"  "+colors.reset:
                bludiste[sloupec][char] = "S"
            elif bludiste[sloupec][char] == colors.bg.green+"  "+colors.reset:
                bludiste[sloupec][char] = "C"
            elif bludiste[sloupec][char] == colors.bg.yellow+"  "+colors.reset:
                bludiste[sloupec][char] = "o"
            else:
                bludiste[sloupec][char]=" "

def vytvoreni_zdi(generovane_bludiste, x, y, zdi, sirka, vyska):
    if 0 < x < sirka - 1 and 0 < y < vyska - 1:
        generovane_bludiste[y][x] = "c"
        zdi.append([x + 1, y])
        zdi.append([x, y + 1])
        zdi.append([x - 1, y])
        zdi.append([x, y - 1])

def generator_bludiste(sirka, vyska):
    if vyska < 5 or sirka < 5:
        sys.stdout.write("minimalni velikost je 5x5"+"\n")
        sirka = int(input("Zadej novou sirku vetsi nez 5: "))
        vyska = int(input("Zadej novou vysku vetsi nez 5: "))
        generator_bludiste(sirka, vyska)
    else:
        generovane_bludiste = [list("z" * sirka) for x in range(vyska)]    #vytvoreni mrizky zdi
        x = random.randint(1, sirka - 2)
        y = random.randint(1, vyska - 2)                        #nechceme zacit okrajem
        
        zdi=list()
        vytvoreni_zdi(generovane_bludiste, x, y, zdi, sirka, vyska)
        while len(zdi) > 0:
            #smazani zdi na okraji nebo jiz "rozbitych zdi"
            meziseznam = [each for each in zdi if not generovane_bludiste[each[1]][each[0]] == "p" and  1 <= each[0] <= sirka - 2 and 1 <= each[1] <= vyska - 2]    
            zdi = meziseznam

            #vybrani nahodne zdi
            if len(zdi) == 1:
                nahoda = 0
            elif len(zdi) > 1:
                nahoda = random.randint(0,len(zdi) - 1)
            else:
                return generovane_bludiste
            x = zdi[nahoda][0]
            y = zdi[nahoda][1]
            #urceni poctu pruchodu kolem zdi
            pocet_nahore = 0
            pocet_dole = 0
            pocet_vlevo = 0
            pocet_vpravo = 0
            if generovane_bludiste[y][x + 1] == "c":
                pocet_vpravo += 1
            if generovane_bludiste[y + 1][x] == "c":
                pocet_dole += 1
            if generovane_bludiste[y][x - 1] == "c":
                pocet_vlevo += 1
            if generovane_bludiste[y - 1][x] == "c":
                pocet_nahore += 1
            
            #pokud je jen jeden pruchod kolem zdi
            if pocet_dole + pocet_nahore + pocet_vlevo + pocet_vpravo == 1:
                generovane_bludiste[y][x] = "p"
                if pocet_vpravo == 1:
                    vytvoreni_zdi(generovane_bludiste, x - 1, y, zdi, sirka, vyska)
                elif pocet_vlevo == 1:
                    vytvoreni_zdi(generovane_bludiste, x + 1, y, zdi, sirka, vyska)
                elif pocet_dole == 1:
                    vytvoreni_zdi(generovane_bludiste, x, y - 1, zdi, sirka, vyska)
                else:
                    vytvoreni_zdi(generovane_bludiste, x, y + 1, zdi, sirka, vyska)
            
            del zdi[nahoda]
        else:
            return generovane_bludiste

def bludiste_zed(x,y,bludiste):
    if bludiste[y-1][x-1] == colors.bg.lightgrey+"  "+colors.reset:
        return True
    else:
        return False

def complete_bludiste(sirka, vyska, pocet_otazek):
    bludiste = generator_bludiste(sirka, vyska)
    graficke_predelani(bludiste)
    pridej_start_cil(bludiste)
    pozice_otazek = pridej_otazky(bludiste, pocet_otazek)
    return bludiste, pozice_otazek

class colors:
    line_home = "\033[H"
    screen_clear = "\033[J"
    line_up = '\033[1A'
    line_clear = '\x1b[2K'
    line_down = '\033[1B'
    line_right = '\033[1C'
    line_left = '\033[1D'
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        yellow='\033[103m'
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

def move(x, y):
    x -= 1
    y -= 1
    sys.stdout.write("\033[%d;%dH" % (y,x))

def vyber_otazky(seznam_otazek):
    otazka = seznam_otazek.pop(random.randint(0, len(seznam_otazek)-1))
    q = otazka[0]
    a = otazka[1:]
    ca = otazka[1]
    random.shuffle(a)
    otazka=list(a)
    otazka.insert(0,q)
    otazka.append(ca)
    return otazka

def otazka_odpoved(otazky,cas):
    current_otazka = vyber_otazky(otazky)
    optA ="A:"+current_otazka[1]
    optB ="B:"+current_otazka[2]
    optC ="C:"+current_otazka[3]
    for i, each in enumerate(current_otazka):
        if each == current_otazka[-1]:
            if i == 1:
                optS = "A"
            elif i == 2:
                optS = "B"
            elif i == 3:
                optS = "C"
            else:
                raise ValueError("Spatne zadana otazka")
            break
    current_otazka = current_otazka[0]


    odpocet = 0
    odpoved = ""
    typer(current_otazka+"\n")
    typer(optA+" "+optB+" "+optC+"\n")
    sys.stdout.write(colors.line_up*2+colors.line_right*(len(current_otazka)+1)+str(cas - odpocet))
    start = time.time()
    while True:
        if keyboard.is_pressed("a") or keyboard.is_pressed("A"):
            odpoved = "A"
            sys.stdout.write(colors.line_down+"\r"+colors.bg.orange+optA+colors.reset+" "+optB+" "+optC)
            sys.stdout.write(colors.line_up+"\r"+colors.line_right*(len(current_otazka)+1+len(str(cas - odpocet))))
        elif keyboard.is_pressed("b") or keyboard.is_pressed("B"):
            odpoved = "B"
            sys.stdout.write(colors.line_down+"\r"+optA+" "+colors.bg.orange+optB+colors.reset+" "+optC)
            sys.stdout.write(colors.line_up+"\r"+colors.line_right*(len(current_otazka)+1+len(str(cas - odpocet))))
        elif keyboard.is_pressed("c") or keyboard.is_pressed("C"):
            odpoved = "C"
            sys.stdout.write(colors.line_down+"\r"+optA+" "+optB+" "+colors.bg.orange+optC+colors.reset)
            sys.stdout.write(colors.line_up+"\r"+colors.line_right*(len(current_otazka)+1+len(str(cas - odpocet))))
        if keyboard.is_pressed("enter"):
            if len(odpoved) > 0:
                sys.stdout.write(colors.line_down*2+"\rUkoncili jste zadavani odpovedi\n")
                sys.stdout.write("Vase odpoved: "+odpoved)
                break
            else:
                time.sleep(0.030)
                sys.stdout.write(colors.line_down*2+"\rZadejte nejdrive odpoved!\n"+colors.line_up*3+colors.line_right*(len(current_otazka)+1+len(str(30 - odpocet))))


        end = time.time()
        if  round(end - start) > odpocet:
            odpocet = round(end - start)
            if cas - odpocet == 9:
                sys.stdout.write(colors.line_left*2+"  ")
            elif cas - odpocet == 0:
                sys.stdout.write(colors.line_left*len(str(cas+1 - odpocet))+str(cas - odpocet))
                sys.stdout.write(colors.line_down*2+"\rVyprsel cas\n")
                sys.stdout.write("Vase odpoved: "+odpoved)
                break
            sys.stdout.write(colors.line_left*len(str(cas+1 - odpocet))+str(cas - odpocet))

    if odpoved == optS:
        sys.stdout.write(" "+colors.bg.green+"Spravne"+colors.reset)
        return True
    else:
        sys.stdout.write(" "+colors.bg.red+"Spatne"+colors.reset+" . Spravne bylo "+optS)
        return False
    
class NPC:
    npcs = []
    def __init__(self, name, view_distance, bludiste):
        self.bludiste = bludiste
        self.name = name
        self.npcs.append(self)
        self.view_distance = view_distance
        self.y = random.randint(1, len(bludiste) - 2)
        self.x = random.randint(1, len(bludiste[0]) - 2)
        while bludiste[self.y][self.x] != "  ":
            self.y = random.randint(1, len(bludiste) - 2)
            self.x = random.randint(1, len(bludiste[0]) - 2)
        move((self.x+1)*2, self.y+2)
        sys.stdout.write(colors.bg.purple+"  "+colors.reset)

    def clear(self):
        self.npcs = list()

    def npc_move(self, player_x, player_y):
        if abs(self.x - player_x) <= self.view_distance and abs(self.y - player_y) <= self.view_distance:
            path = (path_finder(self.bludiste, False, (self.y, self.x), (player_y, player_x)))
            move((self.x+1)*2, self.y+2)
            sys.stdout.write(self.bludiste[self.y][self.x])
            try:
                self.y, self.x = path[1]
            except:
                self.y, self.x = path[0]
            move((self.x+1)*2, self.y+2)
            sys.stdout.write(colors.bg.purple+"  "+colors.reset)
            playsound("/".join(sys.argv[0].split("\\")[:-1])+"ALARM.wav", False)
            if self.x == player_x and self.y == player_y:
                self.npcs.pop(self.npcs.index(self))


def typer(string, ms = 20):
    for each in string: 
        sys.stdout.write(each)
        time.sleep(ms/1000)

def ulozeni_do_souboru(bludiste, jmeno_souboru, cesta = sys.argv[0], slozka = "levels"):
    #ulozi bludiste do souboru v textovem formatu
    graficke_oddelani(bludiste)
    path = cesta.split("\\")
    path = "\\".join(path[:-1])+"\\"+slozka+"\\"+jmeno_souboru
    file = open(path, "w")
    write_content = list()
    for i in range(len(bludiste)):
        write_content.append("".join(bludiste[i])+"\n")
    file.writelines(write_content)
    file.close()
    graficke_predelani(bludiste)

def nacteni_ze_souboru(jmeno_souboru, cesta = sys.argv[0], slozka = "levels"):
    path = cesta.split("\\")
    path = "\\".join(path[:-1])+"\\"+slozka+"\\"+jmeno_souboru
    file = open(path,"r")
    bludiste = [list(x[:-1]) for x in file]
    graficke_predelani(bludiste)
    return bludiste

def path_finder(bludiste, vykreslovani=False, start = colors.bg.black+"  "+colors.reset, end = colors.bg.green+"  "+colors.reset, ms = 10):
    if type(start) == str:
        start_pos = find_start(bludiste, start)
    else:
        start_pos = start
    
    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    path=list()
    visited = set()

    while not q.empty():
        old_path = path.copy()
        current_pos, path = q.get()
        row, col = current_pos
        
        if vykreslovani:
            for each in old_path:
                if each not in path:
                    y, x = each
                    if bludiste[y][x] == "  ":
                        move((x+1)*2, y+2)
                        sys.stdout.write("  ")

            for each in path:
                if each not in old_path:
                    y, x = each
                    if bludiste[y][x] == "  ":
                        move((x+1)*2, y+2)
                        sys.stdout.write(colors.bg.purple+"  "+colors.reset)
            time.sleep(ms/1000)

        if bludiste[row][col] == end or (row, col) == end:
            return path

        neighbours = find_neighbours(bludiste, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour
            if bludiste[r][c] == colors.bg.lightgrey+"  "+colors.reset:
                continue
            
            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)
        


def maze_print(maze, path=set()):
    for i, row in enumerate(maze):
        for j, char in enumerate(row):
            if char == colors.bg.green+"  "+colors.reset:
                sys.stdout.write(colors.bg.green+"  "+colors.reset)
            elif char == colors.bg.black+"  "+colors.reset:
                sys.stdout.write(colors.bg.red+"  "+colors.reset)
            elif (i, j) in path and maze[i][j] == "  ":
                sys.stdout.write(colors.bg.purple+"  "+colors.reset)
            else:
                sys.stdout.write(char)
        sys.stdout.write("\n")

def path_coin_finder(bludiste, pozice_otazek):
    pocet_otazek = len(pozice_otazek)
    complete_path = []
    skore = 0
    current = path_finder(bludiste, end = colors.bg.yellow+"  "+colors.reset)
    complete_path += current
    skore += 1
    while skore <= pocet_otazek//2 + 1:
        current = path_finder(bludiste, start=complete_path[-1], end = colors.bg.yellow+"  "+colors.reset)
        complete_path += current
        skore +=1
        y, x = current[-1]
        bludiste[y][x] = "  "
    current = path_finder(bludiste, start = complete_path[-1])
    complete_path+=current
    for i in pozice_otazek:
        bludiste[i[1]-1][i[0]-1] = colors.bg.yellow+"  "+colors.reset
    return complete_path

def find_start(bludiste, start):
    for i, row in enumerate(bludiste):
        for j, char in enumerate(row):
            if char == start:
                return i, j
    return None

def find_neighbours(bludiste, row, col):
    neighbours = list()

    if row > 0:
        neighbours.append((row - 1, col))
    if row < len(bludiste) - 1:
        neighbours.append((row + 1, col))
    if col > 0:
        neighbours.append((row, col -1))
    if col < len(bludiste[0]) - 1:
        neighbours.append((row, col + 1))

    return neighbours 