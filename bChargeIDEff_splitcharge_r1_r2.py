from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bChargeIDEff(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """

        


        _min="0."
        _max="10.0"
                

        N_bminus_PASS=self.dict_ymc["N_bminus_PASS"]
        N_bplus_PASS=self.dict_ymc["N_bplus_PASS"]
        N_bminus_FAIL=self.dict_ymc["N_bminus_FAIL"]
        N_bplus_FAIL=self.dict_ymc["N_bplus_FAIL"]

        #self.modelBuilder.doVar("r_pass[1, "+_min+" , "+_max+"]")
        #self.modelBuilder.doVar("r_bminus_fail[1, "+_min+" , "+_max+"]")
        #self.modelBuilder.doVar("r_bplus_fail[1, "+_min+" , "+_max+"]")                
            
            
        ####------SF
        ##max = N_FAIL + N_PASS)/N_PASS
        _bminus_max = (float(N_bminus_PASS)+float(N_bminus_FAIL))/float(N_bminus_PASS)
        if _bminus_max > 10 : _bminus_max=10
        _bplus_max = (float(N_bplus_PASS)+float(N_bplus_FAIL))/float(N_bplus_PASS)
        if _bplus_max > 10 : _bplus_max=10

        print('_bminus_max=',_bminus_max)
        print('_bplus_max=',_bplus_max)
        self.modelBuilder.doVar("SF_bminus[1, 0,"+str(_bminus_max)+"]")
        self.modelBuilder.doVar("SF_bplus[1, 0,"+str(_bplus_max)+" ]")

        self.modelBuilder.doVar("r_bminus_fail[1, 0 , 10]")
        self.modelBuilder.doVar("r_bplus_fail[1, 0 , 10]")                

        ## common norm. factor of denominator of b+ b-'s efficiency
        ## rpass*Npass + rfail*Nfail = C_b(Npass + Nfail)
        #self.modelBuilder.doVar("C_b[1, 0,10]")


        #POI_LIST=["SF0,dSF"]
        POI_LIST=["SF_bminus","SF_bplus"]
        

                
        ##-----Add formula


        
        ## eff_mc = N_PASS/N_PASS+N_FAIL
        ## eff_data = r_pass*N_PASS/[r_pass*N_PASS + r_fail*N_FAIL]
        ## SF = data/mc = r_pass*(N_PASS+N_FAIL)/[r_pass*N_PASS + r_fail*N_FAIL]
        ## ->  by this relation, we can express r_pass with SF and r_fail
        ## SF*[r_pass*N_PASS + r_fail*N_FAIL] = r_pass*(N_PASS+N_FAIL)
        ## r_pass*( N_FAIL + N_PASS - SF*N_PASS) = SF*r_fail*N_FAIL
        ## r_pass = SF*r_fail*N_FAIL/[N_FAIL + N_PASS - SF*N_PASS]
        
        self.modelBuilder.factory_( 'expr::r_bminus_pass(\" @0*'+N_bminus_FAIL+'*@1/('+N_bminus_PASS+' + '+N_bminus_FAIL+' - '+N_bminus_PASS+'*@1) \", r_bminus_fail,SF_bminus)')
        print('expr::r_bminus_pass(\" @0*'+N_bminus_FAIL+'*@1/('+N_bminus_PASS+' + '+N_bminus_FAIL+' - '+N_bminus_PASS+'*@1) \", r_bminus_fail,SF_bminus)')
        self.modelBuilder.factory_( 'expr::r_bplus_pass(\" @0*'+N_bplus_FAIL+'*@1/('+N_bplus_PASS+' + '+N_bplus_FAIL+' - '+N_bplus_PASS+'*@1) \", r_bplus_fail,SF_bplus)')
        print('expr::r_bplus_pass(\" @0*'+N_bplus_FAIL+'*@1/('+N_bplus_PASS+' + '+N_bplus_FAIL+' - '+N_bplus_PASS+'*@1) \", r_bplus_fail,SF_bplus)')

        ##r1 = SF*C 
        #self.modelBuilder.factory_( 'expr::r_bminus_pass( \"@0*@1 \", SF_bminus,C_b)')
        #self.modelBuilder.factory_( 'expr::r_bplus_pass( \"@0*@1 \", SF_bplus,C_b)')

        ##r2 = (C-r1)*Npass/Nfail + C
        #self.modelBuilder.factory_( 'expr::r_bminus_fail( \"(@0-@1)*'+N_bminus_PASS+'/'+N_bminus_FAIL+'+ @0 \", C_b,r_bminus_pass)')
        #self.modelBuilder.factory_( 'expr::r_bplus_fail( \"(@0-@1)*'+N_bplus_PASS+'/'+N_bplus_FAIL+'+ @0 \", C_b,r_bplus_pass)')

        ##r2 = r_FAIL > 0
        ## (C-r1)*Npass/Nfail + C  > 0
        ## (Npass+Nfail)*C -r1*Npass >0
        ## by C = r1/SF
        ## (Npass+Nfail)*r1 -r1*Npass*SF > 0
        ## (Npass+Nfail) - Npass*SF > 0
        ## SF < (Npass+Nfail)/N_pass
        ## must be satisfied
        
        ##by SF = SF0 *(1+/-dSF) < 2*SF0
        ##So, applying -> 2*SF0  < min((Npass+Nfail)/N_pass)
        # then SF < 2*SF0 < min((Npass+Nfail)/N_pass) < (Npass+Nfail)/N_pass

        
        ## r_pass must be >= 0
        ##SF*r_fail*N_FAIL/[N_FAIL + N_PASS - SF*N_PASS] > 0
        ##N_FAIL + N_PASS - SF*N_PASS>0
        ##SF*N_PASS < N_FAIL + N_PASS
        ##SF < (N_FAIL + N_PASS)/N_PASS

        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))
        self.passname="NOTSET"
        self.failname="NOTSET"
        self.QCD_on=0
        self.dict_ymc={}

        for po in physOptions:
            if "passname" in po:
                self.passname=po.split("=")[1]
            elif "failname" in po:
                self.failname=po.split("=")[1]            
            elif "=" in po:
                key=po.split("=")[0]
                value=float(po.split("=")[1])
                self.dict_ymc[key]=str(value)
                print( key,value)
            elif "QCD_on" in po:
                self.QCD_on=1
        for key in self.dict_ymc:
            print(key,self.dict_ymc[key])
        if self.passname=="NOSET":
            1/0
        if self.failname=="NOSET":
            1/0
        print(self.passname,self.failname)
    def getYieldScale(self,bin,process): ##bin process in datacard
        print( "----<getYieldScale>----")
        print(process)
        print(bin)
        scale=1

        ##---origin parton
        if "from_bminus" in process:
            #r_bminus_pass
            if self.failname in bin:
                scale="r_bminus_fail"
            elif self.passname in bin:
                scale="r_bminus_pass"
        elif "from_bplus" in process:
            if self.failname in bin:
                scale="r_bplus_fail"
            elif self.passname in bin:
                scale="r_bplus_pass"            
        else:
            scale=1


        ##---QCD
        #if "from_bplus__QCD" in process:
        #    print("QCD")
        #    if self.QCD_on:
        #        scale=1
        #    else:
        #        scale=0
        #elif "from_bminus__QCD" in process:
        #    print("QCD")
        #    if self.QCD_on:
        #        scale=1
        #    else:
        #        scale=0
        #elif "from_Others__QCD" in process:
        #    print("QCD")
        #    if self.QCD_on:
        #        scale=1
        #    else:
        #        scale=0            

        print (bin,process)
        print ('scale->',scale)
        return scale
bChargeIDEffFit=bChargeIDEff()
