path=$(date +%F)
mkdir -p "/home/ubuntu/data/dates/${path}"
mkdir -p "/home/ubuntu/data/keys/${path}"
mkdir -p $path
# ./1.sh &
./2.sh &
./3.sh &
# ./4.sh &
python3.6 zaitakukanri.py 1>>"${path}/zaitakukanri.log" 2>>"${path}/zaitakukanri.log" &
# zip -9 -r $path $path -x \*.log
# python3.6 update.py
# zip -9 -r /home/ubuntu/data/zips/docs /home/ubuntu/data/docs
# zip -9 -r /home/ubuntu/data/zips/images /home/ubuntu/data/images
