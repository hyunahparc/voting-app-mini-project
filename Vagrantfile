# -*- mode: ruby -*-
# vi: set ft=ruby :

NODES = {
  "manager1" => "192.168.99.100",
  "worker1" => "192.168.99.101",
  "worker2" => "192.168.99.102",
}

Vagrant.configure("2") do |config|
  NODES.each do |(node_name, ip_address)|
    config.vm.define node_name do |node|
      node.vm.box = "bento/ubuntu-22.04"
      node.vm.hostname = node_name
      node.vm.network "private_network", ip: ip_address

      # Share project folder into the VM
      config.vm.synced_folder "./", "/home/vagrant/voting-app-swarm"
      
      # Add port forwarding (host → guest)
      if node_name == "manager1"
        node.vm.network "forwarded_port", guest: 5000, host: 5000  # vote 서비스
        node.vm.network "forwarded_port", guest: 3000, host: 3000  # result 서비스
      end

      node.vm.provider "vmware_desktop" do |v|
        v.vmx["displayname"] = node_name
        v.vmx["memsize"] = "1024"
        v.vmx["numvcpus"] = "1"
      end

      # Provisioning script
      node.vm.provision "shell", inline: <<-SHELL
        # Add all nodes to /etc/hosts
        #{NODES.map{ |n_name, ip| "echo '#{ip} #{n_name}' | sudo tee -a /etc/hosts" }.join("\n")}

        # Install Docker
        sudo apt-get update -y
        sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update -y
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

        # Expose Docker daemon over TCP
        sudo mkdir -p /etc/systemd/system/docker.service.d
        sudo bash -c 'echo -e "[Service]\nExecStart=\nExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375" > /etc/systemd/system/docker.service.d/options.conf'
        sudo systemctl daemon-reload
        sudo systemctl restart docker
      SHELL

      # Pull default Docker images
      node.vm.provision "docker" do |d|
        d.pull_images "alpine:latest"
      end
    end
  end
end
