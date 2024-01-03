from charm.toolbox.ecgroup import ECGroup,G
from charm.toolbox.pairinggroup import PairingGroup,G1,ZR
from time import time

# import all three schemes 
from our_scheme import ourscheme
from ling2020 import ling2020
from GPKEETBP2022 import GPKEETBP



print("initiate the curves")
ecc = ECGroup(709)
p = PairingGroup("SS512")

M1 = ecc.random(G)
M2 = p.random(ZR)

print("Setup all schemes")
a = ourscheme(ecc)
b = GPKEETBP(ecc)
c = ling2020(p)

print("\n----------------the running time (ms)------------------\n")

print("  Scheme  \tKeygen_user\tKeygen_group\t    Join    \t    Enc    \t    Dec    \t    Test    ")

t0=time()
(Apk,Ask) = c.keygen_user()
t1=time()
gsk = c.keygen_group()
t2=time()
Apkg = c.join(gsk,Apk)
t3=time()
C = c.enc(Apkg,Ask,Apk,M2)
t4=time()
result = c.decrypt(Apkg,Ask,C)
t5=time()
gtd = c.aut(gsk)
testresult=c.test(C,C,gtd)
t6 = time()
print("Ling et al.\t%.6f \t%.6f \t%.6f \t%.6f \t%.6f \t %.6f "%(t1*1000-t0*1000,t2*1000-t1*1000,t3*1000-t2*1000,t4*1000-t3*1000,t5*1000-t4*1000,t6*1000-t5*1000))


t0=time()
(Apk,Ask) = b.keygen_user()
t1=time()
gsk = b.keygen_group()
t2=time()
gpk = b.join(gsk,Apk)
t3=time()
C = b.enc(gpk,Ask,Apk,M1)
t4=time()
result = b.decrypt(Ask,C,gpk,gsk)
t5=time()
gtd = b.aut(gsk)
testresult = b.test(C,C, gtd)
t6 = time()
print("GPKEET/BP\t%.6f \t%.6f \t%.6f \t%.6f \t%.6f \t %.6f "%(t1*1000-t0*1000,t2*1000-t1*1000,t3*1000-t2*1000,t4*1000-t3*1000,t5*1000-t4*1000,t6*1000-t5*1000))

t0 = time()
(Apk,Ask) = a.keygen_user()
t1 = time()
gsk = a.keygen_group()
t2 = time()
(pkg,skg) = a.join(gsk,Apk)
t3 = time()
C = a.enc(Apk,pkg,skg,M1)
t4 = time()
result = a.decrypt(Ask,C,pkg)
t5 = time()
gtd = a.aut(gsk)
testresult = a.test(C,C,gtd)
t6 = time()
print("our scheme\t%.6f \t%.6f \t%.6f \t%.6f \t%.6f \t %.6f "%(t1*1000-t0*1000,t2*1000-t1*1000,t3*1000-t2*1000,t4*1000-t3*1000,t5*1000-t4*1000,t6*1000-t5*1000))


