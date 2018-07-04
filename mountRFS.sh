#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "[!] This script must be run as root" 
   exit 1
fi

#VARIABLES - Change at will

USER=pq2
mountpoint=/mnt/RFS
fstype=ramfs
#size in MB with m
size=1024m


#CODE


echo "[+] Mounting $size $fstype fs at $mountpoint  ..."
mount -t $fstype -o size=$size $fstype $mountpoint
if [[ $? -ne 0 ]]; then
	echo "[!] There was a problem while mounting. Exit status:" $?
	exit -1
fi
echo "[+] Giving ownership chown to $USER at $mountpoint..."
chown $USER $mountpoint
if [[ $? -ne 0 ]]; then
        echo "[!] There was a problem with chown command. Exit status:" $?
        exit -2
fi
exit 0


