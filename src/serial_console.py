import customtkinter
from PIL import Image

import os
import time

import serial


class SerialConsole(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.currentPort = serial.Serial(
            port=None, baudrate=115200, timeout=0, write_timeout=0)
        self.sent_texts = []
        self.sent_texts_index = 0

        icons_folder = os.path.join(os.getcwd(), 'src', 'icons')
        send_button_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "send_button_light.png")),
                                                  dark_image=Image.open(os.path.join(
                                                      icons_folder, "send_button_dark.png")),
                                                  size=(20, 20))
        clear_button_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "clear_button_light.png")),
                                                   dark_image=Image.open(os.path.join(
                                                       icons_folder, "clear_button_dark.png")),
                                                   size=(20, 20))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2), weight=0)

        self.rx_textbox = customtkinter.CTkTextbox(
            self, bg_color='#343638', state="disabled", wrap="word", border_width=2, corner_radius=0, height=150)
        self.rx_textbox.grid(row=0, column=0, columnspan=3,
                             padx=5, pady=5, sticky="nsew")

        self.tx_entrybox = customtkinter.CTkEntry(
            self, border_width=2, corner_radius=0)
        self.tx_entrybox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.tx_entrybox.bind('<Up>', self.upKeyCmd)
        self.tx_entrybox.bind('<Down>', self.downKeyCmd)

        self.clear_button = customtkinter.CTkButton(
            self, text="", command=self.clear, width=5, height=5, image=clear_button_icon)
        self.clear_button.grid(row=1, column=2, padx=2.5, pady=5)

        self.send_button = customtkinter.CTkButton(
            self, text="", command=self.send, width=5, height=5, image=send_button_icon)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

    def updateSerialSettings(self, serial_port=None, baudrate=None, line_ending=None):
        self.changeBaudrate(baudrate)
        self.changePort(serial_port)
        self.line_ending = line_ending

    def clear(self):
        self.rx_textbox.configure(state="normal")
        self.rx_textbox.delete("0.0", 'end')
        self.rx_textbox.configure(state="disabled")

    def getStrOfChr(self, chr_in_byte):
        cd = ord(chr_in_byte)
        if 0x20 <= cd and cd <= 0x7e or 0xa1 <= cd:
            if cd == 92:
                return '\\\\'
            return chr(cd)
        else:
            if cd == 9:
                return '\t'
            elif cd == 10:
                return '\n'
            elif cd == 13:
                return '\\r'
        return '\\x{:02x}'.format(cd)

    def decodeEsc(self, str_of_chr):
        sbs = bytes([ord(c) for c in str_of_chr])
        dbs = b''
        err = None
        idx = 0
        while idx < len(sbs):
            by = sbs[idx:idx+1]
            if by == b'\\':
                idx += 1
                by = sbs[idx:idx+1]
                if by == b'\\' or by == b"'" or by == b'"':
                    dbs += by
                elif by == b'0':
                    dbs += b'\0'
                elif by == b'a':
                    dbs += b'\a'
                elif by == b'b':
                    dbs += b'\b'
                elif by == b't':
                    dbs += b'\t'
                elif by == b'n':
                    dbs += b'\n'
                elif by == b'v':
                    dbs += b'\v'
                elif by == b'f':
                    dbs += b'\f'
                elif by == b'r':
                    dbs += b'\r'
                elif by == b'x':
                    err = {'from': idx-1, 'to': idx+3,
                           'msg': f'Value Error: invalid {str_of_chr[idx-1:idx+3]} escape at position {idx-1}'}
                    break
                else:
                    if by:
                        ch = chr(ord(by))
                        to = idx + 1
                    else:
                        ch = ''
                        to = idx
                    err = {'from': idx-1, 'to': to,
                           'msg': f"Syntax Error: invalid escape sequence '\\{ch}' at position {idx-1}"}
                    break
            else:
                dbs += by
            idx += 1
        return dbs, err

    def send(self, event=None, cnc_command=None):
        # NOTE: cls, reset and cancel implementations can be simplified in the future. it seems unnecessary to put entrybox delete and return commands in each if statement.
        if cnc_command:
            tx_text = cnc_command
        else:
            tx_text = str(self.tx_entrybox.get())
        lst = len(self.sent_texts)
        if lst > 0 and self.sent_texts[lst-1] != tx_text or lst == 0:
            self.sent_texts.append(tx_text)
        self.sent_texts_index = len(self.sent_texts)
        if tx_text == '':
            return
        if tx_text == 'cls':
            self.clear()
            self.tx_entrybox.delete(0, 'end')
            return
        if tx_text == 'reset':
            self.currentPort.write(b'\x18')  # ctrl+x
            self.tx_entrybox.delete(0, 'end')
            return
        if tx_text == 'cancel':
            self.currentPort.write(b'\x85')  # jog cancel command
            self.tx_entrybox.delete(0, 'end')
            return
        if tx_text == '?':
            # note: write ? without line ending to not receive a response saying "ok"
            self.currentPort.write(b'?')
            return
        bs, err = self.decodeEsc(tx_text)
        if err:
            self.writeConsole(err['msg'] + '\n')
            self.tx_entrybox.xview(err['from'])
            self.tx_entrybox.select_range(err['from'], err['to'])
            self.tx_entrybox.icursor(err['to'])
            return
        if self.line_ending == 'LF':
            bs += b'\n'
        elif self.line_ending == 'CR':
            bs += b'\r'
        elif self.line_ending == 'Both CR&LF':
            bs += b'\r\n'
        self.currentPort.write(bs)
        tx_text = ''.join([self.getStrOfChr(bytes([i])) for i in bs])
        self.writeConsole(tx_text + '\n')
        self.tx_entrybox.delete(0, 'end')

    def upKeyCmd(self, event):
        if self.sent_texts_index == len(self.sent_texts):
            self.lastTxText = str(self.tx_entrybox.get())
        if self.sent_texts_index > 0:
            self.sent_texts_index -= 1
            self.tx_entrybox.delete(0, "end")
            self.tx_entrybox.insert(
                "end", self.sent_texts[self.sent_texts_index])

    def downKeyCmd(self, event):
        if self.sent_texts_index < len(self.sent_texts):
            self.sent_texts_index += 1
            self.tx_entrybox.delete(0, "end")
            if self.sent_texts_index == len(self.sent_texts):
                self.tx_entrybox.insert("end", self.lastTxText)
            else:
                self.tx_entrybox.insert(
                    "end", self.sent_texts[self.sent_texts_index])

    def changePort(self, serial_port):
        if serial_port == self.currentPort.port and self.currentPort.is_open:
            return
        self.disableSending()
        if self.currentPort.is_open:
            self.currentPort.close()
            # self.writeConsole('Serial port closed.\n')
        self.currentPort.port = serial_port
        # self.writeConsole('Connection to the scanner ')
        self.update()
        try:
            self.currentPort.open()
        except:
            # portCbo.set('Select port')
            # self.writeConsole('failed.\n')
            self.master.updateCNCStatus('Disconnected')
            self.currentPort.port = None
        if self.currentPort.is_open:
            self.enableSending()
            self.rxPolling()
            # self.writeConsole('is successful.\n')
            self.master.updateCNCStatus('Connected')
        else:
            # print('Connection failed, retrying.')
            self.after(1000, self.changePort, serial_port)

    def changeBaudrate(self, baudrate):
        if baudrate == self.currentPort.baudrate:
            return
        self.currentPort.baudrate = baudrate

    def writeConsole(self, text):
        # remove 'carriage return' from incoming text
        text = text.replace('\\r', '')
        self.rx_textbox.configure(state="normal")
        self.rx_textbox.insert('end', text)
        self.rx_textbox.see('end')
        self.rx_textbox.configure(state="disabled")

    def rxPolling(self):
        if not self.currentPort.is_open:
            return
        try:
            text = ''
            while self.currentPort.in_waiting > 0:
                ch = self.currentPort.read()
                text += self.getStrOfChr(ch)
            if text:
                # text = text.replace('\\r', '')
                # print(text)
                if text.__contains__('<'):
                    self.master.updateCNCStatus(text)
                # the response contains '>' but not '<' so ignore it
                elif text.__contains__('>'):
                    pass
                else:
                    self.writeConsole(text)
        except serial.SerialException as se:
            self.closePort()
            # print(f'attempting to reconnect to port {self.currentPort.port} in 1 second.')
            self.after(1000, self.changePort, self.currentPort.port)
        self.after(10, self.rxPolling)  # polling in 10ms interval

    def disableSending(self):
        if self.send_button.cget('state') == 'normal':
            self.configureButtons(['send_button'], 'disabled')
        self.tx_entrybox.unbind('<Return>')

    def enableSending(self):
        if self.send_button.cget('state') == 'disabled':
            self.configureButtons(['send_button'], 'normal')
        self.tx_entrybox.bind('<Return>', self.send)

    def closePort(self):
        if self.currentPort.is_open:
            self.currentPort.close()
            self.writeConsole('Serial port closed.\n')
            self.currentPort.port = None
            self.disableSending()

    # def resetConnection(self):
    #     self.closePort()
    #     self.changePort(self.currentPort.port)

    def configureButtons(self, buttons: tuple, state: str):
        button_dict = {'send_button': self.send_button,
                       'clear_button': self.clear_button}
        for button in buttons:
            button_dict.get(button).configure(state=state)
