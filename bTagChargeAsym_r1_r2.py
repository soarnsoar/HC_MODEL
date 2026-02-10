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





        print("C_Others[1, 0 , 3]")
        self.modelBuilder.doVar("C_Others[1, 0 , 3]")
        POI_LIST.append("C_Others")
        ####------SF for b+/b- ---> SF0 +- dSF_Asym

        borigins=["bplus","bminus",]
        for origin in borigins:

            _min="0."
            _max="3.0"

            r1="r_"+origin+"_PASS"
            r2="r_"+origin+"_FAIL" ## will be expressed with C & SF
            self.modelBuilder.doVar(r1+"[1, 0 , 3]")
            self.modelBuilder.doVar(r2+"[1, 0 , 3]")
            POI_LIST.append(r1)
            POI_LIST.append(r2)
        





        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)
        print("POIS",POIS)

    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))

        self.NoScaleOnOthers=0
        self.FreezeSF0=0
        self.ConserveYield=0
        self.Norm_bPlusMinus=0
        self.Norm_MC=0
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
            if 'Norm_bPlusMinus' in po:
                self.Norm_bPlusMinus=1
                print("!! bplus/bminus have the common norm for denominator")
            if 'Norm_MC' in po:
                self.Norm_MC=1
                self.Norm_bPlusMinus=0
                print("!! Add param for overall MC norm")
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

        if self.NoScaleOnOthers:
            if 'from_Others' in process:
                scale="C_Others"

        print (scale)
        return scale
bTagChargeAsymFit=bTagChargeAsym()
