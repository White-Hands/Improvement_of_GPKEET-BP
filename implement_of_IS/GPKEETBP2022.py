#!/usr/bin/python3
from charm.toolbox.PKEnc import PKEnc
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.hash_module import Hash
import time
from charm.toolbox.ecgroup import ECGroup,G


class GPKEETBP(PKEnc):
    
    def __init__(self, groupObj):
        print("#####################\nSetup:")
        PKEnc.__init__(self)
        global group
        group = groupObj
        global g
        g = group.random(G)
        para = {'g':g}
        print("\tpara:",para)
        global l1 
        l1 = group.serialize(group.random(G))
        
    def H0(self,M):
        return group.hash(M,ZR)

    def H1(self,M):
        return group.hash(self.H0(M),ZR)
    
    def H2(self,M):
        return group.hash(M,G)
    
    def H3(self,M):
        h3 = group.hash(M,ZR)
        h3 = group.serialize(h3)+l1
        return h3
    def H4(self,M):
        h4 = group.hash(M,ZR)
        h4 = group.serialize(h4)+group.serialize(h4)+group.serialize(h4)
        return h4
   
    def H5(self,M):
        return group.hash(M,ZR)
   
    def bitand(self,a,b):
        return group.serialize(a)+group.serialize(b)
   
    def bitoplus(self,a,b):
        return bytes([x^y for x, y in zip(a,b)])

   
    def keygen_user(self):
        # x is private, g is public param
        x = group.random(); 
        Y = g ** x
        pk = {'Y':Y}
        sk = {'x':x}

        return (pk, sk)
    
    def keygen_group(self):
        # x is private, g is public param
        s1 = group.random(); 
        s2 = group.random(); 
        gsk = {'s1':s1,'s2':s2}
        
        return gsk
    
    def join(self,gsk,pk):
        
        p1 = pk['Y']**gsk['s1']
        p2 = g**gsk['s2']
        gpk = {'p1':p1,'p2':p2}

        return gpk

    def enc(self,gpk, sk,pk,  M=' '):

       #while len(msg)<len(str(group.random(ZR))):
        #while len(msg)<group.bitsize():
        #    msg=msg+' '
        #msg = bytes(msg,encoding='utf-8')
        #M = msg
        xp = self.H0(M)
        yp = self.H1(M)
            #return 0 

        r1 = group.random(ZR)
        '''
  #      print('r1',r1)
        ##############################
        print('Mr1',M**r1)
        global r2
        '''
        #########################
        r2 = group.random(ZR)

        c1 = gpk['p1']**r1

        c2 = self.H2(M)**(sk['x']*r1)
        
        c3 = g**r2
        
        c4 = self.bitoplus(self.H3(pk['Y']**r2),self.bitand(r1,M))
        
        c5 = self.bitoplus( self.bitand(M**r1,xp) +group.serialize(yp), self.H4( group.serialize( gpk['p2']**r2) +group.serialize(c1) +group.serialize(c2) +group.serialize(c3) +c4))
        '''
        ########################
        c51 =self.bitand(M**r1,xp)+group.serialize(yp)
        print(c51)
        c52 = self.H4(group.serialize(gpk['p2']**r2)+group.serialize(c1)+group.serialize(c2)+group.serialize(c3)+c4)
        print(c52)
        c5 = self.bitoplus(c51,c52)
        
        '''
        ########################
        c6 = self.H5(group.serialize(c1)+group.serialize(c2)+group.serialize(c3)+c4+c5+group.serialize(M**r1))
        
        C = [c1,c2,c3,c4,c5,c6]

        return C

    def decrypt(self, sk, C, gpk,gsk):
        
        M_and_r1 = self.bitoplus(C[3],self.H3(C[2]**sk['x']))
        
        M = M_and_r1[len(M_and_r1)//2:]
        
        r1 = M_and_r1[:len(M_and_r1)//2]
        
        r1 = group.deserialize(r1)
        
        M = group.deserialize(M)
        '''
        print("M",M)
        print("r1",r1)
'''
        
        check1 = gpk['p1']**r1
        #print("\tc1=",C[0])
        #print("\tp1**r1=",check1)
        
        #if C[0]==check1:
        #    print("\tC1=p1**r1:")
        
        Mr1_xp_yp = self.bitoplus(C[4], self.H4( group.serialize(C[2]**gsk['s2']) +group.serialize(C[0]) +group.serialize(C[1]) +group.serialize(C[2]) +C[3]))
        
        Mr1=Mr1_xp_yp[0:len(Mr1_xp_yp)//3]
        
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
        c6 = self.H5(group.serialize(C[0])+group.serialize(C[1])+group.serialize(C[2])+C[3]+C[4]+Mr1)
        
        #print("\tc6=",C[5])
        #print("\tH5(C1||C2||C3||C4||C5||M**r1)=",c6)
        
        M=group.decode(M)
        
        return M


    def aut(self, gsk):
        return gsk['s2']

    def test(self, C1, C2, gtd):

        # step a
        xp1_yp1 = self.bitoplus(C1[4], self.H4( self.bitand(C1[2]**gtd, C1[0])+ self.bitand(C1[1], C1[2])+ C1[3] ))
        
        xp1 = group.deserialize(xp1_yp1[len(xp1_yp1)//3:2*len(xp1_yp1)//3])

        yp1 = group.deserialize(xp1_yp1[2*len(xp1_yp1)//3:])

        xp2_yp2 = self.bitoplus(C2[4], self.H4( self.bitand(C2[2]**gtd, C2[0])+ self.bitand(C2[1], C2[2])+ C2[3] ))
        
        xp2 = group.deserialize(xp2_yp2[len(xp2_yp2)//3:2*len(xp2_yp2)//3])

        yp2 = group.deserialize(xp2_yp2[2*len(xp2_yp2)//3:])


        # step b
        Mr1 = xp1_yp1[0:len(xp1_yp1)//3]
        c6 = self.H5(group.serialize(C1[0])+group.serialize(C1[1])+group.serialize(C1[2])+C1[3]+C1[4]+Mr1)
        if c6 != C1[5]:
            return 0
        
        Mr1 = xp2_yp2[:len(xp2_yp2)//3]
        c6 = self.H5(group.serialize(C2[0])+group.serialize(C2[1])+group.serialize(C2[2])+C2[3]+C2[4]+Mr1)
        if c6 != C2[5]:
            return 0

        # step c
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
        if (yp1/xp1) == (yp2/xp2):
            return 1
        else:
            return 0


if __name__ == "__main__":
    
    groupObj = ECGroup(709)
    
    el = GPKEETBP(groupObj)    
    #(public_key, secret_key) = el.keygen_user()
    
    print("####################\nKeygen_user:")
    (Apk,Ask) = el.keygen_user()
    
    print("\tsender's pk=",Apk)
    print("\tsender's sk=",Ask)
    
    (Bpk,Bsk) = el.keygen_user()
    
    print("\treceiver's pk=",Bpk)
    print("\treceiver's sk=",Bsk)
    
    print("####################\nKeygen_group:")
    gsk = el.keygen_group()
    print("\tgsk=",gsk)
    
    print("####################\nJoin:")
    gpk = el.join(gsk,Apk)
    print("\tsender's gpk=",gpk)
    
    print("####################\nEncryption:")
    msg = ' '+input("\tinput the message: ")
    while len(msg)<17:
        msg=msg+' '
    msg=msg.encode(encoding='utf-8')
        #msg = bytes(msg,encoding='utf-8')
    M = groupObj.encode(msg)
    print('\tplaintext =',group.decode(M))

    C = el.enc(gpk,Ask,Bpk,M)
    
    print('\tciphertext =',C)
    
    print("####################\nDecryption:")
    result = el.decrypt(Bsk,C,gpk,gsk)

    print("\tdecryption results=",result)

    print("####################\nEncrypt another message:")
    msg = ' '+input("\tinput the message: ")
    while len(msg)<17:
        msg=msg+' '
    msg=msg.encode(encoding='utf-8')
        #msg = bytes(msg,encoding='utf-8')
    M = groupObj.encode(msg)
    print('\tplaintext =',group.decode(M))

    C2 = el.enc(gpk,Ask,Bpk,M)
    
    gtd = el.aut(gsk)
    testresult = el.test(C,C2, gtd)
    print("####################\nTest:")
    print('\tC1 =',C)
    print('\tC2 =',C2)
    print("\ntest result:")
    if testresult==1:
        print("\n----------- C = C' ---------------")
    else:
        print("----------- C != C' ---------------")
    
 
    
    

    #cipher_text = el.encrypt(public_key)
    #decrypted_msg = el.decrypt(public_key, secret_key, cipher_text)    
    '''
    if decrypted_msg == msg:
        print("True")
    '''
