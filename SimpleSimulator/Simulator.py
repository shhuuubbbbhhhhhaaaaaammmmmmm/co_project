import math
import sys

mem_m = [0 for i in range(128)]

op_c = {}

t_p = {}

reg = [0 for i in range(8)]

pc_n = -1

pc = -1

hlt = False

trc1 = []

trc2 = []


def bin_down(nm: float) -> str:

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
        fnl = fnl-int(fnl)
    if (len(init) > 8 or init == "0"):
        return "0"
    if (len(init)-1+len(temp) > 5 and temp != ""):
        return "0"
    rslt = ""
    x = len(bin(len(init)-1)[2::])
    for i in range(3-x):
        rslt += "0"
    rslt += bin(len(init)-1)[2::]+init[1::]+temp
    for i in range(8-len(rslt)):
        rslt += "0"
    return rslt[:8:]


def dec(nm: str) -> float:
    xp = int(nm[:3:], 2)
    rslt = "1"
    for i in range(xp):
        if (3+i < 8):
            rslt += nm[i+3]
        else:
            rslt += "0"
    rslt = int(rslt, 2)
    j = -1
    for i in range(xp+3, 8):
        rslt += int(nm[i])*math.pow(2, j)
        j -= 1
    return rslt


dct = {'00000': 'A', '00001': 'A', '00110': 'A', '01010': 'A', '01011': 'A', '01100': 'A', '00000': 'A', '00001': 'A', '00010': 'B', '01000': 'B', '01001': 'B',
       '00010': 'B',  '00011': 'C', '00111': 'C', '01101': 'C', '01110': 'C', '00100': 'D', '00101': 'D', '01111': 'E', '11100': 'E', '11101': 'E', '11111': 'E', '11010': 'F'}

                # flags = {"overflow": False, "Less than Flag": False, "Greater than flag": False,"Equal to flag": False}

                # FV(7) , FL(8) , FG(9) , FE(10) is flag reg for overflow, less than, greater than, equal to

nm = 0
val = 0


def cst(inpt: int, mylen: int) -> str:
    val: str = bin(inpt)[2::]
    val = (mylen - len(val))*'0' + val
    return val


def reuse():
    reg[7] = 0


def funA(op: str, r1: str, r2: str, r3: str):

    val1 = int(r1, 2)
    val2 = int(r2, 2)
    val3 = int(r3, 2)

    global reg
    
    if (op == "00000"):
        reuse()
        reg[val1] = reg[val2]+reg[val3]

        
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
        reg[0] = reg[val1]//reg[val2]
        reg[1] = reg[val1] % reg[val2]

    elif (op == "01101"):
        reg[val2] = reg[val1]
        for i in range(16):
            reg[val2] ^= (1 << i)

    elif (op == "01110"):
        reg[7]=2
        
        if (reg[val1] > reg[val2]):
            # reg[7] |= (1 << 1)
            reg[7]=2
        elif (reg[val1] < reg[val2]):
            # reg[7] |= (1 << 2)
            reg[7]=4
        elif (reg[val1] == reg[val2]):
            # reg[7] |= (1 << 0)
            reg[7] = 1
        reg[7]=2
        

def funD(op: str, r1: str, mem_addr: str):

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


def printop1(op: str, r1: str, imm: str):
    val1 = int(r1, 2)

    if op == "01000":
        print(f"{val1}: {reg[val1]}")
        reuse()

    elif op == "01001":
        immediate = int(imm, 2)
        print(f"{immediate}")
        reuse()


def printop2(op: str, r1: str, imm: str):
    val1 = int(r1, 2)

    if op == "00111":
        print(f"{val1}: {reg[val1]}")
        reuse()

    elif op == "00011":
        immediate = int(imm, 2)
        print(f"{immediate}")
        reuse()


def printop3(op: str, r1: str, imm: str):
    val1 = int(r1, 2)

    if op == "00101":
        print(f"{val1}: {reg[val1]}")
        reuse()

    elif op == "00111":
        immediate = int(imm, 2)
        print(f"{immediate}")
        reuse()


def mem_ld():

    for i in range(256):
        try:
            inpt = input()
            if inpt == '':
                break
            mem_m[i] = int(inpt, 2)
        except EOFError:
            break
        except Exception:
            break
    return


def start(inst: int):
    k = cst(inst, 16)
    op = k[0:5]
    mytype = dct[op]
    global hlt
    if (mytype == 'A'):
        funA(op, k[7:10], k[10:13], k[13:16])

    elif (mytype == 'B'):
        funB(op, k[6:9], k[9:16])

    elif (mytype == 'C'):
        funC(op, k[11:14], k[14::])

    elif (mytype == 'D'):
        funD(op, k[6:9], k[9:16])

    elif (mytype == 'E'):
        funE(op, k[9::])

    elif (op == '11010'):
        hlt = True
        reuse()


def exit_s(pc: int):
    print(cst(pc, 7), end='        ')
    for i in reg:
        print(cst(i, 16), end=' ')
    print()
    return


def exit_m():
    for line in mem_m:
        print(cst(line, 16))
    return


def new_c(pc: int):
    trc1.append(pc)
    return


def new_m(mem_m: int):
    trc2.append(mem_m)
    return


def main():
    mem_ld()
    while (not hlt):
        global pc
        global pc_n
        pc += 1

        if (pc < len(mem_m)):
            inst = mem_m[pc]
            start(inst)
            exit_s(pc)
            new_c(pc)
            if (pc_n != -1):
                pc = pc_n
                pc_n = -1

    exit_m()
    return

main()
