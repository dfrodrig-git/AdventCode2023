# -*- coding: utf-8 -*-





def getInput(test = False) :
    if test :
        f=open('input9thTest')
    else :
        f=open('input9th')

    #p = re.compile('[\dA-Z]{3}')
    #nodes={}
    #path = ''
    x = []
    for line in f :
        data=list(map(int,line.split()))
        x.append(data)
        
    return x



    
def process( sequence ) :
    print("==================================================================")
    newSeqs=[sequence]
    while True :
        print(f"taking care of newSeqs : {newSeqs}")
        newSeq = list(map(lambda x: x[0]-x[1], zip(newSeqs[-1][1:], newSeqs[-1][0:-1])))
        print(f'newSeq: {newSeq}')
        newSeqs.append(newSeq)

        if len([ x for x in newSeq if x != 0]) ==0 :
            break
    
    print(f"New Seqs after running all: {newSeqs}")
    print("")
    
    a=0
    while len(newSeqs) > 1 :
        a=newSeqs.pop(-1)
        print(f'Popped: {a} from {newSeqs}')
        valueAppend=newSeqs[-1][-1]+a[-1]
        print(f'Appending: {valueAppend} to {newSeqs[-1]}')
        newSeqs[-1].append(newSeqs[-1][-1]+a[-1])

    #sequence.append( newSeqs[-1][-1]+sequence[-1])
    print("------------------------------------------------------------------")
    print("")
    
    return sequence


    
def processBackwards(sequence) :
    print("==================================================================")
    newSeqs=[sequence]
    while True :
        print(f"taking care of newSeqs : {newSeqs}")
        newSeq = list(map(lambda x: x[0]-x[1], zip(newSeqs[-1][1:], newSeqs[-1][0:-1])))
        print(f'newSeq: {newSeq}')
        newSeqs.append(newSeq)

        if len([ x for x in newSeq if x != 0]) ==0 :
            break
    
    print(f"New Seqs after running all: {newSeqs}")
    print("")
    
    a=0
    while len(newSeqs) > 1 :
        a=newSeqs.pop(-1)
        print(f'Popped: {a} from {newSeqs}')
        valueInsert=newSeqs[-1][0]-a[0]
        print(f'Inserting: {valueInsert} to {newSeqs[-1]}')
        #newSeqs[-1].append(newSeqs[-1][-1]+a[-1])
        newSeqs[-1].insert(0, valueInsert)

    #sequence.append( newSeqs[-1][-1]+sequence[-1])
    print("------------------------------------------------------------------")
    print("")
    
    return sequence

result = 0
for a in getInput() :
    x = processBackwards(a)[0]
    result += x
    print(f"nextValue for {a} : {x}. Current total = {result}")
    
    
    