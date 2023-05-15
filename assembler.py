f=open("input.txt",'r')
l=f.readlines()
l1=[]
opcodes = {'add': '00000','sub': '00001','mov': '00010','ld ': '00100', 'st ': '00101','mul': '00110','div': '00111','rs ': '01000','ls ': '01001','xor': '01010','or ': '01011','and': '01100','not': '01101','cmp': '01110','jmp': '01111','jlt': '11100','jgt': '11101','je ': '11111','hlt': '11010'
}
registers = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}
s=''
lst = ['add', 'sub', 'mul', 'and', 'xor', 'or ']
lst2 = ['div', 'mov', 'ld ', 'st ', 'rs ', 'ls ', 'not', 'cmp']
lst3=['jmp','jlt','jgt','je ']
import random
vardict={}
f1=open("stdout.txt",'a')
for i in l:
    i=i.strip()
    l1.append(i)
for i in l1:
    print(i)
    if i[0:3]=="var":
        continue
    s=''
    a=i[0:3]
    b=opcodes[a]
    s+=b
    if (a in lst and a!='or ') :
        # if (i[4:6] and i[7:9] and i[10:12])!=('R0' or 'R1' or 'R2' or 'R3' or 'R4' or 'R5' or 'R6') :
        #     print("error")

        Rg1 = i[4:6]
        Rg2 = i[7:9]
        Rg3 = i[10:12]
        rg1=registers[Rg1]
        rg2=registers[Rg2]
        rg3=registers[Rg3]
        s+=rg1
        s+=rg2
        s+=rg3
    elif a == 'or ':
        Rg1 = i[3:5]
        Rg2 = i[6:8]
        Rg3 = i[9:11]
        rg1=registers[Rg1]
        rg2=registers[Rg2]
        rg3=registers[Rg3]
        s+=rg1
        s+=rg2
        s+=rg3

    elif a in lst2 and (i[7:9] and i[4:6]) in registers.values() :
        Regis1 = i[4:6]
        regis2 = i[7:9]
        rg1=registers[Regis1]
        rg2=registers[regis2]
        s+=rg1
        s+=rg2

    elif a == 'mov' and i[4:6] in registers.keys() :
        regis1 = i[4:6]
        if i[7:8]=="R":
            rg1=registers[regis1]
            regis2=i[7:10]
            rg2=registers[regis2]
            s+=rg1
            s+=rg2
        else:    
            imm=i[8::]
            imm=(bin(int(imm)))
            imm=imm[2::]
            if len(imm)<7:
                t=7-len(imm)
                st="0"*t
                st+=imm
                imm=st
            rg1=registers[regis1]
            s+=rg1
            s+=imm

    if (a == 'ld ' or 'st ') and i[3:5] in registers.keys(): 
        regis1 = i[3:5]
        rg1=registers[regis1]
        mem_addr=i[6::]
        if mem_addr in vardict: # Use vardict value if variable is called again
            bmem_addr = vardict[mem_addr]
            if len(bmem_addr)<7:
                t=7-len(bmem_addr)
                st="0"*t
                st+=bmem_addr
                bmem_addr=st
        else: # Generate a new random address and store it in vardict
            bmem_addr=bin(random.randint(0,128)) 
            bmem_addr=bmem_addr[2::]
            vardict[mem_addr]=bmem_addr
        s+=rg1
        s+=bmem_addr
    elif a in lst3:
        s+=opcodes[a]
        if a=="je ":
            imm=i[3::]
        else:
            imm=i[4::] 
        if imm in vardict: # Use address from vardict if label is called again
            bmem_addr = vardict[imm]
        else:  # Generate a new random address and store it in vardict
            bmem_addr=bin(random.randint(0,128))  
            bmem_addr=bmem_addr[2::]
            vardict[imm]=bmem_addr
        s+=bmem_addr

    elif (a == 'rs ' or 'ls ') and i[3:5] in registers.keys() :
        regis1 = i[3:5]
        rg1=registers[regis1]
        if i[6:8]=="R":
            rg1=registers[regis1]
            regis2=i[7:10]
            rg2=registers[regis2]
            s+=rg1
            s+=rg2
        else:    
            imm=i[7::]
            imm=(bin(int(imm)))
            imm=imm[2::]
            if len(imm)<7:
                t=7-len(imm)
                st="0"*t
                st+=imm
                imm=st
            rg1=registers[regis1]
            s+=rg1
            s+=imm
        s+=rg1
    elif a in lst3:
        s+=opcodes[a]
        if a=="je ":
            imm=i[3::]
            imm=(bin(int(imm)))
            imm=imm[2::]
            while bmem_addr not in vardict.values():
                bmem_addr=bin( random.randint(0,128))
                bmem_addr=bmem_addr[2::]
                if len(imm)<7:
                    t=7-len(imm)
                    st="0"*t
                    st+=imm
                    imm=st

        else:
            imm=i[4::]
            while bmem_addr not in vardict.values():
                bmem_addr=bin( random.randint(0,128))
                bmem_addr=bmem_addr[2::]
                if len(bmem_addr)<7:
                    t=7-len(bmem_addr)
                    st="0"*t
                    st+=bmem_addr
                    bmem_addr=st
                vardict[mem_addr]=bmem_addr
                continue
        s+=bmem_addr
    elif "hlt" in i:
        s="1101000000000000"
        # print(s)
        f1.write(s) 
        f1.write("\n")
        break
    if len(s)<16:
        st="0"*(16-len(s))
        s=s[0:5]+st+s[5::]
        f1.write(s) 
        f1.write("\n")
f1.close()
print()
