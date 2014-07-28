__author__ = 'keinmark'

from Tkinter import *
import sqlite3
import datetime

def watchTasks(event):
    root = Tk()
    root.title("Watch Task")
    root.resizable(0, 0)
    connection = sqlite3.connect("stasks.db")
    cursor = connection.cursor()
    rows = cursor.execute("select * from tasks order by done ASC, insertTS DESC")
    connection.commit()

    entries = set()
    for row in rows:
        done = row[3]
        date = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        inserted = date
        title = row[1]
        entries.add((title, inserted, done))

    def dispose(event):
        root.destroy()

    global begin
    begin = 0
    global end
    end = 5

    def moveDown(event):
        global end
        global begin
        if end + 1 < len(entries):
            begin += 1
            end += 1
        show(begin, end)

    def moveUp(event):
        global end
        global begin
        if begin - 1 >= 0:
            begin -= 1
            end -= 1
        show(begin, end)

    all = set()
    def show(begin, end):
        for container in all:
            container.grid_remove()
        all.clear()
        i = 0
        for entry in entries:
            if (i >= begin) and (i <= end):
                done = entry[2]
                color = "black"
                if done == 1:
                    color = "grey"
                container = LabelFrame(root, bd=0, bg="grey", height=2)
                inserted = entry[1]
                insertedLabel = Label(container, text=inserted, fg=color, justify=LEFT, anchor=W, width=55)
                insertedLabel.pack(fill=X)
                title = entry[0]
                if len(title) > 50:
                    title = title[:51]
                    title += "..."
                titleLabel = Label(container, text=title, fg=color, justify=LEFT, anchor=W, width=55)
                titleLabel.pack(fill=X)
                container.grid(row=i, column=1, sticky=W)
                all.add(container)
            i += 1


    root.bind('<Return>', dispose)
    root.bind('<w>', moveUp)
    root.bind('<s>', moveDown)

    show(begin, end)