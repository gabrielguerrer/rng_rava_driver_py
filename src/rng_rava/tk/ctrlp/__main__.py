"""
Copyright (c) 2023 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
This code evokes the RAVA's Tk Control Panel application.

To execute it, enter the following command: python3 -m rng_rava.tk.ctrlp
"""

import rng_rava as rava

TITLE = 'RAVA Control Panel'

SUBAPPS = [rava.tk.ctrlp.rava_subapp_control_panel]


def main():
    # RAVA main app
    tkapp = rava.tk.RAVA_APP(title=TITLE, subapp_dicts=SUBAPPS, rava_class=rava.RAVA_RNG_LED, cfg_log_name='rava_ctrlp')

    # Enter Tk loop
    tkapp.mainloop()


if __name__ == '__main__':
    main()