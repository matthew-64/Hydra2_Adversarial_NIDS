Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell",
    inline: "sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install ubuntu-desktop -y && sudo apt-get install virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11 -y"
  config.vm.provider "virtualbox" do |vb|
        vb.gui = true
        vb.memory = "2048"
        vb.customize ["modifyvm", :id, "--vram", "12"]
  end
  config.vm.network "private_network", type: "dhcp"
  config.vm.synced_folder "./", "/opt/adversarialtestingsdn/"
  config.vm.provision :shell, inline: "sudo /opt/adversarialtestingsdn/setup.sh"
  #config.vm.network :forwarded_port, guest: 8000, host: 8000
  # uncomment the following line will make the vm run experiment automatically
  #config.vm.provision "shell", inline: "python /opt/adversarialtestingsdn/manage.py runserver"
end

