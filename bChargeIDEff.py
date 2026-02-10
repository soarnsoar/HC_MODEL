from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bChargeIDEff(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        POI_LIST=["SF"]
        


        _min="0."
        _max="10.0"
                
        ##give last bin strength additional d.o.f.


        #self.modelBuilder.doVar("r_pass[1, "+_min+" , "+_max+"]")
        self.modelBuilder.doVar("r_fail[1, "+_min+" , "+_max+"]")                
            
            
        ####------SF
        self.modelBuilder.doVar("SF[1, "+_min+" , "+_max+"]")


        N_PASS=self.dict_ymc["N_PASS"]
        N_FAIL=self.dict_ymc["N_FAIL"]
        

                
        ##-----Add formula
        ## eff_mc = N_PASS/N_PASS+N_FAIL
        ## eff_data = r_pass*N_PASS/[r_pass*N_PASS + r_fail*N_FAIL]
        ## SF = data/mc = r_pass*(N_PASS+N_FAIL)/[r_pass*N_PASS + r_fail*N_FAIL]
        ## ->  by this relation, we can express r_pass with SF and r_fail
        ## SF*[r_pass*N_PASS + r_fail*N_FAIL] = r_pass*(N_PASS+N_FAIL)
        ## r_pass*( N_FAIL + N_PASS - SF*N_PASS) = SF*r_fail*N_FAIL
        ## r_pass = SF*r_fail*N_FAIL/[N_FAIL + N_PASS - SF*N_PASS]
        self.modelBuilder.factory_( 'expr::r_pass(\" @0*'+N_FAIL+'*@1/('+N_PASS+' + '+N_FAIL+' - '+N_PASS+'*@1) \", r_fail,SF)')



        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))
        self.passname="NOTSET"
        self.failname="NOTSET"
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

        for key in self.dict_ymc:
            print(key,self.dict_ymc[key])
        if self.passname=="NOSET":
            1/0
        if self.failname=="NOSET":
            1/0
        print(self.passname,self.failname)
    def getYieldScale(self,bin,process): ##bin process in datacard
        print(process)
        print(bin)
        scale=1
        ##---origin parton
        if "from_B" in process:
            print("!! from_B in processname")
            if self.failname in bin:
                scale="r_fail"
            elif self.passname in bin:
                scale="r_pass"
        else:
            scale=1
        
        print( "----<getYieldScale>----")
        print (bin,process)
        print ('scale->',scale)
        return scale
bChargeIDEffFit=bChargeIDEff()
