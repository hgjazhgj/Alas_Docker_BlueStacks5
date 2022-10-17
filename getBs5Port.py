def bs5(*args):
    import os
    import re
    import winreg
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\BlueStacks_nxt')as key:
        dir = winreg.QueryValueEx(key, 'UserDefinedDir')[0]
    with open(os.path.join(dir, 'bluestacks.conf'), encoding='utf-8')as f:
        return re.search(rf'bst\.instance\.Nougat64{f"_{args[0]}"if args else""}\.status\.adb_port="(\d*)"', f.read()).group(1)

import sys
print(bs5(*sys.argv[1:]), end='')
