from filemanager import FileManager

file_manager = FileManager()
file_manager.set_home_from_cfg("myconfig.cfg")

while True:
    cmd = input(f"{file_manager.cur_position}>")
    file_manager.take_cmd(cmd)
