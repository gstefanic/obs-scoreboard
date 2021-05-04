# -*- coding: iso-8859-15 -*-
try:
    from scoreboard import update_scoreboard
except:
    print("`update_scoreboard` import exception")

import tkinter as tk
import tkinter.ttk as ttk
from tkcolorpicker import askcolor
import inspect
import time
from threading import Timer
from types import SimpleNamespace

TEAMS = [{
    "name": "Team A",
    "color": "blue",
    "nameColor": "white",
    "sets": 0,
    "points": 0,
}, {
    "name": "Team B",
    "color": "green",
    "nameColor": "white",
    "sets": 0,
    "points": 0,
},]

root = tk.Tk()
root.title("Scoreboard")
style = ttk.Style(root)
style.theme_use('clam')

# Entry widget
entry = None
entry_confirm = None

def destroy_entry():
    global entry
    global entry_confirm
    #if (entry in not None):
    if (entry is not None):
        if (inspect.isfunction(entry_confirm)):
            entry_confirm()
            entry_confirm = None
        if (entry is not None):
            entry.destroy()
            entry = None
        return True
    return False

def add_button_listeners(button, onClick=None, onHold=None):
    assert button is not None, "`button` parameter is None"
    BUTTON_HOLD_INTERVAL = 1 # seconds

    global held
    global holdTimer
    held = False
    holdTimer = None
    def onPress(event):
        global held
        global holdTimer
        if (destroy_entry() is True):
            held = True
            return
        def onHoldTimer():
            global held
            held = True
            onHold(event) if inspect.isfunction(onHold) else None
            pass
        holdTimer = Timer(BUTTON_HOLD_INTERVAL, onHoldTimer)
        holdTimer.start()
        pass

    def onRelease(event):
        global held
        global holdTimer
        holdTimer.cancel()
        onClick(event) if not held and inspect.isfunction(onClick) else None
        held = False
        pass

    button.bind("<Button>", onPress)
    button.bind("<ButtonRelease>", onRelease)
    return button

def add_team_row(teamIndex):

    #tk.Label(root, text=text).grid(row=row, column=0)
    #sv = tk.StringVar()
    #sv.trace("w", lambda name, index, mode, sv=sv: callback(sv) if inspect.isfunction(callback) else None)
    #tk.Entry(root, bd=5, width=24, textvariable=sv).grid(row=row, column=1)


    nameBtn = tk.Button(root, 
        text=TEAMS[teamIndex]["name"], 
        width=24, 
        bg=TEAMS[teamIndex]["color"],
        activebackground=TEAMS[teamIndex]["color"],
        fg=TEAMS[teamIndex]["nameColor"],
        activeforeground=TEAMS[teamIndex]["nameColor"],
    )
    nameBtn.grid(row=teamIndex, column=0)

    def onNameButtonClick(event):
        newColor = askcolor(TEAMS[teamIndex]["color" if event.num == 1 else "nameColor"], root)[1]
        if (newColor is None):
            return
        if (event.num == 1):
            TEAMS[teamIndex]["color"] = newColor
            update_scoreboard(TEAMS)
            event.widget.configure(bg=newColor, activebackground=newColor)
        else:
            TEAMS[teamIndex]["nameColor"] = newColor
            update_scoreboard(TEAMS)
            event.widget.configure(fg=newColor, activeforeground=newColor)
        pass

    def onNameButtonHold(holdEvent):
        global entry
        global entry_confirm
        entry = tk.Entry(root, bd=1, width=28)
        entry.insert(0, TEAMS[teamIndex]["name"])
        entry.grid(row=teamIndex, column=0)

        def onReturn(event):
            TEAMS[teamIndex]["name"] = event.widget.get() # TODO: check/escape
            update_scoreboard(TEAMS)
            event.widget.destroy()
            holdEvent.widget.configure(text=TEAMS[teamIndex]["name"])
            global entry
            global entry_confirm
            entry = None
            entry_confirm = None
            pass

        def onEntryConfirm():
            global entry
            evnt = {
                "widget": entry
            }
            onReturn(SimpleNamespace(**evnt))

        entry_confirm = onEntryConfirm

        entry.bind('<Return>', onReturn)
        pass

    add_button_listeners(nameBtn, onClick=onNameButtonClick, onHold=onNameButtonHold)

    def onScoreClick(type_):
        assert type_ == "points" or type_ == "sets", "`type_` is invalid"
        def onClick(event):
            curr = TEAMS[teamIndex][type_]
            if (event.num == 1):
                curr += 1
            else:
                curr -= 1 if curr > 0 else 0
            TEAMS[teamIndex][type_] = curr
            update_scoreboard(TEAMS)
            event.widget.configure(text=str(curr))
            pass
        return onClick

    def onScoreHold(type_):
        assert type_ == "points" or type_ == "sets", "`type_` is invalid"
        def onHold(holdEvent):
            if (holdEvent.num == 1):
                global entry
                global entry_confirm
                entry = tk.Entry(root, bd=0, width=3)
                entry.insert(0, str(TEAMS[teamIndex][type_]))
                entry.grid(row=teamIndex, column=1 if type_ == "sets" else 2)

                def onReturn(event):
                    val = TEAMS[teamIndex][type_]
                    try:
                        val = int(event.widget.get())
                    except:
                        print("error: `{}` should be an integer, instead is: {}".format(type_, event.widget.get()))
                    finally:
                        event.widget.destroy()
                    TEAMS[teamIndex][type_] = val
                    update_scoreboard(TEAMS)
                    holdEvent.widget.configure(text=str(val))
                    global entry
                    global entry_confirm
                    entry = None
                    entry_confirm = None
                    pass

                def onEntryConfirm():
                    global entry
                    evnt = {
                        "widget": entry
                    }
                    onReturn(SimpleNamespace(**evnt))
                    
                entry_confirm = onEntryConfirm
                entry.bind('<Return>', onReturn)
                pass
            else:
                TEAMS[teamIndex][type_] = 0
                update_scoreboard(TEAMS)
                holdEvent.widget.configure(text=str(0))
            pass
        return onHold

    setsBtn = tk.Button(root, 
        text=str(TEAMS[teamIndex]["sets"]), 
        width=2, 
        bg="white",
        activebackground="white",
    )
    setsBtn.grid(row=teamIndex, column=1)

    add_button_listeners(setsBtn, onClick=onScoreClick("sets"), onHold=onScoreHold("sets"))

    pointsBtn = tk.Button(root, 
        text=str(TEAMS[teamIndex]["points"]), 
        width=4, 
        bg="white",
        activebackground="white",
    )
    pointsBtn.grid(row=teamIndex, column=2)

    add_button_listeners(pointsBtn, onClick=onScoreClick("points"), onHold=onScoreHold("points"))

add_team_row(0)
add_team_row(1)

root.call('wm', 'attributes', '.', '-topmost', '1')
root.mainloop()