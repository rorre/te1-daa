python test.py sorted 512 &
python test.py random 512 &
python test.py reversed 512 &

python test.py sorted 8192 &
python test.py random 8192 &
python test.py reversed 8192 &

python test.py sorted 65536 &
python test.py random 65536 &
python test.py reversed 65536 &

wait
python result.py