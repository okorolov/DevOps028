# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.network :forwarded_port, guest: 5432, host: 5432, id: "postgres", auto_correct:true
  config.vm.network :forwarded_port, guest: 9000, host: 9000, id: "samsara", auto_correct:true

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

  config.vm.provision :shell, path: "init_script.sh"

end
