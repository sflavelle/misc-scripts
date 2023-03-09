# misc-scripts
Various scripts I made for different purposes


## watchstream.py
Check a list of streams (~/.config/livestreams.conf) using [Streamlink](https://streamlink.github.io/index.html)'s library, check which links are online, and pick from one to load with the Streamlink binary.

Uses the `streamlink`, `inquirer`, `python-rofi` libraries. Non-TTY support is being worked on using [rofi](https://github.com/davatorium/rofi).

Changelog:

- **2023-03-09** - Initial commit. Pings each channel in ~/.config/livestreams.conf with streamlink, gets those which are live, asks the user which to watch, then runs the result with the Streamlink binary.
