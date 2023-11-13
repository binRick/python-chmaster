#!/usr/bin/env bash
set -eou pipefail
run_server()(
	cd assets
	python -m http.server 8081 >&2 &
	pid=$!
	cd ../
	echo $pid
)

pid="$(run_server)"
echo pid=$pid

kill_server(){
	kill $pid
}

trap kill_server EXIT

./server1.py ${@:-}
