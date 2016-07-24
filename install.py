#!/usr/bin/env python

import os, socket, sys

# Creates directories for temporary application files.
def make_cache_dirs():
  cache_dir = os.path.expanduser("~/.cache")
  app_names = ["gdb", "less", "zsh"]

  for app_name in app_names:
    app_cache_dir = os.path.join(cache_dir, app_name)
    os.makedirs(app_cache_dir, exist_ok = True)

# Installs symlinks to configuration files.
def link_config_files():
  script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
  home_dir = os.path.expanduser("~")
  config_dir = os.path.join(home_dir, ".config")
 
  configs_src_dst = [
    ["fontconfig/fonts.conf",              "fontconfig/fonts.conf"],
    ["gdb/init",                           "gdb/init"],
    ["git/config." + socket.gethostname(), "git/config"],
    ["i3/config",                          "i3/config"],
    ["i3/status.py",                       "i3/status.py"],
    ["nvim/base16-tomorrow.vim",           "nvim/colors/base16-tomorrow.vim"],
    ["nvim/init.vim",                      "nvim/init.vim"],
    ["systemd/ssh-agent.service",          "systemd/user/ssh-agent.service"],
    ["termite/config",                     "termite/config"],
    ["zsh/zshenv.all",                     "zsh/.zshenv"],
    ["zsh/zshenv.home",                    os.path.join(home_dir, ".zshenv")],
    ["zsh/zshenv." + socket.gethostname(), "zsh/.zshenv.local"],
    ["zsh/zshrc",                          "zsh/.zshrc"],
  ]

  for config_src_dst in configs_src_dst:
    src_path = os.path.join(script_dir, config_src_dst[0])
    dst_path = config_src_dst[1]

    # Destination paths are implicitly relative to ~/.config
    if not os.path.isabs(dst_path):
      dst_path = os.path.join(config_dir, dst_path)

    # Host-local configuration files are optional.
    if not os.path.exists(src_path):
      continue

    dst_dir = os.path.dirname(dst_path)
    os.makedirs(dst_dir, exist_ok = True)

    if os.path.lexists(dst_path):
      os.remove(dst_path)

    os.symlink(src_path, dst_path)

make_cache_dirs()
link_config_files()
