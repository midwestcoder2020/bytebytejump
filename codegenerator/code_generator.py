from bitmapper_opt import bitmaps,blank,mask
import random
import string
sw=80
sh=24
st= sw*sh
pc=0
scale=8
H=5
W=5

'''
move 000 to 002 and jump to 001
000002001
move 000 to 003 and jump to 002
000003002
'''


def fill_one_pixel(val,index):
    cmds=[]
    v=val << 8
    r=int(H*W)+2
    for x in range(2,r):
        if x != index:
            v = 0 << 8
            cmd_base = v | x
            print(f"moving {v >> 4} to {x}")
            print(cmd_base)
            cmd_base_hex = f'{cmd_base:03x}'
            print(cmd_base_hex)
            cmds.append(cmd_base_hex)
        else:
            v = val << 8
            cmd_base=v | x
            print(f"moving {v >> 4 } to {x}")
            print(cmd_base)
            cmd_base_hex=f'{cmd_base:03x}'
            print(cmd_base_hex)
            cmds.append(cmd_base_hex)
    return cmds

def pixel_to_mask(val,index,u_mask=mask):

    u_mask[index]=str(val)
    return u_mask

def mask_to_blit(user_mask):

    temp_blit = blank

    for x in range(len(user_mask)):
        line_to_edit = list(temp_blit[x])
        line_to_edit[3] = user_mask[x]
        temp_blit[x] = "".join(line_to_edit)

    return temp_blit

def fill_screen(val):
    cmds=[]
    pc=0
    v=val << 8
    r=int(H*W)+2
    for x in range(2,r):
    # for x in range(2,int((H/scale)*(W/scale))+2):
    # for x in range(2,int(128*128)):
        pc=x
        # cmd_base="0001"+hex(pc)[2:].zfill(4)
        cmd_base=v | x
        # cmd_base_hex=f'{cmd_base:02x}'
        print(f"moving {v >> 4 } to {x}")
        print(cmd_base)
        cmd_base_hex=f'{cmd_base:03x}'
        print(cmd_base_hex)
        cmds.append(cmd_base_hex)
        # cmd_base="0001"+hex(pc)[2:].zfill(4)+hex(x-1)[2:].zfill(4)
        # cmds.append(cmd_base)
    return cmds
    # return cmds,pc

def write_pixel(pixel_cord,val):
    cmd_base = "000"+str(val) + hex(pixel_cord)[2:].zfill(4)
    # cmd_base = "000"+str(val) + hex(pixel_cord)[2:].zfill(4) + hex(jump_to)[2:].zfill(4)
    return cmd_base

def write_comment(data):
    cmd_base ="#{}".format(data)
    return [cmd_base]

def repeat():
    return "99999999"

def write_h_line(hoff=1):
    cmds=[]
    for x in range(2,W):
        pc=x+((hoff-1)*W)
        cmd_base="0001"+hex(pc+W)[2:].zfill(4)
        cmds.append(cmd_base)
    return cmds


def noop():
    cmd_base="00000000"
    return [cmd_base]

def jmp(val):
    cmd_base="000000"+hex(val)[2:].zfill(3)
    return [cmd_base]

def blit_flag():
    cmd_base="001"+hex(129)[2:].zfill(3)+"000"
    return [cmd_base]

def repeat_opp(res):
    res.append(repeat())

def draw_line(ys,xs,xlen):
    cmds=[]
    for x in range(2,int(H*W)):

        if x>= xs and x <= xlen:
            cmd_base="0001"+hex(x)[2:].zfill(4)+hex(x-1)[2:].zfill(4)
            cmds.append(cmd_base)
        else:
            cmd_base="0000"+hex(x)[2:].zfill(4)+hex(x-1)[2:].zfill(4)
            cmds.append(cmd_base)

    return cmds



def clear_flag():
    cmd_base="001"+hex(130)[2:].zfill(3)+"000"
    return [cmd_base]

def clear_screen():
    cmds=[]
    for x in range(2,int((H)*(W))+2):
    # for x in range(2,int((H/scale)*(W/scale))+2):
        cmd_base="0000"+hex(x)[2:].zfill(4)
        # cmd_base="0000"+hex(x)[2:].zfill(4)+hex(x-1)[2:].zfill(4)
        cmds.append(cmd_base)
    return cmds


def fill_screen_val(v):
    cmds=[]
    for x in range(2,int((H)*(W))+2):
    # for x in range(2,int((H/scale)*(W/scale))+2):
        cmd_base=f"000{v}"+hex(x)[2:].zfill(4)
        # cmd_base="0000"+hex(x)[2:].zfill(4)+hex(x-1)[2:].zfill(4)
        cmds.append(cmd_base)
    return cmds

def blit_message(res:list,msg:str):
    for m in msg:
        blit_letter(res,m)

def blit_letter(res:list,letter:str):
    res.extend(bitmaps.get(letter))

def checkerboard_rom():
    rom = []

def write_val(val,pos):
    cmds=[]
    v=val << 8
    cmd_base=v | pos
    cmd_base_hex = f'{cmd_base:03x}'
    cmds.append(cmd_base_hex)
    return cmds

if __name__ == '__main__':
    code=[]

    blit_message(code,"a b c d e f g h i j k l m no p  q r s t u v w x y z".upper())
    blit_message(code,"1234567890".upper())
    blit_letter(code,"HAPPY_FACE".upper())
    blit_letter(code,"SAD_FACE".upper())
    blit_letter(code,"MEH_FACE".upper())
    blit_letter(code,"creeper".upper())
    blit_letter(code,"slime".upper())
    blit_letter(code,"mob".upper())

    code.extend(fill_screen(0))

    code.append(999)
    with open("code_scale8.bbj","w+") as f:
        for line in code:
            f.write(str(line))
    f.close()