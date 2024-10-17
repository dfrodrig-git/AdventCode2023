# -*- coding: utf-8 -*-

from collections import Counter
import functools


def getInput(test = False) :
    if test :
        f=open('7thTestInput')
    else :
        f=open('7thinput')

    
    x=[]
    for line in f :
        #print(f'Appending: {line} ')
        x.append(line.split())
        #print(f'Updated: {x}')

    return x

listLabels ='A,K,Q,J,T,9,8,7,6,5,4,3,2'
dictLabels = {}
for i, a in enumerate(listLabels.split(',')) :
    dictLabels[a] = 12-i
    

class Hand() :
    def __init__(self, hand, bid) :
        self.bid = int(bid)
        self.hand = hand
        self.handCounter = Counter(hand)

        #self.strenghts = sum([dictLabels[x[0]]*x[1] for x in list(self.handCounter)])
        
        self.handType = self._handType()
    
    ''' 
    def higherThan(self,otherHand) :
        if self.handType < otherHand.handType :
            return -1
        
        for x in zip(otherHand.hand, self.hand) :
            if x[0] < x[1] :
                return 1
        
        return -1
        
        #if self.strenghts > otherHand.strenghts :
        #    return True
    '''     
        
    def _handType(self) :
        
        distribution=sorted(self.handCounter.values())
        
        if distribution == [5] :
            return 7
        if distribution == [1,4] :
            return 6
        if distribution == [2,3] :
            return 5
        if distribution == [1,1,3]:
            return 4
        if distribution == [1,2,2] :
            return 3
        if distribution == [1,1,1,2] :
            return 2
        return 1
    
    def __str__(self) :
        return f"{self.hand} :: {self.bid}"
    def __repr__(self) :
        return f"{self.hand} :: {self.bid}"

def rank(a,b):
    #print(f"comparing {a}, {b}")
    if a.handType > b.handType :
        return 1
    
    if a.handType < b.handType :
        return -1
    
    for x in zip(a.hand, b.hand) :
        #print(f"comparing: {x},: {dictLabels[x[0]]} to {dictLabels[x[1]]}")
        if dictLabels[x[0]] > dictLabels[x[1]] :
            return 1
        if dictLabels[x[0]] < dictLabels[x[1]] :
            return -1
    
    return 0
    
        
    
                
hands = [Hand(x[0], x[1] ) for x in getInput(test=False)]
print(f"Hands: {hands}")

sortedHands = hands.sort(key=functools.cmp_to_key(rank) )

print(f"sortedHands: {sortedHands}")

handsRanking = list(zip(hands, list(range(1, len(hands)+1))))
print(f"handsRanking: {handsRanking}    ")

result = sum(map(lambda x : x[0].bid*x[1], handsRanking))

print(f'result: {result}')

    
          


    

    