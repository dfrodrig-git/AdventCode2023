# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:34:53 2023

@author: CTW00905
"""

import json

test = False

if test :
    f=open('input4thTest.txt')
else :
    f=open('input4th.txt')

cards = json.load(f)
    
print(f'{cards}')


#puzzle 1
result=0
for x in cards.values() :
    cardsIn = [y for y in x[1] if y in x[0]]
    if len(cardsIn) == 0 :
        continue
    result = result + 2**(len(cardsIn)-1)
    
print(f'Day 4 puzzle 1: {result}')


class Card() :
    def __init__(self, card) :
        self.cardId = int(card[0])
        self.base = card[1][0]
        self.card = card[1][1]
        
        self.matching = [y for y in self.card if y in self.base]
        self.matchlen = len(self.matching)
        #print(f"cardId: {self.cardId}, {self.matching}")
        
        return None
    
def getNextCards(cardId):
    alot = 1
    for i in range(allCards[cardId].matchlen):
        #print(f'getting a next card: {cardId+1+i}')
        alot = alot + getNextCards(cardId+1+i)
    #print(f"cardId: {cardId} got {alot} cards!")
    return alot
    
import time
start_time = time.time()

allCards = {}
for card in cards.items() :
    c = Card(card)
    allCards[c.cardId] = c


result=0
for j in allCards :
    result = getNextCards(j) + result
print(f'Day 4 puzzle 2: {result}')
print("--- %s seconds ---" % (time.time() - start_time))
        

