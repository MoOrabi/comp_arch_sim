import tkinter as tk
from RoundedButton import RoundedButton
from TextArea import CustomTextArea
import assemble_machine
from demo import CustomTable
from tkinter import messagebox
import re

program_counter = 0


def on_down_key(event):
    # Scroll both list boxes down when the down key is pressed
    instruction_memory_idx.yview_scroll(1, "units")
    instruction_memory.yview_scroll(1, "units")


def on_up_key(event):
    # Scroll both list boxes down when the down key is pressed
    instruction_memory_idx.yview_scroll(-1, "units")
    instruction_memory.yview_scroll(-1, "units")


def on_down_key2(event):
    # Scroll both list boxes down when the down key is pressed
    data_memory_idx.yview_scroll(1, "units")
    data_memory.yview_scroll(1, "units")


def on_up_key2(event):
    # Scroll both list boxes down when the down key is pressed
    data_memory_idx.yview_scroll(-1, "units")
    data_memory.yview_scroll(-1, "units")


root = tk.Tk()
root.title("Simple Computer Architecture simulation (Al-Azhar University)")

root.wm_minsize(1366, 768)
root.wm_maxsize(1366, 768)
bg = tk.PhotoImage(file="comp_arch (1).png")
window = tk.Label(root, width=str(1366), height=str(768), image=bg)
window.place(x=0, y=-10)


def is_valid_input(text_input):
    text_input = text_input.strip()
    text_input.replace("  ", " ")
    text_input.replace("   ", " ")
    if text_input.upper() != "NOP" and len(text_input.split(" ")) < 2:
        return False
    instruction_name = text_input.split(" ")[0].upper()
    arguments = []
    first_arg = ''
    if len(text_input.split(" ")) > 1:
        arguments = text_input.split(" ")[1].upper().split(",")
        first_arg = arguments[0]
    second_arg = ""
    if len(arguments) > 1:
        second_arg = arguments[1]
    if ((assemble_machine.inst_lst.count(instruction_name) == 0)
       or (list(text_input).count(" ") > 1)) or (list(text_input).count(",") > 1):
        return False
    register_regex = re.compile("R([0-9]{1,2})$")
    num_regex = re.compile("(([0-9])|([1-9][0-9])|(1[0-9]{2})|(2[0-5][0-5])|"
                           "(0(b|B)[01]{1,8})|(0(x|X)[0-9a-fA-F]{1,2}))$")
    if instruction_name in ['NOT', "INC", "DEC", "CLR"] and not register_regex.match(first_arg, 0,
                                                                                     len(first_arg)):
        return False
    elif instruction_name == "JMP" and not num_regex.match(first_arg, 0):
        return False
    elif (instruction_name in ["ADD", "SUB", "AND", "OR", "XOR", "MOV"] and
          (not register_regex.match(first_arg, 0)
           or not register_regex.match(second_arg, 0))):
        return False
    elif instruction_name == "LDI" and (not register_regex.match(first_arg, 0)
                                        or not num_regex.match(second_arg, 0)):
        return False
    elif instruction_name == "LDS" and (not register_regex.match(first_arg, 0)
                                        or not num_regex.match(second_arg, 0)):
        return False
    elif instruction_name == "STS" and (not num_regex.match(first_arg, 0)
                                        or not register_regex.match(second_arg, 0)):
        return False
    return True


def assembly_button():
    # Delete every thing firstly
    global program_counter
    instruction_memory.delete(0, tk.END)
    instruction_memory_idx.delete(0, tk.END)
    data_memory.delete(0, tk.END)
    data_memory_idx.delete(0, tk.END)
    instruction_reg.config(text="")
    opcode1.delete(0, tk.END)
    opcode2.delete(0, tk.END)
    opcode3.delete(0, tk.END)
    program_counter = 0
    reg_file.delete_all()
    memory_address_reg.config(text="")
    memory_data_reg.config(text="")
    status_reg.config(text="")

    # Enter indexes for instruction memory and data memory and register file
    pc.config(text=assemble_machine.str_binary(bin(program_counter), 8))
    for i in range(256):
        instruction_memory_idx.insert(tk.END, assemble_machine.str_binary(bin(i), 8))
        data_memory_idx.insert(tk.END, assemble_machine.str_binary(bin(i), 8))
        data_memory.insert(tk.END, "")
    for i in range(16):
        reg_file.insert_row((assemble_machine.str_binary(str(i), 4), ""))

    inp = assembly_code.text.get("1.0", 'end-1c')
    if inp == "":
        tk.messagebox.showerror("No Instruction", "There is no instructions to execute!")
        return
    inp = inp.split("\n")
    for input_entry in inp:
        if not is_valid_input(input_entry):
            tk.messagebox.showerror("Invalid instruction", "Assembly input is not valid\n" + input_entry +
                                    "\nInstruction should be like:\nINST Arg1[,Arg2]\n"
                                    "Be careful about white spaces and commas")
            return
    for item in inp:
        machine_code = assemble_machine.assemble_machine(item)
        if len(machine_code) == 1:
            instruction_memory.insert(tk.END, machine_code)
        else:
            instruction_memory.insert(tk.END, machine_code[0])
            instruction_memory.insert(tk.END, machine_code[1])
    fetch1_btn.enable()



assembly_code = CustomTextArea(window, width=14, height=12.4, bg_color="white", fg_color="black", font_size=10)
assembly_code.place(x=45, y=65)

assembly_btn = RoundedButton(window, text="Assembly", border_radius=10, padding=16, command=assembly_button, color="#172f5f")
assembly_btn.place(x=63, y=290)




def fetch_1_button():
    assembly_btn.disable()
    global program_counter
    word = instruction_memory.get(program_counter)
    instruction_reg.config(text=word)
    program_counter = program_counter + 1
    pc.config(text=assemble_machine.str_binary(bin(program_counter), 8))
    fetch1_btn.disable()
    decode1_btn.enable()


fetch1_btn = RoundedButton(window, text="fetch 1", border_radius=10, padding=14, command=fetch_1_button, color="#172f5f")
fetch1_btn.place(x=450, y=300)


def decode_1_button():
    opcode_register_instruction = ["0001", "0010", "0011", "0110", "0111", "1000", "1110"]
    word = instruction_reg.cget("text")
    opcode1.delete(0, tk.END)
    opcode2.delete(0, tk.END)
    if word[0:4] in opcode_register_instruction:
        opcode1.insert(0, word[0:4])
        opcode2.insert(0, word[4:])
    else:
        opcode1.insert(0, word[0:4])

    two_byte_instructions = ["0001", "0010", "0011", "0100", "0101", "1001", "1010", "1011", "1100", "1101"]
    if word[0:4] in two_byte_instructions:
        fetch2_btn.enable()
    else:
        execute_btn.enable()

    decode1_btn.disable()


decode1_btn = RoundedButton(window, text="Decode 1", border_radius=10, padding=14,
                            command=decode_1_button, color="#172f5f")
decode1_btn.place(x=860, y=130)


def fetch_2_button():
    global program_counter
    word = instruction_memory.get(program_counter)
    instruction_reg.config(text=word)
    program_counter = program_counter + 1
    pc.config(text=assemble_machine.str_binary(bin(program_counter), 8))
    fetch2_btn.disable()
    decode2_btn.enable()


fetch2_btn = RoundedButton(window, text="fetch 2", border_radius=10, padding=14,
                           command=fetch_2_button, color="#172f5f")
fetch2_btn.place(x=450, y=330)


def decode_2_button():
    word = instruction_reg.cget("text")
    if opcode1.get() in ["0001", "0010", "0011", "0101"]:
        opcode3.delete(0, tk.END)
        opcode3.insert(0, word)
    else:
        opcode2.delete(0, tk.END)
        opcode2.insert(0, word[0:4])
        opcode3.delete(0, tk.END)
        opcode3.insert(0, word[4:])
    decode2_btn.disable()
    execute_btn.enable()


decode2_btn = RoundedButton(window, text="Decode 2", border_radius=10, padding=14, command=decode_2_button, color="#172f5f")
decode2_btn.place(x=860, y=160)


instruction_memory_idx = tk.Listbox(window, width=8, height=30)
instruction_memory_idx.place(x=211, y=118)

instruction_memory = tk.Listbox(window, width=13, height=30)
instruction_memory.place(x=268, y=118)

scrollbar = tk.Scrollbar(instruction_memory, orient='vertical')
scrollbar.place(x=62, y=0, relheight=1)

instruction_memory.config(yscrollcommand=scrollbar.set)
instruction_memory_idx.config(yscrollcommand=scrollbar.set)

scrollbar.config(command=lambda *args: (instruction_memory_idx.yview(*args), instruction_memory.yview(*args)))


instruction_reg = tk.Label(window, width=21, height=1, background='#ffffff', text="", fg="#172f5f")
instruction_reg.place(x=606, y=121)

opcode1 = tk.Entry(window, width=8, fg='blue', highlightthickness=1, highlightbackground="black",
                   font=('Arial', 10, 'bold'))
opcode1.place(x=600, y=237)

opcode2 = tk.Entry(window, width=8, fg='blue', highlightthickness=1, highlightbackground="black",
                   font=('Arial', 10, 'bold'))
opcode2.place(x=660, y=237)

opcode3 = tk.Entry(window, width=8, fg='blue', highlightthickness=1, highlightbackground="black",
                   font=('Arial', 10, 'bold'))
opcode3.place(x=720, y=237)



reg_file = CustomTable(window, width1=32, width2=60, height=7)
reg_file.place(x=678, y=296)




status_reg = tk.Label(window, width=15, height=1, background='#ffffff', text="", fg="#172f5f", borderwidth=1, relief="solid")
status_reg.place(x=855, y=275)



memory_data_reg = tk.Label(window, width=14, height=1, background="#ffffff", text="", fg="#172f5f", borderwidth=1, relief="solid")
memory_data_reg.place(x=907, y=437)



memory_address_reg = tk.Label(window, width=14, height=1, background="#ffffff", text="", fg="#172f5f", borderwidth=1, relief="solid")
memory_address_reg.place(x=906, y=483)



pc = tk.Label(window, width=14, height=1, background="#ffffff", text="", fg="#172f5f", borderwidth=1, relief="solid")
pc.place(x=582, y=632)


def execute_button():
    func_lst = [NOP, LDI, LDS, STS, MOV, JMP, INC, DEC, CLR, ADD, SUB, AND, OR, XOR, NOT]
    if opcode1.get() != "":
        func_lst[assemble_machine.inst_code.index(opcode1.get())]()
    execute_btn.disable()
    assembly_btn.enable()
    fetch1_btn.enable()


def NOP():
    pass


def LDI():
    reg_file.edit_item(eval("0b"+opcode2.get()), 2, opcode3.get())


def LDS():
    memory_address_reg.config(text=opcode3.get())
    memory_data_reg.config(text=data_memory.get(eval("0b"+opcode3.get())))
    reg_file.edit_item(eval("0b" + opcode2.get()), 2, memory_data_reg.cget("text"))


def STS():
    memory_address_reg.config(text=opcode3.get())
    memory_data_reg.config(text=reg_file.get_item(eval("0b"+opcode2.get()), 1))
    data_memory.delete(eval("0b"+opcode3.get()))
    data_memory.insert(eval("0b"+opcode3.get()), reg_file.get_item(eval("0b"+opcode2.get()), 1))


def MOV():
    reg_file.edit_item(eval("0b"+opcode2.get()), 2, reg_file.get_item(eval("0b"+opcode3.get()), 1))


def JMP():
    global program_counter
    program_counter = eval("0b"+opcode3.get())
    pc.config(text=assemble_machine.str_binary(bin(program_counter), 8))


def INC():
    reg_file.edit_item(eval("0b"+opcode2.get()), 2, assemble_machine.str_binary(bin(eval("0b"+reg_file.get_item(eval("0b"+opcode2.get()), 1)) + 1), 8))


def DEC():
    reg_file.edit_item(eval("0b"+opcode2.get()), 2, assemble_machine.str_binary(bin(eval("0b"+reg_file.get_item(eval("0b"+opcode2.get()), 1)) - 1), 8))


def CLR():
    reg_file.edit_item(eval("0b"+opcode2.get()), 2, "00000000")


def ADD():
    result = eval("0b"+reg_file.get_item(eval("0b"+opcode2.get()), 1)) + eval("0b"+reg_file.get_item(eval("0b"+opcode3.get()), 1))
    reg_file.edit_item(eval("0b"+opcode2.get()), 2, assemble_machine.str_binary(bin(result), 8))


def SUB():
    result = eval("0b"+reg_file.get_item(eval("0b"+opcode2.get()), 1)) - eval("0b"+reg_file.get_item(eval("0b"+opcode3.get()), 1))
    reg_file.edit_item(eval("0b" + opcode2.get()), 2, assemble_machine.str_binary(bin(result), 8))


def AND():
    result = eval("0b"+reg_file.get_item(eval("0b"+opcode2.get()), 1)) & eval("0b"+reg_file.get_item(eval("0b"+opcode3.get()), 1))
    reg_file.edit_item(eval("0b" + opcode2.get()), 2, assemble_machine.str_binary(bin(result), 8))


def OR():
    result = eval("0b" + reg_file.get_item(eval("0b" + opcode2.get()), 1)) | eval("0b" + reg_file.get_item(eval("0b" + opcode3.get()), 1))
    reg_file.edit_item(eval("0b" + opcode2.get()), 2, assemble_machine.str_binary(bin(result), 8))


def XOR():
    result = eval("0b" + reg_file.get_item(eval("0b" + opcode2.get()), 1)) ^ eval("0b" + reg_file.get_item(eval("0b" + opcode3.get()), 1))
    reg_file.edit_item(eval("0b" + opcode2.get()), 2, assemble_machine.str_binary(bin(result), 8))


def NOT():
    result = []
    reg = reg_file.get_item(eval("0b" + opcode2.get()), 1)
    lst = list(reg)
    for digit in lst:
        result.append("1" if digit == "0" else "0")
    result = "".join(result)
    print(result)
    reg_file.edit_item(eval("0b" + opcode2.get()), 2, result)
    # make negative bit in status register equal one if result < 0



execute_btn = RoundedButton(window, text="Execute", border_radius=10, padding=14, command=execute_button, color="#172f5f")
execute_btn.place(x=860, y=600)




data_memory_idx = tk.Listbox(window, width=8, height=30)
data_memory_idx.place(x=1142, y=110)

data_memory = tk.Listbox(window, width=13, height=30)
data_memory.place(x=1200, y=110)

scrollbar2 = tk.Scrollbar(data_memory, orient='vertical')
scrollbar2.place(x=62, y=0, relheight=1)

data_memory.config(yscrollcommand=scrollbar2.set)
data_memory.config(yscrollcommand=scrollbar2.set)

scrollbar2.config(command=lambda *args: (data_memory_idx.yview(*args), data_memory.yview(*args)))


instruction_memory_idx.bind("<Down>", on_down_key)
instruction_memory.bind("<Down>", on_down_key)
instruction_memory_idx.bind("<Up>", on_up_key)
instruction_memory.bind("<Up>", on_up_key)

data_memory_idx.bind("<Down>", on_down_key2)
data_memory.bind("<Down>", on_down_key2)
data_memory_idx.bind("<Up>", on_up_key2)
data_memory.bind("<Up>", on_up_key2)

fetch1_btn.first_disable()
fetch2_btn.first_disable()
decode1_btn.first_disable()
decode2_btn.first_disable()
execute_btn.first_disable()

tk.mainloop()


'''
data_memory.insert_row(("00000000","40364423"))
data_memory.insert_row(("00000001","10803022"))
data_memory.insert_row(("00000010","60040033"))
data_memory.insert_row(("00000011","40800033"))
data_memory.insert_row(("00000100","60000044"))
data_memory.insert_row(("00000101","10000022"))
data_memory.insert_row(("00000110","60000033"))
data_memory.insert_row(("00000111","10000044"))
data_memory.insert_row(("00001000","80364422"))
data_memory.insert_row(("00001001","30358824"))
data_memory.insert_row(("00001010","40364423"))
data_memory.insert_row(("00001011","40364423"))
data_memory.insert_row(("00001100","40364423"))
data_memory.insert_row(("00001101","10803022"))
data_memory.insert_row(("00001110","60040033"))
data_memory.insert_row(("00001111","40800033"))
data_memory.insert_row(("00010000","60000044"))
data_memory.insert_row(("00010001","10000022"))
data_memory.insert_row(("00010010","60000033"))
data_memory.insert_row(("00010011","10000044"))
data_memory.insert_row(("00010100","80364422"))
data_memory.insert_row(("00010101","30358824"))
data_memory.insert_row(("00010110","40364423"))
data_memory.insert_row(("00010111","40364423"))
data_memory.insert_row(("00011000","40364423"))
data_memory.insert_row(("00011001","10803022"))
data_memory.insert_row(("00011010","60040033"))
data_memory.insert_row(("00011011","40800033"))
data_memory.insert_row(("00011100","60000044"))
data_memory.insert_row(("00011101","10000022"))
data_memory.insert_row(("00011110","60000033"))
data_memory.insert_row(("00011111","10000044"))
data_memory.insert_row(("00100000","80364422"))
data_memory.insert_row(("00100001","10803022"))
data_memory.insert_row(("00100010","60040033"))
data_memory.insert_row(("00100011","40800033"))
data_memory.insert_row(("00100100","60000044"))
data_memory.insert_row(("00100101","10000022"))
data_memory.insert_row(("00100110","60000033"))
data_memory.insert_row(("00100111","10000044"))
data_memory.insert_row(("00101000","80364422"))
data_memory.insert_row(("00101001","30358824"))
data_memory.insert_row(("00101010","40364423"))
data_memory.insert_row(("00101011","40364423"))
data_memory.insert_row(("00101100","40364423"))
data_memory.insert_row(("00101101","10803022"))
data_memory.insert_row(("00101110","60040033"))
data_memory.insert_row(("00101111","40800033"))
data_memory.insert_row(("00110000","60000044"))
data_memory.insert_row(("00110001","10000022"))
data_memory.insert_row(("00110010","60000033"))
data_memory.insert_row(("00110011","10000044"))
data_memory.insert_row(("00110100","80364422"))
data_memory.insert_row(("00110101","30358824"))
data_memory.insert_row(("00110110","40364423"))
data_memory.insert_row(("00110111","40364423"))
data_memory.insert_row(("00111000","40364423"))
data_memory.insert_row(("00111001","10803022"))
data_memory.insert_row(("00111010","60040033"))
data_memory.insert_row(("00111011","40800033"))
data_memory.insert_row(("00111100","60000044"))
data_memory.insert_row(("00111101","10000022"))
data_memory.insert_row(("00111110","60000033"))
data_memory.insert_row(("00111111","10000044"))
data_memory.insert_row(("01000000","10000044"))
data_memory.insert_row(("01000001","10803022"))
data_memory.insert_row(("01000010","60040033"))
data_memory.insert_row(("01000011","40800033"))
data_memory.insert_row(("01000100","60000044"))
data_memory.insert_row(("01000101","10000022"))
data_memory.insert_row(("01000110","60000033"))
data_memory.insert_row(("01000111","10000044"))
data_memory.insert_row(("01001000","80364422"))
data_memory.insert_row(("01001001","30358824"))
data_memory.insert_row(("01001010","40364423"))
data_memory.insert_row(("01001011","40364423"))
data_memory.insert_row(("01001100","40364423"))
data_memory.insert_row(("01001101","10803022"))
data_memory.insert_row(("01001110","60040033"))
data_memory.insert_row(("01001111","40800033"))
data_memory.insert_row(("01010000","60000044"))
data_memory.insert_row(("01010001","10000022"))
data_memory.insert_row(("01010010","60000033"))
data_memory.insert_row(("01010011","10000044"))
data_memory.insert_row(("01010100","80364422"))
data_memory.insert_row(("01010101","30358824"))
data_memory.insert_row(("01010110","40364423"))
data_memory.insert_row(("01010111","40364423"))
data_memory.insert_row(("01011000","40364423"))
data_memory.insert_row(("01011001","10803022"))
data_memory.insert_row(("01011010","60040033"))
data_memory.insert_row(("01011011","40800033"))
data_memory.insert_row(("01011100","60000044"))
data_memory.insert_row(("01011101","10000022"))
data_memory.insert_row(("01011110","60000033"))
data_memory.insert_row(("01011111","10000044"))
data_memory.insert_row(("01100000","80364422"))
data_memory.insert_row(("01100001","10803022"))
data_memory.insert_row(("01100010","60040033"))
data_memory.insert_row(("01100011","40800033"))
data_memory.insert_row(("01100100","60000044"))
data_memory.insert_row(("01100101","10000022"))
data_memory.insert_row(("01100110","60000033"))
data_memory.insert_row(("01100111","10000044"))
data_memory.insert_row(("01101000","80364422"))
data_memory.insert_row(("01101001","30358824"))
data_memory.insert_row(("01101010","40364423"))
data_memory.insert_row(("01101011","40364423"))
data_memory.insert_row(("01101100","40364423"))
data_memory.insert_row(("01101101","10803022"))
data_memory.insert_row(("01101110","60040033"))
data_memory.insert_row(("01101111","40800033"))
data_memory.insert_row(("01110000","60000044"))
data_memory.insert_row(("01110001","10000022"))
data_memory.insert_row(("01110010","60000033"))
data_memory.insert_row(("01110011","10000044"))
data_memory.insert_row(("01110100","80364422"))
data_memory.insert_row(("01110101","30358824"))
data_memory.insert_row(("01110110","40364423"))
data_memory.insert_row(("01110111","40364423"))
data_memory.insert_row(("01111000","40364423"))
data_memory.insert_row(("01111001","10803022"))
data_memory.insert_row(("01111010","60040033"))
data_memory.insert_row(("01111011","40800033"))
data_memory.insert_row(("01111100","60000044"))
data_memory.insert_row(("01111101","10000022"))
data_memory.insert_row(("01111110","60000033"))
data_memory.insert_row(("01111111","10000044"))
'''
