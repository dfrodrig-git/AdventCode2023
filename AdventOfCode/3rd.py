# -*- coding: utf-8 -*-
import re

test = False

if test:
    with open("input3rdTest.txt", "r") as file :
        lines = file.readlines()

else : 
    with open("input3rd.txt", 'r') as file :
        lines = file.readlines()
    
ROWLEN=len(lines)
COLLEN=len(lines[0])

#find symbol
ps=re.compile('[^\d.\n]')
specialCharactersLoc=[]

#find number
pn=re.compile('\d+')
numbersLoc=[]

#find gear symbol
pg=re.compile('\*')
gearsLoc=[]

def checkSymbolInNeighbourhood(x,y, value, symbolsLoc):
    #print(f'checking {x},{y}:{value}')
    size = len(value)
    xmin = x-1 if x >0 else 0
    ymin = y-1 if y >0 else 0
    xmax = x+size+1 if x+size+1 <= COLLEN else COLLEN
    ymax = y+2 if y+2 <= ROWLEN else ROWLEN
    #print(f'xmin:{xmin},xmax:{xmax},ymin:{ymin},ymax:{ymax}')
    for a in range (xmin, xmax, 1) :        
        for b in range(ymin, ymax, 1) :
            #print(f'({a},{b})')
            if (a,b) in symbolsLoc :
                return (True, (a,b))
    return (False, (-1,-1))

for i, line in enumerate(lines) :
    for m in ps.finditer(line) :
        specialCharactersLoc.append((m.start(),i))

for i, line in enumerate(lines) :
    for m in pg.finditer(line):
        gearsLoc.append((m.start(), i))
        
for i, line in enumerate(lines) :
    for m in pn.finditer(line):
        numbersLoc.append((m.start(), i, m.group())) 



validNumbers = []
for number in numbersLoc :
    if checkSymbolInNeighbourhood(number[0],number[1], number[2], specialCharactersLoc)[0]  :
        validNumbers.append(int(number[2]))

gearNumbers = {}
for number in numbersLoc :
    gearVicinity = checkSymbolInNeighbourhood(number[0], number[1], number[2], gearsLoc) 
    gearCenterLoc = gearVicinity[1] 
    if gearCenterLoc not in gearNumbers:
        gearNumbers[gearCenterLoc] = set([])
    #print(f'checking {gearCenterLoc}, {number}  ')
    if gearVicinity[0] :
        #print(f'adding to symbol {gearCenterLoc} gear: {number} ')
        gearNumbers[gearCenterLoc].add(number)
    
    

print(f'1st part: {sum(validNumbers)} :: {validNumbers}')

#print(f'2nd part: {[gearsLoc]}')
#print(f'{gearNumbers}')
gears = [x[1] for x in gearNumbers.items() if len(x[1]) == 2]
print(f'Filtered: {gears}')
gearResult = 0
for x in gears :
    print(x)
    product = 1
    for y in x :
        print(int(y[2]))       
        product = int(y[2])*product
    print(product)
    gearResult = gearResult + product

print(f'2nd part result : {gearResult}')
