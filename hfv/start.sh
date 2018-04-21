#bin/sh
python3 testDevice.py &
python3 listenSer.py &
python3 getData.py &
python3 workProcess.py 
