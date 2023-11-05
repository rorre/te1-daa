python test.py sorted 512 --reuse &
python test.py random 512 --reuse &
python test.py reversed 512 --reuse &

python test.py sorted 8192 --reuse &
python test.py random 8192 --reuse &
python test.py reversed 8192 --reuse &

python test.py sorted 65536 --reuse &
python test.py random 65536 --reuse &
python test.py reversed 65536 --reuse &

wait
python result.py