
from tkinter import *
from tkinter import ttk

import serial
import serial.tools.list_ports


#
def Refresh_Availabel_Serial_Port(combobox):
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
    else:
        for i in range(0, len(port_list)):
            print(port_list[i])

    combobox['value'] = port_list
    combobox.current(0)

def Read_Devices():
    if uart_device.isOpen():
        uart_device.write()
    else:
        uar

# 主程序窗口
root = Tk()
root.title("控制器产测工具")

# 控件
uart_name_label = Label(root, text = "串口名称")
uart_name_combobox = ttk.Combobox(root)
uart_connect_button = Button(root, text = "打开串口")
uart_refresh_button = Button(root, text = "刷新串口")


read_devices_button = Button(root, text = "读取设备地址")
read_devices_button.bind("<Button-1>", Read_Devices)
devices_combobox = ttk.Combobox(root)

switch_on_button = Button(root, text = "开灯")
switch_off_button = Button(root, text = "关灯")
set_duty_0_button = Button(root, text = "设置占空比：0")
set_duty_25_button = Button(root, text = "设置占空比：25")
set_duty_50_button = Button(root, text = "设置占空比：50")
set_duty_75_button = Button(root, text = "设置占空比：75")
set_duty_100_button = Button(root, text = "设置占空比：100")


logs_text = Text(root)

# 布局
uart_name_label.pack()
uart_name_combobox.pack()
uart_connect_button.pack()
uart_refresh_button.pack()

read_devices_button.pack()
devices_combobox.pack()
switch_on_button.pack()
switch_off_button.pack()
set_duty_0_button.pack()
set_duty_25_button.pack()
set_duty_50_button.pack()
set_duty_75_button.pack()
set_duty_100_button.pack()

logs_text.pack()

uart_device = serial.Serial(baudrate = 115200, bytesize = 8, parity = "E", stopbits = 1)

#
Refresh_Availabel_Serial_Port(uart_name_combobox)




root.mainloop()



