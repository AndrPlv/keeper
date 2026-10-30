import customtkinter as CTk
import serial.tools.list_ports


ports = serial.tools.list_ports.comports()
ports_list = [str(j.device) for j in ports]
ports_list.insert(0, 'None')
def restart():
    ports = serial.tools.list_ports.comports()
    ports_list = [str(j.device) for j in ports]
    ports_list.insert(0, 'None')
    port.configure(values=ports_list)


root = CTk.CTk()

root.title("GUI для добавления пользователей")
root.geometry('450x400')
root.resizable(False, False)

Welcome = CTk.CTkLabel(root, text="Добавление пользователя", font=('Arial', 16, 'bold'))
Welcome.place(x=10, y=10)

port = CTk.CTkOptionMenu(root, values=ports_list, command=lambda: print('hello'))
port.place(x=250,y=10)

reverse_button = CTk.CTkButton(root, text="", width=30, height=30, command=restart)
reverse_button.place(x=400, y=10)



root.mainloop()
