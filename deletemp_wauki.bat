echo "stops docker"
sudo docker stop postgresdb2 fe_odoo2 fe_odoo_general fe_odoo_golomix
sudo docker ps
echo "delete temps"
echo "" > $(docker inspect --format='{{.LogPath}}' postgresdb2)
echo "" > $(docker inspect --format='{{.LogPath}}' fe_odoo2)
echo "" > $(docker inspect --format='{{.LogPath}}' fe_odoo_general)
echo "" > $(docker inspect --format='{{.LogPath}}' fe_odoo_golomix)
echo "start dockers"
sudo docker start postgresdb2 fe_odoo2 fe_odoo_general fe_odoo_golomix
