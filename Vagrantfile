# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "debian/jessie64"

  # We can now access the VM from the IP address below.
  config.vm.network "private_network", ip: "10.0.0.1"

  config.vm.provider "virtualbox" do |vb|
    #Memory in kb
    vb.memory = "1024"
  end
  config.vm.provision :shell, path: "setup.sh"
end
