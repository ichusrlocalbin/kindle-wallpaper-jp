# raspberry pi の環境構築

## raspberry piの種類

* raspberry 3-b (ボードから確認)

### バージョン表

どの端末にどのバージョンを入れられるかの表

https://en.wikipedia.org/wiki/Raspberry_Pi_OS#Version_history

### version

```
$ cat /etc/os-release 
PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
NAME="Raspbian GNU/Linux"
VERSION_ID="11"
```

## headless setting

macからだと、Paragon社の extFS for Mac (有料)を使うと、ext4にmount出来るため、raspberry piのファイルを直接触れる。

## imageをsd cardに書き込み

https://www.raspberrypi.com/software/ でダウンロードしたimagerを使えば、イメージの設定を選んで、イメージの書き込みまで出来る。
* 無線LANの設定
* sshのkeyの設定
64bitでうまくいかなかった(これが原因かは不明)ので、32bitにした。

### ~~イメージのダウンロード~~

https://www.raspberrypi.com/software/operating-systems/

2023-12-05-raspios-bookworm-arm64.img

### ~書き込み~

https://www.cyberciti.biz/faq/how-to-write-raspbian-jessie-image-file-to-sd-cards-on-apple-macos-os-x/

```
diskutil list
```
でどこにマウントされているか調べる。

```
/dev/disk4 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *31.9 GB    disk4
   1:             Windows_FAT_32 boot                    66.1 MB    disk4s1
   2:                      Linux                         31.8 GB    disk4s2
```

以下、 `/dev/disk4` にあるものとする

```
diskutil unmountDisk /dev/disk4
```

```
sudo dd bs=2M if=~/Downloads/2023-12-05-raspios-bookworm-arm64.img of=/dev/rdisk4
```

`rdisk4` と `r` がついている点に注意


## 設定

### ssh

`/home/pi/.ssh/authorized_keys`

```
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0XGEYgxfZziZOkPP/ce2MO5MTEq/BHjeBtOLn/11cPrjikdTXdEJAWwB8dW/LZErf+nVd/uMjPq+F2jbZHhmrz9bxdWGzKfvOKZxNEO167JqL01TcUcF69I++TX7+jJiSikr5fbrLYMA3qeOwW6RaOEy0y0t9tlXHnZJMBTkti+LkGy7rZMRv57vBZ/gXy6ne2yBLzjyqt5kHKx8JyDvwAuOaKdQsN78wsEKRPei0UpYhuK3qw2MVYz10Pxlanruc7GW35U9mbFp5yICp0/25VRzVGexD7x8Q27K6zaRm6NAWs2q6kDirNrcvs7/xTePUnXInX2E/wM9FrwQS849dQ== watanabe.masahiro.g@gmail.com
```

### wifi

`/etc/wpa_supplicant/wpa_supplicant.conf`

https://www.seeedstudio.com/blog/2021/01/25/three-methods-to-configure-raspberry-pi-wifi/

```
country=GB
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
        ssid="masa"
        psk="otaxxxxxx"
}
```

`/etc/network/interfaces.d/wlan0`

```
allow-hotplug wlan0
iface wlan0 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

`/etc/dhcpcd.conf`

```
# A sample configuration for dhcpcd.
# See dhcpcd.conf(5) for details.

# Allow users of this group to interact with dhcpcd via the control socket.
#controlgroup wheel

# Inform the DHCP server of our hostname for DDNS.
hostname

# Use the hardware address of the interface for the Client ID.
clientid
# or
# Use the same DUID + IAID as set in DHCPv6 for DHCPv4 ClientID as per RFC4361.
#duid

# Persist interface configuration when dhcpcd exits.
persistent

# Rapid commit support.
# Safe to enable by default because it requires the equivalent option set
# on the server to actually work.
option rapid_commit

# A list of options to request from the DHCP server.
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
# Most distributions have NTP support.
option ntp_servers
# Respect the network MTU.
# Some interface drivers reset when changing the MTU so disabled by default.
#option interface_mtu

# A ServerID is required by RFC2131.
require dhcp_server_identifier

# Generate Stable Private IPv6 Addresses instead of hardware based ones
slaac private

# A hook script is provided to lookup the hostname if not set by the DHCP
# server, but it should not be run by default.
nohook lookup-hostname

interface wlan0
static ip_address=10.0.1.199/24
static routers=10.0.1.1
static domain_name_servers=10.0.1.1
```

`~/.ssh/config`

```
Host pi
     HostName 10.0.1.199
     User pi
     StrictHostKeyChecking  no
     PasswordAuthentication no
     IdentityFile           ~/.ssh/id_rsa_raspberry_pi
     IdentitiesOnly        yes
     HostKeyAlgorithms +ssh-rsa
     PubkeyAcceptedAlgorithms +ssh-rsa
```

### docker install

[Install Docker Engine on Raspberry Pi OS (32-bit)]https://docs.docker.com/engine/install/raspberry-pi-os/ に従う

古いバージョンの削除

```bash
$ for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

リポジトリの設定

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/raspbian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up Docker's APT repository:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/raspbian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

インストール

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

sudoなしでの実行

```bash
sudo usermod -aG docker pi
```

一回ログアウトして入り直し
```bash
exit
ssh pi
```

テスト
```bash
$ groups
pi adm dialout cdrom sudo audio video plugdev games users input render netdev lpadmin docker gpio i2c spi
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```


### kindle-wallpaper-jp

```bash
cd
git clone https://github.com/ichusrlocalbin/kindle-wallpaper-jp.git
```
