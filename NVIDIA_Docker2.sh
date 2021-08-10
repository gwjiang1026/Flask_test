
#install docker ce 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial edge" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update && sudo apt-get install -y docker-ce=5:18.09.4~3-0~ubuntu-xenial

#install NVDIA and Driver/CUDA
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo apt-get update
sudo apt-get install -y linux-headers-$(uname -r)
sudo apt-get -o Dpkg::Options::="--force-overwrite" install -y cuda-10-0 cuda-drivers


#TEST NVIDIA Dirver and  CUDA
sudo nvidia-smi


#install NVIDIA Docker v2
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu16.04/amd64/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2=2.0.3+docker18.09.4-1 nvidia-container-runtime=2.0.0+docker18.09.4-1
sudo pkill -SIGHUP dockerd

#update docker ce
sudo apt search docker-ce
sudo apt install -y docker-ce

#test
sudo docker run --runtime=nvidia --gpus all --rm nvidia/cuda:9.0-base nvidia-smi
