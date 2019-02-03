# BSides Tampa 2019
#### A Thousand Words
#### Stego - 50 points
#### Rating - 1/5 stars


This challenge was a stego challenge made by StormCTF. This challenge was a pretty cool stego challenge in which you were given a list of supposed IPs that was told to have a secret message contained within them.

## Steps

We were first given a .zip archive called [A_Thousand_Words.zip][2] which contained the actual challenge file. After unzipping the file with the password given for all the challenges we get the file  `A Thousand Words.txt`
```
unzip -P BSides2019 A_Thousand_Words.zip
```

After getting the actual challenge file, I ran the usual suite of `file`, `strings | grep BSides` (CTF Flag format), and `xxd` on it to make sure that I was dealing with an text file.

Now knowing I was dealing with actual ASCII text I went ahead and opened it with `more "A Thousand Words.txt"`

At the top of the file we get this story:
```
A Thousand Words Challenge
Story:
Our spies in Relatively_Evil_Country are trying to get us a message to end the conflict.
One of them managed to get us this cryptic message. It just looks like a bunch of IP addresses but that can't be right.
Your mission, should you choose to accept it: Find the message hidden somewhere in the numbers below.
```
After that we get a list of IPs that look normal but after scrolling down I noticed that the IPs last byte all end in 1. So between that and the challenge description stated " A picture is worth "( from the common saying "a picture is worth a thousand words") I was able to decide the the first 3 bytes of the IPs correponded to RGB values of a pixel!

Luckily I saw another writeup of a similar problem only a couple of weeks ago from a tech/ctf youtuber [@JohnHammond][1] and knew how to proceed

 Using that knowledge I was able to to strip out the story from the text file given with
 ```
 cat "A Thousand Words.txt" | grep "^\d" > stripped.txt
 ```

 With this new [stripped.txt][3] I had to then code a python script to put the image back together. Using the line length of 100,000. (calculated `cat stripped.txt| egrep -c "^\d"`) I set the width and height to be 320x320 (just above 100000 pixels). I then read each line of the stripped file and put the pixel/IPs in a list with each value being a tuple of RGB values
 ```python
from PIL import Image

pixels = []
w = 320
h = 320
filename = "stripped.txt"

file = open(filename,"r")

for lines in file:
        color = lines.strip().split('.')
        r = int(color[0])
        g = int(color[1])
        b = int(color[2])
        pixels.append([r,g,b])
 ```
 By printing out the list I could see that I had all the values successfully.

I then used a well-known Python Imaging library called [Pillow][4] that allowed me to build a image out of the RGB values seen in the list.
```python
size = w+1,h+1
img = Image.new("RGB",size)
data = img.load()
counter = 0
for y in range(0,h):
        for x in range(0,w):
                r,g,b = pixels[counter]
                data[x,y] = (r,g,b)
                counter += 1
                #print (x,y,":",counter)

img.save("flag.png")
```
I first had trouble with the list overflowing due to the image size being larger than the pixels provided. This led to images that looked like this.

![flag_failed][5]

But hey, at least we know we are close.
So I go and resize the image to 100x1000 (multiples of 100,000) and we get there! After rotating the image 90 degrees counterclockwise then flipping it vertically we get the flag!

![flag][6]

Flag: BSides{Stego1:01ecedA98eb2Fec92bC16BbB2B59C6a}
#### +50 points

Overall this was a fun problem and it was a joy to see the image come out piece by piece! Thanks to @StormCTF and @HackTheBox for coming up with the problem!

[1]: https://www.youtube.com/watch?v=81sDM2HoGOs
[2]: ./A_Thousand_Words.zip
[3]: ./stripped.txt
[4]: https://python-pillow.org
[5]: ./flag_failed1.png
[6]: ./flag.png
