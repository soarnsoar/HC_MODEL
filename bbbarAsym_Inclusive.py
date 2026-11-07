from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bbbarAsym(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        #####---POIs -> slope/intercept  -> slopeshape's signal strength & nominal shape's signal strength.

        POI_LIST=[]
        self.modelBuilder.doVar("bPDFasym[0,-1,1]")

        self.modelBuilder.doVar("C[1,0.1,2]")


        POI_LIST.append('bPDFasym')



        self.modelBuilder.factory_( 'expr::r_bbar(\"@0*(1+@1)\", C,bPDFasym)')
        self.modelBuilder.factory_( 'expr::r_b(\"@0*(1-@1)\", C,bPDFasym)')


        

        POIS=",".join(POI_LIST)
        print(POIS)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))

        self.opt1=False
        for po in physOptions:
            if po=="someoption":
                self.opt1=True
        
    def getYieldScale(self,bin,process): ##bin process in datacard
        scale=1
        if 'DYbminus' in process:            
            print("DY b-")
            scale='r_b'
            
        elif 'DYbplus' in process:
            print("DY b+")
            scale='r_bbar'

        print(process,scale)
        return scale
bbbarAsymFit=bbbarAsym()
