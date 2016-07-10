# Networking, Security, Data

A bunch of other concepts we need to know. How do computers talk to each other? Are default passwords bad?

## Networking

[Raspberry Pi Networking Lessons](https://www.raspberrypi.org/learning/networking-lessons/)

* Network configuration for our cluster
 - Public or NAT access via WiF
 - Restrict parallel application and storage traffic over private
 Ethernet
* [Private network](https://en.wikipedia.org/wiki/Private_network)
  ([RFC 1918](https://tools.ietf.org/html/rfc1918)) addresses defined
  for the Ethernet interfaces.
* You've probably seen these as `192.168.0.1` or similar.
* The network is `10.0.0.0/23` (Don't know what the `/23` means? Looks
  at this [cheat sheet](https://www.aelius.com/njh/subnet_sheet.html).)
* Here's the private addresses for four nodes. These can be changed in
  the configuration easily.

  ```
  10.0.0.10	pinode-0
  10.0.0.11	pinode-1
  10.0.0.12	pinode-2
  10.0.0.13	pinode-3
  ```

* Make sure they don't collide at your home institution!
* Look at `pinode-0`'s
  [network interface configuration](../config/pinode-0/network/interfaces)
  for an example.
* We assume that the WiFi addresses are handled by [Dynamic Host Configuration Protocol](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol) (DHCP).

## Security

* Default passwords are only OK on isolated devices.
* SDSC is hit by a quarter to half-a-million login attacks daily.
* Several hundred of those attempts to login are as the default Pi user.
* If your Raspberry Pi is going onto a network you don't know, change
  the password.
* Your school's network might not be trustworthy. If a device (like a
laptop) on the network is compromised it can scan the private network.
* Don't store passwords or important information on the Pis unless
  you're managing properly.

### SSH

* SSH is a secure way to connect to another machine via the command
line.
* Used everywhere for administration and software development.
* Can use passwords or
  [SSH keys](http://www.cyberciti.biz/faq/how-to-set-up-ssh-keys-on-linux-unix/)
  (public and private files to handle cryptography).
* We use keys for access between the Pis in our cluster.
  - We generate a public-private pair with no passphrase and add the
  public one to the authorized list.
  - Because of this, these keys are only good within our cluster.
  - **Do not reuse them outside of the cluster!**

## Data

* When first set up, each Raspberry Pi has its own _home directory_ `/home/pi`
for the `pi` user.
* This is typically where you keep all of the files you're working on,
programs you're writing, etc.
* It's convenient to have the same data on all the Pis.
* We can solve this by having `pinode-0` export (share) its `/home`
directory to the other nodes over the private network.
* This is done using
  [Network File System](https://en.wikipedia.org/wiki/Network_File_System)
  (NFS) like sharing drives on Windows.
* We put it on the private Ethernet network to keep it fast and
secure.
* The export definition one `pinode-0` is

  ```
  /home              10.0.0.0/23(rw,sync)
  ```

* The other nodes mount this using

  ```
  10.0.0.10:/home  /home          nfs    defaults           0       0
  ```
  
## Next

[Configuration](config.md)

## Previous

[Assembly](assembly.md)

## Agenda

[Agenda](agenda.md)
