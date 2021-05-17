# Neon8-Discord-Bot
*A discord bot I'm attempting to make to do some useful things for playing Vampire the Masquerade 5e.*

*I literally have no idea what I'm doing, so my code is a mess. Sorry. :)*
&nbsp;  
## Things That I'm Using
* **Python 3.5.3 or higher** is required, at minimum. Probably higher though, I'm not really sure. But discord.py requires Python 3.5.3 I am making this bot in [Python 3.9.2](https://www.python.org/downloads/release/python-392/), the most recent stable version at this time.

* **[Discord.py](https://github.com/Rapptz/discord.py) API wrapper**. I was originally using v 1.6.0, but updated to 1.7.1.

* **[SQLite 3.35](https://www.sqlite.org/download.html)**. The RETURNING clause is new in 3.35, which just came out in March 2021, so some of my code won't work without it. I'm using version 3.35.4.

* **[Quantumrandom](https://pypi.org/project/quantumrandom/)** module, for true random number generation. It's really just for funsies, and takes quite a bit longer than pseudo-RNG using randint, but hey, if you think the pseudo-RNG gods hate you, here is an alternative.

* **[Pytz](https://pypi.org/project/pytz/)** for local timezone conversion. I'm using version 2021.1.
&nbsp;  
## What does it do?

### Rolls dice
![Embed and plain text rolls](https://user-images.githubusercontent.com/80991664/118560961-8d782180-b727-11eb-83ca-59b1c75144a4.png)
##### Syntax: `<.command> <total # of dice> <# of hunger dice> <# of successes needed> <comment>`

* There are two versions of the dice roller: a plain text output, and an embed output
* Can add a comment of any length
* Shows the success condition of the roll (e.g. `Success` and `Bestial Failure`), followed by number of successes
* Can use "y" or "yes" in place of the number of hunger dice, to use the hunger value saved in the database for that user

### Takes Notes
![Note-taking](https://user-images.githubusercontent.com/80991664/118562423-e47ef600-b729-11eb-8895-c2ad616ed9cc.png)

* You can write, read, list all available notes, and delete one or more notes
* Commands are, respectively: `.write <note title>`, `.read <note title>`, `.notes`, `.delnote <note title(s)>`
* You can also edit an existing note with `.edit <note title>`. It will send you the contents of the note for you to copypasta, make the edits you want, and then send it back
&nbsp; 

### Some silliness
* Make rolls using quantum number generation with `.qroll`
* Tell the bot that it is a good bot (or a bad bot)
* Send a random image of a peacock
* Damn the Tremere!


## Changes in version 0.0.4
(Some of these are from version 0.0.3 but I never wrote them down. Oops)

* Integrated with the database for rolling dice, so you can use your hunger stat saved in the database!
* Added an editnote command to be able to edit notes
* Made functions to check degeneration and do a remorse roll, but I have to test them more and fine tune them before I can implement them
* Deleted some modules that were unnecessary, and consolidated some. General cleanup.
* Added a bunch of TODOs for me to look at in future :)


## Future

* Working on making specific commands for things like remorse rolls, rouse checks, and frenzy tests, which automatically adjust stats if you fail (if applicable)
* An info command to bring up rules that we commonly have to look up. E.g. `.info degeneration` would show the page number and a summary of how degeneration works
* Full-on character sheets perhaps? We shall see...

&nbsp;  
![dimi sheet](https://user-images.githubusercontent.com/80991664/118564896-6e30c280-b72e-11eb-9530-f30dd5fafdcf.png)