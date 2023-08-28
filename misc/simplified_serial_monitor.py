## Attempt at simplifying the code for the serial monitor.

import tkinter as tk
from tkinter import ttk as ttk
from tkinter import scrolledtext as tkscroll
from tkinter import messagebox as msgbox
import serial
import serial.tools.list_ports as list_ports
import time
import json
import sys

def get_str_of_chr(chr_in_byte):
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

def decode_esc(str_of_chr):
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

def sendCmd(event):
	global sentTexts, sentTextsPtr
	txt = str(txText.get())
	lst = len(sentTexts)
	if txt != '':
		bs, err = decode_esc(txt)
		if err:
			writeConsole(err['msg'] + '\n')
			txText.xview(err['from'])
			txText.selection_range(err['from'], err['to'])
			txText.icursor(err['to'])
			return
		if lst > 0 and sentTexts[lst-1] != txt or lst == 0:
			sentTexts.append(txt)
		sentTextsPtr = len(sentTexts)
		if lineEndingCbo.current() == 1:
			bs += b'\n'
		elif lineEndingCbo.current() == 2:
			bs += b'\r'
		elif lineEndingCbo.current() == 3:
			bs += b'\r\n'
		currentPort.write(bs)
		txt = ''.join([get_str_of_chr(bytes([i])) for i in bs])
		writeConsole(txt + '\n')
		txText.delete(0, tk.END)

def upKeyCmd(event):
	global sentTextsPtr, lastTxText
	if sentTextsPtr == len(sentTexts):
		lastTxText = str(txText.get())
	if sentTextsPtr > 0:
		sentTextsPtr -= 1
		txText.delete(0, tk.END)
		txText.insert(tk.END, sentTexts[sentTextsPtr])

def downKeyCmd(event):
	global sentTextsPtr
	if sentTextsPtr < len(sentTexts):
		sentTextsPtr += 1
		txText.delete(0, tk.END)
		if sentTextsPtr == len(sentTexts):
			txText.insert(tk.END, lastTxText)
		else:
			txText.insert(tk.END, sentTexts[sentTextsPtr])

def changePort(event):
	global portDesc
	if portCbo.get() == currentPort.port:
		return
	disableSending()
	if currentPort.is_open:
		currentPort.close()
		writeConsole(portDesc + ' closed.\n')
	currentPort.port = portCbo.get()
	portDesc = ports[currentPort.port]
	writeConsole('Opening port...')
	root.update()
	try:
		currentPort.open()
	except:
		root.title(APP_TITLE)
		portCbo.set('Select port')
		#msgbox.showerror(APP_TITLE, "Couldn't open the {} port.".format(portDesc))
		writeConsole(' failed!!!\n')
		currentPort.port = None
	if currentPort.is_open:
		root.title(APP_TITLE + ': ' + ports[currentPort.port])
		enableSending()
		rxPolling()
		writeConsole(' done.\n')
		#msgbox.showinfo(APP_TITLE, '{} opened.'.format(portDesc))

def changeBaudrate(event):
	currentPort.baudrate = BAUD_RATES[baudrateCbo.current()]

def clearOutputCmd():
	rxText.configure(state=tk.NORMAL)
	rxText.delete('1.0', tk.END)
	rxText.configure(state=tk.DISABLED)

def showTxTextMenu(event):
	if txText.selection_present():
		sta=tk.NORMAL
	else:
		sta=tk.DISABLED
	for i in range(2):
		txTextMenu.entryconfigure(i, state=sta)
	try:
		root.clipboard_get()
		txTextMenu.entryconfigure(2, state=tk.NORMAL)
	except:
		txTextMenu.entryconfigure(2, state=tk.DISABLED)
	try:
		txTextMenu.tk_popup(event.x_root, event.y_root)
	finally:
		txTextMenu.grab_release()

def showRxTextMenu(event):
	if len(rxText.tag_ranges(tk.SEL)):
		rxTextMenu.entryconfigure(0, state=tk.NORMAL)
	else:
		rxTextMenu.entryconfigure(0, state=tk.DISABLED)
	if currentPort.isOpen():
		rxTextMenu.entryconfigure(2, state=tk.NORMAL)
	else:
		rxTextMenu.entryconfigure(2, state=tk.DISABLED)
	try:
		rxTextMenu.tk_popup(event.x_root, event.y_root)
	finally:
		rxTextMenu.grab_release()

def writeConsole(txt):
	txt = txt.replace('\\r', '') # remove 'carriage return' from incoming text
	rxText.configure(state=tk.NORMAL)
	rxText.insert(tk.END, txt)
	rxText.see(tk.END)
	rxText.configure(state=tk.DISABLED)

def rxPolling():
	if not currentPort.is_open:
		return
	preset = time.perf_counter_ns()
	try:
		while currentPort.in_waiting > 0 and time.perf_counter_ns()-preset < 2000000: # loop duration about 2ms
			ch = currentPort.read()
			txt = ''
			txt += get_str_of_chr(ch)
			writeConsole(txt)
	except serial.SerialException as se:
		closePort()
		msgbox.showerror(APP_TITLE, "Couldn't access the {} port".format(portDesc))
	root.after(10, rxPolling) # polling in 10ms interval

def listPortsPolling():
	global ports
	ps = {p.name: p.description for p in list_ports.comports()}
	pn = sorted(ps)
	if pn != portCbo['values']:
		portCbo['values'] = pn
		if len(ports) == 0: # if no port before
			portCbo['state'] = 'readonly'
			portCbo.set('Select port')
			enableSending()
		elif len(pn) == 0: # now if no port
			portCbo['state'] = tk.DISABLED
			portCbo.set('No port')
			disableSending()
		ports = ps
	root.after(1000, listPortsPolling) # polling every 1 second

def disableSending():
	sendBtn['state'] = tk.DISABLED
	txText.unbind('<Return>')

def enableSending():
	sendBtn['state'] = tk.NORMAL
	txText.bind('<Return>', sendCmd)

def closePort():
	if currentPort.is_open:
		currentPort.close()
		writeConsole(portDesc + ' closed.\n')
		currentPort.port = None
		disableSending()
		portCbo.set('Select port')
		root.title(APP_TITLE)

def showAbout():
	msgbox.showinfo(APP_TITLE, 'Designed by Engin Can Sürmeli, August 2023')

def exitRoot():
	data = {}
	data['lineending'] = lineEndingCbo.current()
	data['baudrateindex'] = baudrateCbo.current()
	data['portindex'] = portCbo.current()
	data['portlist'] = ports
	with open(fname+'.json', 'w') as jfile:
		json.dump(data, jfile, indent=4)
		jfile.close()
	root.destroy()

if __name__ == '__main__':
	APP_TITLE = 'Serial Monitor'
	BAUD_RATES = (300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 76800, 115200, 23040, 500000, 1000000, 2000000)
	ports = {p.name: p.description for p in list_ports.comports()}
	currentPort = serial.Serial(port=None, baudrate=115200, timeout=0, write_timeout=0)
	portDesc = ''
	sentTexts = []
	sentTextsPtr = 0
	ico = None

	data = {}
	fname = sys.argv[0].rsplit('.', 1)[0]
	jfile = None
	try:
		jfile = open(fname+'.json')
		data = json.load(jfile)
	except FileNotFoundError as fnfe:
		pass
	if jfile:
		jfile.close()

	root = tk.Tk()
	root.title(APP_TITLE)
	try:
		ico = tk.PhotoImage(file = fname+'.png')
	except:
		pass
	if ico:
		root.iconphoto(False, ico)
	root.protocol("WM_DELETE_WINDOW", exitRoot)

	tk.Grid.rowconfigure(root, 0, weight=1)
	tk.Grid.rowconfigure(root, 1, weight=999)
	tk.Grid.rowconfigure(root, 2, weight=1)

	tk.Grid.columnconfigure(root, 0, weight=1)
	tk.Grid.columnconfigure(root, 1, weight=1)
	tk.Grid.columnconfigure(root, 2, weight=1)
	tk.Grid.columnconfigure(root, 3, weight=999)
	tk.Grid.columnconfigure(root, 4, weight=1)
	tk.Grid.columnconfigure(root, 5, weight=1)
	tk.Grid.columnconfigure(root, 6, weight=1)

	txText = tk.Entry(root)
	txText.grid(row=0, column=0, columnspan=6, padx=4, pady=8, sticky=tk.N+tk.EW)
	txText.bind('<Up>', upKeyCmd)
	txText.bind('<Down>', downKeyCmd)
	txText.bind('<Button-3>', showTxTextMenu)

	sendBtn = tk.Button(root, width=12, text='Send', state=tk.DISABLED, command=lambda:sendCmd(None))
	sendBtn.grid(row=0, column=6, padx=4, pady=4, sticky=tk.NE)

	rxText = tkscroll.ScrolledText(root, height=20, state=tk.DISABLED, font=('Courier', 10), wrap=tk.WORD)
	rxText.grid(row=1, column=0, columnspan=7, padx=4, sticky=tk.NSEW)
	rxText.bind('<Button-3>', showRxTextMenu)

	portCbo = ttk.Combobox(root, width=10)
	portCbo.grid(row=2, column=3, padx=4, pady=4, sticky=tk.SE)
	portCbo.bind('<<ComboboxSelected>>', changePort)
	portCbo['values'] = sorted(ports)
	if len(ports) > 0:
		portCbo['state'] = 'readonly'
		portCbo.set('Select port')
	else:
		portCbo['state'] = tk.DISABLED
		portCbo.set('No port')

	lineEndingCbo = ttk.Combobox(root, width=14, state='readonly')
	lineEndingCbo.grid(row=2, column=4, padx=4, pady=4, sticky=tk.SE)
	lineEndingCbo['values'] = ('No line ending', 'Newline', 'Carriage return', 'Both CR & NL')
	di = data.get('lineending')
	if di != None:
		lineEndingCbo.current(di)
	else:
		lineEndingCbo.current(0)

	baudrateCbo = ttk.Combobox(root, width=12, state='readonly')
	baudrateCbo.grid(row=2, column=5, padx=4, pady=4, sticky=tk.SE)
	baudrateCbo['values'] = list(str(b) + ' baud' for b in BAUD_RATES)
	baudrateCbo.bind('<<ComboboxSelected>>', changeBaudrate)
	di = data.get('baudrateindex')
	if di != None:
		baudrateCbo.current(di)
		currentPort.baudrate = BAUD_RATES[di]
	else:
		baudrateCbo.current(4) # 9600 baud
		currentPort.baudrate = BAUD_RATES[4]

	clearBtn = tk.Button(root, width=12, text='Clear output', command=clearOutputCmd)
	clearBtn.grid(row=2, column=6, padx=4, pady=4, sticky=tk.SE)

	txTextMenu = tk.Menu(txText, tearoff=0)
	txTextMenu.add_command(label='Cut', accelerator='Ctrl+X', command=lambda:txText.event_generate('<<Cut>>'))
	txTextMenu.add_command(label='Copy', accelerator='Ctrl+C', command=lambda:txText.event_generate('<<Copy>>'))
	txTextMenu.add_command(label='Paste', accelerator='Ctrl+V', command=lambda:txText.event_generate('<<Paste>>'))

	rxTextMenu = tk.Menu(rxText, tearoff=0)
	rxTextMenu.add_command(label='Copy', accelerator='Ctrl+C', command=lambda:rxText.event_generate('<<Copy>>'))
	rxTextMenu.add_separator()
	rxTextMenu.add_command(label='Close active port', command=closePort)
	rxTextMenu.add_separator()
	rxTextMenu.add_command(label='About', command=showAbout)
 
	listPortsPolling()

	root.update()
	sw = root.winfo_screenwidth()
	sh = root.winfo_screenheight()
	rw = root.winfo_width()
	rh = root.winfo_height()
	root.minsize(rw, 233)
	root.geometry(f'{rw}x{rh}+{int((sw-rw)/2)}+{int((sh-rh)/2)-30}')

	di = data.get('portindex')
	if di != None and di != -1 and data.get('portlist') == ports:
		portCbo.current(di)
		changePort(None)

	root.mainloop()