class Field:
    NONE = -1

    # Unimplemented Fields
    WIRI = 1
    WPRI = 2

    # Implemented Fields
    WARL = 3
    # WARL => What is the function mapping write values to read values?
    WLRL = 4
    # WLRL => What are the legal values?

    # My Notation
    REG = 5 # warl type
    MASKED_REG = 6 # warl type
    DERIVED = 7

    def __init__(self, name, width, opt = -1):
        self.name = name
        self.width = width
        self.opt = opt
    def holds_state(self):
        """Return True if this Field holds useful state."""
        if self.opt == Field.WIRI or self.opt == Field.WPRI:
            return False
        else:
            return True
    def __str__(self):
        opt = { -1 : 'Field.NONE',
                1 : 'Field.WIRI',
                2 : 'Field.WPRI',
                3 : 'Field.WARL',
                4 : 'Field.WLRL',
                5 : 'Field.REG',
                6 : 'Field.MASKED_REG',
                7 : 'Field.DERIVED'}[self.opt]
        if self.opt != -1:
            return "Field('%s', %d, %s)" % (self.name, self.width, opt)
        else:
            return "Field('%s', %d)" % (self.name, self.width)

class ReadOnly:
    """Wrap Field to make it read only."""
    def __init__(self, field):
        self.field = field
    def __getattr__(self, attr):
        return self.field.__getattribute__(attr)
    def __str__(self):
        return 'ReadOnly(%s)' % (str(self.field))

def WIRI(width):
    """Create Write-Invalid Read-Invalid field."""
    if width < 1:
        raise ValueError("Width must be at least 1")
    return Field('', width, Field.WIRI)

def WPRI(width = -1):
    """Create Write-Preserve Read-Invalid field."""
    if width < 1:
        raise ValueError("Width must be at least 1")
    return Field('', width, Field.WPRI)

class CSR:
    """RISC-V Control and Status Register"""
    def __init__(self, name, address, *fields):
        self.name = name
        self.address = address
        if len(fields) == 1 and isinstance(fields[0], tuple):
            self.fields = fields[0]
        else:
            self.fields = fields
    def get_width(self):
        width = 0
        for field in self.fields:
            width += field.width
        return width
    def __str__(self):
        return "CSR('%s', %s, %s)" % (self.name, hex(self.address), ', '.join(list(map(str, self.fields))))
