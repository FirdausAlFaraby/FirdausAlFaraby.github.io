#Produce sublist (subset allowing duplicates)
def sublist(s):
    S=len(s)
    sublist=[]
    for i in range(2**S-1): #produce binary structure
        b=bin(i)
        B=list(b)[2:]
        while len(B)<S:
            B=['0']+B
        #print(B)
        l=[]
        for i in range(S): #overlay binary structure on the list to include or not
            if B[i]=='0':
                l.append(s[i])
        if l not in sublist:
            sublist.append(l)
    sublist.sort(key=len)
    return sublist

#Produce permutations of a sublist
import itertools
def order(s): 
    S=list(set((itertools.permutations(s))))
    return S

#Convert number bases
def baseb(n,b): 
    f=n//b
    r=n%b
    if n==0:
        return '0'
    elif f==0:
        return str(r)
    else:
        return baseb(f,b)+str(r)

#Produce permutations of the four basic operations of length n    
def subop(n): 
    operation={0:'+',1:'-',2:'*',3:'/'}
    subop=[]
    for i in range(4**n): #Produce quartenary structure
        b=list(baseb(i,4))
        while len(b)<n:
            b=['0']+b
        l=[]
        for i in range(n): #Overlay quartenary structure
            l.append(operation[int(b[i])])
        subop.append(l)
    subop.sort(key=len)
    return subop

#Produce bracket structures of length 'order'
import itertools
def brackets(order): 
    if order==1: 
        return [0]
    elif order==2:
        return [[0,0]]
    else: #combine all structures of lower orders that add up to 'order' on the left and right of each other
        a=[]
        for i in range(1,(order//2)+1):
            for structure in brackets(order-i):
                for costructure in brackets(i):
                    a.extend([[structure,costructure],[costructure,structure]]) 
        A=list(a for a,_ in itertools.groupby(a))
        return A

def countdown(s):
    '''
    list s: list of numbers
    '''
    keep={}                                                           #start a dictionary for computation:result
    for subl in sublist(s):                                           #choose a subset of the list
        for perm in order(subl):                                      #choose a permutation of the subsets
            for opset in subop(len(perm)-1):                          #choose an operation permutation
                for brak in brackets(len(perm)):                      #choose a bracket structure
                    h=str(brak).replace('[','(').replace(']',')')     #overlay all the choices, and remove whitespace
                    for i in perm:
                        p=h.find('0')
                        h=h[:p]+str(i)+h[p+1:]
                    for j in opset:
                        q=h.find(',')
                        h=h[:q]+j+h[q+1:]
                    h=''.join(h.split())
                    #print(h)
                    
                    try:                                              #division by zero error handling
                        result=round(eval(h),2)
                        if result not in keep.values():
                            keep[h]=result
                    except ZeroDivisionError:
                        pass
                    #print(str(h)+'='+str(result))      
    '''
    temp=[]                                                           #remove duplicate results and choose simplest computation
    res={}
    for key,val in keep.items():
        if val not in temp:
            temp.append(val)
            res[key]=val    
    '''
    return keep

def check(n,s,list_type): #Produce list of all possible results
    '''
    int n: integer target to check
    list s: list of numbers
    str list_type: checks in resulting list consisting of 'natural', 'integer', 'real'
    '''

    dic=countdown(s)
    
    dic=dict(sorted(dic.items(),key=lambda item:item[1]))                    #sort based on result
    if list_type=='natural' or 'integer':                                    #choose result space
        dic={key:value for key,value in dic.items() if type(value)==int}
        if list_type=='natural':
            dic={key:value for key,value in dic.items() if value>0}
    lis=list(dic.values())
    
    if n in lis:
        print('Yes it can be done!')
        print(f'{list(dic.keys())[list(dic.values()).index(n)]}={n}')
    else:
        close={i:abs(n-i) for i in lis}
        c=min(close,key=close.get)
        print(f'No, it is impossible! {n} cannot be computed from {s} using the four basic operations')
        print(f'The closest we can get is {c} from {list(dic.keys())[list(dic.values()).index(c)]}.')
    return (lis,dic,s)

def check_other(n,dic,s): #Check for other results using same list without running countdown again
    '''
    int n: other number target to check
    dict dic: dictionary returned from check()
    list s: list of numbers
    '''
    lis=list(dic.values())
    if n in lis:
        print('Yes it can be done!')
        print(f'{list(dic.keys())[list(dic.values()).index(n)]}={n}')
    else:
        close={i:abs(n-i) for i in lis}
        c=min(close,key=close.get)
        print(f'No, it is impossible! {n} cannot be computed from {s} using the four basic operations.')
        print(f'The closest we can get is {c} from {list(dic.keys())[list(dic.values()).index(c)]}.')

def main():
    f=check(574,[3,2,5,4,10],'natural')
    check_other(154,f[1],f[2])

if __name__=='__main__':
    main()