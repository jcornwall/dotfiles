#!/usr/bin/env python

from datetime import datetime
import dbus.mainloop.glib, gi.repository.GObject
import i3pystatus, os, subprocess, threading

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
