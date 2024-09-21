# MARRtino AudioServer program #

MARRtino Python AudioServer program to play sounds saved as uncompressed PCM 16 bit 44100 Hz WAV files.

## Install ##

Note: installation is not necessary when using dockerized components.

* Requires pyglet

```
$ sudo -H pip install pyglet
```

* Libraries for speech and sound
```
$ sudo apt install sox
$ sudo apt install libttspico-utils
```
In case of 'locale.Error: unsupported locale setting' set 
```
export LC_ALL=C
```



## Run ##

* Run the server

```
$ python audio_server.py [TTSPORT] [ASRPORT]

```

Note: to run it from a remote shell set 'export DISPLAY=:0'

* Run the client

Connect with a TCP client sending the name of the sound to play (i.e., filename without ".wav")
or a string to say beginning with TTS (e.g., 'TTS hello, how are you?')

Example:

```
$ python audio_client.py [IP] [PORT]

```



## Adding new sounds ##

WAV (PCM 16 bit 44100 Hz) files must be placed in the 'sounds' directory.


* Synth generation

```
$ sox -n --no-show-progress -G --channels 1 -r 44100 -b 16 -t wav bip.wav synth 0.25 sine 800 
$ sox -n --no-show-progress -G --channels 1 -r 44100 -b 16 -t wav bop.wav synth 0.25 sine 400 
```

* Voice generation
```
$ pico2wave -l "it-IT" -w start.wav "Bene! Si Parte!"
```

* Record souund

Use audacity.



