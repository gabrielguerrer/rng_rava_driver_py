"""
Copyright (c) 2024 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
This code evokes the RAVA's Tk Acquisition application.

To execute it, enter the following command: python3 -m rng_rava.tk.acq
"""

import rng_rava as rava

TITLE = 'RAVA Acquisition'

rava_subapp_control_panel = rava.tk.ctrlp.rava_subapp_control_panel
rava_subapp_control_panel['show_button']= False
SUBAPPS = [rava_subapp_control_panel,
           rava.tk.acq.rava_subapp_acquisition]


def main():
    # RAVA main app
    tkapp = rava.tk.RAVA_APP(title=TITLE, subapp_dicts=SUBAPPS, rava_class=rava.RAVA_RNG, cfg_log_name='rava_acq')

    # Enter Tk loop
    tkapp.mainloop()


if __name__ == '__main__':
    main()