# pylint: disable=unused-variable

# 5 hajó: 5e-1db; 4e:1db; 3e:2db; 2e:1db
# A-J; 1-10 tábla
# A hajók csak függőlegesen vagy vízszintesen lehetnek elrendezve, em lóghatnak ki, és nem lóghatnak egymásra
# Találat: X
# Nem talált: O
# Ha egy hajó minden elemét találat éri akkor az  elsüllyed, ezt jelezni kell.
# Játékosok feladata 1.: elhelyezni a hajókat a táblán a szabályoknak megfelelően
# Játékosok feladata 2.: lőni, úgy hogy minél nagyobb valószínűséggel találja el az ellenséget
# Játékosok feladata 3.: jelezni hogy talált vagy nem, illetve hogy elsűjedt-e a hajó, vagy hogy esűllyedt-e a flotta
# Játékosok feladata 4.: rögzíteni a próbálkozásokat és a találatokat


# Változók: üres táblázat; hajók, lövések, felhasználó neve.

# Kirajzoljuk a táblát, felette főcím.
# Üdvözöljük a felhasználót. Ismertetjük a játékszabályt.
# Hajók elhelyezése: megadjuk a hajók típusát, majd bekérjük a pozícióját egyesével, egy kezdőértéket és egy irányt. 
# A program kiegészíti a hajókat, és ellenőrizi hogy, nincs-e ütközés egy korábban elhelyezett hajóval, illetve nem lóg-e ki a táblázatból. 
# A számítógép randomgenerátort használ z elhelyezésre.
# Elekzdődnek a lövések a koordináták megadásával. A számítógép randomgenerátort használ először a teljes táblára, de ha talál akkor lecsöken a random scope-ja a környező koordinátákra, ha ismét talál akkor csak az adott vonal mentén lő. Ha az egyik irány elfogyott, akkor a másik irányt erőlteti.
# Ha elsűjed egy hajó akkor azt bejelentjük, a számítógép algoritmusa újból a tágab scope-on van.
# Ha az összes ellenséges hajó elsűjedt akkor bejelentjük a győzelmet, és megmutatjuk mindkét táblát.

import random
import os
import msvcrt

#Táblázat:
table = [
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "]]

tableAirBomb = [
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "],
[" _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "," _ "]]

#Hajó típusok, a számértékük a hossukat jelöli:
CARRIER = 5
BATTLESHIP = 4
CRUISER = 3
SUBMARINE = 3
DESTROYER = 2

a = 0
SHIPS = [CARRIER, BATTLESHIP, CRUISER, SUBMARINE, DESTROYER]
SHIPLENGTH = SHIPS[a]
SHIPFLOTTLENGTH = len(SHIPS)
AIRBOMBLEFT = 30


#Táblázat rajzoló ciklusfüggvény:
def table_draw(table):
    # os.system('cls')
    print()
    print("          Torpedó játék")
    print()
    row = int(0)
    col = int(0)
    print("   ","A ","B ","C ","D ","E ","F ","G ","H ","I ","J ")
    n = 0
    for i in table[row]:
        print("", n, "", end="")
        n += 1
        for i in table:
            print(table[row][col], end="")
            col += 1     
        col = 0
        row += 1
        print()
    print()

# table_draw(table)

#print("A fenti táblán 5db hadihajót kell elhelyezned. Ad meg a hajók helyzetét egyenként!")
#print()
# CARRIER = input("Add meg az 5 egység hosszú hordozó egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját (pl.: b1,b2): ")
# BATTLESHIP = input("Add meg az 4 egység hosszú csatahajó egyik végének kezdő koordinátájátv, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# CRUISER = input("Add meg az 3 egység hosszú cirkáló egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# SUBMARINE = input("Add meg az 3 egység hosszú tengeralattjáró egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")
# DESTROYER = input("Add meg az 2 egység hosszú romboló egyik végének kezdő koordinátáját, valamint az irányát meghatározó függőleges vagy vizszintes irányban lévő szomszédos cella koordinátáját: ")


def randomStartCoords():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return x,y


def randomLegalDirection(x,y,):
    direction = []
    print("random coordináták:",x,y)
    if x >= SHIPLENGTH:
        directionLeft = [-1,0]
        direction.append(directionLeft)
        print("bal", directionLeft)
    if x <= 10-SHIPLENGTH:
        directionRight = [1,0]
        direction.append(directionRight)
        print("jobb", directionRight)
    if y >= SHIPLENGTH:
        directionUp = [0,-1]
        direction.append(directionUp)
        print("fel", directionUp)
    if y <= 10-SHIPLENGTH:
        directionDown = [0,1]
        direction.append(directionDown)
        print("le", directionDown)
    print("lehetséges irányok:",direction)
    randomDirection = random.choice(direction)
    print("random irány:",randomDirection)
    return randomDirection


def checkShipPlace(x,y,randomDirection,SHIPLENGTH):
    randomDirection = randomDirection
    i = 0
    while i < SHIPLENGTH:
        if table[y + randomDirection[1]*i][x + randomDirection[0]*i] == " _ ":
            i += 1
        elif table[y + randomDirection[1]*i][x + randomDirection[0]*i] != " _ ":
            break
    return i


def placeShip(x,y,randomDirection,SHIPLENGTH):
    randomShipCoords = []
    i = 0
    while i < SHIPLENGTH:
        table[y + randomDirection[1]*i][x + randomDirection[0]*i] = " H "
        shipCoords = (y + randomDirection[1]*i, x + randomDirection[0]*i)
        randomShipCoords.append(shipCoords)
        print("rand ship coords:", randomShipCoords)
        i += 1
    return randomShipCoords


def placeRandomShips():
    allRandomShipsCoords = []
    a = 0
    while a < SHIPFLOTTLENGTH:
        SHIPLENGTH = SHIPS[a]
        x,y = randomStartCoords()
        randomDirection = randomLegalDirection(x,y)
        checkShipPlaceValue = checkShipPlace(x,y,randomDirection,SHIPLENGTH)
        print("check ship place value:",checkShipPlaceValue == SHIPLENGTH)
        if checkShipPlaceValue == SHIPLENGTH:
            placeShipCoords = placeShip(x,y,randomDirection,SHIPLENGTH)
            print("place ship Coords:",placeShipCoords == SHIPLENGTH)
            if len(placeShipCoords) == SHIPLENGTH:
                allRandomShipsCoords.append(placeShipCoords)
                a += 1
                print("a értéke:", a)
        print("köv hajótípus:", SHIPLENGTH)
    return allRandomShipsCoords


def inputCoord():
    char = "abcdefghijq"
    char1 = "0123456789q"
    coordStr1 = "_"
    coordStr2 = "_"
    coord = [int(-1),int(-1)]
    while coord[0] == -1 and coord[0] != 10:
        print("Adj meg egy értéket a vízszintes tengelyen a-j-ig:")
        coordStr1 = msvcrt.getwch()
        print("A koordináta:",coordStr1,",",coordStr2)
        coordStr1.casefold()
        coord[0] = char.find(coordStr1[0],0,11)
    while coord[1] == -1 and coord[1] != 10 and coord[0] != 10:
        print("Adj meg egy értéket a függőleges tengelyen 0-9-ig:")
        coordStr2 = msvcrt.getwch()
        print("A koordináta:",coordStr1,",",coordStr2)
        coordStr2.casefold()
        coord[1] = char1.find(coordStr2[0],0,11)
    print("A koordináta értéke:",coord)
    return coord


def sink(Air_y,Air_x,allRandomShipsCoords,shinkShipCount):
    shinkShipCount = shinkShipCount
    AirY = 0
    AirX = 0
    s = []
    shipPart = []
    for i in range(0,10):
        for k in range(0,10):
            if table[AirX][AirY] == " T ":
                s = (AirX,AirY)
                shipPart.append(s)
            AirX += 1     
        AirX = 0
        AirY += 1
    print(shipPart)
    for i in allRandomShipsCoords:
        if sorted(tuple(i)) == sorted(tuple(shipPart)):
            shinkShipCount += 1
            for i in shipPart:
                tableAirBomb[i[0]][i[1]] = " S "
                table[i[0]][i[1]] = " S "
    return shinkShipCount


def AirBombGame():
    shinkShipCount = 0
    allRandomShipsCoords = placeRandomShips()
    global AIRBOMBLEFT
    print("A számítógép elhelyezte az öt hajóból álló flottát, kezdődhet a játék!" )
    print()
    print("q = Kilépés")
    print()
    print("A légitámadásból", AIRBOMBLEFT-1, "bombád maradt.")
    table_draw(table)
    coord = [0,0]
    AirY = 0
    AirX = 0
    i = 0
    while i <= AIRBOMBLEFT-1:
        coord = inputCoord()
        AirY = coord[0]
        AirX = coord[1]
        table_draw(tableAirBomb)
        if AirY == 10 or AirX == 10:
            print("Kilépés..")
            break
        if table[AirX][AirY] == " H ":
            table[AirX][AirY] = " T "
            tableAirBomb[AirX][AirY] = " T "
            shinkShipCount = sink(AirY,AirX,allRandomShipsCoords,shinkShipCount)
            if shinkShipCount == SHIPFLOTTLENGTH:
                break
            table_draw(tableAirBomb)
            print("elsűlyeszett hajók száma:", shinkShipCount)
            print("Talált!")
            print()
            print("q = Kilépés")
            print()
            print("A légitámadásból", AIRBOMBLEFT-i, "bombád maradt.")
        elif tableAirBomb[AirX][AirY] == " O " or tableAirBomb[AirX][AirY] == " T ":
            print("Ide már lőttél!")
            print()
            print("q = Kilépés")
            print()
            print("A légitámadásból", AIRBOMBLEFT-i, "bombád maradt. Ne pazarolj!")
        elif table[AirX][AirY] == " _ ": 
            table[AirX][AirY] = " O "
            tableAirBomb[AirX][AirY] = " O "
            table_draw(tableAirBomb)
            print("Mellé...")
            print()
            print("q = Kilépés")
            print()
            print("A légitámadásból", AIRBOMBLEFT-i, "bombád maradt.")
        i += 1
    return shinkShipCount
        

shinkShipCount = AirBombGame()

table_draw(table)

if shinkShipCount > 0 and shinkShipCount < SHIPFLOTTLENGTH:
    print("Gratulálunk!", shinkShipCount, "hajót sűlyeszetél el a flottából!")
elif shinkShipCount == SHIPFLOTTLENGTH:
    print("Gratulálunk! A teljes flottát elsűlyesztetted!")
else:
    print("Legközelebbre több szerencsét kívánunk...")
print()
print("Viszlát!")

# Extra funkciók:
# Megoldás oop -vel hajó öntőforma irányokkal stb.
# webes verzió elkészítése

# Tervezett funkciók:
# hajók betűjele különböző legyen a táblán
# Játktípus választás, légitámadás, vagy hajócsata! Játék ismétlése, menü...

# Hibajavítás:
# ha két különböző halyót találok el anélkül hogy elsűlyednének, akkor a sűlyedés minden esetben meghiúsul. Megoldás, hogy azonosítom a hajókat.
# Bombák száma esetlen

# Dokumentáció:
# kommentelni a részeket, áttekinthetővé tenni a kódot.
# Mi okozott nehézséget: komplex bemeneti szűrő észítése, funkciók egymásba ágyazása, loopok egymásba ágyazása, műveleti sorrend