
import threading
import socket

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

bld = Gtk.Builder()
bld.add_from_file('ui.glade')

wnd = bld.get_object('wnd')
txt_log = bld.get_object('txt_log')
txt_ip = bld.get_object('txt_ip')
txt_msg = bld.get_object('txt_msg');
buf = bld.get_object('buf')

quit = False
port = 12345
sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sck.bind(('0.0.0.0', port))
sck.settimeout(0.5)

def close_app(obj):
	global quit
	sck.close()
	Gtk.main_quit()
	quit = True

def send_msg(obj):
	ip = txt_ip.get_text()
	msg = txt_msg.get_text() + '\n'
	itr = buf.get_end_iter()
	buf.insert(itr, 'me: ' + msg)
	sck.sendto(msg.encode(), (ip, port))
	pass

def receive_msg():
	global quit
	while quit == False:
		try:
			msg, ip = sck.recvfrom(100)
			itr = buf.get_end_iter()
			buf.insert(itr, ip[0] + ': ' + msg.decode())
		except:
			pass

tab = {
	'on_wnd_destroy': close_app,
	'on_btn_send_clicked': send_msg,
}

bld.connect_signals(tab)

thr = threading.Thread(target=receive_msg)
thr.start()

wnd.show_all()

Gtk.main()
