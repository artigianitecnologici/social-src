#!/bin/bash

# full device #/dev/mmcblk0, /dev/sdb 
SDDEVICE=/dev/sdb
# partition 1 (boot) #/dev/mmcblk0p1, /dev/sdb1
SDDEVICEp1=/dev/sdb1
# partition 2 (root) #/dev/mmcblk0p2, /dev/sdb2
SDDEVICEp2=/dev/sdb2


if [ -z "$1" ]; then
OUTFILE=marrtino
else
OUTFILE=$1
fi

echo $OUTFILE

# All partitions excluding partition table
#sudo dd if=${SDDEVICE} b  s=512 skip=2048 count=20611072 | pv -s 10G | dd of=${OUTFILE}.img

# Only boot partition
dd if=${SDDEVICEp1} bs=512 of=${OUTFILE}_boot.img
# count=131072

# Only root partition
dd if=${SDDEVICEp2} bs=512 | pv -s 10G | dd of=${OUTFILE}_root.img
# count=42659840


