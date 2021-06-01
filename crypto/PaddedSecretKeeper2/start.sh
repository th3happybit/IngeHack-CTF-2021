#! /bin/sh
echo "Start Run Socat"
echo "[Debug] " socat tcp-listen:9999,fork,su=nobody EXEC:"python server.py"
exec socat -v tcp-listen:9999,fork,reuseaddr,su=chall EXEC:"python server.py"