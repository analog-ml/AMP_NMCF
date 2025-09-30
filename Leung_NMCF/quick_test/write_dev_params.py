"""
This script is used to generate block of spice commands that used to
access BSIM4 device internal device parameters.

This one is for SKY130 process.

You can just run it once to generate the script for the DCOP analysis.

"""

# fmt: off
class DeviceParams(object):
    """
    This class is used to generate the file: RGNN_RL/simulation/AMP_NMCF_dev_params.spice
    for storing abbreviation of device parameters

    Example:
        let gmbs_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[gmbs]
        let gm_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[gm]
        let gds_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[gds]
        let vdsat_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[vdsat]
        let vth_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[vth]
        let id_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[id]
        let ibd_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[ibd]
        let ibs_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[ibs]
        let gbd_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[gbd]
        let gbs_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[gbs]
        let isub_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[isub]
        let igidl_M0=@m.x1.XM0.msky130_fd_pr__pfet_01v8[igidl]

        write AMP_NMCF_op gmbs_M0 gm_M0 gds_M0 vdsat_M0 vth_M0  ... 
    """

    def __init__(self, spice_file, warning_msg=False):
        self.spice_file = spice_file
        self.dev_names_mos = (
            'nfet3_01v8',
            'nfet3_01v8_lvt',
            'nfet3_03v3_nvt',
            'nfet3_05v0_nvt',
            'nfet3_20v0',
            'nfet3_g5v0d10v5',
            'nfet3_g5v0d16v0',
            'nfet_01v8',
            'nfet_01v8_esd',
            'nfet_01v8_lvt',
            'nfet_01v8lvt_nf'
            'nfet_01v8_nf',
            'nfet_03v3_nvt',
            'nfet_03v3_nvt_nf',
            'nfet_05v0_nvt',
            'nfet_05v0_nvt_nf',
            'nfet_20v0_iso',
            'nfet_20v0_nvt',
            'nfet_20v0_zvt',
            'nfet_g5v0d10v5',
            'nfet_g5v0d10v5_esd',
            'nfet_g5v0d10v5_nf',
            'nfet_g5v0d10v5_nvt_esd',
            'nfet_g5v0d16v0',
            'nfet_g5v0d16v0_nf',
            'pfet3_01v8',
            'pfet3_01v8',
            'pfet3_01v8',
            'pfet3_20v0',
            'pfet3_g5v0d10v5',
            'pfet3_g5v0d16v0',
            'pfet_01v8',
            'pfet_01v8_hvt',
            'pfet_01v8_hvt_nf',
            'pfet_01v8_lvt',
            'pfet_01v8_lvt_nf',
            'pfet_01v8_nf',
            'pfet_20v0',
            'pfet_g5v0d10v5',
            'pfet_g5v0d10v5_nf',
            'pfet_g5v0d16v0',
            'pfet_g5v0d16v0_nf'
            )
        self.dev_names_r = (
            'res_generic_l1',
            'res_generic_m1',
            'res_generic_m2',
            'res_generic_m3',
            'res_generic_m4',
            'res_generic_m5',
            'res_generic_nd',
            'res_generic_pd',
            'res_generic_po',
            'res_high_po',
            'res_high_po_0p35',
            'res_high_po_0p69',
            'res_high_po_1p41',
            'res_high_po_2p85',
            'res_high_po_5p73',
            'res_iso_pw',
            'res_xhigh_po',
            'res_xhigh_po_0p35',
            'res_xhigh_po_0p69',
            'res_xhigh_po_1p41',
            'res_xhigh_po_2p85',
            'res_xhigh_po_5p73'
            )
        self.dev_names_c = (
            'cap_mim_m3_1',
            'cap_mim_m3_2',
            'cap_var_hvt',
            'cap_var_lvt',
            'vpp_cap'
            )
        if warning_msg == True:
            for i in self.ckt_hierarchy:
                dev_name = i[2]
                dev_type = i[3]
                if dev_type == 'm' or dev_type == 'M':
                    if dev_name not in self.dev_names_mos:
                        print(f'This MOS is not in sky130 PDK. A valid device name can be {self.dev_names_mos}.')    
                elif dev_type == 'r' or dev_type == 'R':
                    if dev_name not in self.dev_names_r:
                        print(f'This resistor is not in sky130 PDK. A valid device name can be {self.dev_names_r}.')    
                elif dev_type == 'c' or dev_type == 'C':
                    if dev_name not in self.dev_names_c:
                        print(f'This capacitor is not in sky130 PDK. A valid device name can be {self.dev_names_c}.')    
                elif dev_type == 'i' or dev_type == 'I':
                    None
                elif dev_type == 'v' or dev_type == 'V':
                    None
                else:
                    print('You have a device type that cannot be found here...')
        # 45 attributes for mos
        self.params_mos = (
            'gmbs',
            'gm',
            'gds',
            'vdsat',
            'vth',
            'id',
            'ibd',
            'ibs',
            'gbd',
            'gbs',
            'isub',
            'igidl',
            'igisl',
            'igs',
            'igd',
            'igb',
            'igcs',
            'vbs',
            'vgs',
            'vds',
            'cgg',
            'cgs',
            'cgd',
            'cbg',
            'cbd',
            'cbs',
            'cdg',
            'cdd',
            'cds',
            'csg',
            'csd',
            'css',
            'cgb',
            'cdb',
            'csb',
            'cbb',
            'capbd',
            'capbs',
            #'qg',
            #'qb',
            #'qs',
            #'qinv',
            #'qdef',
            #'gcrg',
            #gtau'
            )
        # 20 attributes for r
        self.params_r = (
            'r',
            'ac',
            'temp',
            'dtemp',
            'l',
            'w',
            'm',
            'tc',
            'tc1',
            'tc2',
            'scale',
            'noise',
            'i',
            'p',
            'sens_dc',
            'sens_real',
            'sens_imag',
            'sens_mag',
            'sens_ph',
            'sens_cplx'
            )
        # 18 attributes for c
        self.params_c = (
            'capacitance',
            'cap',
            'c',
            'ic',
            'temp',
            'dtemp',
            'w',
            'l',
            'm',
            'scale',
            'i',
            'p',
            'sens_dc',
            'sens_real',
            'sens_imag',
            'sens_mag',
            'sens_ph',
            'sens_cplx'
            )
        # 8 attributes for i source
        self.params_i = (
            'dc',
            'acmag',
            'acphase',
            'acreal',
            'acimag',
            'v',
            'p',
            'current'
            )
        # 7 attributes for v source
        self.params_v = (
            'dc',
            'acmag',
            'acphase',
            'acreal',
            'acimag',
            'i',
            'p',
            )
    def gen_dev_params(self, file_name):
        lines = []        
        write_file = ''  
        with open(self.spice_file, "r") as f:
            for line in f:
                if "sky130_fd_pr__" not in line or line.startswith("X") == False:
                    continue

                # XM9 net063 vinp net31 net31 sky130_fd_pr__pfet_01v8 l=mosfet_8_2_l_gm1_pmos w='mosfet_8_2_w_gm1_pmos*1'  m=mosfet_8_2_m_gm1_pmos  
                # XC1 net049 vout sky130_fd_pr__cap_mim_m3_1 W=30 L=30 MF=M_C1 m=M_C1
                data = line.strip().split()
                symbol_name = data[0]   
                subckt = 'x1' + '.' + symbol_name.lower()   
                # dev_name = i[2]    
                if symbol_name.startswith("XM"):
                    dev_name = data[5].replace("sky130_fd_pr__","")
                    dev_type = 'm'

                elif symbol_name.startswith("XC"):
                    dev_name = data[3].replace("sky130_fd_pr__","")
                    dev_type = 'c'


                if dev_type == 'm' or dev_type == 'M':
                    for param in self.params_mos:  
                        if subckt == '':           
                            raise ValueError('In this PDK, transistor is instantiated as a subckt! Subckt is missing here.')
                        else:
                            if dev_name in self.dev_names_mos:
                                # e.g: let gm_M0 = @m.x1.XM0.msky130_fd_pr__pfet_01v8[gm]
                                line = f'let {param}_{symbol_name}=@m.{subckt}.msky130_fd_pr__{dev_name}[{param}]'
                            else:
                                raise ValueError('This device is not defined in this PDK.')
                        lines.append(line)
                        write_file = write_file + f'{param}_{symbol_name} '
                    lines.append('')   
                elif dev_type == 'r' or dev_type == 'R':
                    for param in self.params_r:
                        if subckt == '':
                            raise ValueError('In this PDK, resistor is instantiated as a subckt! Subckt is missing here.')
                        else:               
                            if dev_name in self.dev_names_r:
                                raise ValueError('it is not straightforward to extract resistance info from this PDK, \
                                                so for resistance just use Rsheet * L / W / M for approximation. Remove the resistors from the ckt_hierarchy.')
                            else:
                                raise ValueError('This device is not defined in this PDK.')
                        lines.append(line)
                        write_file = write_file + f'{param}_{symbol_name} '
                    lines.append('')    
                elif dev_type == 'c' or dev_type == 'C':
                    for param in self.params_c:
                        if subckt == '':   
                            raise ValueError('In this PDK, capacitor is instantiated as a subckt! Subckt is missing here.')
                        else:
                            if dev_name in self.dev_names_c:
                                line = f'let {param}_{symbol_name}=@c.{subckt}.c1[{param}]'
                            else:
                                raise ValueError('This device is not defined in this PDK.')
                        lines.append(line)
                        write_file = write_file + f'{param}_{symbol_name} '
                    lines.append('')    
                elif dev_type == 'i' or dev_type == 'I':
                    for param in self.params_i:
                        if subckt == '':  
                            line = f'let {param}_{symbol_name}=@{dev_name}[{param}]'
                        else:
                            line = f'let {param}_{symbol_name}=@i.{subckt}.{dev_name}[{param}]'
                        lines.append(line)
                        write_file = write_file + f'{param}_{symbol_name} '
                    lines.append('')    
                elif dev_type == 'v' or dev_type == 'V':
                    for param in self.params_v:
                        if subckt == '':
                            line = f'let {param}_{symbol_name}=@{dev_name}[{param}]'
                        else:
                            line = f'let {param}_{symbol_name}=@v.{subckt}.{dev_name}[{param}]'
                        lines.append(line)
                        write_file = write_file + f'{param}_{symbol_name} '
                    lines.append('')           
                else:
                    None
                
        lines.append(f'write {file_name} ' + write_file)   
        return lines  
            

            
if __name__ == '__main__':

    dev_params_script = DeviceParams("Leung_NMCF.cir").gen_dev_params(file_name='Leung_NMCF_region')
    
    with open('AMP_NMCF_dev_params.spice', 'w') as f:
        for line in dev_params_script:
            f.write(f'{line}\n')                        


# fmt: on
