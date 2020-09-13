# 导入库

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

import time

import serial
import serial.tools.list_ports

# 类定义
class PLC_Controller_Test:
    def __init__(self):
        # 主程序窗口
        self.root = Tk()
        self.root.title("单灯控制器产测工具")

        # 主窗口
        self.uart_config_frame = Frame(self.root)
        self.devices_frame = Frame(self.root)
        self.controller_text_frame = Frame(self.root)
        self.logs_frame = Frame(self.root)

        # 设置窗口布局
        self.uart_config_frame.grid(row=0, column=0)
        self.devices_frame.grid(row=1, column=0)
        self.controller_text_frame.grid(row=0, column=1, rowspan=2)
        self.logs_frame.grid(row=0, column=2, rowspan=2)

        # 控件
        self.uart_name_label = Label(self.uart_config_frame, text="串口名称：", width = 10)
        self.uart_name_combobox = ttk.Combobox(self.uart_config_frame, width = 10)
        self.uart_connect_button = Button(self.uart_config_frame, text="打开串口", width = 10, command = self.Open_Serial_Port_Clicked)
        self.uart_refresh_button = Button(self.uart_config_frame, text="刷新串口", width = 10, command = self.Refresh_Availabel_Serial_Port_Clicked)

        #
        self.get_availabel_devices_button = Button(self.devices_frame, text="读取设备地址", command = self.Get_Availabel_Devices_Clicked)
        self.devices_combobox = ttk.Combobox(self.devices_frame)

        self.switch_on_button = Button(self.controller_text_frame, text="开灯", width = 15, command = self.Switch_On_Clicked)
        self.switch_off_button = Button(self.controller_text_frame, text="关灯", width = 15, command = self.Switch_Off_Clicked)
        self.set_duty_0_button = Button(self.controller_text_frame, text="设置占空比：0", width = 15, command = self.Set_Duty_0_Clicked)
        self.set_duty_25_button = Button(self.controller_text_frame, text="设置占空比：25", width = 15, command = self.Set_Duty_25_Clicked)
        self.set_duty_50_button = Button(self.controller_text_frame, text="设置占空比：50", width = 15, command = self.Set_Duty_50_Clicked)
        self.set_duty_75_button = Button(self.controller_text_frame, text="设置占空比：75", width = 15, command = self.Set_Duty_75_Clicked)
        self.set_duty_100_button = Button(self.controller_text_frame, text="设置占空比：100", width = 15, command = self.Set_Duty_100_Clicked)

        self.logs_text = Text(self.logs_frame)

        # 布局
        self.uart_name_label.grid(row = 0, column = 0)
        self.uart_name_combobox.grid(row = 0, column = 1)
        self.uart_connect_button.grid(row = 1, column = 0)
        self.uart_refresh_button.grid(row = 1, column = 1)

        self.devices_combobox.grid(row = 0, column = 0)
        self.get_availabel_devices_button.grid(row = 1, column = 0)

        self.switch_on_button.pack()
        self.switch_off_button.pack()
        self.set_duty_0_button.pack()
        self.set_duty_25_button.pack()
        self.set_duty_50_button.pack()
        self.set_duty_75_button.pack()
        self.set_duty_100_button.pack()

        self.logs_text.pack()

        # 串口设备
        self.uart_device = serial.Serial(baudrate=115200, bytesize=8, parity="E", stopbits=1)

        # 刷新串口
        self.Refresh_Availabel_Serial_Port_Clicked()

        # 主程序循环
        self.root.mainloop()

    # 打开串口
    def Open_Serial_Port_Clicked(self):
        print("打开串口！")
        if self.uart_device.isOpen():
            # 串口已经被打开
            self.uart_device.close()
            if self.uart_device.isOpen():
                self.uart_connect_button["text"] = "关闭串口"
            else:
                self.uart_connect_button["text"] = "打开串口"
        else:
            # 串口未打开
            self.uart_device.port = self.uart_name_combobox.get().split()[0]
            self.uart_device.open()
            if self.uart_device.isOpen():
                self.uart_connect_button["text"] = "关闭串口"
            else:
                showwarning(title = "警告", message = "打开串口失败！")
                self.uart_connect_button["text"] = "打开串口"

    # 刷新可用串口
    def Refresh_Availabel_Serial_Port_Clicked(self):
        print("刷新可用串口！")
        uart_name_list = []
        port_list = list(serial.tools.list_ports.comports())
        if 0 != len(port_list):
            for i in range(0, len(port_list)):
                uart_name_list.append(port_list[i][0])
            self.uart_name_combobox['value'] = uart_name_list
            self.uart_name_combobox.current(0)
        else:
            print("没有连接串口设备！")
            self.uart_name_combobox['value'] = [" "]
            self.uart_name_combobox.current(0)

    # 读取子设备Mac地址
    def Get_Availabel_Devices_Clicked(self):
        print("读取子设备Mac地址！")
        if self.uart_device.isOpen():
            cmd_str = "AT+TOPOINFO=1,32\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
        else:
            showwarning(title = "警告", message = "请先打开串口！")

    # 开灯
    def Switch_On_Clicked(self):
        print("开灯！")
        if self.uart_device.isOpen():
            cmd_str = "AT+SEND=FFFFFFFFFFFF,200,<{\"method\":\"setValue\",\"params\":{\"pa0\":0}}>,1\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
            self.logs_text.insert("insert", time.asctime(time.localtime(time.time())) + "开灯：\r\n")
            self.logs_text.insert("insert", cmd_str)
        else:
            showwarning(title = "警告", message = "请先打开串口！")

    # 关灯
    def Switch_Off_Clicked(self):
        print("关灯！")
        if self.uart_device.isOpen():
            cmd_str = "AT+SEND=FFFFFFFFFFFF,200,<{\"method\":\"setValue\",\"params\":{\"pa0\":1}}>,1\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
            self.logs_text.insert("insert", time.asctime(time.localtime(time.time())) + "关灯：\r\n")
            self.logs_text.insert("insert", cmd_str)
        else:
            showwarning(title = "警告", message = "请先打开串口！")

    # PWM输出0%
    def Set_Duty_0_Clicked(self):
        print("PWM输出0%！")
        if self.uart_device.isOpen():
            cmd_str = "AT+SEND=FFFFFFFFFFFF,200,<{\"method\":\"setValue\",\"params\":{\"duty0\":0}}>,1\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
            self.logs_text.insert("insert", time.asctime(time.localtime(time.time())) + "设置PWM输出0%：\r\n")
            self.logs_text.insert("insert", cmd_str)
        else:
            showwarning(title = "警告", message = "请先打开串口！")

    # PWM输出25%
    def Set_Duty_25_Clicked(self):
        print("PWM输出25%！")
        if self.uart_device.isOpen():
            cmd_str = "AT+SEND=FFFFFFFFFFFF,200,<{\"method\":\"setValue\",\"params\":{\"duty0\":25}}>,1\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
            self.logs_text.insert("insert", time.asctime(time.localtime(time.time())) + "设置PWM输出25%：\r\n")
            self.logs_text.insert("insert", cmd_str)
        else:
            showwarning(title = "警告", message = "请先打开串口！")

    # PWM输出50%
    def Set_Duty_50_Clicked(self):
        print("PWM输出50%！")
        if self.uart_device.isOpen():
            cmd_str = "AT+SEND=FFFFFFFFFFFF,200,<{\"method\":\"setValue\",\"params\":{\"duty0\":50}}>,1\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
            self.logs_text.insert("insert", time.asctime(time.localtime(time.time())) + "设置PWM输出50%：\r\n")
            self.logs_text.insert("insert", cmd_str)
        else:
            showwarning(title = "警告", message = "请先打开串口！")

    # PWM输出75%
    def Set_Duty_75_Clicked(self):
        print("PWM输出75%！")
        if self.uart_device.isOpen():
            cmd_str = "AT+SEND=FFFFFFFFFFFF,200,<{\"method\":\"setValue\",\"params\":{\"duty0\":75}}>,1\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
            self.logs_text.insert("insert", time.asctime(time.localtime(time.time())) + "设置PWM输出75%：\r\n")
            self.logs_text.insert("insert", cmd_str)
        else:
            showwarning(title = "警告", message = "请先打开串口！")

    # PWM输出100%
    def Set_Duty_100_Clicked(self):
        print("PWM输出100%！")
        if self.uart_device.isOpen():
            cmd_str = "AT+SEND=FFFFFFFFFFFF,200,<{\"method\":\"setValue\",\"params\":{\"duty0\":100}}>,1\r\n"
            self.uart_device.write(cmd_str.encode(encoding='UTF-8'))
            self.logs_text.insert("insert", time.asctime(time.localtime(time.time())) + "设置PWM输出100%：\r\n")
            self.logs_text.insert("insert", cmd_str)
        else:
            showwarning(title = "警告", message = "请先打开串口！")

app = PLC_Controller_Test()