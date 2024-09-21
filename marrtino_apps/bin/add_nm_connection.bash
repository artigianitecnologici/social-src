#!/bin/bash

# Use
#   ./add_nm_connection.bash ID IFNAME SSID password priority <auto|address gateway dns>
# Example:
#   ./add_nm_connection.bash Aux wlan0 HomeWifi mypassword 10 192.168.25/24 192.168.25.1 8.8.8.8


ID=$1
IFNAME=$2
SSID=$3
PASS=$4
PRIORITY=$5
ADDR=$6
GW=$7
DNS=$8

sudo nmcli c delete $ID

if [ "$ADDR" == "auto" ]; then

sudo nmcli c add \
  connection.id $ID \
  connection.interface-name $IFNAME \
  connection.type 802-11-wireless \
  connection.autoconnect true \
  connection.autoconnect-priority $PRIORITY \
  802-11-wireless.ssid $SSID \
  802-11-wireless.mode infrastructure \
  802-11-wireless-security.auth-alg open \
  802-11-wireless-security.key-mgmt wpa-psk \
  802-11-wireless-security.psk $PASS \
  ipv4.method auto \
  ipv4.dns 8.8.8.8

else

sudo nmcli c add \
  connection.id $ID \
  connection.interface-name wlan0 \
  connection.type 802-11-wireless \
  connection.autoconnect true \
  connection.autoconnect-priority $PRIORITY \
  802-11-wireless.ssid $SSID \
  802-11-wireless.mode infrastructure \
  802-11-wireless-security.auth-alg open \
  802-11-wireless-security.key-mgmt wpa-psk \
  802-11-wireless-security.psk $PASS \
  ipv4.method manual \
  ipv4.addresses $ADDR \
  ipv4.gateway $GW \
  ipv4.dns $DNS

fi






