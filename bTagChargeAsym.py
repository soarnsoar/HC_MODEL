from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bTagChargeAsym(PhysicsModel):

    def __init__(self):
        PhysicsModel.__init__(self)
    def preProcessNuisances(self, nuisances):

        if not any(row[0] == "theta_C_Others" for row in nuisances):
            nuisances.append(
                ("theta_C_Others", False, "param", ["0", "1"], [])
            )
            

    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        POI_LIST=[]
        origins=["bplus","bminus"]
        
        ####------SF for b+/b- ---> SF0 +- dSF_Asym

        self.modelBuilder.doVar("dAsym[0, -1. ,1]")
        if self.FreezeSF0:
            self.modelBuilder.factory_( 'expr::SF0(\"1.\", dAsym)')
        else:
            self.modelBuilder.doVar("SF0[1, 0. ,2]")
            POI_LIST.append("SF0")
        self.modelBuilder.factory_( 'expr::SF_bplus(\"@0*(1.+@1)\", SF0,dAsym)')
        self.modelBuilder.factory_( 'expr::SF_bminus(\"@0*(1.-@1)\", SF0,dAsym)')


        POI_LIST.append("dAsym")

        self.modelBuilder.doVar("C_b[1., 0. ,3.0]")
        if self.FreezeSF0:
            self.modelBuilder.doVar("C_Others[1., 0. ,3.0]")
        else:
            if not self.modelBuilder.out.var("theta_C_Others"):
                self.modelBuilder.doVar("theta_C_Others[0,-5,5]")

            # 50% log-normal normalization factor
            self.modelBuilder.factory_(
                'expr::C_Others("pow(1.5,@0)", theta_C_Others)'
            )
        
            
        for origin in origins:

            _min="0."
            _max="3.0"
        
            ##----Load init yield of each channel
            #N1=Pass
            #N2=Fail
            N1=self.dict_ymc["N_"+origin+"_PASS"]
            N2=self.dict_ymc["N_"+origin+"_FAIL"]

            r1="r_"+origin+"_PASS"
            r2="r_"+origin+"_FAIL" ## will be expressed with C & SF
            C="C_b"  ## Pass + Fail Overall norm factor
            SF="SF_"+origin

                        
            ## r1 = SF*C
            self.modelBuilder.factory_( 'expr::'+r1+'(\"@0*@1\", '+SF+','+C+')')
            print('expr::'+r1+'(\"@0*@1\", '+SF+','+C+')')
            ## r2 = (C-r1)*N1/N2 + C
            self.modelBuilder.factory_( 'expr::'+r2+'(\"(@0-@1)*'+N1+'/'+N2+' + @0 \", '+C+','+r1+')')
            print('expr::'+r2+'(\"(@0-@1)*'+N1+'/'+N2+' + @0 \", '+C+','+r1+')')



        




        POIS=",".join(POI_LIST)
        ##----UseOnly dAsym As POI
        #POIS="dAsym"
        #if self.Norm_bPlusMinus:
        #    POIS+=",C_b"
        #    POIS+=",C_Others"
        self.modelBuilder.doSet("POI",POIS)
        print("POIS",POIS)

    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))
        self.FreezeSF0=0
        
        self.dict_ymc={}

        for po in physOptions:

            if "=" in po:
                key=po.split("=")[0]
                value=float(po.split("=")[1])
                self.dict_ymc[key]=str(value)
                print( key,value)
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

        if 'from_Others' in process:
            scale="C_Others"
        print (scale)
        return scale
bTagChargeAsymFit=bTagChargeAsym()
