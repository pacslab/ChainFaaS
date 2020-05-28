sudo apt update
sudo apt -y install docker.io

docker ps
sudo docker ps

sudo usermod -aG docker $USER
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "/home/$USER/.docker" -R
sudo chown "$USER":"$USER" /var/run/docker.sock
sudo chmod g+rwx /var/run/docker.sock -R
sudo systemctl enable docker

sudo systemctl start docker
sudo systemctl enable docker

sudo apt update
sudo apt  install docker-compose

CADDY_TELEMETRY=on curl https://getcaddy.com | bash -s personal hook.service
# pip3 install -r requirements.txt