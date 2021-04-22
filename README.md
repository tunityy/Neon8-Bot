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
## Changes

### Dice Rolling
Added a cog and associated functions for rolling dice for v5. Includes a plain output, embed output, and a plain version using quantum number generation for funsies.
* Need to integrate with the database so that hunger dice can automatically be added to rolls
* Eventually make specific rolls for things like remorse and rouse, that will automatically adjust the pertinent stats if you fail

### Taking Notes
Added a note-taking cog! I have functions to write, read, list all available notes, and delete one or more notes.
* I'm also working on making it so you can edit an existing note.

### Database Stuff!
Trying to make it so I can look up character stats in the database, in various combinations. I've done a lot of work, but now I'm trying to streamline. I'm in the super awkward in-between stage where everything is a huge mess right now, but I wanted to make a new commit to back up what I have done so far.