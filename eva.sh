path=$(date +%F)
mkdir "/home/ubuntu/data/dates/${path}"
mkdir "/home/ubuntu/data/keys/${path}"
./run.sh
# ./update.sh
zip -9 -r /home/ubuntu/data/zips/docs /home/ubuntu/data/docs
zip -9 -r /home/ubuntu/data/zips/images /home/ubuntu/data/images
