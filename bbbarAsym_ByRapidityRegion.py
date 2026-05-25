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
        self.modelBuilder.doVar("bPDFasym_broad[0,-1,1]")
        self.modelBuilder.doVar("bPDFasym_low_peak[0,-1,1]")
        self.modelBuilder.doVar("bPDFasym_mid_peak[0,-1,1]")
        self.modelBuilder.doVar("bPDFasym_high_peak[0,-1,1]")

        self.modelBuilder.doVar("C_broad[1,0.1,2]")
        self.modelBuilder.doVar("C_low_peak[1,0.1,2]")
        self.modelBuilder.doVar("C_mid_peak[1,0.1,2]")
        self.modelBuilder.doVar("C_high_peak[1,0.1,2]")

        POI_LIST.append('bPDFasym_broad')
        POI_LIST.append('bPDFasym_low_peak')
        POI_LIST.append('bPDFasym_mid_peak')
        POI_LIST.append('bPDFasym_high_peak')


        self.modelBuilder.factory_( 'expr::r_bbar_broad(\"@0*(1+@1)\", C_broad,bPDFasym_broad)')
        self.modelBuilder.factory_( 'expr::r_b_broad(\"@0*(1-@1)\", C_broad,bPDFasym_broad)')

        self.modelBuilder.factory_( 'expr::r_bbar_low_peak(\"@0*(1+@1)\", C_low_peak,bPDFasym_low_peak)')
        self.modelBuilder.factory_( 'expr::r_b_low_peak(\"@0*(1-@1)\", C_low_peak,bPDFasym_low_peak)')

        self.modelBuilder.factory_( 'expr::r_bbar_mid_peak(\"@0*(1+@1)\", C_mid_peak,bPDFasym_mid_peak)')
        self.modelBuilder.factory_( 'expr::r_b_mid_peak(\"@0*(1-@1)\", C_mid_peak,bPDFasym_mid_peak)')

        self.modelBuilder.factory_( 'expr::r_bbar_high_peak(\"@0*(1+@1)\", C_high_peak,bPDFasym_high_peak)')
        self.modelBuilder.factory_( 'expr::r_b_high_peak(\"@0*(1-@1)\", C_high_peak,bPDFasym_high_peak)')

        

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
            if 'broad' in bin:
                scale='r_b_broad'
            elif 'low_peak' in bin:
                scale='r_b_low_peak'
            elif 'mid_peak' in bin:
                scale='r_b_mid_peak'
            elif 'high_peak' in bin:
                scale='r_b_high_peak'                                

        elif 'DYbplus' in process:
            print("DY b+")
            if 'broad' in bin:
                scale='r_bbar_broad'
            elif 'low_peak' in bin:
                scale='r_bbar_low_peak'
            elif 'mid_peak' in bin:
                scale='r_bbar_mid_peak'
            elif 'high_peak' in bin:
                scale='r_bbar_high_peak'                                

        print(process,scale)
        return scale
bbbarAsymFit=bbbarAsym()
