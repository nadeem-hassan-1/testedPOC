provider "google" {
  project     = "saip-poc-0106"
  region      = "me-central2"
  zone        = "me-central2-a"
  credentials = file("~/saip-poc-0106-e05f2284f87b.json")
}

resource "google_compute_instance" "haproxy_test_vm" {
  name         = "haproxy-test-vm"
  machine_type = "e2-medium"
  zone         = "me-central2-a"

  boot_disk {
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2404-lts-amd64"
    }
  }

  network_interface {
    subnetwork = "saip-subnet"
    access_config {}
  }

  metadata = {
    startup-script = <<-EOT
      #!/bin/bash
      set -e
      apt-get update
      apt-get install -y haproxy

      cat <<EOF > /etc/haproxy/haproxy.cfg
      global
        log /dev/log    local0
        maxconn 2000

      defaults
        log     global
        mode    http
        option  httplog
        timeout connect 5s
        timeout client  50s
        timeout server  50s

      frontend http_front
        bind *:80
        default_backend http_back

      backend http_back
        server app1 app1.saip-subnet.c.saip-poc-0106.internal:80 check
        server app2 app2.saip-subnet.c.saip-poc-0106.internal:80 check
      EOF

      systemctl restart haproxy
    EOT
  }

  tags = ["loadbalancer"]
}

resource "google_compute_instance" "app1" {
  name         = "app1"
  machine_type = "e2-micro"
  zone         = "me-central2-a"

  boot_disk {
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2404-lts-amd64"
    }
  }

  network_interface {
    subnetwork = "saip-subnet"
    access_config {}
  }

  metadata = {
    startup-script = <<-EOT
      #!/bin/bash
      set -e
      apt-get update
      apt-get install -y nginx
      echo "Hello from app1" > /var/www/html/index.html
      systemctl restart nginx
    EOT
  }

  tags = ["app"]
}

resource "google_compute_instance" "app2" {
  name         = "app2"
  machine_type = "e2-micro"
  zone         = "me-central2-a"

  boot_disk {
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2404-lts-amd64"
    }
  }

  network_interface {
    subnetwork = "saip-subnet"
    access_config {}
  }

  metadata = {
    startup-script = <<-EOT
      #!/bin/bash
      set -e
      apt-get update
      apt-get install -y nginx
      echo "Hello from app2" > /var/www/html/index.html
      systemctl restart nginx
    EOT
  }

  tags = ["app"]
}

