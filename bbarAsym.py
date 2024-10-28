from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bbarAsym(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        #####---POIs -> slope/intercept  -> slopeshape's signal strength & nominal shape's signal strength.
        ####Contraint ->  totalweight=[0,2]
        POI_LIST=[]
        self.modelBuilder.doVar("bbar_over_b[1,0.5,1.5]")
        self.modelBuilder.doVar("r_b[1,0.5,1.5]")
        POI_LIST.append('bbar_over_b')
        POI_LIST.append('r_b')
        self.modelBuilder.factory_( 'expr::r_bbar(\"@0*@1\", bbar_over_b,r_b)')
        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))

        self.opt1=False
        for po in physOptions:
            if po=="someoption":
                self.opt1=True
        
    def getYieldScale(self,bin,process): ##bin process in datacard
        #print("<getYieldScale>")
        #print(process)
        if "DYbbar"==process or "DY_bbar"==process or "DY_bplus"==process :
            print("DY b+")
            return "r_bbar"
        elif "DYbevt"==process or "DYb"==process or "DY_b"==process or "DY_bminus"==process:
            print("DY b-")
            return "r_b"
        else: ## other bkg
            return 1

    
bbarAsymFit=bbarAsym()
