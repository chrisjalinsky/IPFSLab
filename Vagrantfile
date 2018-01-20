require 'yaml'

VAGRANTFILE_API_VERSION = "2"

base_dir = File.expand_path(File.dirname(__FILE__))
inventory_file = base_dir + "/ansible/ipfs_inventory.yaml"

servers = YAML.load_file(inventory_file)
meta = servers["_meta"]

def create_vm(config, name, index, ip, memory, cpu, disks, ifaces, box)

  config.vm.define "#{name}" do |de|

    de.vm.box = "#{box}"
    de.vm.hostname = "#{name}"
    set_network(de, ifaces, index)

    de.vm.provider :virtualbox do |vb|

      vb.customize ['modifyvm', :id, '--memory', "#{memory}"]
      vb.customize ['modifyvm', :id, '--cpus', "#{cpu}"]

      if disks.any?
          disks.each_with_index do |d, idx|

            new_idx = idx + 1
            disk_defaults = set_disk_defaults(d, name, new_idx)

            vb.customize ['createhd',
              '--filename', "#{disk_defaults[:filename]}",
              '--size', "#{disk_defaults[:size]}"] unless File.exist?("#{disk_defaults[:filename]}.vdi")

            vb.customize ['storageattach', :id,
              '--storagectl', "SATA Controller",
              '--port', 3 + new_idx,
              '--device', 0,
              '--type', 'hdd',
              '--medium', "#{disk_defaults[:filename]}.vdi"]
          end
      end
    end
  end
end

def set_network(definition, iface_array, index)
  if iface_array.any?
    iface_array.each do |iface|
      if iface.has_key?("bridge")
        definition.vm.network :public_network, bridge: "#{iface['bridge']}"
      elsif iface.has_key?("ip")
        definition.vm.network :private_network, ip: "#{iface['ip']}"
      end
    end
  else
    definition.vm.network :private_network, ip: "10.10.10.#{20 + index}"
  end
end

def set_disk_defaults(disk, name, index, disksize=10000)
  defaults = Hash.new()
  if disk['name']
    defaults[:filename] = "#{disk['name']}-#{index}"
  else
    defaults[:filename] = "#{name.split('.').first}-#{index}"
  end

  if disk['size']
    defaults[:size] = disk['size']
  else
    defaults[:size] = disksize
  end
  return defaults
end

def set_defaults(meta, host, index)

  defaults = Hash.new()

  if meta["hostvars"] && meta["hostvars"][host] && meta["hostvars"][host]["vagrant_cpu"]
    defaults[:cpu] = meta["hostvars"][host]["vagrant_cpu"]
  else
    defaults[:cpu] = 1
  end

  if meta["hostvars"] && meta["hostvars"][host] && meta["hostvars"][host]["vagrant_mem"]
    defaults[:mem] = meta["hostvars"][host]["vagrant_mem"]
  else
    defaults[:mem] = 2048
  end

  if meta["hostvars"] && meta["hostvars"][host] && meta["hostvars"][host]["vagrant_box"]
    defaults[:box] = meta["hostvars"][host]["vagrant_box"]
  else
    defaults[:box] = "bento/ubuntu-16.04"
  end

  if meta["hostvars"] && meta["hostvars"][host] && meta["hostvars"][host]["vagrant_disks"] and meta["hostvars"][host]["vagrant_disks"].any?
    defaults[:disks] = meta["hostvars"][host]["vagrant_disks"]
  else
    defaults[:disks] = []
  end

  if meta["hostvars"] && meta["hostvars"][host] && meta["hostvars"][host]["vagrant_ifaces"] and meta["hostvars"][host]["vagrant_ifaces"].any?
    defaults[:ifaces] = meta["hostvars"][host]["vagrant_ifaces"]
  else
    defaults[:ifaces] = []
  end

  return defaults
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.ssh.insert_key = false
  create_vm_arr = []

  if servers.any?
    servers.each do |ansible_key, vars|
      if vars["hosts"]
        vars["hosts"].each do |host|
          create_vm_arr.push(host)
        end
      end
    end
  end

  if create_vm_arr.any?
    create_vm_arr.uniq.each_with_index do |host, i|
      hostvars = set_defaults(meta, host, i)
      create_vm(config, host, i, hostvars[:ip], hostvars[:mem], hostvars[:cpu], hostvars[:disks], hostvars[:ifaces], hostvars[:box])
    end
  end
end
