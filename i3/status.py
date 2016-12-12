#!/usr/bin/env python

from datetime import datetime
import dbus.mainloop.glib, gi.repository.GObject
import i3pystatus, i3pystatus.mail.maildir, os, subprocess, threading

class RedshiftTimed(i3pystatus.IntervalModule):
  settings = (
    "color_disabled",
    "format_day",
    "format_night",
    "interval",
    "time_morning",
    "time_evening",
    "temp_morning",
    "temp_evening",
    "time_transition",
  )

  color_disabled = "#48413a"
  format_day = "  <span color='#b7ba53'></span>   {temp}K "
  format_night = "  <span color='#b7ba53'></span>   {temp}K "
  interval = 60
  time_day = "05:00"
  time_night = "21:00"
  time_transition = "00:30"
  temp_day = 6500
  temp_night = 3700
  temp_last = 0

  enabled = True
  on_rightclick = "toggle"

  def init(self):
    time_day_struct = datetime.strptime(self.time_day, "%H:%M")
    time_night_struct = datetime.strptime(self.time_night, "%H:%M")
    time_trans_struct = datetime.strptime(self.time_transition, "%H:%M")

    self.time_day_mins = self.time_struct_to_mins(time_day_struct)
    self.time_night_mins = self.time_struct_to_mins(time_night_struct)
    self.time_trans_mins = self.time_struct_to_mins(time_trans_struct)

    # Enforce a successive ordering of day and night.
    self.time_night_mins = self.order_time_with_day(self.time_night_mins)

    self.time_mid_mins = (self.time_day_mins + self.time_night_mins) / 2
    self.run()

  def run(self):
    time_now_mins = self.time_struct_to_mins(datetime.now())

    # Enforce a successive ordering of day and current time.
    time_now_mins = self.order_time_with_day(time_now_mins)

    if (time_now_mins < self.time_night_mins):
      format_now = self.format_day
    else:
      format_now = self.format_night

    if self.enabled:
      # Two clamped lerps: night to day and day to night.
      # Mid-point of day/night used to select lerp direction.
      if (time_now_mins < self.time_mid_mins):
        lerp_from = self.temp_night
        lerp_to = self.temp_day
        lerp_start_mins = self.time_day_mins
      else:
        lerp_from = self.temp_day
        lerp_to = self.temp_night
        lerp_start_mins = self.time_night_mins

      lerp_by = max(0.0, min(1.0, (time_now_mins - lerp_start_mins) / self.time_trans_mins))
      temp_now = lerp_from + lerp_by * (lerp_to - lerp_from)

      # Round temperature to a multiple of 100K.
      temp_now = int(round(temp_now / 100.0)) * 100

      fdict = { "temp" : temp_now }
      self.output = { "full_text" : i3pystatus.formatp(format_now, **fdict) }
    else:
      temp_now = self.temp_day

      fdict = {
        "temp" : temp_now,
      }

      self.output = {
        "full_text" : i3pystatus.formatp(format_now, **fdict),
        "color" : self.color_disabled
      }

    if temp_now != self.temp_last:
      self.temp_last = temp_now

      subprocess.call(["redshift", "-O", str(temp_now)],
        stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

  def toggle(self):
    self.enabled = not self.enabled
    self.run()

  def time_struct_to_mins(self, time_struct):
    return time_struct.hour * 60 + time_struct.minute

  def order_time_with_day(self, time_mins):
    if self.time_day_mins > time_mins:
      time_mins += 3600

    return time_mins

class VPNManager(i3pystatus.Module):
  settings = (
    "color_disabled",
    "format",
    "vpn_name",
  )

  color_disabled = "#48413a"
  format = "  <span color='#b7ba53'></span>   {vpn_name} "
  vpn_name = None

  enabled = False

  def init(self):
    thread = threading.Thread(target = self.monitor_nm)
    thread.start()

  def monitor_nm(self):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)
    import NetworkManager

    def nm_props_changed(*args, **kwargs):
      self.enabled = False
      self.vpn_name = "VPN"

      for conn in NetworkManager.NetworkManager.ActiveConnections:
        if conn.Vpn:
          self.enabled = True
          self.vpn_name = conn.Connection.GetSettings()["connection"]["id"]

      self.update_output()

    nm_props_changed()
    NetworkManager.NetworkManager.connect_to_signal('PropertiesChanged', nm_props_changed)

    def activate_vpn():
      if self.enabled:
        return

      for conn in NetworkManager.Settings.ListConnections():
        if conn.GetSettings()["connection"]["type"] == "vpn":
          for dev in NetworkManager.NetworkManager.GetDevices():
            if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED and dev.Managed:
              break

          NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
          break

    def deactivate_vpn():
      if not self.enabled:
        return

      for conn in NetworkManager.NetworkManager.ActiveConnections:
        if conn.Vpn:
          NetworkManager.NetworkManager.DeactivateConnection(conn)
          break

    self.on_leftclick = activate_vpn
    self.on_rightclick = deactivate_vpn

    loop = gi.repository.GObject.MainLoop()
    loop.run()

  def update_output(self):
    fdict = {
      "vpn_name" : self.vpn_name,
    }

    self.output = {
      "full_text" : i3pystatus.formatp(self.format, **fdict),
    }

    if not self.enabled:
      self.output["color"] = self.color_disabled

    self.send_output()

status = i3pystatus.Status()

status.register(
  "clock",
  format = "  <span color='#b7ba53'></span>   %R ",
  hints = {
    "markup" : "pango",
    "background" : "#231e18",
    "border" : "#231e18",
    "separator_block_width" : 10,
  },
  interval = 30,
)

status.register(
  "clock",
  format = "  <span color='#b7ba53'></span>   %a %-d %b ",
  hints = {
    "markup" : "pango",
    "background" : "#231e18",
    "border" : "#231e18",
    "separator_block_width" : 10,
  },
  interval = 60,
)

status.register(
  RedshiftTimed,
  hints = {
    "markup" : "pango",
    "background" : "#231e18",
    "border" : "#231e18",
    "separator_block_width" : 10,
  }
)

status.register(
  "mail",
  format = "  <span color='#b7ba53'></span>   {unread} ",
  backends = [
    i3pystatus.mail.maildir.MaildirMail(directory = os.path.expanduser("~/mail/INBOX"))
  ],
  hide_if_null = False,
  color = "#c79668",
  color_unread = "#c79668",
  hints = {
    "markup" : "pango",
    "background" : "#231e18",
    "border" : "#231e18",
    "separator_block_width" : 10,
  }
)

status.register(
  VPNManager,
  hints = {
    "markup" : "pango",
    "background" : "#231e18",
    "border" : "#231e18",
    "separator_block_width" : 10,
  }
)

status.register(
  "pulseaudio",
  format = "  <span color='#b7ba53'></span>   {volume}% ",
  color_muted = "#48413a",
  hints = {
    "markup" : "pango",
    "background" : "#231e18",
    "border" : "#231e18",
    "separator_block_width" : 10,
  }
)

status.run()
