#!/bin/sh

run_pytest() {
    pytest "$@"
}

run_bash() {
    exec /bin/bash -l
}

run_main() {
    while true; do
        python main.py
        sleep 60
    done
}

case "$1" in
    pytest)
        shift
        run_pytest "$@"
        ;;
    bash)
        run_bash
        ;;
    *)
        run_main
        ;;
esac