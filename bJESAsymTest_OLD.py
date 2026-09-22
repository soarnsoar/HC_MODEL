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

        self.modelBuilder.doVar("C[1, 0.5. ,1.5]")


        POI_LIST.append("C")
        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)
        print("POIS",POIS)

    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))


    def getYieldScale(self,bin,process): ##bin process in datacard


        return "C"
bJESAsymTestFit=bJESAsymTest()
