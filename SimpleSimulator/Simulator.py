import math
import sys

# Memory array
mem_m = [0 for i in range(128)]

# Operation code dictionary
op_c = {}

# Temporary placeholders
t_p = {}

# Register array
reg = [0 for i in range(8)]

# Next program counter
pc_n = -1

# Program counter
pc = -1

# Halt flag
hlt = False

# Trace array 1
trc1 = []

# Trace array 2
trc2 = []


def bin_down(nm: float) -> str:
    """
    Converts a floating-point number between 1 and 252 to binary representation.

    Args:
    nm (float): The floating-point number to convert.

    Returns:
    str: The binary representation of the number.
    """
    if (nm < 1 or nm > 252):
        return "0"
    
    a = str(nm)
    init = ""
    fnl = ""
    flag = True
    
    for i in a:
        if (i == '.'):
            flag = False
        if (flag):
            init += i
        else:
            fnl += i
    
    if (flag):
        return "0"
    
    init = str(bin(int(init))[2::])
    fnl = float(fnl)
    temp = ""
    
    while (fnl != 0):
        fnl *= 2
        temp += str(int(fnl))
        fnl = fnl - int(fnl)
    
    if (len(init) > 8 or init == "0"):
        return "0"
    
    if (len(init) - 1 + len(temp) > 5 and temp != ""):
        return "0"
    
    rslt = ""
    x = len(bin(len(init) - 1)[2::])
    
    for i in range(3 - x):
        rslt += "0"
    
    rslt += bin(len(init) - 1)[2::] + init[1::] + temp
    
    for i in range(8 - len(rslt)):
        rslt += "0"
    
    return rslt[:8:]


def dec(nm: str) -> float:
    """
    Converts a binary representation to a floating-point number.

    Args:
    nm (str): The binary representation to convert.

    Returns:
    float: The floating-point number.
    """
    xp = int(nm[:3:], 2)
    rslt = "1"
    
    for i in range(xp):
        if (3 + i < 8):
            rslt += nm[i + 3]
        else:
            rslt += "0"
    
    rslt = int(rslt, 2)
    j = -1
    
    for i in range(xp + 3, 8):
        rslt += int(nm[i]) * math.pow(2, j)
        j -= 1
    
    return rslt


# Dictionary for decoding operation codes
dct = {'00000': 'A', '00001': 'A', '00110': 'A', '01010': 'A', '01011': 'A', '01100': 'A', '00000': 'A', '00001': 'A', '00010': 'B', '01000': 'B', '01001': 'B',
       '00010': 'B',  '00011': 'C', '00111': 'C', '01101': 'C', '01110': 'C', '00100': 'D', '00101': 'D', '01111': 'E', '11100': 'E', '11101': 'E', '11111': 'E', '11010': 'F'}


# Global variables for reuse
nm = 0
val = 0


def cst(inpt: int, mylen: int) -> str:
    """
    Converts an integer to a binary representation with leading zeros.

    Args:
    inpt (int): The integer to convert.
    mylen (int): The length of the binary representation.

    Returns:
    str: The binary representation of the integer.
    """
    val: str = bin(inpt)[2::]
    val = (mylen - len(val)) * '0' + val
    return val


def reuse():
    """
    Resets the reuse register.
    """
    reg[7] = 0


def funA(op: str, r1: str, r2: str, r3: str):
    """
    Performs operation A based on the operation code and register values.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    r2 (str): The binary representation of register 2.
    r3 (str): The binary representation of register 3.
    """
    val1 = int(r1, 2)
    val2 = int(r2, 2)
    val3 = int(r3, 2)

    global reg

    if (op == "00000"):
        reuse()
        reg[val1] = reg[val2] + reg[val3]

    elif (op == "00001"):
        reuse()
        
        if reg[val1] >= reg[val2]:
            reg[val3] = reg[val1] - reg[val2]
        else:
            reg[val3] = 0
            reg[7] |= (1 << 3)

    elif (op == "00110"):
        reuse()
        
        reg[val3] = reg[val2] * reg[val1]

        if (reg[val3] >= 65536):
            reg[val3] %= 65536
            reg[7] |= (1 << 3)

    elif (op == "01010"):
        reuse()
        
        for i in range(16):
            if reg[val1] & (1 << i) ^ reg[val2] & (1 << i):
                reg[val3] |= (1 << i)
            elif reg[val3] & (1 << i):
                reg[val3] ^= (1 << i)

    elif (op == "01011"):
        reuse()
        
        temp = 0
        
        for i in range(16):
            if reg[val1] & (1 << i) | reg[val2] & (1 << i):
                reg[val3] |= (1 << i)

    elif (op == "01100"):
        reuse()
        
        temp = 0
        
        for i in range(16):
            if reg[val1] & (1 << i) & reg[val2] & (1 << i):
                temp |= (1 << i)
        
        reg[val3] = temp


def funB(op: str, r1: str, imm: str):
    """
    Performs operation B based on the operation code, register value, and immediate value.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    imm (str): The binary representation of the immediate value.
    """
    val1 = int(r1, 2)
    imm = int(imm, 2)

    if (op == "00010"):
        reuse()
        reg[val1] = imm

    elif (op == "01001"):
        reuse()
        reg[val1] = reg[val1] << imm

    elif (op == "01000"):
        reuse()
        reg[val1] = reg[val1] >> imm


def funC(op: str, r1: str, r2: str):
    """
    Performs operation C based on the operation code and register values.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    r2 (str): The binary representation of register 2.
    """
    val1 = int(r1, 2)
    val2 = int(r2, 2)
    
    if val1 == "111":
        reg[val1] = "001"
        
    if val2 == "111":
        reg[val2] = "001"

    if (op == "00011"):
        reg[val2] = reg[val1]
        reuse()

    elif (op == "00111"):
        reuse()
        reg[0] = reg[val1] // reg[val2]
        reg[1] = reg[val1] % reg[val2]

    elif (op == "01101"):
        reg[val2] = reg[val1]
        
        for i in range(16):
            reg[val2] ^= (1 << i)

    elif (op == "01110"):
        reg[7] = 2
        
        if (reg[val1] > reg[val2]):
            reg[7] = 2
        elif (reg[val1] < reg[val2]):
            reg[7] = 4
        elif (reg[val1] == reg[val2]):
            reg[7] = 1
        
        reg[7] = 2


def funD(op: str, r1: str, mem_addr: str):
    """
    Performs operation D based on the operation code, register value, and memory address.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    mem_addr (str): The binary representation of the memory address.
    """
    val1 = int(r1, 2)
    val_mem = int(mem_addr, 2)

    if (op == "00100"):
        new_m(val_mem)
        reg[val1] = mem_m[val_mem]
        reuse()
        return

    elif (op == "00101"):
        new_m(val_mem)
        mem_m[val_mem] = reg[val1]
        reuse()
        return


def funE(op: str, mem_addr: str):
    """
    Performs operation E based on the operation code and memory address.

    Args:
    op (str): The operation code.
    mem_addr (str): The binary representation of the memory address.
    """
    global pc_n
    val_mem = int(mem_addr, 2)

    if (op == "01111"):
        pc_n = val_mem - 1
        reuse()

    elif (op == "11100"):
        if (reg[7] == 4 or reg[7] == 12):
            pc_n = val_mem - 1
        reuse()

    elif (op == "11101"):
        if (reg[7] == 2 or reg[7] == 10):
            pc_n = val_mem - 1
        reuse()

    elif (op == "11111"):
        if (reg[7] == 1 or reg[7] == 9):
            pc_n = val_mem - 1
        reuse()


def printop1(op: str, r1: str, r2: str, r3: str):
    """
    Prints the operation and register values for trace array 1.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    r2 (str): The binary representation of register 2.
    r3 (str): The binary representation of register 3.
    """
    op_name = op_c[op]
    trc1.append(op_name + " R" + str(int(r1, 2)) + ", R" + str(int(r2, 2)) + ", R" + str(int(r3, 2)))


def printop2(op: str, r1: str, imm: str):
    """
    Prints the operation and register values for trace array 2.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    imm (str): The binary representation of the immediate value.
    """
    op_name = op_c[op]
    trc2.append(op_name + " R" + str(int(r1, 2)) + ", " + str(int(imm, 2)))


def printop3(op: str, r1: str, r2: str):
    """
    Prints the operation and register values for trace array 3.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    r2 (str): The binary representation of register 2.
    """
    op_name = op_c[op]
    trc1.append(op_name + " R" + str(int(r1, 2)) + ", R" + str(int(r2, 2)))


def printop4(op: str, r1: str, mem_addr: str):
    """
    Prints the operation and register values for trace array 4.

    Args:
    op (str): The operation code.
    r1 (str): The binary representation of register 1.
    mem_addr (str): The binary representation of the memory address.
    """
    op_name = op_c[op]
    trc2.append(op_name + " R" + str(int(r1, 2)) + ", " + str(int(mem_addr, 2)))


def printop5(op: str, mem_addr: str):
    """
    Prints the operation and register values for trace array 5.

    Args:
    op (str): The operation code.
    mem_addr (str): The binary representation of the memory address.
    """
    op_name = op_c[op]
    trc2.append(op_name + " " + str(int(mem_addr, 2)))


def new_m(addr: int):
    """
    Extends the memory array if the memory address is out of bounds.

    Args:
    addr (int): The memory address.
    """
    global mem_m
    
    if (addr >= len(mem_m)):
        mem_m.extend([0] * (addr - len(mem_m) + 1))


# Main execution loop
while (not hlt):
    pc += 1

    if (pc >= len(op_c)):
        break

    inst = op_c[pc]
    op = inst[0]
    r1 = inst[1]
    r2 = inst[2]
    r3 = inst[3]
    imm = inst[4]
    mem_addr = inst[5]

    if (op == "A"):
        funA(op, r1, r2, r3)
        printop1(op, r1, r2, r3)

    elif (op == "B"):
        funB(op, r1, imm)
        printop2(op, r1, imm)

    elif (op == "C"):
        funC(op, r1, r2)
        printop3(op, r1, r2)

    elif (op == "D"):
        funD(op, r1, mem_addr)
        printop4(op, r1, mem_addr)

    elif (op == "E"):
        funE(op, mem_addr)
        printop5(op, mem_addr)

    nm += 1

    if (nm >= 5):
        nm = 0
        pc_n = pc + 1

    if (pc_n < pc):
        hlt = True

    pc = pc_n


# Print trace array 1
for i in range(len(trc1)):
    print("Trace 1: " + trc1[i])

# Print trace array 2
for i in range(len(trc2)):
    print("Trace 2: " + trc2[i])
