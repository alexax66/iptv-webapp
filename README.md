# IPTV Web App

## Motivation

Looking for an easy application to simulate linear (satellite or cable) TV but using the TV station's own IPTV streams without requiring the Internet provider's or an over-the-top (OTT) provider's TV streaming service. It uses the streams which TV stations themselves publish (in Germany, public stations financed by the general population).

Just like a real TV: One application for the live streams of all TV stations, not one per station (ARD, ZDF, etc.)

## Features

- Load and parse M3U playlists, e.g,. from https://github.com/jnk22/kodinerds-iptv/blob/master/iptv/kodi/kodi_tv.m3u or from https://github.com/Free-TV/IPTV/blob/master/playlists/playlist_germany.m3u8
- Switch channels using the + and - buttons on the keyboard, and/or using 1-digit and 2-digit numbers on the remote control or keyboard
- Automatically play the selected channel

## Installation

Just open [`index.html`](https://htmlpreview.github.io/?https://github.com/probonopd/iptv-webapp/blob/main/index.html) in a modern web browser.

### On Smart TVs

As a stetch goal, it would be nice if we could get this to work on, e.g., Samsung (pre-Tizen) Smart TVs with the "Samsung Legacy Platform" (Orsay), e.g., the F series from 2013.

To sideload:

- Copy the contents of this directory into a directory on a FAT32 formatted USB stic
- Insert the USB stick into your Samsung TV
- Navigate to the "Smart Hub" on your TV
- Go to "My Apps" and look for an option to manage or install apps from a USB device

Currently it can be launched but doesn't seem to play the streams. We need to find a way to see the debug output of the embedded browser in the Samsung Smart TV to see what is going on. Possibly we need to use the [TV SDK for Samsung Legacy Platform](https://developer.samsung.com/smarttv/legacy/tools/history.html) to do this in a simulator?
