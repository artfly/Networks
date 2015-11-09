import signal
import socket
import struct
import sys
from threading import Thread
import tkinter


BORN, MSG, DEAD = range(3)
nicknames = []
MSG_FORMAT = '=b'
s = None

tk = tkinter.Tk()
log_field = None
input_field = None
name_field = None


def init_gui(nickname):
    global log_field, input_field, name_field
    text = tkinter.StringVar()
    name = tkinter.StringVar()
    text.set('')
    name.set(nickname)
    tk.title("Simple chat")
    w = 400
    h = 300
    ws = tk.winfo_screenwidth()
    hs = tk.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    tk.geometry('%dx%d+%d+%d' % (w, h, x, y))

    log_field = tkinter.Text(tk)
    log_field.tag_configure('server_msg', foreground='red')
    name_field = tkinter.Entry(tk, textvariable=name)
    name_field.configure(state='readonly')
    input_field = tkinter.Entry(tk, textvariable=text)
    input_field.pack(side='bottom', fill='x', expand='true')
    name_field.pack(side='bottom', fill='x', expand='true')
    log_field.pack(side='top', fill='both', expand='true')
    input_field.focus_set()


def update_log():
    log_field.see(tkinter.END)
    s.setblocking(False)
    try:
        data = s.recv(1024).decode("utf-8")
        chunks = data.split()
        if data is '':
            log_field.insert(tkinter.END, "user with this username is already existing" + "\n", 'server_msg')
            sys.exit(1)
        elif chunks[0] == "!user":
            nicknames.append(chunks[1])
            log_field.insert(tkinter.END, "user %s connected" % chunks[1] + "\n", 'server_msg')
        elif chunks[0] == "!quit":
            nicknames.remove(chunks[1])
            log_field.insert(tkinter.END, "user %s left chat" % chunks[1] + "\n", 'server_msg')
        else:
            log_field.insert(tkinter.END, data + "\n")

    except:
        tk.after(1, update_log)
        return
    tk.after(1, update_log)
    return


def send_msg(event):
    content = input_field.get()
    if content == '' or content.split()[0] == "!users":
        log_field.insert(tkinter.END, ' '.join(nicknames) + "\n", 'server_msg')
        input_field.delete(0, 'end')
        return
    full_msg = struct.pack(MSG_FORMAT, MSG) + content.encode("utf-8")
    print(s)
    s.send(full_msg)
    log_field.insert(tkinter.END, name_field.get() + ":" + content + "\n")
    input_field.delete(0, 'end')


def exterminate():
    s.send(struct.pack(MSG_FORMAT, DEAD))
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage : %s <server_ip> <server_port> <nickname>")
        sys.exit(1)
    server_ip, server_port, nickname = sys.argv[1:]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, int(server_port)))
    msg = struct.pack(MSG_FORMAT, BORN) + nickname.encode("utf-8")
    s.send(msg)
    connected = s.recv(1024).decode("utf-8")
    nicknames.extend(connected.split())
    init_gui(nickname)
    input_field.bind('<Return>', send_msg)
    tk.after(1, update_log)
    tk.protocol("WM_DELETE_WINDOW", exterminate)
    tk.mainloop()
