echo "stops docker"
sudo docker stop db10
sudo docker stop fe_odoo
sudo docker ps
echo "delete temps"
echo "" > $(docker inspect --format='{{.LogPath}}' db10)
echo "" > $(docker inspect --format='{{.LogPath}}' fe_odoo)
echo "start dockers"
sudo docker start db10
sudo docker start fe_odoo
sudo docker ps
