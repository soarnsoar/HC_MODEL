from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bTagChargeAsym(PhysicsModel):

    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        POI_LIST=[]
        origins=["bplus","bminus","Others"]
        
        ####------SF for Others(Not from b+/-  --> Not setting Charge Asym Factor 
        
        _min="0.0"
        _max="10.0"
        N1=self.dict_ymc["N_Others_PASS"]
        N2=self.dict_ymc["N_Others_FAIL"]
        ####----measured efficiency cannot be > 1, so, SF*initeff<1 -> SF_max = 1/initeff
        _max_SF=min( float(_max), ((float(N1)+float(N2))/float(N1)))        
        _max_SF=str(_max_SF)




        if not self.NoScaleOnOthers :
            print("SF_Others[1, "+_min+" , "+_max_SF+"]")
            self.modelBuilder.doVar("SF_Others[1, "+_min+" , "+_max_SF+"]")
        
        ####------SF for b+/b- ---> SF0 +- dSF_Asym

        self.modelBuilder.doVar("dAsym[0, -1. ,1]")
        
        if self.FreezeSF0:
            print("[Freeze SF0]")
            #self.modelBuilder.doVar("SF0[1., 1. ,1.]")
            self.modelBuilder.factory_( 'expr::SF0(\"1.\", dAsym)')
        else:
            self.modelBuilder.doVar("SF0[1, 0. ,3.0]")
            POI_LIST.append("SF0")            


        self.modelBuilder.factory_( 'expr::SF_bplus(\"@0*(1+@1)\", SF0,dAsym)')
        self.modelBuilder.factory_( 'expr::SF_bminus(\"@0*(1-@1)\", SF0,dAsym)')


        POI_LIST.append("dAsym")
        if not self.NoScaleOnOthers:
            POI_LIST.append("SF_Others")
            True
        for origin in origins:
            if self.NoScaleOnOthers:
                if origin=="Others" : continue

            _min="0."
            _max="3.0"
            if "Others" in origin :
                _min="0.0"
                _max="10.0"


            ##----Load init yield of each channel
            #N1=Pass
            #N2=Fail
            N1=self.dict_ymc["N_"+origin+"_PASS"]
            N2=self.dict_ymc["N_"+origin+"_FAIL"]


            r2="r_"+origin+"_FAIL"
            SF="SF_"+origin

            if self.ConserveYield:

                ##r1P+r2F = P+F
                ##--> r2 = (P+F-r1P)/F
                ##--> in this case, SF = r1
                ##--> r2 = (P+F - SF*P)/F
                
                #self.modelBuilder.factory_( 'expr::SF0(\"1.\", dAsym)')
                #expr::r2("(N1+N2-N1*@0)/N2", SF)
                self.modelBuilder.factory_( 'expr::'+r2+'(\"'+'('+N1+'+'+N2+'-'+N1+'*@0)/'+N2+''+'\", '+SF+')')

            else:
                print("-Add param",r2)
            
                self.modelBuilder.doVar(r2+"[1, "+_min+" , "+_max+"]")                
            
            

            
            #if origin != "Others":
            #    POI_LIST.append(SF)
            #    POI_LIST.append(r2)    

            POI_LIST.append(r2)    

                
            ##-----Add formula

            
            #SF="SF_"+origin
            r1="r_"+origin+"_PASS"
            ## r1 = SF*r2*N2/(N1+N2-SF*N1)
            if self.ConserveYield:
                self.modelBuilder.factory_( 'expr::'+r1+'(\"@0\", '+SF+')')                
            else:
                self.modelBuilder.factory_( 'expr::'+r1+'(\"@0*@1*'+N2+'/('+N1+'+'+N2+'-'+N1+'*@0)\", '+SF+','+r2+')')

        




        POIS=",".join(POI_LIST)
        ##----UseOnly dAsym As POI
        POIS="dAsym"

        
        self.modelBuilder.doSet("POI",POIS)
        print("POIS",POIS)

    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))

        self.NoScaleOnOthers=0
        self.FreezeSF0=0
        self.ConserveYield=0
        self.dict_ymc={}

        for po in physOptions:

            if "=" in po:
                key=po.split("=")[0]
                value=float(po.split("=")[1])
                self.dict_ymc[key]=str(value)
                print( key,value)
            if 'ApplyBtagSF' in po:
                self.NoScaleOnOthers=1
                print("!!ApplyBtagSF!!")
            if 'FloatOthers' in po:
                self.NoScaleOnOthers=0
                print("!!FloatOtherOrigins!!")
            if 'ConserveYield' in po:
                self.ConserveYield=1
            if 'FreezeSF0' in po:
                self.FreezeSF0=1
                print("!!Freeze SF0!!")
        for key in self.dict_ymc:
            print(key,self.dict_ymc[key])
    def getYieldScale(self,bin,process): ##bin process in datacard

        scale=1

        origin=""
        PassFail=""
        ##---origin parton
        if "from_bminus" in process:
            origin="bminus"
            
        elif "from_bplus" in process:
            origin="bplus"

        elif "from_Others" in process:
            origin="Others"
        else:
            print( "---Unkown origin of -->",process)
            1/0
        
        ##---PASS OR FAIL

        if "PASS" in bin: 
            PassFail="PASS"
        elif "FAIL" in bin:
            PassFail="FAIL"
        else:
            print("---Unknown Pass OR Fail of cut-->",bin)
        print( "----<getYieldScale>----")
        print (bin,process)
        
        scale= "r_"+origin+"_"+PassFail
        print (scale)
        if self.NoScaleOnOthers:
            if 'from_Others' in process:
                return 1
        return scale
bTagChargeAsymFit=bTagChargeAsym()
