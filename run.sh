rm -rf logs && mkdir logs

ngspice -b -o logs/dc_analysis.log AMP_NMCF_ACDC.cir
ngspice -b -o logs/tran_analysis.log AMP_NMCF_Tran.cir



