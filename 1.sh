path=$(date +%F)
python3.6 leopalace21.py 1>>"${path}/leopalace21.log" 2>>"${path}/leopalace21.log" &
python3.6 livemax-system.py 1>>"${path}/livemax-system.log" 2>>"${path}/livemax-system.log" &
python3.6 artavenue.py 1>>"${path}/artavenue.log" 2>>"${path}/artavenue.log" &
