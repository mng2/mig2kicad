from skidl import *
import parseXDC

#########################
# Part Setup

art = Part('FPGA_Xilinx_Artix7','XC7A200T-FFG1156',footprint='BGA-1156_34x34_35.0x35.0mm_Pitch1.0mm')

mem = Part('ddr3-sdram-96fbga-8gb','DDR3-SDRAM-96FBGA-8Gb',footprint='FBGA-96-DDR3-SDRAM')

#########################
# Import XDC

r = parseXDC.toList('mig_7series_32.xdc')
d = parseXDC.makeDict(r)

#########################
# Connect nets

dgnd = Net('DGND')
art['GND'] += dgnd     # connect all FPGA ground pins!

mem['VSS'] += dgnd

#for n in d:
#    if 'PACKAGE_PIN' in d[n]:
#        print(parseXDC.decomp(n))

dq = Bus('ddr3_dq', 16)
for i in range(16):
    dq[i] += mem['DQ'+str(i)]
    n = 'ddr3_dq['+str(i)+']'
    pin = d[n]['PACKAGE_PIN']
    dq[i] += art[pin]

addr = Bus('ddr3_addr', 14)
for i in range(14):
    addr[i] += mem['ADDR'+str(i)]
    n = 'ddr3_addr['+str(i)+']'
    pin = d[n]['PACKAGE_PIN']
    addr[i] += art[pin]

ba = Bus('ddr3_ba', 3)
for i in range(3):
    ba[i] += mem['BA'+str(i)]
    n = 'ddr3_ba['+str(i)+']'
    pin = d[n]['PACKAGE_PIN']
    ba[i] += art[pin]
    
rasn = Net('ddr3_ras_n')
rasn += mem['~RAS']
rasn += art[ d['ddr3_ras_n']['PACKAGE_PIN'] ]

casn = Net('ddr3_cas_n')
casn += mem['~CAS']
casn += art[ d['ddr3_cas_n']['PACKAGE_PIN'] ]

wen = Net('ddr3_we_n')
wen += mem['~WE']
wen += art[ d['ddr3_we_n']['PACKAGE_PIN'] ]

resetn = Net('ddr3_reset_n')
resetn += mem['~RESET']
resetn += art[ d['ddr3_reset_n']['PACKAGE_PIN'] ]

cke = Net('ddr3_cke[0]')
cke += mem['CKE']
cke += art[ d['ddr3_cke[0]']['PACKAGE_PIN'] ]

odt = Net('ddr3_odt[0]')
odt += mem['ODT']
odt += art[ d['ddr3_odt[0]']['PACKAGE_PIN'] ]

ldqsp = Net('ddr3_dqs_p[0]')
ldqsp += mem['LDQS']
ldqsp += art[ d['ddr3_dqs_p[0]']['PACKAGE_PIN'] ]

ldqsn = Net('ddr3_dqs_n[0]')
ldqsn += mem['~LDQS']
ldqsn += art[ d['ddr3_dqs_n[0]']['PACKAGE_PIN'] ]

udqsp = Net('ddr3_dqs_p[1]')
udqsp += mem['UDQS']
udqsp += art[ d['ddr3_dqs_p[1]']['PACKAGE_PIN'] ]

udqsn = Net('ddr3_dqs_n[1]')
udqsn += mem['~UDQS']
udqsn += art[ d['ddr3_dqs_n[1]']['PACKAGE_PIN'] ]

ckp = Net('ddr3_ck_p[0]')
ckp += mem['CK']
ckp += art[ d['ddr3_ck_p[0]']['PACKAGE_PIN'] ]

ckn = Net('ddr3_ck_n[0]')
ckn += mem['~CK']
ckn += art[ d['ddr3_ck_n[0]']['PACKAGE_PIN'] ]

#########################
# Generate netlist

generate_netlist()
