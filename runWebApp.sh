#!/usr/bin/env bash
cd ~/lolstardewvalleyoverlay
nohup ~/env/bin/waitress-serve --port=8869 webapp:app
