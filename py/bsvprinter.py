from csrs import ReadOnly

def bsv_field_init(field):
    """Construct string for initializing a field in BSV"""
    if field.holds_state():
        return 'Reg#(Bit#(%d)) %s_field <- mkReg(0)' % (field.width, field.name)
    else:
        return None

def bsv_field_ref(field):
    if isinstance(field, ReadOnly):
        return 'readOnlyReg(%s_field)' % (field.name)
    elif field.holds_state():
        return field.name + '_field'
    else:
        return "readOnlyReg(%d'b0)" % (field.width)

def bsv_csr_init(csr):
    fields = ', '.join(map(bsv_field_ref, csr.fields))
    if len(csr.fields) == 1:
        return 'Reg#(Bit#(%d)) %s = %s;' % (csr.get_width(), csr.name, fields)
    else:
        return 'Reg#(Bit#(%d)) %s = concatReg%d(%s);' % (csr.get_width(), csr.name, len(csr.fields), fields)

def bsv_csr_ref(csr):
    return csr.name

