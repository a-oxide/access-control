#!/bin/bash
intexit() {
    # Kill all subprocesses (all processes in the current process group)
    kill -HUP -$$
}

hupexit() {
    # HUP'd (probably by intexit)
    echo
    echo "Interrupted"
    exit
}
trap hupexit HUP
trap intexit INT

export FLASK_APP=webapp
export FLASK_ENV=development
echo "Starting camera"
python live_feed.py &
sleep 18
flask run --host=0.0.0.0

wait