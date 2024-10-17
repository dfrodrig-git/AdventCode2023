# -*- coding: utf-8 -*-

from math import prod 

def getInput(test = False) :
    if test :
        f=open('6thTestInput')
    else :
        f=open('6th input')

    
    x=[]
    for line in f :
        x.append(  list(map(int,line.split()[1:])))
     
    timeDist = list(zip(x[0], x[1]))
    
    return timeDist


def getDifferences(timeDistance) :
    time, distance = timeDistance
    #print(f"checking {time, distance}")
    ways = 0
    for pressedTime in range(time):
        pressedDistance = pressedTime*(time-pressedTime)
        if pressedDistance > distance :
            #print(f"pressing for {pressedTime}, ran:{pressedDistance} ")
            ways +=1
            
    #print(f"found : {ways} to win ")
    return ways


def resolve(test = False) :
    
    return prod(map(getDifferences, getInput(test))) 
        

def testResolve() :
    result = resolve(True)
    if result == 288 :
        print(f"all good {result})")
    else :
        print(f"all bad {result}")
          
testResolve()

print(f"Final result: {resolve()}")

print(f"Test result 2 : {prod(map(getDifferences, [(71530, 940200)]))}")
40828492

233101111101487
print(f"result 2 : {prod(map(getDifferences, [(40828492, 233101111101487)]))}")