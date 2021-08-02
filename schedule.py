from tkinter import *
from tkinter.font import Font
import time
from tkinter import messagebox
from tkinter import filedialog
import os
on_now = True
deadline_hour = 23
deadline_minute = 59
deadline_second = 59
deadline_text = "23 59 59"


def calcul():
    import datetime as dt
    x = dt.datetime.now()
    a = dt.datetime(x.year,x.month,x.day,x.hour,x.minute,x.second)
    b = dt.datetime(x.year,x.month,x.day,deadline_hour,deadline_minute,deadline_second)

    rs = (b-a).total_seconds()
    return int(rs)

def remain_time():
    global REMAINING,deadline_hour,deadline_minute,deadline_second,deadline_text
    if on_now == False:
        REMAINING = calcul() 
        if REMAINING <= 1:
            second_str = "second"
            if REMAINING < 0:
                messagebox.showinfo(title="Time up!",message="Have you finished yet?")
                deadline_hour = 23
                deadline_minute = 59
                deadline_second = 59
                deadline_text = "23 59 59"

        else:
            second_str = "seconds"
       
        if int(deadline_text[0]) > 2:
            deadline_hour_text = "0" + deadline_text[0]
        else: 
            deadline_hour_text = str(deadline_text[0:2])

        deadline_minute_text = str(deadline_text[3:5])

        deadline_second_text = str(deadline_text[6:])

        clock_label.config(text=f"You only have {REMAINING} {second_str} to deadline {deadline_hour_text}:{deadline_minute_text}:{deadline_second_text}",font=("Comic Sans MS",15,"bold"))
        
        clock_label.after(1000,remain_time)




def clock():
    if on_now == True:
        current_time = time.strftime("%I:%M:%S %p \n%A")
        clock_label.config(text=current_time,font=("Comic Sans MS",20,"bold"))
    
        clock_label.after(1000,clock)

def on():
    global on_now
    on_now = True

    clock()
    off_button.config(command=off,text="Change display mode")

def off():
    global on_now
    on_now = False
    remain_time()
    off_button.config(command=on,text="Change display mode")

def set_deadline():
    global deadline_hour,deadline_minute,deadline_second,deadline_text
    deadline_text = my_entry.get()
    my_entry.delete(0,END)
    deadline_text_list =  deadline_text.split(" ")
    print(deadline_text_list)
    deadline_hour = int(deadline_text_list[0])
    deadline_minute = int(deadline_text_list[1])
    deadline_second  = int(deadline_text_list[2])
    print(deadline_hour,deadline_minute,deadline_second)
    remain_time()



def delete_item():
    my_list.delete(ANCHOR)

def add_item():
    my_list.insert(END,my_entry.get())
    my_entry.delete(0,END)

def cross_off_item():
    my_list.itemconfig(
        my_list.curselection(),fg="#dedede"
        )
    my_list.selection_clear(0,END)


def uncross_item():
    my_list.itemconfig(
        my_list.curselection(),fg="black"
        )
    my_list.selection_clear(0,END)

def delete_cross():
    count = 0
    while count < my_list.size():
        if my_list.itemcget(count,"fg") == "#dedede":
            my_list.delete(my_list.index(count))
        else:
            count += 1

def save_list():
    import pickle
    file_name = filedialog.asksaveasfilename(
        initialdir="",
        title="Save File",
        filetypes=(
            ("Dat Files","*.dat"),
            ("All Files","*.*"))
        )
    if file_name:
        if file_name.endswith(".dat"):
            pass
        else:
            file_name = f'{file_name}.dat'
        delete_cross()

        stuff = my_list.get(0,END)

        output_file = open(file_name,'wb')

        pickle.dump(stuff,output_file)

def open_list():
    import pickle
    file_name = filedialog.askopenfilename(
        initialdir="",
        title="Open File",
        filetypes=(
            ("Dat Files","*.dat"),
            ("All Files","*.*"))
        )
    if file_name:
        my_list.delete(0,END)

        input_file = open(file_name,'rb')

        stuff = pickle.load(input_file)

        for item in stuff:
            my_list.insert(END,item)

def clear_list():
    my_list.delete(0,END)

def hang():
    root.overrideredirect(True)
    hang_button.config(text="un_hang",command=un_hang)

def un_hang():
    root.overrideredirect(False)
    hang_button.config(text="hang",command=hang)



root = Tk()
root.title("Schedule")
root.iconbitmap("D:\\nguyên\\learn\\schedule\\lg.ico")


my_font = Font(
    family="Brush Script MT",
    size=30,
    weight="bold"
    )

my_frame = Frame(root)
my_frame.pack(pady=10)


my_list = Listbox(my_frame,
    font=("Comic Sans MS",30),
    width=25, 
    height=5,
    bg="SystemButtonFace",
    bd = 0,
    highlightthickness=0,
    selectbackground="#a6a6a6",
    activestyle="none",


    )
my_list.pack(side=LEFT,fill=BOTH)



my_scrollbar = Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT,fill=BOTH)


my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview)

my_entry = Entry(root,font=("Comic Sans MS",30))
my_entry.pack(pady=20)

button_frame = Frame(root)
button_frame.pack()

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="File",menu=file_menu)

file_menu.add_command(label="Save List",command=save_list)
file_menu.add_command(label="Open List",command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Clear List",command=clear_list)

delete_button = Button(button_frame,text="Delete",command=delete_item,font=("Comic Sans MS",15))
add_button = Button(button_frame,text="Add",command=add_item,font=("Comic Sans MS",15))
cross_button = Button(button_frame,text="Cross Off",command=cross_off_item,font=("Comic Sans MS",15))
uncross_button = Button(button_frame,text="Uncross",command=uncross_item,font=("Comic Sans MS",15))
delete_cross_button = Button(button_frame,text="Delete cross",command=delete_cross,font=("Comic Sans MS",15))
set_button = Button(button_frame,text="Set",command=set_deadline,font=("Comic Sans MS",15))
off_button = Button(root,text="Change display mode",command=off,font=("Comic Sans MS",15))
hang_button = Button(root,text="Hang mode",command=hang,font=("Comic Sans MS",15))


delete_button.grid(row=0,column=0,pady=10)
add_button.grid(row=0,column=1,padx=20,pady=10)
cross_button.grid(row=0,column=2,pady=10)
uncross_button.grid(row=1,column=0,padx=20)
set_button.grid(row=1,column=1)
delete_cross_button.grid(row=1,column=2)
off_button.pack(side=LEFT,pady=20)
hang_button.pack(side=LEFT,padx=20)

clock_label = Label(root,text="",font=("Comic Sans MS",20,"bold"))
clock_label.pack(side=BOTTOM)

clock()

root.mainloop()