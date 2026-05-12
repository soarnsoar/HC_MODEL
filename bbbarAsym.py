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
        self.modelBuilder.doVar("bPDFasym_Under_m4.5[0,-1,1]")
        self.modelBuilder.doVar("bPDFasym_m4.5_To_m3.5[0,-1,1]")
        self.modelBuilder.doVar("bPDFasym_Over_m3.5[0,-1,1]")

        self.modelBuilder.doVar("C_Under_m4.5[1,0.1,2]")
        self.modelBuilder.doVar("C_m4.5_To_m3.5[1,0.1,2]")
        self.modelBuilder.doVar("C_Over_m3.5[1,0.1,2]")

        POI_LIST.append('bPDFasym_Under_m4.5')
        POI_LIST.append('bPDFasym_m4.5_To_m3.5')
        POI_LIST.append('bPDFasym_Over_m3.5')
        self.modelBuilder.factory_( 'expr::r_bbar_Under_m4.5(\"@0*(1+@1)\", C_Under_m4.5,bPDFasym_Under_m4.5)')
        self.modelBuilder.factory_( 'expr::r_bbar_m4.5_To_m3.5(\"@0*(1+@1)\", C_m4.5_To_m3.5,bPDFasym_m4.5_To_m3.5)')
        self.modelBuilder.factory_( 'expr::r_bbar_Over_m3.5(\"@0*(1+@1)\", C_Over_m3.5,bPDFasym_Over_m3.5)')

        self.modelBuilder.factory_( 'expr::r_b_Under_m4.5(\"@0*(1-@1)\", C_Under_m4.5,bPDFasym_Under_m4.5)')
        self.modelBuilder.factory_( 'expr::r_b_m4.5_To_m3.5(\"@0*(1-@1)\", C_m4.5_To_m3.5,bPDFasym_m4.5_To_m3.5)')
        self.modelBuilder.factory_( 'expr::r_b_Over_m3.5(\"@0*(1-@1)\", C_Over_m3.5,bPDFasym_Over_m3.5)')
        

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
            if 'logx_Over_m3.5' in process:
                scale='r_b_Over_m3.5'
            elif 'logx_Under_m4.5' in process:
                scale='r_b_Under_m4.5'
            elif 'logx_m4.5_To_m3.5' in process:
                scale='r_b_m4.5_To_m3.5'
        elif 'DYbplus' in process:
            print("DY b+")
            if 'logx_Over_m3.5' in process:
                scale='r_bbar_Over_m3.5'
            elif 'logx_Under_m4.5' in process:
                scale='r_bbar_Under_m4.5'
            elif 'logx_m4.5_To_m3.5' in process:
                scale='r_bbar_m4.5_To_m3.5'

        print(process,scale)
        return scale
bbbarAsymFit=bbbarAsym()
