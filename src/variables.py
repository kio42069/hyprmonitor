import os
from datetime import date

USER            = os.getlogin()
APPLICATION_CMD = "hyprctl activeworkspace -j"
TAB_CMD         = "hyprctl clients -j"
TODAY           = str(date.today())
BASE_DIR        = f"/home/{USER}/.config/hypr/hyprmonitor"
POLLING_RATE    = 1         # in seconds
