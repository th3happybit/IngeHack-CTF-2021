#! /bin/sh
echo "Start Run Socat"
echo "[Debug] " socat tcp-listen:9999,fork,su=nobody EXEC:"python station.py"
exec socat -v tcp-listen:9999,fork,reuseaddr,su=chall EXEC:"python station.py"