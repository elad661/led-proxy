#!/bin/bash
install --mode=0755 ledproxy.py /usr/sbin/ledproxy
install --mode=0644 led-proxy.service /usr/lib/systemd/system/led-proxy.service
install --mode=0644 com.eladalfassa.LedProxy.conf /etc/dbus-1/system.d/com.eladalfassa.LedProxy.conf
systemctl daemon-reload
