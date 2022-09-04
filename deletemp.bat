echo "stops docker"
sudo docker stop postgres
sudo docker stop odoo_instance_11
sudo docker ps
echo "delete temps"
echo "" > $(docker inspect --format='{{.LogPath}}' postgres)
echo "" > $(docker inspect --format='{{.LogPath}}' odoo_instance_11)
echo "start dockers"
sudo docker start postgres
sudo docker start odoo_instance_11
sudo docker ps
