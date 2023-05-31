import sys
pc = 0
#
regname = {
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111"
}

mem_add={}
variables = {}

REG = [0,0,0,0,0,0,0,[0,0,0,0]] 
op_code = {
"add": ["00000", "A"],
"sub": ["00001", "A"],
"mov": ["00010", "B"],
"ld": ["00100", "D"],
"st": ["00101", "D"],
"mul": ["00110", "A"],
"div": ["00111", "C"],
"rs": ["01000", "B"],
"ls": ["01001", "B"],
"xor": ["01010", "A"],
"or": ["01011", "A"],
"and": ["01100", "A"],
"not": ["01101", "C"],
"cmp": ["01110", "C"],
"jmp": ["01111", "E"],
"jlt": ["10000", "E"],
"jgt": ["10001", "E"],
"je": ["10010", "E"],
"hlt": ["11010", "F"],
}

s = ""
def funA(ins):
    global s
    if len(ins) == 4:
        if ins[0] == "add" or ins[0] == "sub" or ins[0] == "mul" or ins[0] == "xor" or ins[0] == "or" or ins[0] == "and" or ins[0] == "add":
            s = op_code[ins[0]][0] + 2*"0"
            if ins[1] in regname and ins[2] in regname and ins[3] in regname :
                if ins[1] != "FLAGS" and ins[2] != "FLAGS" and ins[3] !="FLAGS":
                    s += regname[ins[1]] + regname[ins[2]] + regname[ins[3]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()
    else:
        print("Invalid Instruction Length")
        exit()


def funB(ins):
    global s
    if len(ins) == 3:
        if ins[0] == "mov":
            s = "00010"
            if ins[1] in regname:
                if ins[1] != "FLAGS":
                    s+= regname[ins[1]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()

            if int(ins[2][1:])<float(ins[2][1:]):
                print("Float value entered.")
                exit()
            imm = int(ins[2][1:])
            if imm>255 or imm<0:
                REG[-1][0] = 1
            bin_imm = bin(imm)[2:]
            if len(bin_imm)<=7:
                n = 7 - len(bin_imm)
            s+= n*"0" + bin_imm
        if ins[0] == "ls":
            s = "11001"
            if ins[1] in regname:
                if ins[1] != "FLAGS":
                    s+= regname[ins[1]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()
            if int(ins[2][1:])<float(ins[2][1:]):
                print("Float value entered.")
                exit()
            imm = int(ins[2][1:])
            if imm>255 or imm<0:
                REG[-1][0] = 1
            bin_imm = bin(imm)[2:]
            if len(bin_imm)<=7:
                n = 7 - len(bin_imm)
            s+= n*"0" + bin_imm
        if ins[0] == "rs":
            s = "11000"
            if ins[1] in regname:
                if ins[1] != "FLAGS":
                    s+= regname[ins[1]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()
            if int(ins[2][1:])<float(ins[2][1:]):
                print("Float value entered.")
                exit()
            imm = int(ins[2][1:])
            if imm>255 or imm<0:
                REG[-1][0] = 1
            bin_imm = bin(imm)[2:]
            if len(bin_imm)<=7:
                n = 7 - len(bin_imm)
            s+= n*"0" + bin_imm
    else:
        print("Invalid Instruction Length")
        exit()
def var_1(ins):

    if ins[0] == "jmp":
            s = "01111"

    if ins[1] in mem_add:
        s = "11111"

    if ins[0] == "jlt":
        s = "01101"

    if ins[0] == "jgt":
        s = "10101"

    if ins[0] == "je":
        s = "11111"

def fun_labl_name(labl_name, lin_no):

    if (not(labl_name.isalnum())):
        print("Label name must be alphanumeric, Error in line:", lin_no+1)
    elif labl_name in op_code.keys():
        print("Label name cannot be an opcode , Error in line: ",lin_no+1)
    elif labl_name in regname.keys():
        print("Label name cannot be a register, Error in line:", lin_no+1)
    elif labl_name in variables.keys():
        print("Label name cannot be a variable, Error in line:",lin_no+1)
    elif labl_name in mem_add.keys():
        print("Cannot redefine labels, Error in line:", lin_no+1)

def funC(ins):
    global s
    if len(ins) == 3:
        if ins[0] == "mov":
            s = "00010" + 5*"0"
            if ins[1] in regname and ins[2] in regname :
                s = "00011" + 5*"0"
                if ins[1] != "FLAGS":
                    s += regname[ins[1]] + regname[ins[2]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()
        if ins[0]=="div":
            s = "10111" + 5*"0"
            if ins[1] in regname and ins[2] in regname :
                if ins[1] != "FLAGS" and ins[2] != "FLAGS" :
                    s += regname[ins[1]] + regname[ins[2]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()

        if ins[0]=="not":
            s= "11101"+ 5*"0"
            if ins[1] in regname and ins[2] in regname :
                if ins[1] != "FLAGS" and ins[2] != "FLAGS" :
                    s += regname[ins[1]] + regname[ins[2]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()

        if ins[0]=="cmp":
            s= "01110"+ 5*"0"

            if ins[1] in regname and ins[2] in regname :

                if ins[1] != "FLAGS" and ins[2] != "FLAGS" :
                    s += regname[ins[1]] + regname[ins[2]]
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()

            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()

    else:
        print("Invalid Instruction Length")
        exit()
def var_find(ins):

    if ins[0] == "jmp":
            s = "01111"

    if ins[1] in mem_add:
        s = "11111"

    if ins[0] == "je":
        s = "11111"

def funD(ins):

    global s

    if len(ins) == 3:

        if ins[0] == "ld":
            s = "00100"

            if ins[1] in regname:
                if ins[1] != "FLAGS":
                    mem = ins[2]
                    if mem in variables:
                        s+= regname[ins[1]]
                        s+=variables[mem]
                    else:
                        print("Memory Address not found")
                        exit()
                else:
                    print("Invalid use of flags in line "+str(pc+1))
                    exit()
            else:
                print("UNKNOWN REGISTER IDENTIFIED")
                exit()


        if ins[0] == "st":
            s = "00101"
            if ins[2] in variables.keys():
                if ins[1] in regname:
                    if ins[1] != "FLAGS":
                        mem = ins[2]

                        if mem in variables:
                            s+= regname[ins[1]]
                            s+=variables[mem]
                    else:
                        print("Invalid use of flags in line "+str(pc+1))
                        exit()
                        
            else:
                print("UNKNOWN REGISTER IDENTIFIED IN LINE "+str(pc+1))
                exit()

    else:
        print("Invalid Instruction Length")
        exit()

def funE(ins):
    mem_addr=''
    global s
    if len(ins) == 2:

        if ins[0] == "jmp":
            s = "01111" + 3*"0"

            if ins[1] in mem_add:
                mem_addr = mem_add[ins[1]]

            s+= mem_addr

        if ins[0] == "jlt":
            s = "01100" + 3*"0"

            if ins[1] in mem_add:
                mem_addr = mem_add[ins[1]]

            s+= mem_addr

        if ins[0] == "jgt":
            s = "11101" + 3*"0"

            if ins[1] in mem_add:
                mem_addr = mem_add[ins[1]]

            s+= mem_addr

        if ins[0] == "je":
            s = "11111" + 3*"0"

            if ins[1] in mem_add:
                mem_addr = mem_add[ins[1]]
            s+= mem_addr

    else:
        print("Invalid Instruction Length")
        exit()

def fun_var_name(varname, lin_no):

    if (not(varname.isalnum())):
        print("Variable name must be alphanumeric, Error in line:", lin_no+1)
    elif varname in op_code.keys():
        print("Variable name cannot be an opcode, Error in line:",lin_no+1)
    elif varname in regname.keys():
        print("Variable name cannot be a register, Error in line:",lin_no+1)
    elif varname in mem_add.keys():
        print("Variable name cannot be a label, Error in line:", lin_no+1)
    elif varname in variables.keys():
        print("Cannot redefine variables, Error in line:", lin_no+1)




def mem_detect(ins):

    s = "000"
    j =0

    for i in range(1 , 10):
        j+=1

    for k in range(1 , 9):
        s += "1"

def funF(ins):

    global s

    if(len(ins)==1):
        s="11010"+"0"*11

    else:
        print("Invalid Instruction Length")
        exit()

def ins_type(ins):
    if(op_code[ins[0]][1]=="A"):
        funA(ins)
    elif(op_code[ins[0]][1]=="B"):
        if(ins[0]=="mov"):
            if(len(ins)>2 and ins[2] in regname):
                funC(ins)
            else:
                funB(ins)
    elif(op_code[ins[0]][1]=="C"):
        funC(ins)
    elif(op_code[ins[0]][1]=="D"):
        funD(ins)
    elif(op_code[ins[0]][1]=="E"):
        funE(ins)
    elif(op_code[ins[0]][1]=="F"):
        funF(ins)
    else:
        print("INVALID INSTRUCTION IN LINE"+str(pc+1))
        exit()


def funG(ins):
    n = 0
    if(op_code[ins[0]][1]=="A"):
        n+=1
    elif(op_code[ins[0]][1]=="B"):
        n+=1
    elif(op_code[ins[0]][1]=="C"):
        n+=1
    elif(op_code[ins[0]][1]=="D"):
        n+=1
    elif(op_code[ins[0]][1]=="E"):
        n+=1
    elif(op_code[ins[0]][1]=="F"):
        n+=1
    elif(op_code[ins[0]][1]=="G"):
        n+=1
    elif(op_code[ins[0]][1]=="H"):
        n+=1


def var_detect(ins):

    if ins[0] == "jmp":
            s = "01111"

    if ins[1] in mem_add:
        s = "11111"

    if ins[0] == "jlt":
        s = "01101"

    if ins[0] == "jgt":
        s = "10101"

    if ins[0] == "je":
        s = "11111"


element=[]
t = True
curr_instruct =''
while (t == True) :

    try:

        curr_instruct = input()        
        element.append(curr_instruct)
        if curr_instruct=="" :
            t=False
    except EOFError:
        break

l=len(element)
k=0
flag = 0
var_error = 0
out = []

for j in range(len(element)-1,-1):
    if(j!=[]):
        if j!="hlt":
            print("Halt is not the last instruction, Error in line", element.index("hlt"))
            exit()

hltno=0
for i in element:
    if("hlt" in i):
        hltno+=1
if(hltno>1):
    print("MULTIPLE HLT DETECTED")
    exit()
elif(hltno==0):
    print("NO HLT INSTRUCTION DETECTED")
    exit()



flag=0

for i in element:

    if(i[0:3]=="var" and flag==0):
        k+=1
    elif(i[0:3]=="var" and flag==1):
        var_error=1
    else:
        flag=1

t=0
if(var_error!=1):

    for i in element:
        if(i==[]):
            t+=1
    k=l-k-1-t

    for i in element:

        j=i.split()

        if j == []:
            pc-=1
            pass
        
        elif(j[0] in op_code.keys()):
            if len(j)>1:
                if j[1] not in op_code.keys():
                    if j[1] not in mem_add:
                        s1=bin(pc+1)[2:]
                        s1="0"*(7-len(s1))+s1
                        mem_add[j[1]]=s1
            ins_type(j)
            out.append(s)
        elif i[0][-1]==":":
            fun_labl_name(i[1],pc)
        elif(j[1] in op_code.keys()):
            s1=bin(pc)[2:]
            s1="0"*(7-len(s1))+s1
            mem_add[j[0][:-1]]=s1
            ins_type(j[1:])
            out.append(s)
        elif(j[0]=="var"):
            s1=bin(k+1)[2:]
            s1="0"*(7-len(s1))+s1
            fun_var_name(j[1],pc)
            variables[j[1]]=s1
            k+=1
            continue
        elif i[0][-1]==":":
            fun_labl_name(i[1],pc)

        else:
            errorType="INVALID INSTRUCTION"
            print(errorType)
            exit()
        pc+=1

else:
    print("ALL VARIABLES MUST BE DEFINED AT THE BEGINNING")
    exit()

if REG[-1][0]==1:
    print("Illegal Immediate value")
    exit()

for i in out:
    if len(i)<16:
        st="0"*(16-len(i))
        i=i[0:5]+st+i[5::]
    print(i)
exit()
