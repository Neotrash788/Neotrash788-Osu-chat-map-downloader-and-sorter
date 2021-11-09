Given given a text file with the beatmap links and headings the program will download all the beatmaps in the text file and sort them into folders based on the headings before them. Timestamps and

The input file sould look like this:

1 This is a heading
2 osu.ppy.sh/beatmapsets/873811#osu/1829038!
3 Also a heading
4 00:00
5 is listening to [osu.ppy.sh/beatmapsets/
6 906786#/1909493 Koda Kumi - Guess Who Is Back (TV Size)
7 is listening to [osu.ppy.sh/beatmapsets/\359472#/\792670 Itou Kanako - Amadeus]

Then inside the 'OsuFiles' folder there will be a tree which looks like this:

This is a heading:
---map1.osz

Also a heading
---map2.osz
---map3.osz

This requires selenium to be installed, if you do not have selenium run the 'install.bat' file which will install it with the command line.

This also requires the webdriver for the version of chrome you are useing, to find the version you can click the 'three verticle dots' in the top right of a chrome windo. Then click 'Help' and 'About Chrome'

The download link is here, make sure you replace the webdriver in the folder with the version which souports you with the same name.

https://chromedriver.chromium.org/downloads The one this comes with is version 95
