led-proxy: A simple service to control the scroll-lock LED
==========================================================

led-proxy exposes a simplistic dbus service that allows user to control the scroll-lock LED.

Usage
-----
To install, run `sudo ./setup.sh`

Then start it, `sudo systemctl enable led-proxy.service --now`
and then you can talk to `com.eladalfassa.LedProxy` on the DBus system bus.

If you want to use it the same way you would've used `xset` in your shell scripts,
use `dbus-send`. For example:

```bash
#
# Toggle LED
#
dbus-send --system --type=method_call --dest=com.eladalfassa.LedProxy /Leds com.eladalfassa.LedProxy.Toggle
#
# Turn LED off
#
dbus-send --system --type=method_call --dest=com.eladalfassa.LedProxy /Leds com.eladalfassa.LedProxy.TurnOff
#
# Turn LED on
#
dbus-send --system --type=method_call --dest=com.eladalfassa.LedProxy /Leds com.eladalfassa.LedProxy.TurnOn
```

dependencies: `sudo dnf intall python3-dbus python3-gobject`

Why?
----
Back in the days of X11, you could control the scroll-lock LED using the `xset` command,
but that's no longer possible under Wayland.

And while you could easily use `chmod` on the relevant sysfs path to allow any user to control the LED,
I don't believe it makes sense to do that on every startup.

I also don't believe it makes sense to run a program as root just so it can blink an LED,
it's much safer to have a small service that exposes this over DBus instead.

TODO
----
This is a very basic implementation. It should be improved to support more than
one LED (right now it'll just use the first scroll-lock LED it finds, which might not actually exist, and may not be the one you want).

It would also make sense to use a proper build system (like meson), and not just a basic shell script.

Also, re-write to use GDbus w/ pygobject, because apparently dbus-python is deperecated.
