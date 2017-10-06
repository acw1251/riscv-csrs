import sys
import csrs
import bsvprinter

use_symbolic = True

if use_symbolic:
    from symb import symbolic, symbol, memoize_compute, compute, collect, cond
    all_symb_fields = []
    all_symb_csrs = []
    all_real_fields = []
    all_real_csrs = []

    Field = collect(all_symb_fields)(symbolic(collect(all_real_fields)(csrs.Field)))
    CSR = collect(all_symb_csrs)(symbolic(collect(all_real_csrs)(csrs.CSR)))
    WIRI = symbolic(csrs.WIRI)
    WPRI = symbolic(csrs.WPRI)
    ReadOnly = symbolic(csrs.ReadOnly)

    xlen = symbol('xlen')
    maxxlen = xlen
else:
    from symb import collect

    def cond(condition, ifTrue, ifFalse):
        if condition:
            return ifTrue
        else:
            return ifFalse

    all_real_fields = []
    all_real_csrs = []

    Field = collect(all_real_fields)(csrs.Field)
    CSR = collect(all_real_csrs)(csrs.CSR)
    WIRI = csrs.WIRI
    WPRI = csrs.WPRI
    ReadOnly = csrs.ReadOnly

    xlen = 64
    maxxlen = 64

# misa fields
mxl = Field("mxl", 2, Field.WARL)
extensions = Field("extensions", 26, Field.WARL)

# mstatus fields
sxl = Field("sxl", 2)
uxl = Field("uxl", 2)
tsr = Field("tsr", 1)
tw = Field("tw", 1)
tvm = Field("tvm", 1)
mxr = Field("mxr", 1)
sum = Field("sum", 1)
mprv = Field("mprv", 1)
xs = Field("xs", 2)
fs = Field("fs", 2)
mpp = Field("mpp", 2)
spp = Field("spp", 1)
mpie = Field("mpie", 1)
spie = Field("spie", 1)
upie = Field("upie", 1)
mie = Field("mie", 1)
sie = Field("sie", 1)
uie = Field("uie", 1)
sd = Field("sd", 1, Field.DERIVED) # Derived from fs and xs !((fs == 0) && (xs == 0))

# mtvec fields
mtvec_base = Field("mtvec_base", maxxlen-2)
mtvec_mode = Field("mtvec_mode", 2)

# medeleg fields
medeleg = Field("medeleg", maxxlen, Field.WARL)

# mideleg fields
mideleg = Field("mideleg", maxxlen, Field.WARL)

# mip fields
meip = Field("meip", 1)
seip = Field("seip", 1)
ueip = Field("ueip", 1)
mtip = Field("mtip", 1)
stip = Field("stip", 1)
utip = Field("utip", 1)
msip = Field("msip", 1)
ssip = Field("ssip", 1)
usip = Field("usip", 1)

# mie fields
meie = Field("meie", 1)
seie = Field("seie", 1)
ueie = Field("ueie", 1)
mtie = Field("mtie", 1)
stie = Field("stie", 1)
utie = Field("utie", 1)
msie = Field("msie", 1)
ssie = Field("ssie", 1)
usie = Field("usie", 1)

# mcycle fields
mcycle = Field("mcycle", 64, Field.DERIVED)
 
# minstret fields
minstret = Field("minstret", 64, Field.DERIVED)

# mcounteren fields
m_hpm = Field("m_hpm", 29, Field.WARL)
m_ir = Field("m_ir", 1, Field.WARL)
m_tm = Field("m_tm", 1, Field.WARL)
m_cy = Field("m_cy", 1, Field.WARL)
# Technically this is always a 32-bit CSR that gets sign extended for 64-bit

# mscratch fields
mscratch = Field("mscratch", maxxlen)

# mepc fields
mepc = Field("mepc", maxxlen) # bottom 1 or 2 bits should be read-only

# mcause fields
mcause_interrupt = Field("mcause_interrupt", 1)
mcause_code = Field("mcause_code", maxxlen-1, Field.WLRL)
 
# mtval fields
mtval = Field("mtval", maxxlen)

# supervisor-mode CSR fields

# sstatus fields
# no extra fields

# sip fields
# no extra fields

# sie fields
# no extra fields

# scounteren fields
s_hpm = Field("s_hpm", 29, Field.WARL)
s_ir = Field("s_ir", 1, Field.WARL)
s_tm = Field("s_tm", 1, Field.WARL)
s_cy = Field("s_cy", 1, Field.WARL)

# sscratch fields
sscratch = Field("sscratch", maxxlen)

# sepc fields
sepc = Field("sepc", maxxlen) # bottom 1 or 2 bits should be read-only

# scause fields
scause_interrupt = Field("scause_interrupt", 1)
scause_code = Field("scause_code", maxxlen-1, Field.WLRL)

# stval fields
stval = Field("stval", maxxlen)

# satp fields
vm_mode = Field("vm_mode", cond(maxxlen != 32, 4, 1))
asid = Field("asid", cond(maxxlen != 32, 16, 9))
ppn = Field("ppn", cond(maxxlen != 32, 44, 22))

# user-mode CSR fields

# fcsr fields
fflags = Field("fflags", 5)
frm = Field("frm", 3)

# CSRs

CSR("misa", 0x301, mxl, WIRI(xlen-28), extensions)
CSR("mstatus", 0x300,
    cond( xlen != 32,
        (ReadOnly(sd), WPRI(xlen-37), sxl, uxl, WPRI(9), tsr, tw, tvm, mxr, sum, mprv,
        xs, fs, mpp, WPRI(2), spp, mpie, WPRI(1), spie, upie, mie, WPRI(1), sie, uie),
        (ReadOnly(sd), WPRI(8), tsr, tw, tvm, mxr, sum, mprv,
        xs, fs, mpp, WPRI(2), spp, mpie, WPRI(1), spie, upie, mie, WPRI(1), sie, uie)
    ))

CSR("mtvec", 0x305,
        mtvec_base, mtvec_mode)
CSR("medeleg", 0x302, medeleg)
CSR("mideleg", 0x302, mideleg)
CSR("mip", 0x344,
        WIRI(xlen-12), ReadOnly(meip), WIRI(1), seip, ueip, ReadOnly(mtip), WIRI(1), stip, utip, ReadOnly(msip), WIRI(1), ssip, usip)
CSR("mie", 0x304,
        WPRI(xlen-12), meie, WPRI(1), seie, ueie, mtie, WPRI(1), stie, utie, msie, WPRI(1), ssie, usie)
CSR("mcycle", 0xB00, ReadOnly(mcycle))
CSR("minstret", 0xB02, ReadOnly(minstret))
# Technically this is always a 32-bit CSR that gets zero extended for 64-bit
CSR("mcounteren", 0x306,
        m_hpm, m_ir, m_tm, m_cy)
CSR("mscratch", 0x340, mscratch)
CSR("mepc", 0x341, mepc)
CSR("mcause", 0x342, mcause_interrupt, mcause_code)
CSR("mtval", 0x343, mtval)
CSR("sstatus", 0x100,
        ReadOnly(sd), WPRI(xlen-35), uxl, WPRI(12), mxr, sum, WPRI(1),
        xs, fs, WPRI(4), spp, WPRI(2), spie, upie, WPRI(2), sie, uie)
# XXX: THIS DOES NOT FULLY MATCH THE SPECIFICATION
# XXX: THIS IS ALSO ANDED WITH THE MIDELEG CSR
CSR("sip", 0x144,
        WIRI(xlen-10), ReadOnly(seip), ueip, WIRI(2), ReadOnly(stip), ReadOnly(utip), WIRI(2), ssip, usip)
# XXX: THIS DOES NOT FULLY MATCH THE SPECIFICATION
# XXX: THIS IS ALSO ANDED WITH THE MIDELEG CSR
CSR("sie", 0x104,
        WPRI(xlen-10), seie, ueie, WPRI(2), stie, utie, WPRI(2), ssie, usie)
# Technically this is always a 32-bit CSR that gets zero extended for 64-bit
CSR("scounteren", 0x106,
        s_hpm, s_ir, s_tm, s_cy)
CSR("sscratch", 0x140, sscratch)
CSR("sepc", 0x141, sepc)
CSR("scause", 0x142, scause_interrupt, scause_code)
CSR("stval", 0x143, stval)
CSR("satp", 0x180, vm_mode, asid, ppn)
CSR("fflags", 0x001, WIRI(xlen-5), fflags)
CSR("frm", 0x002, WIRI(xlen-3), frm)
CSR("fcsr", 0x003, WPRI(xlen-8), frm, fflags)

if use_symbolic:
    print('symbolic example:')
    print('str(vm_mode) = ' + str(vm_mode))
    # if using symbolic operations, evaluate all the CSRs to populate the
    # all_real_csrs list
    for symb_csr in all_symb_csrs:
        compute(symb_csr, { 'xlen' : 64 })

print('\nFields:\n    ' + ('\n    '.join(map(str, all_real_fields))))
print('\nCSRs:\n    ' + ('\n    '.join(map(str, all_real_csrs))))
print('\nBSV:')
print('    \\\\ Field Definitions')
for field in all_real_fields:
    print('    ' + bsvprinter.bsv_field_init(field))
print('    \\\\ CSR Definitions')
for csr in all_real_csrs:
    print('    ' + bsvprinter.bsv_csr_init(csr))
