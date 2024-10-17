# -*- coding: utf-8 -*-



import re

test = False

if test :
    f=open('input5thTest.txt')
else :
    f=open('input5th.txt')

seedList = []
productionMap = {}

p = re.compile('[a-z\-]* map')

stage = ''
for line in f :
    #print(f'Checking line: {line}: len{len(line)} ')
    if len(line) <2 :
        continue
    if line.startswith("seeds") :
        a = line.split(" ")
        seedList = list(map(int, a[1:]))
        continue
    else :
        a = p.findall(line)
        if len(a) > 0 :
            stage = a[0][:len(a)-5]
            productionMap[stage] = []
        else :
            a=list(map(lambda x:int(x), line.split(" ")))
            productionMap[stage].append(a)

    




def doMap( x, stepMap) :
    #print(f'getting x for {stepMap} ')
    result = x
    
    for numberMap in stepMap :
        if numberMap[1] <= x < numberMap[1]+numberMap[2] :
            result = numberMap[0]+x-numberMap[1]
    return result


#productionMapPaths

def goToLocation( x ):
    #return functools.reduce(doMap,  productionMap )
    for step in ['seed-to-soil',
                 'soil-to-fertilizer',
                 'fertilizer-to-water',
                 'water-to-light',
                 'light-to-temperature',
                 'temperature-to-humidity',
                 'humidity-to-location'
                 ] :
        #if (x,step) in productionMapCache :
            #x = productionMapCache[(x,step)]
        #else :
            #key=x
            x = doMap(x, productionMap[step])
            #productionMapCache[(key,step)] = x
    return x
    
import time
start_time = time.time()

resultLocations = []    
for seed in seedList :
    seedLocation=goToLocation(int(seed))
    #print(f'Getting seed Location: #{seed} : {seedLocation} ')
    resultLocations.append(seedLocation)


print("In: --- %s seconds ---" % (time.time() - start_time))
print(f'Exercise 1 result test:{test} 35: {min(resultLocations)}')    



#def mapRange( ranges, mapRef ):
    

def mapFunction( item, mapRef ) :
    #print(f'Checking {item} for {mapRef}')
    for rangeKey, rangeValue in ranges[mapRef].items() :
        #print(f'validating if {item} in {rangeKey}')
        if item in rangeKey :
            #print(f'yes!')
            return rangeValue+item
    return item
        
start_time = time.time()
''' 
resultLocations=[]
for xr in map(lambda x,y: range(x,x+y),seedList[0::2], seedList[1::2]) :
    print(f'Computing seeds: {len(xr)}')
    start_time = time.time()

    for seed in xr[:1000000] :
        seedLocation=goToLocation(int(seed))
        resultLocations.append(seedLocation)
    
    print("In: --- %s seconds ---" % (time.time() - start_time))
''' 
seedRanges =map(lambda x,y: range(x,x+y),seedList[0::2], seedList[1::2]) 

    
result = [] #newSeedList
for mapRef in ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 
               'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location'] :
    print(f'Computing seeds: {len(result)}')
    start_time = time.time()
    result = [mapFunction(x, mapRef) for x in result] 
    print(f'Got {result} for {mapRef}')
    print("In: --- %s seconds ---" % (time.time() - start_time))

print(f'{result}')
    
print(f'Exercise 2 result test:{test} 46: {min(result)}')    


print('Exercise 2 : new -----------------------------------------------------')
_maxRanges = 100#4294967296
ranges={}
for k, v in productionMap.items() :
    ranges[k] = {}
    for a in v :
        tmp_range=range(a[1],a[1]+a[2])
        add_on = a[0]-a[1]
        ranges[k][tmp_range] = (add_on, (a[0],a[0]+a[2]))

#Missing Ranges
for k,v in ranges.items() :
    print(f'Checking Ranges for {k}')
    tmp_r = sorted(v, key = lambda x:x.start)
    check=zip(tmp_r, tmp_r[1:])
    a=list(map(lambda x: (x[0].stop - x[1].start, x[0].stop, x[1].start) , check))
    filtered=[x for x in a if (x[0] != 0)]
    print(f'{filtered}')
    for missingRange in filtered:
        print(f'will add Range {range(missingRange[1], missingRange[2])} to {k}')
        ranges[k][range(missingRange[1], missingRange[2])]=(0, (missingRange[1], missingRange[2]))
    curMax = max([x.stop for x in tmp_r])
    if curMax < _maxRanges :
        ranges[k][range(curMax, _maxRanges)]=(0, (curMax, _maxRanges))
    curMin = min([x.start for x in tmp_r])
    if curMin > 0 :
        ranges[k][range(0, curMin)]=(0, (0, curMin))

#Reduce
def reduceRanges(sourceRange, stepRef) :
    print(f'reducing: {sourceRange} for {stepRef}')
    rangeKeys = []
    appendRange = False
    for rangeKey, rangeValue in sorted(ranges[stepRef].items(), key=lambda x:x[0].start ) :
        print(f'checking {sourceRange} in: {rangeKey}, {rangeValue}. Append Range: {appendRange}')
        if sourceRange.start in rangeKey and sourceRange.stop in rangeKey :
            rangeKeys.append(range(sourceRange.start+rangeValue[0], sourceRange.stop + rangeValue[0]))
            appendRange = False
            continue
        if sourceRange.start in rangeKey :
            rangeKeys.append(range(sourceRange.start+rangeValue[0], rangeKey.stop+rangeValue[0]))
            appendRange = True
            continue
        if sourceRange.stop in rangeKey :
            rangeKeys.append(range(rangeKey.start+rangeValue[0], sourceRange.stop+rangeValue[0]))
            appendRange = False
            continue
        if appendRange == True :
            rangeKeys.append(range(rangeKey.start+rangeValue[0],rangeKey.stop+rangeValue[0]))
        #print(f'new rangeKeys {rangeKeys}')
    
    print(f'Returning: {set(rangeKeys)}')
    return set(rangeKeys)

srcRanges =map(lambda x,y: range(x,x+y),seedList[0::2], seedList[1::2])

for mapRef in ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 
               'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location'] :
    print(f'-----------------------------------------------------------------')
    srcRanges = [x for y in map(lambda x: reduceRanges(x, mapRef), set(srcRanges))  for x in y]
    print(f'new srcRanges for {mapRef}: {set(srcRanges)}')

result = [x.start for x in srcRanges]

print(f'Exercise 2 result test:{test} 46: {min(result)}')    




#what are the ranges for a given association
class RangeMap() :
    def __init__(self, category, ran):
        self.category = category
        self.minD, self.maxD = ran[0]
        self.minS, self.maxS = ran[1]
    
    def splitDestinationRange(self,a) :
        
        lowRan = [(self.minD, self.minD + a-self.minS) ,  (self.minS, a)]
        highRan = [(self.maxD-(self.maxS-a)  ,self.maxD), (a, self.maxS)]
        
        return RangeMap(self.category, lowRan), RangeMap(self.category, highRan)
        
    

def createAllRanges(rangeMap) :
    rangeMap.sort(key=lambda x:x[1])
    cur = 0
    result = []
    for d, s, delta in rangeMap :
        if cur < s :
            newRange = [(cur, cur+s-1), (cur, cur+s-1), s-cur-1]
            result.append(newRange)
            result.append([(d,d+delta-1),(s,s+delta-1),delta])
            cur = s+delta
        else : 
            result.append([(d,d+delta-1),(s,s+delta-1),delta])
            cur = s + delta

    return result

rangeList={}
for k,v in productionMap.items() :
    print(f'for {k} we got:')
    ranges=createAllRanges(v)
    rangeList[k] = ranges
    print(f'{ranges}')
    #for ran in ranges :
    #    rangeMap = #RangeMap(k, ran)
    #    #rangeList[k].append(rangeMap)

ranges={}
for k, v in productionMap.items() :
    ranges[k] = {}
    for a in v :
        tmp_range=range(a[1],a[1]+a[2])
        add_on = a[0]-a[1]
        ranges[k][tmp_range] = add_on

#x = (destination, source, rangen)
#def nextCategoryValue(x) :
    
'''
resultLocations = []

seedLocationCache = []
import time

for xr in map(lambda x,y: range(x,x+y),seedList[0::2], seedList[1::2]) :
    print(f'Computing seeds: {len(xr)}')
    start_time = time.time()

    for seed in xr :

        if seed in seedLocationCache :
            continue
        seedLocation=goToLocation(int(seed))
        #print(f'Getting seed Location: #{seed} : {seedLocation} ')
        resultLocations.append(seedLocation)
        seedLocationCache.append(seed)

    print("In: --- %s seconds ---" % (time.time() - start_time))

print(f'Exercise 2 result test:{test}: {min(resultLocations)}')    

'''