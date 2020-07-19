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

# install docker compose
echo "Installing docker compose"
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

CADDY_TELEMETRY=on curl https://getcaddy.com | bash -s personal hook.service
# pip3 install -r requirements.txt