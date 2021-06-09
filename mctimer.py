import os
import sys
import platform
import json
import glob
import datetime
import time 
import tkinter as tk
from bindglobal import BindGlobal

#"THE BEER-WARE LICENSE" (Revision 42):
#bleach86 wrote this file. As long as you retain this notice you can do whatever you want with this stuff. 
#If we meet some day, and you think this stuff is worth it, you can buy me a beer in return

#Will make sure to do so given the opportunity
#Love, AeroAstroid

def format_time(t):
    # cut digits off the time string

    digits = len(t.split(".")[1])
    if digits > 3:
        t = t[:(3-digits)]
    
    if t.split(":")[0] == "0":
        t = t[2:]
    else:
        digits = len(t.split(".")[1])
        t = t[:(1-digits)]
    
    return t

json_file = 'mct_config.json'
with open(json_file) as json_f:
    config = json.load(json_f)
if config['borderless'] == 'true':
     config['borderless']
    
else:
    config['borderless'] = False

system_type = platform.system()
if system_type == 'Linux':
    directory = os.path.expanduser(config['linux_saves'])
elif system_type == 'Darwin':
    directory = os.path.expanduser(config['mac_saves'])
elif system_type == 'Windows':
    directory = os.path.expanduser(config['windows_saves'])

amount2 = 0
last_amount = 0
window = tk.Tk()
window.configure(bg=config['bg_color'])
bg = BindGlobal(widget=window)

window.lt_value = tk.StringVar()
window.rta_value = tk.StringVar()
window.igt_value = tk.StringVar()
window.lt = tk.StringVar()
window.rta = tk.StringVar()
window.igt = tk.StringVar()
window.att = tk.StringVar()

rt = time.time()
old_version = False
count = 0
ig = 0
run_time = 0
last_igt_check = time.time()

if config['auto_start'] == 'true':
    click1 = 1
    click2 = 1
else:
    click1 = 0
    click2 = 0

def get_time(force_new=False):

    try:
        global last_amount
        global old_version
        global amount2
        global ig
        global last_igt_check
        global run_time
        latest = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
        
        if system_type == "Linux" or system_type == "Darwin":
            path_start = latest + '/stats/'
            
        else:
            path_start = latest + '\\stats\\'
        json_f = glob.glob(path_start + '*.json')
        timer = json_f[0]
        
        with open(timer) as json_f:
            data = json.load(json_f)
            try:
                amount = data['stats']['minecraft:custom']['minecraft:play_one_minute']
            except:
                amount = data['stat.playOneMinute']
                old_version = True
            json_f.close()
            
            if amount2 != float(amount) / 20 or force_new:
                last_igt_check = time.time()
            
            amount2 = float(amount) / 20
            run_time = str(datetime.timedelta(seconds=amount2, milliseconds=0.5))

            if ig == 1:
                config['attempts'] = str(int(config['attempts']) + 1)
                print(f"--- SEED #{config['attempts']} ---")
                
                with open(json_file, mode="w") as json_f:
                    json.dump(config, json_f, indent=4)
                
                window.att.set(f"Attempt #{config['attempts']}")

            if last_amount == amount:
                ig = 0
                return format_time(run_time)
            else:
                print(latest + "\nTime: " + run_time)
                last_amount = amount
                ig = 0
                return format_time(run_time)
        
    except Exception:
        ig = 1
        return '00:00.000'

def window2():
    lt_label = tk.Label(fg=config['lt_color'], bg=config['bg_color'],
    font=(config['text_font'], 15), textvariable=window.lt)
    lt_label.place(x=5, y=55)
    window.lt.set("LT")

    lt_value = tk.Label(fg=config['lt_color'], bg=config['bg_color'],
    font=(config['numbers_font'], 30), textvariable=window.lt_value)
    lt_value.place(x=245, y=36, anchor="ne")

    rta_label = tk.Label(fg=config['rta_color'], bg=config['bg_color'],
    font=(config['text_font'], 12), textvariable=window.rta)
    rta_label.place(x=5, y=100)
    window.rta.set("RTA")

    rta_value = tk.Label(fg=config['rta_color'], bg=config['bg_color'],
    font=(config['numbers_font'], 25), textvariable=window.rta_value)
    rta_value.place(x=245, y=86, anchor="ne")

    igt_label = tk.Label(fg=config['igt_color'], bg=config['bg_color'],
    font=(config['text_font'], 12), textvariable=window.igt)
    igt_label.place(x=5, y=136)
    window.igt.set("IGT")

    igt_value = tk.Label(fg=config['igt_color'], bg=config['bg_color'],
    font=(config['numbers_font'], 20), textvariable=window.igt_value)
    igt_value.place(x=245, y=126, anchor="ne")

    atts = tk.Label(fg=config['lt_color'], bg=config['bg_color'],
    font=(config['numbers_font'], 15), textvariable=window.att)
    atts.place(x=125, y=5, anchor="n")
    window.att.set(f"Attempt #{config['attempts']}")

    bg.gbind(config['pause'], on_press)
    bg.gbind(config['reset_start'], on_press2)
    bg.gbind(config['exit'], clicked3)
    #window.bind("<Button-1>", clicked)
    #window.bind("<Button-3>", clicked2)
    rta_value.after(0, update_time)
    rta_value.after(0, update_time2)
    window.title("MCtimer (AA fork)")
    window.attributes('-topmost', True)
    window.overrideredirect(config['borderless'])
    window.geometry(config['window_pos'])
    window.mainloop()

def update_time():
    global rt
    global click1

    if click1 == 2:
        get_time(force_new=True)
        click1 = 1
    
    window.rta_value.set(real_time())

    if click1 == 1:
        amount3 = amount2 + (time.time() - last_igt_check)
        run_time = str(datetime.timedelta(seconds=amount3, milliseconds=0.5))
        window.lt_value.set(format_time(run_time))

    if click2 == 0:
        rt = time.time()
        window.igt_value.set(get_time())
        window.rta_value.set("00:00.000")

    if ig == 1:
        window.lt_value.set("00:00.000")

    window.after(config['rta_update'], update_time)

def update_time2():
    window.igt_value.set(get_time())
    window.after(1500, update_time2)

def on_press(event):
    left_click()

def on_press2(event):
    right_click()

def clicked3(event):
    sys.exit(1)

def clicked2(event):
    right_click()

def clicked(event):
    left_click()

def left_click():
    global click1
    if click1 >= 1:
        click1 = 0
    elif click1 == 0:
        click1 = 2
        get_time()

def right_click():
    global click1
    global click2
    if click2 == 1:
        click1 = 0
        click2 = 0
    elif click2 == 0:
        click2 = 1
        click1 = 1

def real_time():
    global rt
    global click1
    global click2
    global amount2
    global old_version
    global count
    global ig
    if config['auto_start'] == 'true':
        if ig == 1:
            rt = time.time()
            click1 = 1
            click2 = 1
            count = 0
            return '00:00.000'
        else:
            if old_version == True and count == 0:
                ig = 0
                rt = float(time.time()) - float(amount2)
                rtc = str(datetime.timedelta(seconds=rt))

                count = 1
                return format_time(rtc)
            else:
                ig = 0
                rt2 = time.time()
                real_time = rt2 - rt
                rtc = str(datetime.timedelta(seconds=real_time))

                return format_time(rtc)
    else:
        if click1 == 1:
            rt2 = time.time()
            real_time = rt2 - rt
            rtc = str(datetime.timedelta(seconds=real_time))

            return format_time(rtc)

def main():
    window2()

main()