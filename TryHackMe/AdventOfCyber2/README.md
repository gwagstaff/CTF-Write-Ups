# Advent of Cyber 2
#### Get started with Cyber Security in 25 Days - Learn the basics by doing a new, beginner friendly security challenge every day leading up to Christmas.
#### [Room Link](1)

## Tasks
1. [Day 1] Web Exploitation A Christmas Crisis

Welcomeeeee back to the Advent of Cyber! Since the last year hopefully Santa's elfs are better at securing the network!

First off, we see there is information about DNS, HTTP, and cookies making you think that this will likely focus on basics and work up through the days as we perform more challenges and get better with our skills. After deploying the target machine and open up the IP in the web browser we see this screen asking us to register.

 ![Day1Webpage](2)

We go ahead and register with some credentials and are greeted with this page:

  ![Day1Console][3]

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

 ![SantaConsole][4]

 After firing up all the controls we get our flag!

 This was a good intro and hopefully you learned a few things or brushed up on your skills for the upcoming days!

 See yall on Day 2!

2. Sample
3. Sample
4. Sample
5. Sample

## Review

For links:
[1]: https://tryhackme.com/room/adventofcyber2
[2]: .\resources\day1_webpage.png
[3]: .\resources\day1_console.png
[4]: .\resources\day1_santaconsole.png
[5]:
