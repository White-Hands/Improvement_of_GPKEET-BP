#!/usr/bin/python3
from charm.toolbox.PKEnc import PKEnc
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.hash_module import Hash
import time
from charm.toolbox.ecgroup import ECGroup,G


class ourscheme(PKEnc):
    def __init__(self, groupObj):
        print("#####################\nSetup:\n")
        PKEnc.__init__(self)
        global group
        group = groupObj
        global g
        g = group.random(G)
        para = {'g':g}
        print("\tpara:",para)
        global l1 
        l1 = group.serialize(group.random(G))
        
    def H1(self,M):
        return group.hash(M,ZR)
    
    def H2(self,M):
        return group.hash(self.H1(M),ZR)

    def H3(self,M):
        return group.serialize(M)+l1

    def H4(self,M):
        h4 = group.hash(M,ZR)
        h4 = group.serialize(h4)+l1+l1
        return h4

    def H5(self,M):
        h5 = group.hash(M,ZR)
        h5 = group.serialize(h5)
        return h5

    def H6(self,M):
        return group.hash(M,ZR)

    def bitand(self,a,b):
        return group.serialize(a)+group.serialize(b)
    
    def bitoplus(self,a,b):
        return bytes([x^y for x, y in zip(a,b)])

    def keygen_user(self):
        # x is private, g is public param
        
        x = group.random(); 
        Y = g ** x
        
        pk = {'pk':Y}
        sk = {'x':x}
        
        return (pk, sk)
    
    def keygen_group(self):
        #print("####################\nKeygen_group:\n")
        # x is private, g is public param
        
        s1 = group.random(); 
        s2 = group.random(); 
        s3 = group.random(); 
        s4 = group.random(); 
        
        gsk = {'s1':s1,'s2':s2,'s3':s3,'s4':s4}
        
        #print("\tgsk:",gsk)
        return gsk
    
    def join(self,gsk,pk):
        #print("####################\nJoin:\n")

        r = group.random()

        pkg1 = pk['pk']**gsk['s1']
        pkg2 = g**gsk['s2']

        skg1 = r*gsk['s3']
        skg2 = r*gsk['s4']
        
        pkg = {'pkg1':pkg1,'pkg2':pkg2}
        skg = {'skg1':skg1,'skg2':skg2}
        
        #print("\tpkg:",pkg)
        #print("\tskg:",skg)
        return (pkg,skg)

    def enc(self,pk, pkg,skg,  M=' '):
        xp = self.H1(M)
        yp = self.H2(M)

        xpskg1 = xp*skg['skg1']
        ypskg2 = yp*skg['skg2']

        t1 = group.random(ZR)
        t2 = group.random(ZR)

        C1 = pkg['pkg1']**t1

        C2 = g**t2

        C3 = self.bitoplus( self.H3(pk['pk']**t2), self.bitand(M,t1) ) 

        xpskg1_ypskg2=self.bitand( xpskg1, ypskg2)
        h = self.H5(xpskg1_ypskg2 )

        C4 = self.bitoplus( xpskg1_ypskg2 + h, self.H4( self.bitand( pkg['pkg2']**t2, C1)+ group.serialize(C2)+ C3 ))

        C5 = self.H6( self.bitand(C1, C2) + C3+ C4 + self.bitand(M, t1))

        C = [C1,C2,C3,C4,C5]

        #print('\n\tC=',C)
        return C  
       

    def decrypt(self, sk, C, pkg):
        #print("####################\nDecryption:\n")

        M_and_t1 = self.bitoplus(C[2],self.H3(C[1]**sk['x']))

        M = M_and_t1[:len(M_and_t1)//2]
        t1 = M_and_t1[len(M_and_t1)//2:]
        
        t1 = group.deserialize(t1)
        M = group.deserialize(M)


        check1 = pkg['pkg1']**t1
        #print("\tC1=",C[0])
        #print("\tpkg1**t1=",check1)
        if C[0]!=check1:
        #    print("\n-------- C1=pkg1**t1 ----------")
            return 0 
        
        '''
        print('Mr1',group.deserialize(Mr1))
        ################################
        print('Mr1_xp',Mr1_xp_yp)
        Mr1_xp_yp = self.bitoplus(C[4],self.H4(group.serialize(gpk['p2']**r2)+group.serialize(C[0])+group.serialize(C[1])+group.serialize(C[2])+C[3]))
        print('Mr1_xp',Mr1_xp_yp)
        Mr1=Mr1_xp_yp[:len(Mr1_xp_yp)//3]
        c52 = self.H4(group.serialize(gpk['p2']**r2)+group.serialize(C[0])+group.serialize(C[1])+group.serialize(C[2])+C[3])
        print('c52',c52)
        print('Mr1',group.deserialize(Mr1))
        '''
        ################################
        
        C6 = self.H6( self.bitand(C[0], C[1]) + C[2]+ C[3] + self.bitand(M, t1))

        #print("\n\tC5=",C[4])
        #print("\tH5(C1||C2||C3||C4||M||t1)=",C6)
        if C[4]!=C6:
            #print("\n-------- H5(C1||C2||C3||C4||M||t1)=C5 ----------")
            return 0
        M=group.decode(M)
        return M

    def aut(self, gsk):
        return gsk['s2']
    
    def test(self, C1, C2, gtd):

        # step a
        left1 = self.bitoplus(C1[3], self.H4( self.bitand(C1[1]**gtd, C1[0])+ (group.serialize(C1[1])+C1[2]) ))

        h1 = left1[2*len(left1)//3:]
        xpskg1 = left1[0:len(left1)//3]
        ypskg1 = left1[len(left1)//3:2*len(left1)//3]
        
        left2 = self.bitoplus(C2[3], self.H4( self.bitand(C2[1]**gtd, C2[0])+ (group.serialize(C2[1])+C2[2]) ))

        h2 = left2[2*len(left2)//3:]
        xpskg2 = left2[0:len(left2)//3]
        ypskg2 = left2[len(left2)//3:2*len(left2)//3]
        
        # step b
        if h1!= self.H5(xpskg1+ypskg1):
            return 0
        if h2 != self.H5(xpskg2+ypskg2 ):
            return 0
        

        # step c
        xpskg1 = group.deserialize(xpskg1)
        ypskg1 = group.deserialize(ypskg1)
        xpskg2 = group.deserialize(xpskg2)
        ypskg2 = group.deserialize(ypskg2)
        if (ypskg1/xpskg1) == (ypskg2/xpskg2):
            return 1
        else:
            return 0
        '''
        print(xp1_yp1)
        print(xp2_yp2)
        print('Mr1',group.deserialize(Mr1))
        print(xp1)
        print(yp1)
        print(xp2)
        print(yp2)
        print(float(xp1/yp1))
        print(float(xp2/yp2))
        print(xp1)
        print(yp1)
        print((xp1/yp1))
        print((xp2/yp2))
        '''
        
        #if (1000*xp1/yp1) == (1000*xp2/yp2):


if __name__ == "__main__":

    groupObj = ECGroup(709)

    our = ourscheme(groupObj)    
    
    print("####################\nKeygen_user:")
    (Apk,Ask) = our.keygen_user()
    
    print("\tsender's pk=",Apk)
    print("\tsender's sk=",Ask)
    
    (Bpk,Bsk) = our.keygen_user()
    
    print("\treceiver's pk=",Bpk)
    print("\treceiver's sk=",Bsk)
    
    print("####################\nKeygen_group:")
    gsk = our.keygen_group()
    print("\tgsk=",gsk)
    
    print("####################\nJoin:")
    (pkg, skg) = our.join(gsk,Apk)
    print("\tsender's pkg=",pkg)
    print("\tsender's skg=",skg)
    
    print("####################\nEncryption:\n")

    msg = ' '+input("\tinput the message: ")
    while len(msg)<17:
        msg=msg+' '
    msg=msg.encode(encoding='utf-8')
    M = group.encode(msg)

    print('\tplaintext =',group.decode(M))
     
    C = our.enc(Bpk,pkg,skg, M)
    
    print('\tciphertext =',C)
    
    print("####################\nDecryption:")
    result = our.decrypt(Bsk,C,pkg)
    
    print("\n\tdecryption results:",result)


    print("####################\nEncrypt another message:")
    msg = ' '+input("\tinput the message: ")
    while len(msg)<17:
        msg=msg+' '
    msg=msg.encode(encoding='utf-8')
        #msg = bytes(msg,encoding='utf-8')
    M = groupObj.encode(msg)
    print('\tplaintext =',group.decode(M))

    C2 = our.enc(Apk,pkg,skg,M)
    
    gtd = our.aut(gsk)
    testresult = our.test(C,C2, gtd)
    print("####################\nTest:")
    print('\tC1 =',C)
    print('\tC2 =',C2)
    print("\ntest result:")
    if testresult==1:
        print("\n----------- C = C' ---------------")
    else:
        print("----------- C != C' ---------------")
    

