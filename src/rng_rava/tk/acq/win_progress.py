"""
Copyright (c) 2024 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
Progress window used by the Acquisition sub-app.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm


### VARS

PAD = 10


### WIN_PROGRESS

class WIN_PROGRESS(tk.Toplevel):

    def __init__(self, parent):
        # Initiate WIN_PROGRESS
        super().__init__(parent)
        self.name = 'WIN_PROGRESS'
        self.title(' Progress ')
        self.geometry('350x100+{}+{}'.format(self.master.winfo_x() + self.master.winfo_width() + 10, self.master.winfo_y()))
        self.rowconfigure([0], weight=1)
        self.columnconfigure([0], weight=1)
        self.resizable(False, False) # No resize
        self.protocol('WM_DELETE_WINDOW', lambda: None)

        # Widgets
        self.frame = ttk.Frame(self, padding=(PAD, PAD))
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.columnconfigure([0], weight=1)
        self.frame.rowconfigure([0,1], weight=1)

        self.var_progress = tk.DoubleVar(value=0)
        self.pb_progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=200, mode='determinate', variable=self.var_progress, maximum=100.0)
        self.pb_progress.grid(row=0, column=0, sticky='ew', padx=2*PAD)

        self.bt_cancel = ttk.Button(self.frame, text='Cancel', command=self.prog_cancel)
        self.bt_cancel.grid(row=1, column=0)

        # Start
        self.acquiring = False

    
    def set_extra_title(self, extra_str=''):
        self.title(' Progress ' + extra_str)


    def show(self):
        self.acquiring = True
        self.prog_update(0)
        self.geometry('350x100+{}+{}'.format(self.master.winfo_x() + self.master.winfo_width() + 10, self.master.winfo_y()))
        self.wm_deiconify()
        self.master.update()    # Update widgets on non-threaded mode
        self.grab_set()         # Can't perform other actions while progress window is shown


    def hide(self):
        self.acquiring = False
        self.grab_release()
        self.withdraw()
        self.set_extra_title('')
    

    def __enter__(self):
        self.show()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.hide()


    def prog_update(self, progress):
        self.var_progress.set(progress)
        self.master.update()    # Update widgets on non-threaded mode


    def prog_cancel(self):        
        if tkm.askyesno(parent=self, title=('Cancel'), message='Cancel?'):
            self.acquiring = False
            try:
                self.master.rng_acq.stop()
            except:
                pass