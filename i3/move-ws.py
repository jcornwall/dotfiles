#!/usr/bin/env python

import i3ipc, sys

def MoveWsToActiveScreen(ws_name):
  # Find the focused output.
  i3 = i3ipc.Connection()

  out_focus = next((ws["output"] for ws in i3.get_workspaces() if ws["focused"]), None)
  if out_focus == None:
    raise RuntimeError("no focused workspace found")

  # Move the target workspace to the focused output.
  i3.command("workspace " + ws_name + "; move workspace to output " + out_focus)

def UsageAndExit():
  sys.stderr.write("usage: move-ws.py <workspace_name>\n")
  sys.exit(1)

if __name__ == "__main__":
  try:
    usage_msg = "usage: move-ws.py <workspace_name>"

    if len(sys.argv) != 2:
      raise RuntimeError(usage_msg)

    MoveWsToActiveScreen(sys.argv[1])

  except Exception as ex:
    sys.stderr.write("move-ws.py: " + str(ex) + "\n")
    sys.exit(1)
