# lolstardewvalleyoverlay
I'm a dork

## What is this
This is a website you can run and also use as an overlay in OBS to track your friendship points with others people. It's a manual tracker, it doesn't integrate with the game in anyway. In that sense, I suppose you could use it for any reason and not just for Stardew Valley.

## How do I use this?
Windows instructions. Linux instructions are mostly the same, except running the .sh versions of the files.
* Install python
  * Windows (linux nerds should know how to do this...): 
  * Open a terminal or command prompt
  * type ```winget install -e --id Python.Python.3.12```
  * Close the terminal
* Download this package
  * Click the Code button and either Open with GitHub Desktop, or Download ZIP
  * If you downloaded the ZIP unzip it somewhere
* Shift + Right click on the folder that contains the files you downloaded (or the folder you unzipped them in) and select "Open Terminal here" or "Open Powershell here" or similar
* Type install.bat
* Then type run.bat
* In your browser go to http://127.0.0.1:8069/adminpanel
* If you want to add it in OBS or 'view it', use http://127.0.0.1/
* When you update the adminpanel, it'll auto update the view in OBS or whatever. By default the non-admin view refreshes every 2 seconds. You can change refresh time in adminpanel.
