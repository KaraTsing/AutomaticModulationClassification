#from Tkinter import Tk, Label, Button, Scale
import Tkinter as tk
import data_generators_WIN

# try using
# - Frame: 
# - Checkbutton
# - Radiobutton
# - Listbox
# - Entry


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Data Generator")
        self.snr_value = 0

        self.label = tk.Label(master, text="Control Data Modulation")
        self.label.pack()

        self.qpsk_button = tk.Button(master, text="Gen QPSK", command=self.send_QPSK)
        self.qpsk_button.pack()
        
        self.bpsk_button = tk.Button(master, text="Gen BPSK", command=self.send_BPSK)
        self.bpsk_button.pack()

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.scale_test = tk.Scale(master, from_=-20, to=20, variable=self.snr_value)
        self.scale_test.pack()
    
    def send_QPSK(self):
        print("Sending QPSK, SNR: " + str(self.snr_value))
        gen_qpsk(snr_value)
        
    def send_BPSK(self):
        print("Sending BPSK, SNR: " + str(self.snr_value))

root = tk.Tk()
my_gui = MyFirstGUI(root)
tk.root.mainloop()
