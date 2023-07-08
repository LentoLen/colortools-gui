# window.py
#
# Copyright 2023 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk, Gio
from gi.repository import Xdp, XdpGtk4
from colortools import color_utils
import asyncio



@Gtk.Template(resource_path='/io/github/lentolen/window.ui')
class ColortoolsGuiWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ColortoolsGuiWindow'

    color_button = Gtk.Template.Child()
    copy_name = Gtk.Template.Child()
    colorname = Gtk.Template.Child()
    color_picker_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.color_picker_button.connect("clicked", self.colorPicker)
        self.color_button.connect("notify::rgba", self.onDialogChange)
        self.copy_name.connect("clicked", self.copyName)
        self.colorname.connect("activate", self.onColornameChange)

        self.clp = Gdk.Display().get_default().get_clipboard()

        self.portal = Xdp.Portal()
        self.parent = XdpGtk4.parent_new_gtk(self)

    def colorPicker(self, btn):
        asyncio.run(self.colorPickerResult())

    async def colorPickerResult(self):
        result = self.portal.pick_color(self.parent)
        await asyncio.sleep(1)
        print(result)
        r, g, b = result.deep_unpack()

        color = Gdk.RGBA(red=r, green=g, blue=b, alpha=1.0)
        print(f"Selected color is: {color.to_string()}")

    def copyName(self, btn):
        self.clp.set(self.colorname.get_text())

    def onDialogChange(self, button, rgba=None):
        color_string = self.color_button.get_rgba().to_string()
        numbers = color_string[color_string.index("(") + 1:color_string.index(")")].split(",")
        rgb_tuple = tuple(int(num) for num in numbers[:3])
        self.convertAll(rgb_tuple)

    def onColornameChange(self, e):
        colorname = self.colorname.get_text()
        colorname = color_utils.colorname_to_rgb(colorname, "meodai")
        print(colorname)
        if colorname is not None:
            self.convertAll(colorname)

    def convertAll(self, rgb):
        hexc = color_utils.rgb_to_hex(rgb)

        color = Gdk.RGBA()
        color.parse(hexc)
        self.color_button.set_rgba(color)

        colorname = color_utils.rgb_to_colorname(rgb, "meodai")
        self.colorname.set_text(colorname)

