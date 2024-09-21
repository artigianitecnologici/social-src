#!/bin/bash

# full device #/dev/mmcblk0, /dev/sdb 
SDDEVICE=/dev/mmcblk0
# partition 1 (boot) #/dev/mmcblk0p1, /dev/sdb1
SDDEVICEp1=/dev/mmcblk0p1
# partition 2 (root) #/dev/mmcblk0p2, /dev/sdb2
SDDEVICEp2=/dev/mmcblk0p2

# No partition table
if [ ! -z "$1" ]; then
#sudo dd if=$1 | pv -s 11G | dd of=${SDDEVICE} bs=512 seek=2048 conv=noerror

# Only boot partition
dd if=$1_boot.img bs=512 of=${SDDEVICEp1}
# count=131072 

# Only root partition
dd if=$1_root.img | pv -s 11G | dd bs=512 of=${SDDEVICEp2}
# count=42659840

sudo sync
fi

