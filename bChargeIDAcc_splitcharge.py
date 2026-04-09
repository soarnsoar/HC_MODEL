from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class bChargeIDAcc(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        PhysicsModel.__init__(self)



    def doParametersOfInterest(self):
        print("<doParametersOfInterest>")
        """Create POI out of signal strength """

        ##acc = (correctly measured)/(wrongly measured + correctly measured)
        
        _min="0."
        _max="10.0"
                

        N_bminus_CORR=self.dict_ymc["N_bminus_CORR"]
        N_bplus_CORR=self.dict_ymc["N_bplus_CORR"]
        N_bminus_WRONG=self.dict_ymc["N_bminus_WRONG"]
        N_bplus_WRONG=self.dict_ymc["N_bplus_WRONG"]

        #self.modelBuilder.doVar("r_pass[1, "+_min+" , "+_max+"]")
        #self.modelBuilder.doVar("r_bminus_fail[1, "+_min+" , "+_max+"]")
        #self.modelBuilder.doVar("r_bplus_fail[1, "+_min+" , "+_max+"]")                
            
            
        ####------SF
        ##max = N_WRONG + N_CORR)/N_CORR
        _bminus_max = (float(N_bminus_CORR)+float(N_bminus_WRONG))/float(N_bminus_CORR)
        if _bminus_max > 10 : _bminus_max=10
        _bplus_max = (float(N_bplus_CORR)+float(N_bplus_WRONG))/float(N_bplus_CORR)
        if _bplus_max > 10 : _bplus_max=10

        print('_bminus_max=',_bminus_max)
        print('_bplus_max=',_bplus_max)
        self.modelBuilder.doVar("SF_bminus[1, 0,"+str(_bminus_max)+"]")
        self.modelBuilder.doVar("SF_bplus[1, 0,"+str(_bplus_max)+" ]")
        ## common norm. factor of denominator of b+ b-'s accuracy
        ## rcorr*Ncorr + rwrong*Nwrong = C_b(Ncorr + Nwrong)
        self.modelBuilder.doVar("C_b[1, 0,10]")
        if self.Norm_bkg:
            self.modelBuilder.doVar("C_others[1, 0,10]")
        else:
            self.modelBuilder.factory_( 'expr::C_others( \"1 \", C_b)')
        #POI_LIST=["SF0,dSF"]
        POI_LIST=["SF_bminus","SF_bplus"]
        

                
        ##-----Add formula


        
        ## acc_mc = N_CORR/N_CORR+N_WRONG
        ## acc_data = r_corr*N_CORR/[r_corr*N_CORR + r_wrong*N_WRONG]
        ## SF = data/mc = r_corr*(N_CORR+N_WRONG)/[r_corr*N_CORR + r_wrong*N_WRONG]
        ## ->  by this relation, we can express r_corr with SF and r_wrong
        ## SF*[r_corr*N_CORR + r_wrong*N_WRONG] = r_corr*(N_CORR+N_WRONG)
        ## r_corr*( N_WRONG + N_CORR - SF*N_CORR) = SF*r_wrong*N_WRONG
        ## r_corr = SF*r_wrong*N_WRONG/[N_WRONG + N_CORR - SF*N_CORR]
        
        #self.modelBuilder.factory_( 'expr::r_bminus_corr(\" @0*'+N_bminus_WRONG+'*@1/('+N_bminus_CORR+' + '+N_bminus_WRONG+' - '+N_bminus_CORR+'*@1) \", r_bminus_wrong,SF_bminus)')
        #self.modelBuilder.factory_( 'expr::r_bplus_corr(\" @0*'+N_bplus_WRONG+'*@1/('+N_bplus_CORR+' + '+N_bplus_WRONG+' - '+N_bplus_CORR+'*@1) \", r_bplus_wrong,SF_bplus)')


        ##r1 = SF*C 
        self.modelBuilder.factory_( 'expr::r_bminus_corr( \"@0*@1 \", SF_bminus,C_b)')
        self.modelBuilder.factory_( 'expr::r_bplus_corr( \"@0*@1 \", SF_bplus,C_b)')

        ##r2 = (C-r1)*Ncorr/Nwrong + C
        self.modelBuilder.factory_( 'expr::r_bminus_wrong( \"(@0-@1)*'+N_bminus_CORR+'/'+N_bminus_WRONG+'+ @0 \", C_b,r_bminus_corr)')
        self.modelBuilder.factory_( 'expr::r_bplus_wrong( \"(@0-@1)*'+N_bplus_CORR+'/'+N_bplus_WRONG+'+ @0 \", C_b,r_bplus_corr)')

        ##r2 = r_WRONG > 0
        ## (C-r1)*Ncorr/Nwrong + C  > 0
        ## (Ncorr+Nwrong)*C -r1*Ncorr >0
        ## by C = r1/SF
        ## (Ncorr+Nwrong)*r1 -r1*Ncorr*SF > 0
        ## (Ncorr+Nwrong) - Ncorr*SF > 0
        ## SF < (Ncorr+Nwrong)/N_corr
        ## must be satisfied
        
        ##by SF = SF0 *(1+/-dSF) < 2*SF0
        ##So, applying -> 2*SF0  < min((Ncorr+Nwrong)/N_corr)
        # then SF < 2*SF0 < min((Ncorr+Nwrong)/N_corr) < (Ncorr+Nwrong)/N_corr

        
        ## r_corr must be >= 0
        ##SF*r_wrong*N_WRONG/[N_WRONG + N_CORR - SF*N_CORR] > 0
        ##N_WRONG + N_CORR - SF*N_CORR>0
        ##SF*N_CORR < N_WRONG + N_CORR
        ##SF < (N_WRONG + N_CORR)/N_CORR

        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print("<setPhysicsOptions>")
        print(str(physOptions))
        
        self.QCD_on=0
        self.Norm_bkg=0
        self.splitQCD=0
        self.dict_ymc={}

        for po in physOptions:
            if "=" in po:
                key=po.split("=")[0]
                value=float(po.split("=")[1])
                self.dict_ymc[key]=str(value)
                print( key,value)
            elif "QCD_on" in po:
                self.QCD_on=1
            elif "Norm_bkg" in po:
                self.Norm_bkg=1
            elif "splitQCD" in po:
                self.splitQCD=1
        for key in self.dict_ymc:
            print(key,self.dict_ymc[key])

    def getYieldScale(self,bin,process): ##bin process in datacard
        print( "----<getYieldScale>----")
        print(process)
        print(bin)
        scale=1

        ##---origin parton
        if "from_bminus" in process:
            #r_bminus_corr
            if 'MeasuredPlus' in bin:
                scale="r_bminus_wrong"
            elif 'MeasuredMinus' in bin:
                scale="r_bminus_corr"
        elif "from_bplus" in process:
            if 'MeasuredMinus' in bin:
                scale="r_bplus_wrong"
            elif 'MeasuredPlus' in bin:
                scale="r_bplus_corr"            
        else:
            scale='C_others'


        ##---QCD
        if self.splitQCD:
            if "from_bplus__QCD" in process:
                print("QCD")
                if self.QCD_on:
                    scale='C_others'
                else:
                    scale=0
            elif "from_bminus__QCD" in process:
                print("QCD")
                if self.QCD_on:
                    scale='C_others'
                else:
                    scale=0
            elif "from_Others__QCD" in process:
                print("QCD")
                if self.QCD_on:
                    scale='C_others'
                else:
                    scale=0            

        print (bin,process)
        print ('scale->',scale)
        return scale
bChargeIDAccFit=bChargeIDAcc()
