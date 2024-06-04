# IPTV Web App

## Motivation

Looking for an easy application to simulate linear (satellite or cable) TV but using the TV station's own IPTV streams without requiring the Internet provider's or an over-the-top (OTT) provider's TV streaming service. It uses the streams which TV stations themselves publish (in Germany, public stations financed by the general population).

Just like a real TV: One application for the live streams of all TV stations, not one per station (ARD, ZDF, etc.)

## Features

- Load and parse M3U playlists, e.g,. from https://github.com/jnk22/kodinerds-iptv/blob/master/iptv/kodi/kodi_tv.m3u or from https://github.com/Free-TV/IPTV/blob/master/playlists/playlist_germany.m3u8
- Switch channels using the + and - buttons on the keyboard, and/or using 1-digit and 2-digit numbers on the remote control or keyboard
- Automatically play the selected channel

## Installation

Just open [`webapp/index.html`](https://raw.githack.com/probonopd/iptv-webapp/main/webapp/index.html) in a web browser on the PC (tested in 2023 Edge).

### On Smart TVs

As a stetch goal, it would be nice if we could get this (or something similar to it) to work on, e.g., Samsung (pre-Tizen) Smart TVs with the "Samsung Legacy Platform" (Orsay), e.g., the F series from 2013.

To sideload:

- Copy the contents of this directory into a directory on a FAT32 formatted USB stick
- Insert the USB stick into your Samsung TV
- Navigate to the "Smart Hub" on your TV
- Go to "My Apps" and look for an option to manage or install apps from a USB device

Currently it can be launched but doesn't seem to play the streams. We need to find a way to see the debug output of the embedded browser in the Samsung Smart TV to see what is going on. Possibly we need to use the [TV SDK for Samsung Legacy Platform](https://developer.samsung.com/smarttv/legacy/tools/history.html) to do this in a simulator, e.g., from Samsung TV SDK 4.1.

For information on how to load Orsay applications via the network, see https://github.com/oherau/jellyfin-samsung-orsay-os. Using a USB stick seems simpler but possibly does not open the port to access the Remote Web Inspector (RWI) at http://tvip:7011, unlike when loading Orsay applications via the network. As an alternative to RWI, the Weinre debugger might be used: https://www.youtube.com/watch?v=4nL6xey13fE (the server seems to require `node` on the machine on which the server is to be hosted).

`samsung-orsay/server.py` contains a web server that can serve Orsay applications over the network without the need to package them as zip files first (it does that on the fly), potentially allowing for relatively quick development-test cycles.