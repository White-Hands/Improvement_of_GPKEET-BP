#!/usr/bin/python3
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.hash_module import Hash
import time
from charm.toolbox.ecgroup import ECGroup,G

def ecctest(curve):
    p=ECGroup(curve)
    print(curve)
    x = p.random(G)
    a = p.random(ZR)
    b = p.random(ZR)
    pk1 = x**a
    pk2 = x**b
    if pk2**a == pk1**b:
        print("succeed!")
    starttime = time.time()
    for i in range(0,1000):
        x**a
    print(pk1)
    totaltime= time.time()-starttime
    print("mul in G:        ",totaltime)
    
    starttime = time.time()
    for i in range(0,1000): 
        hash_a = p.hash(a,ZR)
    totaltime= time.time()-starttime
    print("m2p in ZR:       ",totaltime)
    
    starttime = time.time()
    for i in range(0,1000): 
        hash_a = p.hash(a,G)
    totaltime= time.time()-starttime
    print("m2p in  G:       ",totaltime)
    
    starttime = time.time()
    for i in range(0,1000):
        hash_b = p.encode(b'12345678901234567')
    endtime = time.time()
    print(" encode :        ",endtime-starttime,"ms")

    starttime = time.time()
    for i in range(0,1000):
        text = p.decode(hash_b)
    endtime = time.time()
    print(" decode :        ",endtime-starttime,"ms")

    starttime = time.time()
    for i in range(0,1000):
        hash_b = p.serialize(b)
    endtime = time.time()
    print(" serialize ZR :  ",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        b = p.deserialize(hash_b)
    endtime = time.time()
    print(" deserialize ZR :",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        hash_b = p.serialize(x)
    endtime = time.time()
    print(" serialize G :   ",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        hash_bb = bytes([x^y for x, y in zip (hash_b,hash_b)])
    endtime = time.time()
    print(" oplus :         ",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        x = p.deserialize(hash_b)
    endtime = time.time()
    print(" deserialize G : ",endtime-starttime,"ms")
    
def pairingtest(curve):
    p = PairingGroup(curve)
    x = p.random(G1)
    y = p.random(G2)
    a = p.random(ZR)
    b = p.random(ZR)
    print(curve)
    if pair(x**a,y**b) == pair(x**b,y**a):
        print("succeed!")


    print(x)
    starttime = time.time()
    for i in range(0,1000):
        exy=pair(x,y)
    endtime = time.time()
    print("     pairing:",endtime-starttime,"ms")
    starttime = time.time()
    for i in range(0,1000):
        x**a
    endtime = time.time()
    print(" G1 exponent:",endtime-starttime,"ms")
    starttime = time.time()
    for i in range(0,1000):
        y**b
    endtime = time.time()
    print(" G2 exponent:",endtime-starttime,"ms")
    starttime = time.time()
    for i in range(0,1000):
        exy**a
    endtime = time.time()
    print(" GT exponent:",endtime-starttime,"ms")

    starttime = time.time()
    for i in range(0,1000):
        hash_a = p.hash(a,G1)
    endtime = time.time()
    print(" m2p in   G1:",endtime-starttime,"ms")
    Zr = Hash
    starttime = time.time()
    for i in range(0,1000):
        hash_b = Hash.hashToZr(b)
    endtime = time.time()
    print(" hz in    Zr:",endtime-starttime,"ms")

    starttime = time.time()
    for i in range(0,1000):
        hash_b = p.init(ZR,b)
    endtime = time.time()
    print(" init       :",endtime-starttime,"ms")

    starttime = time.time()
    for i in range(0,1000):
        hash_b = p.serialize(b)
    endtime = time.time()
    print("serialize ZR:",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        b = p.deserialize(hash_b)
    endtime = time.time()
    print("deserializeZ:",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        hash_b = p.serialize(x)
    endtime = time.time()
    print("serialize G1:",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        hash_bb = bytes([x^y for x, y in zip (hash_b,hash_b)])
    endtime = time.time()
    print(" oplus      :",endtime-starttime,"ms")
    
    starttime = time.time()
    for i in range(0,1000):
        x = p.deserialize(hash_b)
    endtime = time.time()
    print("deserial  G1:",endtime-starttime,"ms")
    
#timetest(int(input("curve")))
ecctest(709)
#ecctest(710)
pairingtest("SS512")
