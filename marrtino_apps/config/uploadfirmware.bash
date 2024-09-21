#!/bin/bash

cd $HOME/src/srrg/srrg2_orazio/srrg2_orazio/firmware_build/atmega2560
make clean
make orazio.elf
avr-objcopy -O ihex -R .eeprom orazio.elf orazio.hex
avrdude -p m2560 -P /dev/orazio   -c  -b 115200    -D -q -V -C /usr/share/arduino/hardware/tools/avr/../avrdude.conf -c wiring -U flash:w:orazio.hex:i


