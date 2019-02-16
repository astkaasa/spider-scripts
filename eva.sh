path=$(date +%F)
./run.sh
./update.sh
zip -9 -r /home/ubuntu/data/zips/docs /home/ubuntu/data/docs
zip -9 -r /home/ubuntu/data/zips/images /home/ubuntu/data/images
