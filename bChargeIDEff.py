from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bChargeIDEff(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        POI_LIST=[]
        origin_parton_bins=["bplus","bminus","light"]
        charge_obj_bins=["muH","muL","eH","eL","jG","jB"]
        pt_bins=["30To50","50To70","70To100","100To140","140ToInf"]

        for origin_parton in origin_parton_bins:
            for pt in pt_bins:
                ##give last bin strength additional dof
                r6="r_"+origin_parton+"_"+charge_obj_bins[5]+"_"+pt
                self.modelBuilder.doVar(r_param_last+"[1,0.2,1.8]")
                POI_LIST(r_param_last)
                ####------SF
                SF1="SF_"+origin_parton+"_"+charge_obj_bins[0]+"_"+pt
                SF2="SF_"+origin_parton+"_"+charge_obj_bins[1]+"_"+pt
                SF3="SF_"+origin_parton+"_"+charge_obj_bins[2]+"_"+pt
                SF4="SF_"+origin_parton+"_"+charge_obj_bins[3]+"_"+pt
                SF5="SF_"+origin_parton+"_"+charge_obj_bins[4]+"_"+pt
                SF6="SF_"+origin_parton+"_"+charge_obj_bins[5]+"_"+pt
                self.modelBuilder.doVar(SF1+"[1,0.2,1.8]")
                self.modelBuilder.doVar(SF2+"[1,0.2,1.8]")
                self.modelBuilder.doVar(SF3+"[1,0.2,1.8]")
                self.modelBuilder.doVar(SF4+"[1,0.2,1.8]")
                self.modelBuilder.doVar(SF5+"[1,0.2,1.8]")
                self.modelBuilder.doVar(SF6+"[1,0.2,1.8]")
                POI_LIST.append(SF1)
                POI_LIST.append(SF2)
                POI_LIST.append(SF3)
                POI_LIST.append(SF4)
                POI_LIST.append(SF5)
                POI_LIST.append(SF6)


                ##-----Add formula
                r5="r_"+origin_parton+"_"+charge_obj_bins[4]+"_"+pt                
                ## r5 = SF5*r6/SF6
                self.modelBuilder.factory_( 'expr::'+r5+'(\"@0*@1/@2\", '+SF5+',"'+r6+','+SF6+')')
                ## r4 = SF4*(r5N5 + r6N6)/(N4+N5+N6-SF4*N4)
                self.modelBuilder.factory_( 'expr::'+r4+'(\"@0*(N5*@1 + N6*@2)/(N4+N5+N6-N4*@0)\", '+SF4+','+r5+','+r6+')')
        #self.modelBuilder.doVar("SF_bplus_30To50[1,0.5,1.5]")
        #self.modelBuilder.doVar("SF_bminus_30To50[1,0.5,1.5]")

        #POI_LIST.append('bbar_over_b')
        #POI_LIST.append('r_b')
        
        #self.modelBuilder.factory_( 'expr::r_bbar(\"@0*@1\", bbar_over_b,r_b)')

        self.modelBuilder.factory_()


        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))

        self.dict_ymc={}

        for po in physOptions:
            if "=" in po:
                key=po.split("=")[0]
                value=float(po.split("=")[0])
                self.dict_ymc[key]=value
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

    
bChargeIDEffFit=bChargeIDEff()
