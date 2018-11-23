import re
def parse_rew(path):
    eq = []
    with open(path, 'r') as f:
        for l in [re.sub(' +', ' ', s).split(' ') for s in f.read().splitlines()]:
            if len(l) == 12 and l[0] == 'Filter' and l[2] == 'ON' and l[3] == 'PK' and l[4] == 'Fc':
                eq += ([l[5], l[8], l[11]], )
    sox_eq = []
    for p in eq:
        sox_eq += ('equalizer', p[0], p[2]+'q', p[1], )
    return ' '.join(sox_eq)

# cmd_rec = '< music.raw'
cmd_rec = 'python recorder.py'
cmd_play = 'python player.py'
# cmd_rec = 'recorder'
# cmd_play = 'player'
eq_left = parse_rew('left.txt')
eq_right = parse_rew('right.txt')
cmd = (
    "trap 'echo trapped; kill -9 $(jobs -p); kill $!; rm -f $L1 $L2 $R1 $R2' 1 2 3 15 EXIT;"
    "L1=$(mktemp -u); R1=$(mktemp -u); L2=$(mktemp -u); R2=$(mktemp -u);"
    "mkfifo $L1 $L2 $R1 $R2;"
    "sox -t raw -b 16 -e signed -c 2 -r 48000 $L1"
    " -t raw -b 16 -e signed -c 1 -r 48000 $L2 remix 1 " + eq_left + " &"
    "sox -t raw -b 16 -e signed -c 2 -r 48000 $R1"
    " -t raw -b 16 -e signed -c 1 -r 48000 $R2 remix 2 " + eq_right + " &"
    + cmd_rec + " tee $L1 > $R1 &"
    "sox -M -t raw -b 16 -e signed -c 1 -r 48000 $L2"
    " -t raw -b 16 -e signed -c 1 -r 48000 $R2"
    " -t raw -b 16 -e signed -c 2 -r 48000 - | cat - | "+cmd_play+" & wait"
    )

import signal
def handle_exit(signum, frame):
    proc.terminate()  # global variable
    print('terminated')
signal.signal(signal.SIGINT, handle_exit)

import subprocess
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
proc.wait()

# debug
# stdout, stderr = proc.communicate()
# print(stdout.decode('utf-8'), stderr.decode('utf-8'))
