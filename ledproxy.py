#!/usr/bin/env python3
# ledproxy.py - Simple proxy service to control the scroll-lock LED
#
# Copyright © 2018 Elad Alfassa <elad@fedoraproject.org>
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

import dbus
import dbus.service
import os
import os.path
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


class LedService(dbus.service.Object):
    def __init__(self, conn=None, object_path=None, bus_name=None):
        super().__init__(conn, object_path, bus_name)

    def get_led_path(self):
        """Get path to the first available scroll-lock LED"""
        for led in os.listdir("/sys/class/leds"):
            if 'scrolllock' in led:
                return f"/sys/class/leds/{led}"
        return False

    @dbus.service.method("com.eladalfassa.LedProxy")
    def Toggle(self):
        """Toggle LED"""
        path = self.get_led_path()
        with open(os.path.join(path, "brightness"), "r+") as f:
            current_state = bool(int(f.read()))
            f.seek(0)
            f.write(str(int(not current_state)))

    @dbus.service.method("com.eladalfassa.LedProxy")
    def TurnOn(self):
        """Turn LED on"""
        path = self.get_led_path()
        with open(os.path.join(path, "brightness"), "r+") as f:
            f.write('1')

    @dbus.service.method("com.eladalfassa.LedProxy")
    def TurnOff(self):
        """Turn LED off"""
        path = self.get_led_path()
        with open(os.path.join(path, "brightness"), "r+") as f:
            f.write('0')


def main():
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    name = dbus.service.BusName("com.eladalfassa.LedProxy", bus)
    service = LedService(bus, "/Leds")

    mainloop = GLib.MainLoop()
    mainloop.run()


if __name__ == "__main__":
    main()
