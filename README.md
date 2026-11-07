
# SilenceBreaker #

Random sound alert program inspired by *"1 Hour of Silence Occasionally Interrupted by ____"* videos.
It allows you to select any variety of random interruption sounds.


## Installation ##

## Linux Mint, Linux Lite:
```
git clone https://github.com/JsaBuilds/silencebreaker.git
pip install -r requirements.txt
bash setup.sh
```

## Ubuntu (tested on 24.04):

```
git clone https://github.com/JsaBuilds/silencebreaker.git
sudo apt install python3-pygame python3-tk
bash setup.sh
```

## Adding sounds ##

When you first setup and launch the program, you will be prompted to select a directory in which to store
your sound files. The program automatically adds sounds from that directory to the main panel as alert 
buttons. To change that directory later, click on the 'Select alerts folder' button.
You may add subfolders to the alerts directory to create seperate playlists (tabs) in the program.
(NOTE: Currently there is no refresh in place. In order to see new sounds added to the panel, you must
restart the program.)

## Controls ##

Press `A` to activate all sounds under a tab.

Press `Q` to deactivate all sounds under a tab.

Use UP and DOWN arrow keys to precisely adjust maximum delay time.

Use RIGHT and LEFT arrow keys to increment / decrement maximum delay time by 1 minute.

Switch between tabs with the tab buttons on the right side of the screen. (Tabs are categorized by subdirectories)