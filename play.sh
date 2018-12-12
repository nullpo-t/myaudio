#!/bin/sh

set -x

trap 'echo trapped; killall -9 sox; rm -f $L1 $L2 $R1 $R2' 1 2 3 15 EXIT; \
L1=$(mktemp -u); R1=$(mktemp -u); L2=$(mktemp -u); R2=$(mktemp -u); \
mkfifo $L1 $L2 $R1 $R2; \
sox -t raw -b 16 -e signed -c 2 -r 48000 $L1 \
  -t raw -b 16 -e signed -c 1 -r 48000 $L2 remix 1 gain -10 & \
sox -t raw -b 16 -e signed -c 2 -r 48000 $R1 \
  -t raw -b 16 -e signed -c 1 -r 48000 $R2 remix 2 gain -10 & \
< music.raw tee $L1 > $R1 & \
sox -M -t raw -b 16 -e signed -c 1 -r 48000 $L2 \
  -t raw -b 16 -e signed -c 1 -r 48000 $R2 \
  -t raw -b 16 -e signed -c 2 -r 48000 - | cat - | python player.py & wait
