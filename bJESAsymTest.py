from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bJESAsymTest(PhysicsModel):

    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        POI_LIST=[]
        origins=["bplus","bminus"]
        
        ####------SF for b+/b- ---> SF0 +- dSF_Asym

        self.modelBuilder.doVar("C_b[1, 0.5. ,1.5]")
        #self.modelBuilder.doVar("dC_b[0, -1. ,1.]")

        self.modelBuilder.factory_( 'expr::r_bplus( \"@0 \", C_b)')
        self.modelBuilder.factory_( 'expr::r_bminus( \"@0 \", C_b)')


        POI_LIST.append("C_b")
        #POI_LIST.append("dC_b")

        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)
        print("POIS",POIS)

    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))


    def getYieldScale(self,bin,process): ##bin process in datacard
        scale=1
        if 'bplus' in process:
            scale="r_bplus"

        if 'bminus' in process:
            scale="r_bminus"
            
        return scale
bJESAsymTestFit=bJESAsymTest()
