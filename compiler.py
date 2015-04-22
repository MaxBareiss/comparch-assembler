import intelhex
import sys
import re

ih = intelhex.IntelHex()
fp = 0

with open(sys.argv[1],'r') as file:
    i = 0
    for line in file:
        i = i + 1
        found = False
        match = re.search('^NOP',line)
        if match is not None:
            ih[fp] = 0
            ih[fp+1] = 0
            fp = fp+2
            continue
        match = re.search('^([A-Z]+)\s*R([0-7])\s*$',line) # Things with 1 argument
        if match is not None:
            groups = match.groups()
            if groups[0] == 'CLR':
                ih[fp] = (0x40 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6)%256
                fp = fp+2
            elif groups[0] == 'SET':
                ih[fp] = (0x5E | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6)%256
                fp = fp+2
            elif groups[0] == 'JMPR':
                ih[fp] = (0x9A | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6)%256
                fp = fp+2
            elif groups[0] == 'IN':
                ih[fp] = (0x84 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6)%256
                fp = fp+2
            elif groups[0] == 'OUT':
                ih[fp] = (0x86 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6)%256
                fp = fp+2
            elif groups[0] == 'DIR':
                ih[fp] = (0x88 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6)%256
                fp = fp+2
            else:
                print "Syntax error line ",i
            continue
        match = re.search('^([A-Z]+)\s*R([0-7])\s*,\s*R([0-7])\s*$',line) # Things with 2 arguments
        if match is not None:
            groups = match.groups()
            if groups[0] == 'INC':
                ih[fp] = (0x60 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3)%256
                fp = fp+2
            elif groups[0] == 'DEC':
                ih[fp] = (0x64 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3)%256
                fp = fp+2
            elif groups[0] == 'MOVA':
                ih[fp] = (0x58 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3)%256
                fp = fp+2
            elif groups[0] == 'MOVB':
                ih[fp] = (0x54 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]))%256
                fp = fp+2
            elif groups[0] == 'SHR':
                ih[fp] = (0x72 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3)%256
                fp = fp+2
            elif groups[0] == 'SHL':
                ih[fp] = (0x70 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3)%256
                fp = fp+2
            elif groups[0] == 'NOT':
                ih[fp] = (0x46 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3)%256
                fp = fp+2
            else:
                print "Syntax error line ",i
            continue
        match = re.search('^([A-Z]+)\s*R([0-7])\s*,\s*R([0-7])\s*,\s*R([0-7])\s*$',line) # Things with 3 arguments
        if match is not None:
            groups = match.groups()
            if groups[0] == 'ADD':
                ih[fp] = (0x68 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3 | int(groups[3]))%256
                fp = fp+2
            elif groups[0] == 'SUB':
                ih[fp] = (0x6C | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3 | int(groups[3]))%256
                fp = fp+2
            elif groups[0] == 'AND':
                ih[fp] = (0x50 | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3 | int(groups[3]))%256
                fp = fp+2
            elif groups[0] == 'OR':
                ih[fp] = (0x5C | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3 | int(groups[3]))%256
                fp = fp+2
            elif groups[0] == 'XOR':
                ih[fp] = (0x4C | (int(groups[1]) & 4 == 4))%256
                ih[fp+1] = (int(groups[1]) << 6 | int(groups[2]) << 3 | int(groups[3]))%256
                fp = fp+2
            else:
                print "Syntax error line ",i
            continue
        match = re.search('^([A-Z]+)\s*([\-0-9]+)$',line) # Things with a constant
        if match is not None:
            groups = match.groups()
            if groups[0] == 'JMPI':
                ih[fp] = (0x98 | (int(groups[1]) & 1))%256
                ih[fp+1] = int(groups[1]) & 0xFF
                fp = fp+2
            else:
                print "Syntax error line ",i
            continue
        match = re.search('^([A-Z]+)\s*R([0-7])\s*,\s*([\-0-9]+)$',line) # Things with 1 argument and a constant
        if match is not None:
            groups = match.groups()
            if groups[0] == 'ADDI':
                ih[fp] = (0x08 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'SUBI':
                ih[fp] = (0x10 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'ANDI':
                ih[fp] = (0x18 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'ORI':
                ih[fp] = (0x28 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'XORI':
                ih[fp] = (0x30 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'LDM':
                ih[fp] = (0xA0 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'STM':
                ih[fp] = (0xA8 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'BRZ':
                ih[fp] = (0xB0 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'BRN':
                ih[fp] = (0xB8 | int(groups[1]))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            elif groups[0] == 'LDI':
                ih[fp] = (0xC0 | int(groups[1]) << 3 | ((int(groups[2]) & 0x700) >> 8))%256
                ih[fp+1] = int(groups[2]) & 0xFF
                fp = fp+2
            else:
                print "Syntax error line ",i
            continue
        print "Invalid line ",i

ih.tofile('programmem.hex','hex')