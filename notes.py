# Author : BATALI OUALID 
# MASTER MCSC2 - 2019/2020
# PROJET CRYPTOGRAPHIE AVANCEE 
# Ce script a besoin de quelques modifications ! 


def list2int(alist):
    return int('0b' + ''.join(alist),2)

def int2list(n):
    return list(bin(n))[2:]

def rblock(m,r):
    m = str(bin(m))
    m = m[2:] # deleting the prefix 0b
    mpadded = m + '1' + '0' * (r - (len(m) + 1) % r )
    rblocks = []
    for i in range(0,len(mpadded),r):
        rblocks.append(mpadded[i:i+r])
    return rblocks

def abso(m,rr):
    rblocks = rblock(m,rr)
    state = ['0' * 80]
    for i in range(len(rblocks)):
        m = list2int(rblocks[i])
        r = list2int(state[:8])
        cliste = state[8:]
        mr = r ^ m
        state = int2list(mr) + state[8:]
        state = PI(state)
    return state
def Hash(m,r):
    state = abso(m,r)
    output = []
    for _ in range(10):
        output = output + state[:r]
        state = PI(state)
    output = list2int(output)
    return output

def PI(state):
    # R = 45 for SPONGENT-88
    # Convert the list state to the int 
    for i in range(45):
        state = InvlCounter(i) << 80 ^ list2int(state) ^ lCounter(i)
        paddstate = ['0' for _ in range(88 - len(int2list(state)))]
        state = sBoxLayer(paddstate + int2list(state))
        state = pLayer(state)
    return state
 # the article doesnt explain how the LFSR depends on b.
def lCounter(i):
    """ lCounter is a state of an LSFR """
    m = 0b000101
    for _ in range(i):
        m = (m >> 1) | (((m & 1) ^ ((m & 2) >> 1)) << 5)        
    return m
def InvlCounter(i):
    m = lCounter(i)
    s = ((m&1)<<5)|((m&2)<<3)|((m&4)<<1)|((m&8)>>1)|((m&16)>>3)|((m&32)>>5)
    return s 

def sBoxLayer(stat):
    SBOX = {'0000':'1110', '0001':'1101', '0010':'1011', '0011':'0000',
            '0100':'0010', '0101':'0001', '0110':'0100', '0111':'1111',
            '1000':'0111','1001':'1010', '1010':'1000', '1011':'0101',
            '1100':'1001', '1101':'1100','1110':'0011', '1111':'0110'}
    b = len(stat)
    newstate = ''
    for i in range(0,b+1,4):
        if i+4 < b+1:
            elt = ''.join(stat[i:i+4])
            newstate += SBOX[elt]
    return list(newstate)

def pLayer(state):
    newstate = state 
    b = len(state)
    def Pb(j,b):
        if j == b-1 :
            return b - 1
        return (j * b // 4) % (b - 1)
    for j in range(b):
        newstate[j] = state[Pb(j,b)]
    return newstate

