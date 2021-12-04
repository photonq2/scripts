#!/bin/bash

#i could have done this with opt but i decided its a dirty script

if [[ $EUID -ne 0 ]]; then
   echo "[!] This script must be run as root" 
   exit -1
fi

if id "$1" &>/dev/null; then
    user=$1
else
    echo "[!] user do not exist. give me user as first param"
    exit -2
fi

if [[ -d "$2" ]]
then
    mountpoint=$2
else
    echo "[!] directory do not exist. give me mountpoint as second param"
    exit -2
fi

if [[ -d "$3" ]]
then
    size=$3
else
    echo "[!] i need a size 1234m. give me size as third param"
    exit -2
fi

fstype=ramfs


echo "[+] Mounting $size $fstype fs at $mountpoint  ..."
mount -t $fstype -o size=$size $fstype $mountpoint
if [[ $? -ne 0 ]]; then
	echo "[!] There was a problem while mounting. Exit status:" $?
	exit -1
fi

echo "[+] Giving ownership chown to $user at $mountpoint..."
chown $USER $mountpoint
if [[ $? -ne 0 ]]; then
        echo "[!] There was a problem with chown command. Exit status:" $?
        exit -2
fi

echo "[+] Good to go. Mounted for $user, at $mountpoint. Size: $size"
exit 0


