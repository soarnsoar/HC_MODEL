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

                _min="0.2"
                _max="1.8"
                if "light" in origin_parton :
                    _min="0.0"
                    _max="10.0"

                ##give last bin strength additional d.o.f.
                r6="r_"+origin_parton+"_"+charge_obj_bins[5]+"_"+pt
                print("-Add param",r6)
                self.modelBuilder.doVar(r6+"[1, "+_min+" , "+_max+"]")                
                #POI_LIST.append(r6)

                ####------SF
                SF1="SF_"+origin_parton+"_"+charge_obj_bins[0]+"_"+pt
                SF2="SF_"+origin_parton+"_"+charge_obj_bins[1]+"_"+pt
                SF3="SF_"+origin_parton+"_"+charge_obj_bins[2]+"_"+pt
                SF4="SF_"+origin_parton+"_"+charge_obj_bins[3]+"_"+pt
                SF5="SF_"+origin_parton+"_"+charge_obj_bins[4]+"_"+pt
 
                self.modelBuilder.doVar(SF1+"[1, "+_min+" , "+_max+"]")
                self.modelBuilder.doVar(SF2+"[1, "+_min+" , "+_max+"]")
                self.modelBuilder.doVar(SF3+"[1, "+_min+" , "+_max+"]")
                self.modelBuilder.doVar(SF4+"[1, "+_min+" , "+_max+"]")
                self.modelBuilder.doVar(SF5+"[1, "+_min+" , "+_max+"]")


                POI_LIST.append(SF1)
                POI_LIST.append(SF2)
                POI_LIST.append(SF3)
                POI_LIST.append(SF4)
                POI_LIST.append(SF5)


                ##----Load init yield of each channel
                #N1,N2,N3,N4,N5,N6
                N6=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[5]+"_"+pt]
                N5=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[4]+"_"+pt]
                N4=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[3]+"_"+pt]
                N3=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[2]+"_"+pt]
                N2=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[1]+"_"+pt]
                N1=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[0]+"_"+pt]
                
                ##-----Add formula
                ##--SF6(==>Bad jet SF->completely (anti)correlated to SF5, which means it can be expressed in SF5)
                SF6="SF_"+origin_parton+"_"+charge_obj_bins[5]+"_"+pt
                ## SF6 = (N5+N6-N5*SF5)/N6
                self.modelBuilder.factory_( 'expr::'+SF6+'(\"('+N5+ '+' + N6 + '- '+N5+'*@0)/'+N6+'\", '+SF5+')')
                ##---jG(=Good jet)
                r5="r_"+origin_parton+"_"+charge_obj_bins[4]+"_"+pt                
                ## r5 = SF5*r6/SF6
                self.modelBuilder.factory_( 'expr::'+r5+'(\"@0*@1/@2\", '+SF5+','+r6+','+SF6+')')
                ##---eL(=LowScore-Electron)
                r4="r_"+origin_parton+"_"+charge_obj_bins[3]+"_"+pt
                ## r4 = SF4*(r5N5 + r6N6)/(N4+N5+N6-SF4*N4)
                self.modelBuilder.factory_( 'expr::'+r4+'(\"@0*('+N5+'*@1 + '+N6+'*@2)/('+N4+'+'+N5+'+'+N6+'-'+N4+'*@0)\", '+SF4+','+r5+','+r6+')')
                ##---eH(=HighScore-Electron)
                r3="r_"+origin_parton+"_"+charge_obj_bins[2]+"_"+pt
                ## r3 = SF3*(r4N4 + r5N5 + r6N6)/(N3+N4+N5+N6-SF3*N3)
                self.modelBuilder.factory_( 'expr::'+r3+'(\"@0*('+N4+'*@1 + '+N5+'*@2 + '+N6+'*@3)/('+N3+'+'+N4+'+'+N5+'+'+N6+'-'+N3+'*@0)\", '+SF3+','+r4+','+r5+','+r6+')')
                ##---muL(=LowScore-Muon)
                r2="r_"+origin_parton+"_"+charge_obj_bins[1]+"_"+pt
                ## r2 = SF2*(r3N3 + r4N4 + r5N5 + r6N6)/(N2+N3+N4+N5+N6-SF2*N2)
                self.modelBuilder.factory_( 'expr::'+r2+'(\"@0*('+N3+'*@1 + '+N4+'*@2 + '+N5+'*@3 + '+N6+'*@4)/('+N2+'+'+N3+'+'+N4+'+'+N5+'+'+N6+'-'+N2+'*@0)\", '+SF2+','+r3+','+r4+','+r5+','+r6+')')
                ##--muH(=HighScore-Muon)
                r1="r_"+origin_parton+"_"+charge_obj_bins[0]+"_"+pt
                ## r1 = SF1*(r2N2 + r3N3 + r4N4 + r5N5 + r6N6)/(N1+N2+N3+N4+N5+N6-SF1*N1)
                self.modelBuilder.factory_( 'expr::'+r1+'(\"@0*('+N2+'*@1 + '+N3+'*@2 + '+N4+'*@3 + '+N5+'*@4 +'+N6+'*@5)/('+N1+'+'+N2+'+'+N3+'+'+N4+'+'+N5+'+'+N6+'-'+N1+'*@0)\", \
                '+SF1+','+r2+','+r3+','+r4+','+r5+','+r6+')')

        #self.modelBuilder.factory_()


        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))

        self.dict_ymc={}

        for po in physOptions:
            if "=" in po:
                key=po.split("=")[0]
                value=float(po.split("=")[1])
                self.dict_ymc[key]=str(value)
                print( key,value)
    def getYieldScale(self,bin,process): ##bin process in datacard
        #print("<getYieldScale>")
        #print(process)
        #LeptonMinus_bJetLeptonicSide_TestMuon_HasSLTMuonHigh_30To50_2017
        #bTaggedJet_from_LightAndCharm__TTLJ

        #if "DYbbar"==process or "DY_bbar"==process or "DY_bplus"==process :
        #    print("DY b+")
        #    return "r_bbar"
        #elif "DYbevt"==process or "DYb"==process or "DY_b"==process or "DY_bminus"==process:
        #    print("DY b-")
        #    return "r_b"
        #else: ## other bkg
        #    return 1

        scale=1
        #"r_"+origin_parton+"_"+charge_obj_bins[0]+"_"+pt
        origin_parton=""
        charge_obj_bin=""
        pt=""
        ##---origin parton
        if "from_bminus" in process:
            origin_parton="bminus"
        elif "from_bplus" in process:
            origin_parton="bplus"
        elif "from_LightAndCharm" in process:
            origin_parton="light"
        else:
            print( "---Unkown parton origin")
            1/0
        
        ##---charge_obj_bins
        #charge_obj_bins=["muH","muL","eH","eL","jG","jB"]
        if "SLTMuonHigh" in bin:
            charge_obj_bin="muH"
        elif "SLTMuonLow" in bin:
            charge_obj_bin="muL"
        elif "SLTElectronHigh" in bin:
            charge_obj_bin="eH"
        elif "SLTElectronLow" in bin:
            charge_obj_bin="eL"
        elif "GoodBJet" in bin:
            charge_obj_bin="jG"
        elif "BadBJet" in bin:
            charge_obj_bin="jB"
        else:
            print( "---unknown charge_obj_bin-->",bin)
            1/0
        
        ##--ptbinning
        #pt_bins=["30To50","50To70","70To100","100To140","140ToInf"]

        if "30To50" in bin:
            pt="30To50"
        elif "50To70" in bin:
            pt="50To70"
        elif "70To100" in bin:
            pt="70To100"
        elif "100To140" in bin:
            pt="100To140"
        elif "140ToInf" in bin:
            pt="140ToInf"
        else:
            print( "---unknown pt bin--->",bin)
        
        print( "----<getYieldScale>----")
        print (bin,process)
        scale= "r_"+origin_parton+"_"+charge_obj_bin+"_"+pt
        print (scale)
        return scale
bChargeIDEffFit=bChargeIDEff()
