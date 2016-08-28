#!/usr/bin/env python

import i3pystatus

status = i3pystatus.Status()

status.register(
  "clock",
  format = "   %a %-d %b <b>%R</b>  ",
  hints = { "markup" : "pango" },
  interval = 30,
)

status.register(
  "pulseaudio",
  format = "   {volume}%",
)

status.run()
