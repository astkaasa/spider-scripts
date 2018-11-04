path=$(date +%F)
mkdir -p $path
./1.sh &
./2.sh &
./3.sh &
./4.sh &
# python3.6 zaitakukanri.py 1>>"${path}/zaitakukanri.log" 2>>"${path}/zaitakukanri.log"
# zip -9 -r $path $path -x \*.log
