#!/usr/bin/env bash
cd ~/lolstardewvalleyoverlay
#~/env/bin/waitress-serve --port=8869 webapp:app
~/env/bin/flask --app webapp.py --debug run --host=0.0.0.0 --port=8869

