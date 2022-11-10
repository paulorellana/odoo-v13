sudo git pull
echo "Paramatro: " $1
cp -R $1 ../odooperuerp_v13/addons/;
sudo docker restart fe_odoo;
