import customtkinter as CTk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import serial.tools.list_ports
import requests
import time


CTk.set_appearance_mode('dark')

rate = 9600

ports = serial.tools.list_ports.comports()
ports_list = [str(j.device) for j in ports]
ports_list.insert(0, 'None')
def restart():
    user_port = port.get()
    ports = serial.tools.list_ports.comports()
    ports_list = [str(j.device) for j in ports]
    ports_list.insert(0, 'None')
    port.configure(values=ports_list)
    if not(user_port in ports_list):
        port.set("None")
def get_id():
    try:
        ser = serial.Serial(port.get(), rate, timeout=1)
        time.sleep(2)

        line = ser.readline().decode('utf-8').strip()
        COM_port = line[line.index(":")+1:]
        if COM_port:
            Card_ID.configure(text=COM_port)
        else:
            CTkMessagebox(
                title="Информация",
                message="Считыватель ничего не отправил, возможно нужно сменить порт",
                icon="warning",
                option_1="OK")              
    except:
        if port.get() == "None":
            CTkMessagebox(
                title="Ошибка",
                message="Выберете порт на котором расположено устройство RFID",
                icon="warning",
                option_1="OK")           
        else:
            CTkMessagebox(
                title="Ошибка",
                message="Ошибка при работе с портом",
                icon="cancel",
                option_1="OK")
    finally:
        if ser.open:
            ser.close()
def send():
    try:
        if Card_ID.cget("text") and Name_user.get() and Group_user.get():
            send = {'password': password,
                'CardID': Card_ID.cget("text"),
                'NameUser': Name_user.get(),
                'Group': Group_user.get(),
                'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'act': 'add'
            }
            code = requests.post(ip, json=send)
            if code.status_code == 200:
                CTkMessagebox(
                    title="Ответ",
                    message="Успешно",
                    icon="info",
                    option_1="OK")
            else:
                CTkMessagebox(
                    title="Ошибка",
                    message=f"Возрат: {code.status_code}",
                    icon="cancel",
                    option_1="OK")
        else:
            CTkMessagebox(
                title="Недосчёт",
                message="Перед тем как отправить, следует заполнить все поля",
                icon="info",
                option_1="OK")             
    except:
            CTkMessagebox(
                title="Ошибка",
                message=f"Возникла непредвиденная ошибка",
                icon="warning",
                option_1="OK")                    
root = CTk.CTk()

root.title("GUI для добавления пользователей")
root.geometry('450x350')
root.resizable(False, False)

Welcome = CTk.CTkLabel(root, text="Добавление пользователя", font=('Arial', 16, 'bold'))
Welcome.place(x=10, y=10)

port = CTk.CTkOptionMenu(root, values=ports_list)
port.place(x=250,y=10)

reverse_button = CTk.CTkButton(root, text="", width=30, height=30, command=restart)
reverse_button.place(x=400, y=10)

form = CTk.CTkFrame(root, width=430, height=200)
form.place(x=10, y=60)



text_form = CTk.CTkLabel(form, text="Заполните форму для добавления нового пользователя", font=('Arial', 14, 'bold'))
text_form.place(x=10, y=10)

Name_user = CTk.CTkEntry(form, placeholder_text='ФИО ученика', font=('Arial', 14, 'bold'), width=200)
Name_user.place(x=110, y=50)

Group_user = CTk.CTkEntry(form, placeholder_text='Группа ученика', font=('Arial', 14, 'bold'), width=200)
Group_user.place(x=110, y=100)

Card_ID = CTk.CTkLabel(form, text="АБ4Ц 62 03", font=("Arial", 18, "bold"), fg_color="#506691", corner_radius=10, width=200)
Card_ID.place(x=110, y=150)

GETid = CTk.CTkButton(root, text="Запросить id", command=get_id, font=('Arial', 14, 'bold'))
GETid.place(x=10,y=300)

send = CTk.CTkButton(root, text="Отправить", command=send, font=('Arial', 14, 'bold'))
send.place(x=300,y=300)

root.mainloop()
