from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bChargeIDEffAcc(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """
        POI_LIST=[]
        origin_parton_bins=["bplus","bminus","light"]
        charge_obj_bins=["muH","muL","eH","eL","jG","jB"]
        pt=self.pt

        for origin_parton in origin_parton_bins:


            _min="0."
            _max="3.0"
            if "light" in origin_parton :
                _min="0.0"
                _max="10.0"


            ##----Load init yield of each channel
            #N1,N2,N3,N4,N5,N6
            #N6=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[5]+"_"+pt]
            #N5=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[4]+"_"+pt]
            #N4=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[3]+"_"+pt]
            #N3=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[2]+"_"+pt]
            #N2=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[1]+"_"+pt]
            #N1=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[0]+"_"+pt]

            N6=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[5]]
            N5=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[4]]
            N4=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[3]]
            N3=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[2]]
            N2=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[1]]
            N1=self.dict_ymc["N_"+origin_parton+"_"+charge_obj_bins[0]]

                
            ##give last bin strength additional d.o.f.
            r6="r_"+origin_parton+"_"+charge_obj_bins[5]
            print("-Add param",r6)
            self.modelBuilder.doVar(r6+"[1, "+_min+" , "+_max+"]")                
            
            
            ####------SF 
            SF1="SF_"+origin_parton+"_"+charge_obj_bins[0]
            SF2="SF_"+origin_parton+"_"+charge_obj_bins[1]
            SF3="SF_"+origin_parton+"_"+charge_obj_bins[2]
            SF4="SF_"+origin_parton+"_"+charge_obj_bins[3]
            SF5="SF_"+origin_parton+"_"+charge_obj_bins[4]
            
            ####----measured efficiency cannot be > 1, so, SF*initeff<1 -> SF_max = 1/initeff
            _max_SF1=min( float(_max), ( float(N6) + float(N5) + float(N4) + float(N3) + float(N2) + float(N1) ) / float(N1)    )
            _max_SF2=min( float(_max), ( float(N6) + float(N5) + float(N4) + float(N3) + float(N2)  ) / float(N2)    )
            _max_SF3=min( float(_max), ( float(N6) + float(N5) + float(N4) + float(N3)   ) / float(N3)    )
            _max_SF4=min( float(_max), ( float(N6) + float(N5) + float(N4)   ) / float(N4)    )
            _max_SF5=min( float(_max), ( float(N6) + float(N5)   ) / float(N5)    )
            _max_SF6=min( float(_max), ( float(N6) + float(N5)   ) / float(N6)    )

            _max_SF1=str(_max_SF1)
            _max_SF2=str(_max_SF2)
            _max_SF3=str(_max_SF3)
            _max_SF4=str(_max_SF4)
            _max_SF5=str(_max_SF5)
            _max_SF6=str(_max_SF6)

            print(SF1+"[1, "+_min+" , "+_max_SF1+"]")
            print(SF2+"[1, "+_min+" , "+_max_SF2+"]")
            print(SF3+"[1, "+_min+" , "+_max_SF3+"]")
            print(SF4+"[1, "+_min+" , "+_max_SF4+"]")
            print(SF5+"[1, "+_min+" , "+_max_SF5+"]")


            self.modelBuilder.doVar(SF1+"[1, "+_min+" , "+_max_SF1+"]")
            self.modelBuilder.doVar(SF2+"[1, "+_min+" , "+_max_SF2+"]")
            self.modelBuilder.doVar(SF3+"[1, "+_min+" , "+_max_SF3+"]")
            self.modelBuilder.doVar(SF4+"[1, "+_min+" , "+_max_SF4+"]")
            self.modelBuilder.doVar(SF5+"[1, "+_min+" , "+_max_SF5+"]")
            
            if origin_parton != "light":
                POI_LIST.append(SF1)
                POI_LIST.append(SF2)
                POI_LIST.append(SF3)
                POI_LIST.append(SF4)
                POI_LIST.append(SF5)
                POI_LIST.append(r6)    


                
            ##-----Add formula
            ##--SF6(==>Bad jet SF->completely (anti)correlated to SF5, which means it can be expressed in SF5)
            SF6="SF_"+origin_parton+"_"+charge_obj_bins[5]
            ## SF6 = (N5+N6-N5*SF5)/N6
            self.modelBuilder.factory_( 'expr::'+SF6+'(\"('+N5+ '+' + N6 + '- '+N5+'*@0)/'+N6+'\", '+SF5+')')
            ##---jG(=Good jet)
            r5="r_"+origin_parton+"_"+charge_obj_bins[4]
            ## r5 = SF5*r6/SF6
            self.modelBuilder.factory_( 'expr::'+r5+'(\"@0*@1/@2\", '+SF5+','+r6+','+SF6+')')
            ##---eL(=LowScore-Electron)
            r4="r_"+origin_parton+"_"+charge_obj_bins[3]
            ## r4 = SF4*(r5N5 + r6N6)/(N4+N5+N6-SF4*N4)
            self.modelBuilder.factory_( 'expr::'+r4+'(\"@0*('+N5+'*@1 + '+N6+'*@2)/('+N4+'+'+N5+'+'+N6+'-'+N4+'*@0)\", '+SF4+','+r5+','+r6+')')
            ##---eH(=HighScore-Electron)
            r3="r_"+origin_parton+"_"+charge_obj_bins[2]
            ## r3 = SF3*(r4N4 + r5N5 + r6N6)/(N3+N4+N5+N6-SF3*N3)
            self.modelBuilder.factory_( 'expr::'+r3+'(\"@0*('+N4+'*@1 + '+N5+'*@2 + '+N6+'*@3)/('+N3+'+'+N4+'+'+N5+'+'+N6+'-'+N3+'*@0)\", '+SF3+','+r4+','+r5+','+r6+')')
            ##---muL(=LowScore-Muon)
            r2="r_"+origin_parton+"_"+charge_obj_bins[1]
            ## r2 = SF2*(r3N3 + r4N4 + r5N5 + r6N6)/(N2+N3+N4+N5+N6-SF2*N2)
            self.modelBuilder.factory_( 'expr::'+r2+'(\"@0*('+N3+'*@1 + '+N4+'*@2 + '+N5+'*@3 + '+N6+'*@4)/('+N2+'+'+N3+'+'+N4+'+'+N5+'+'+N6+'-'+N2+'*@0)\", '+SF2+','+r3+','+r4+','+r5+','+r6+')')
            ##--muH(=HighScore-Muon)
            r1="r_"+origin_parton+"_"+charge_obj_bins[0]
            ## r1 = SF1*(r2N2 + r3N3 + r4N4 + r5N5 + r6N6)/(N1+N2+N3+N4+N5+N6-SF1*N1)
            self.modelBuilder.factory_( 'expr::'+r1+'(\"@0*('+N2+'*@1 + '+N3+'*@2 + '+N4+'*@3 + '+N5+'*@4 +'+N6+'*@5)/('+N1+'+'+N2+'+'+N3+'+'+N4+'+'+N5+'+'+N6+'-'+N1+'*@0)\", '+SF1+','+r2+','+r3+','+r4+','+r5+','+r6+')')



            if "light" in origin_parton : continue
            ##----Charge Accuracy Correction Factor----##
            ##--need initial accuracy of MC sample
            #N1c= correct charge
            #N1w= wrong charge
            #intiial accuracy, a1_init = N1c_init/N1_init
            ##Let correction factor => beta1
            ##Then, a1_fit = beta1*a1
            ###--for correct charge
            ## final process strength = r1 * beta1 * a1_init 
            ###--for wrong charge
            ## final process strength = r1 * (1-beta1 * a1_init) 

            init_a6=self.dict_ymc["a_"+origin_parton+"_"+charge_obj_bins[5]]
            init_a5=self.dict_ymc["a_"+origin_parton+"_"+charge_obj_bins[4]]
            init_a4=self.dict_ymc["a_"+origin_parton+"_"+charge_obj_bins[3]]
            init_a3=self.dict_ymc["a_"+origin_parton+"_"+charge_obj_bins[2]]
            init_a2=self.dict_ymc["a_"+origin_parton+"_"+charge_obj_bins[1]]
            init_a1=self.dict_ymc["a_"+origin_parton+"_"+charge_obj_bins[0]]


            b6="b_"+origin_parton+"_"+charge_obj_bins[5]
            b5="b_"+origin_parton+"_"+charge_obj_bins[4]
            b4="b_"+origin_parton+"_"+charge_obj_bins[3]
            b3="b_"+origin_parton+"_"+charge_obj_bins[2]
            b2="b_"+origin_parton+"_"+charge_obj_bins[1]
            b1="b_"+origin_parton+"_"+charge_obj_bins[0]
            ## 0<=beta1*init_a1<=1    ---> max(beta1)=1/init_a1
            _max6 = str(min(float(_max),float(1/float(init_a6))))
            _max5 = str(min(float(_max),float(1/float(init_a5))))
            _max4 = str(min(float(_max),float(1/float(init_a4))))
            _max3 = str(min(float(_max),float(1/float(init_a3))))
            _max2 = str(min(float(_max),float(1/float(init_a2))))
            _max1 = str(min(float(_max),float(1/float(init_a1))))
           
            print(b6+"[1, "+_min+" , "+_max6+"]")
            print(b5+"[1, "+_min+" , "+_max5+"]")
            print(b4+"[1, "+_min+" , "+_max4+"]")
            print(b3+"[1, "+_min+" , "+_max3+"]")
            print(b2+"[1, "+_min+" , "+_max2+"]")
            print(b1+"[1, "+_min+" , "+_max1+"]")


            self.modelBuilder.doVar(b6+"[1, "+_min+" , "+_max6+"]")
            self.modelBuilder.doVar(b5+"[1, "+_min+" , "+_max5+"]")
            self.modelBuilder.doVar(b4+"[1, "+_min+" , "+_max4+"]")
            self.modelBuilder.doVar(b3+"[1, "+_min+" , "+_max3+"]")
            self.modelBuilder.doVar(b2+"[1, "+_min+" , "+_max2+"]")
            self.modelBuilder.doVar(b1+"[1, "+_min+" , "+_max1+"]")
            ## define rc --> total signal strength = rc6*r6 
            ##---rc = b1*init_a1/init_a1 = b1
            ##---rw = (1-b1*init_a1)/(1-init_a1)
            rc6="rc_"+origin_parton+"_"+charge_obj_bins[5]
            rc5="rc_"+origin_parton+"_"+charge_obj_bins[4]
            rc4="rc_"+origin_parton+"_"+charge_obj_bins[3]
            rc3="rc_"+origin_parton+"_"+charge_obj_bins[2]
            rc2="rc_"+origin_parton+"_"+charge_obj_bins[1]
            rc1="rc_"+origin_parton+"_"+charge_obj_bins[0]
            
            self.modelBuilder.factory_( 'expr::'+rc6+'(\"@0*@1 \",'+b6+','+r6+')')
            self.modelBuilder.factory_( 'expr::'+rc5+'(\"@0*@1 \",'+b5+','+r5+')')
            self.modelBuilder.factory_( 'expr::'+rc4+'(\"@0*@1 \",'+b4+','+r4+')')
            self.modelBuilder.factory_( 'expr::'+rc3+'(\"@0*@1 \",'+b3+','+r3+')')
            self.modelBuilder.factory_( 'expr::'+rc2+'(\"@0*@1 \",'+b2+','+r2+')')
            self.modelBuilder.factory_( 'expr::'+rc1+'(\"@0*@1 \",'+b1+','+r1+')')


            rw6="rw_"+origin_parton+"_"+charge_obj_bins[5]
            rw5="rw_"+origin_parton+"_"+charge_obj_bins[4]
            rw4="rw_"+origin_parton+"_"+charge_obj_bins[3]
            rw3="rw_"+origin_parton+"_"+charge_obj_bins[2]
            rw2="rw_"+origin_parton+"_"+charge_obj_bins[1]
            rw1="rw_"+origin_parton+"_"+charge_obj_bins[0]            
            #rw = (1-b1*init_a1)/(1-init_a1)
            self.modelBuilder.factory_( 'expr::'+rw6+'(\" (1.- @0*'+init_a6+' )/(1. - '+init_a6+')*@1  \",'+b6+','+r6+')')
            self.modelBuilder.factory_( 'expr::'+rw5+'(\" (1.- @0*'+init_a5+' )/(1. - '+init_a5+')*@1  \",'+b5+','+r5+')')
            self.modelBuilder.factory_( 'expr::'+rw4+'(\" (1.- @0*'+init_a4+' )/(1. - '+init_a4+')*@1  \",'+b4+','+r4+')')
            self.modelBuilder.factory_( 'expr::'+rw3+'(\" (1.- @0*'+init_a3+' )/(1. - '+init_a3+')*@1  \",'+b3+','+r3+')')
            self.modelBuilder.factory_( 'expr::'+rw2+'(\" (1.- @0*'+init_a2+' )/(1. - '+init_a2+')*@1  \",'+b2+','+r2+')')
            self.modelBuilder.factory_( 'expr::'+rw1+'(\" (1.- @0*'+init_a1+' )/(1. - '+init_a1+')*@1  \",'+b1+','+r1+')')


            POI_LIST.append(b6)
            POI_LIST.append(b5)
            POI_LIST.append(b4)
            POI_LIST.append(b3)
            POI_LIST.append(b2)
            POI_LIST.append(b1)

        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)
        print("POIS",POIS)

    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))

        self.dict_ymc={}

        for po in physOptions:
            if "ptbin" in po:
              self.pt=po.split("=")[1]  
            elif "=" in po:
                key=po.split("=")[0]
                value=float(po.split("=")[1])
                self.dict_ymc[key]=str(value)
                print( key,value)
        for key in self.dict_ymc:
            print(key,self.dict_ymc[key])
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
        real_charge=0
        measured_charge=0
        ##---origin parton
        if "from_bminus" in process:
            origin_parton="bminus"
            real_charge=-1
        elif "from_bplus" in process:
            origin_parton="bplus"
            real_charge=+1
        elif "from_LightAndCharm" in process:
            origin_parton="light"
            real_charge=0
        else:
            print( "---Unkown parton origin")
            1/0
        
        ##---charge_obj_bins
        #charge_obj_bins=["muH","muL","eH","eL","jG","jB"]
        if "SLTMuonHigh" in bin: 
            charge_obj_bin="muH"
            if "SLTMuonHighPlus" in bin:
                measured_charge=1
            elif "SLTMuonHighMinus" in bin:
                measured_charge=-1
            else:
                print("--unknown measured charge->",bin)
                1/0
        elif "SLTMuonLow" in bin:
            charge_obj_bin="muL"
            if "SLTMuonLowPlus" in bin:
                measured_charge=1
            elif "SLTMuonLowMinus" in bin:
                measured_charge=-1
            else:
                print("--unknown measured charge->",bin)
                1/0
        elif "SLTElectronHigh" in bin:
            charge_obj_bin="eH"
            if "SLTElectronHighPlus" in bin:
                measured_charge=1
            elif "SLTElectronHighMinus" in bin:
                measured_charge=-1
            else:
                print("--unknown measured charge->",bin)
                1/0
        elif "SLTElectronLow" in bin:
            charge_obj_bin="eL"
            if "SLTElectronLowPlus" in bin:
                measured_charge=1
            elif "SLTElectronLowMinus" in bin:
                measured_charge=-1
            else:
                print("--unknown measured charge->",bin)
                1/0
        elif "GoodBJet" in bin:
            charge_obj_bin="jG"
            if "GoodBJetPlus" in bin:
                measured_charge=1
            elif "GoodBJetMinus" in bin:
                measured_charge=-1
            else:
                print("--unknown measured charge->",bin)
                1/0
        elif "BadBJet" in bin:
            charge_obj_bin="jB"
            if "BadBJetPlus" in bin:
                measured_charge=1
            elif "BadBJetMinus" in bin:
                measured_charge=-1
            else:
                print("--unknown measured charge->",bin)
                1/0
        else:
            print( "---unknown charge_obj_bin-->",bin)
            1/0
        

        
        print( "----<getYieldScale>----")
        print (bin,process)
        if real_charge==0: ## light parton -origin
            scale= "r_"+origin_parton+"_"+charge_obj_bin
        else: ## if bminus OR bplus -> charged real bjet.
            if measured_charge==real_charge:
                scale="rc_"+origin_parton+"_"+charge_obj_bin
            else:
                scale="rw_"+origin_parton+"_"+charge_obj_bin

        print (scale)
        return scale
bChargeIDEffAccFit=bChargeIDEffAcc()
