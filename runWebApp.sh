#!/usr/bin/env bash
cd ~/lolstardewvalleyoverlay
nohup ~/env/bin/waitress-serve --port=8888 webapp:app >> webapp.log &
