import customtkinter
from PIL import Image

import os

import serial
import serial.tools.list_ports as list_ports


class SerialConsole(customtkinter.CTkFrame):
    def __init__(self, master, serial_port=None, baudrate=None, line_ending=None):
        super().__init__(master)

        self.master = master
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.line_ending = line_ending
        
        self.DATABITS = (serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS)
        self.PARITY = (serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_NONE, serial.PARITY_MARK, serial.PARITY_SPACE)
        self.PARITY_VAL = ('Even', 'Odd', 'None', 'Mark', 'Space')
        self.STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO)
        self.ports = {p.name: p.description for p in list_ports.comports()}
        self.currentPort = serial.Serial(port=None, baudrate=115200, timeout=0, write_timeout=0)
        self.sent_texts = []
        self.sent_texts_index = 0
        self.isEndByNL = True
        self.lastUpdatedBy = 2
     
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
            self, bg_color='#343638', state="disabled", wrap="word", border_width=5, corner_radius=0)
        self.rx_textbox.grid(row=0, column=0, columnspan=3,
                             padx=5, pady=5, sticky="nsew")
        self.rx_textbox.insert('0.0', "RX: \n")

        self.tx_entrybox = customtkinter.CTkEntry(self)
        self.tx_entrybox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.clear_button = customtkinter.CTkButton(
            self, text="", command=self.clear, width=5, height=5, image=clear_button_icon)
        self.clear_button.grid(row=1, column=1, padx=2.5, pady=5)

        self.send_button = customtkinter.CTkButton(
            self, text="", command=self.send, width=5, height=5, image=send_button_icon)
        self.send_button.grid(row=1, column=2, padx=5, pady=5)
        
        

    def clear(self):
        self.rx_textbox.configure(state="normal")
        self.rx_textbox.delete("0.0", 'end')
        self.rx_textbox.configure(state="disabled")
        
    def decode_esc(self, str_of_chr):
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
                    err = {'from': idx-1, 'to': idx+3, 'msg': f'Value Error: invalid {str_of_chr[idx-1:idx+3]} escape at position {idx-1}'}
                    break
                else:
                    if by:
                        ch = chr(ord(by))
                        to = idx + 1
                    else:
                        ch = ''
                        to = idx
                    err = {'from': idx-1, 'to': to, 'msg': f"Syntax Error: invalid escape sequence '\\{ch}' at position {idx-1}"}
                    break
            else:
                dbs += by
            idx += 1
        return dbs, err

    def send(self, event=None):
        tx_text = str(self.tx_entrybox.get())
        lst = len(self.sent_texts)
        if tx_text != "":
            bs, err = self.decode_esc(tx_text)
            if err:
                self.writeConsole(err['msg'] + '\n', 2)
                self.tx_entrybox.xview(err['from'])
                self.tx_entrybox.selection_range(err['from'], err['to'])
                self.tx_entrybox.icursor(err['to'])
                return
            if lst > 0 and self.sent_texts[lst-1] != tx_text or lst == 0:
                self.sent_texts.append(tx_text)
            self.sent_textsPtr = len(self.sent_texts)
            if self.line_ending == 1:
                bs += b'\n'
            elif self.line_ending == 2:
                bs += b'\r'
            elif self.line_ending == 3:
                bs += b'\r\n'
            self.currentPort.write(bs)
            tx_text = ''.join([self.get_str_of_chr(bytes([i])) for i in bs])
            self.writeConsole(tx_text)
            
    def writeConsole(self, text, upd=0):
            self.rx_textbox.configure(state="normal")
            self.rx_textbox.insert('end', text + "\n")
            self.rx_textbox.see('end')
            self.rx_textbox.configure(state="disabled")
            self.tx_entrybox.delete(0, 'end')

    def disableSending(self):
        self.send_button.configure(state="disabled")
        self.tx_entrybox.unbind('<Return>')

    def enableSending(self):
        self.send_button.configure(state="normal")
        self.tx_entrybox.bind('<Return>', self.send)
        
    def receive(self, rx_text):
        self.rx_textbox.configure(state="normal")
        self.rx_textbox.insert('end', rx_text)
        self.rx_textbox.configure(state="disabled")
        self.rx_textbox.see('end')
