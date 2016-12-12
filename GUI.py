import Tkinter as tk


win = tk.Tk()

win.title("GUI Time")
win.resizable(0,0) #Disables resizing
label = tk.Label(win,text="MY GUI") #Adds a Lable
label.grid({'column':20,'row':2,'padx':20,'pady':20})


#Adding A Button
def clickMe():
    action.configure({"text":"I have been clicked!"})
    label.configure({"foreground":"red"})

action = tk.Button(win, text = "Go")
action.configure({"command":clickMe})
action.grid({'column':40,'row':100})

#Adding a Entry Field
def clickMe():
    action.configure({"text":"Hey there, " + name.get()})
    label.configure({"foreground":"red"})

name = tk.StringVar()

nameBox = tk.Entry(win,{'width':12,'textvariable':name})
nameBox.grid({'column':0,'row':1})
print(name.get())
win.mainloop() #loop wait for an event with the exit clause of hitting the X button, etc. Starts GUI.
