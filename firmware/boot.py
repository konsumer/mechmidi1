import supervisor

# disable writing REPL to OLED (not useful and ugly)
supervisor.status_bar.display = False
supervisor.status_bar.console = False
display.root_group = None