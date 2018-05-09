import subprocess
def Print(msg):
    print(msg)
def Input():
    print("\033[1;35mopencps $ \033[0m", end='')
    return input()
    
command_list = subprocess.getoutput('cd bin && ls *.py').split('\n')
commands = [x.split('.')[0] for x in command_list if x != 'controler.py']

while True:
    cmd = Input()
    if cmd in ['quit', 'bye', 'exit']:
        Print("bye")
        break
    if cmd[0] == '%':
        c_list = [x for x in cmd[1:].split(' ')]
        if c_list[0] == 'cd':
            print("not support command")
            continue
        subprocess.call((c_list))
        continue 
    if not cmd.split(' ')[0] in commands:
        Print('Illegal Command!')
        continue
    else:
        c_list = cmd.split(' ')
        run_commands = "python3 "
        c_list[0] = 'bin/' + c_list[0] + '.py'
        c_list = ['python'] + c_list
        subprocess.call((c_list))



