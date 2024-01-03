#!/usr/bin/python3
from charm.toolbox.PKEnc import PKEnc
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.hash_module import Hash
import time
from charm.toolbox.ecgroup import ECGroup,G


class ling2020(PKEnc):
    def __init__(self, groupObj):
        print("#####################\nSetup:\n")
        PKEnc.__init__(self)
        global p
        p = groupObj
        global g
        g = p.random(G1)
        para = {'g':g}
        print("\tpara:",para)
        global l1 
        l1 = p.serialize(p.random(G1))
        
    def H1(self,M):
        return p.hash(M,G1)
    
    def H2(self,M):
        return p.hash(M,G1)

    def H3(self,M):
        return p.serialize(M)+l1

    def H4(self,M):
        h4 = p.hash(M,ZR)
        return h4

    def bitand(self,a,b):
        return p.serialize(a)+p.serialize(b)
    
    def bitoplus(self,a,b):
        return bytes([x^y for x, y in zip(a,b)])

    def keygen_user(self):
        ##print("####################\nKeygen_user:\n")
        # x is private, g is public param
        
        x = p.random(); 
        Y = g ** x
        
        pk = {'pk':Y}
        sk = {'x':x}
        
        return (pk, sk)
    
    def keygen_group(self):
        #print("####################\nKeygen_group:\n")
        # x is private, g is public param
        
        s1 = p.random(); 
        s2 = p.random(); 
        
        gsk = {'s1':s1,'s2':s2}
        
        #print("\tgsk:",gsk)
        return gsk
    
    def join(self,gsk,pk):
        #print("####################\nJoin:\n")


        pkg1 = pk['pk']**gsk['s1']
        pkg2 = g**gsk['s2']

        
        pkg = {'pkg1':pkg1,'pkg2':pkg2}
        
        #print("\tpkg:",pkg)
        return pkg

    def enc(self, pkg, sk ,pk ,M):
        #print("####################\nEncryption:\n")



        t1 = p.random(ZR)
        t2 = p.random(ZR)

        C1 = pkg['pkg1']**t1

        C2 = self.H1(M)**( sk['x'] * t1) * self.H2( pkg['pkg2'] **t2)

        C3 = g**t2

        C4 = self.bitoplus( self.H3(pk['pk']**t2), self.bitand(M,t1) ) 

        C5 = self.H4( self.bitand(C1, C2) + p.serialize(C3)+ C4 + self.bitand(M, t1))
        '''
  #      #print('r1',r1)
        ##############################
        #print('Mr1',M**r1)
        global r2
        '''
        #########################
        '''
        ########################
        c51 =self.bitand(M**r1,xp)+group.serialize(yp)
        #print(c51)
        c52 = self.H4(group.serialize(gpk['p2']**r2)+group.serialize(c1)+group.serialize(c2)+group.serialize(c3)+c4)
        #print(c52)
        c5 = self.bitoplus(c51,c52)
        
        '''
        ########################
        C = [C1,C2,C3,C4,C5]

        #print('\n\tC=',C)
        return C

    def decrypt(self, pkg,  sk, C):
        #print("####################\nDecryption:\n")

        M_and_t1 = self.bitoplus(C[3],self.H3(C[2]**sk['x']))

        M = M_and_t1[:len(M_and_t1)//2]
        t1 = M_and_t1[len(M_and_t1)//2:]
        
        t1 =p.deserialize(t1)
        M = p.deserialize(M)


        '''
        #print("M",M)
        #print("r1",r1)
'''
        check1 = pkg['pkg1']**t1
        #print("\tC1=",C[0])
        #print("\tpkg1**r1=",check1)
        if C[0]!=check1:
            return 0
            #print("\n-------- C1=pkg1**t1 ----------")
        
        
        C6 = self.H4( self.bitand(C[0], C[1]) + p.serialize(C[2])+ C[3] + self.bitand(M, t1))

        #print("\n\tC5=",C[4])
        #print("\tH4(C1||C2||C3||C4||M||r1)=",C6)
        if C[4]!=C6:
            return 0
            #print("\n-------- H4(C1||C2||C3||C4||M||r1)=C5 ----------")
        #M=p.decode(M)
        return M

    def aut(self, gsk):
        return gsk['s2']

    def test(self, C1, C2, gtd):
        
        left = pair(C1[0], C2[1]/ self.H2(C2[2]**gtd))
        right = pair(C2[0], C1[1]/ self.H2(C1[2]**gtd))

        '''
            #print("\tleft=",left)
            #print("\tright=",right)
        '''
        if left==right:
            return 1
        else:
            return 0 
            
if __name__ == "__main__":

    groupObj = PairingGroup("SS512")

    scheme = ling2020(groupObj)    

    print("####################\nKeygen_user:\n")
    (Apk,Ask) = scheme.keygen_user()
    print("\tsender's pk:",Apk)
    print("\tsender's sk:",Ask)
    (Bpk,Bsk) = scheme.keygen_user()
    print("\trecevier's pk:",Apk)
    print("\trecevier's sk:",Ask)

    print("####################\nKeygen_group:\n")
    gsk = scheme.keygen_group()
    print("\tgsk=",gsk)

    print("####################\nJoin:\n")
    Apkg = scheme.join(gsk,Apk)
    print("\tsender's group pk=",Apkg)

    print("####################\nEncryption:\n")
    msg = int(input("\tinput the message: "))
    M = groupObj.init(ZR,msg)

    C = scheme.enc(Apkg,Ask,Bpk,M)
    print("\tcipertext=",C)

    print("####################\nDecryption:\n")
    result = scheme.decrypt(Apkg,Bsk,C)


    print("\n\tdecryption results:",result)

    print("####################\nAnother Encryption:\n")
    msg = int(input("\tinput the message: "))
    M = groupObj.init(ZR,msg)
    C2 = scheme.enc(Apkg,Ask,Bpk,M)
    
    gtd = scheme.aut(gsk)
    print("####################\nTest:\n")
    testresult=scheme.test(C,C2,gtd)
    print("\nC=",C)
    print("\nC'=",C2)
    print("\ntest result:")
    if testresult==1:
        print("\n----------- C = C' ---------------")
    else:
        print("----------- C != C' ---------------")
