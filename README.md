<p align="center">
    <h1 align = "center">CRT-MultiApp</h1>
</p>
<p align="center">
    
Originally a quiz app made in Python with TKinter where you can put in a list of player names and a list of questions, and be tested on them!
But it is now a general fun app that has a CRT style screen and a bunch of cool options via a Text Terminal type interface.

There are also a bunch of other features too! Such as _rickrolls_, a _gamble_ feature and default player and quiz questions, along with other projected ideas that aren't do do with the main **quiz** function. I am planning on adding more features (such as gamemodes other than the main quiz) later, and these will appear in the README! To get a full list of commands while in the terminal, you can type 'help', and to learn how to use the commands, type 'syntax'!

There are no answers in the quiz mode, it is designed for you to host in front of a class of students or colleagues and test them, with the host clicking keys to determine whether they got a question _right_ or _wrong_!

**WARNING! CONTAINS FLASHING! DO NOT USE IF SENSITIVE TO FLASHING LIGHTS**

</p>

The **projected** OS versions will be:
 - Windows (x64)
 - MacOS (15 - Apple Silicon)
 - Linux (Ubuntu)
 - If more **OS**s are requested, then create a [Suggest Issue](https://github.com/sadgituser/CRT-MultiApp/issues/new?template=feature_suggest.md) with the code for the build.yml GitHub Actions file!

<p align="center">

![App Screenshot](/Assets/app_screenshotpng.png)

</p>

<p align="center">
    
That is basically it, if you want to try it out, then download the latest [Release](https://github.com/sadgituser/Python-Quiz/releases) from GitHub for your OS!

Ensure to use `chmod +x` if running the file on Linux to grant executing permissions!


There are also some other important keybinds (_QUIZ MODE_) that you will need to know, such as:
 - 'y': Correct answer! Allows that player to progress in the game
 - 'i': Incorrect answer! The player will go to last chance if they are not already on it, else be eliminated!
 - 'p': If the player has skips remaining, then skip the question that they are on
 - 'q': Manually trigger 'Last Chance' for the player. Adds 5 seconds to their timer and when the quiz is continued, they will be re-asked the same question again!
 - 'n': Proceed to the next player and question in the quiz after the screen flash

In _quiz mode_, 'Last Chance' can be manually triggered. 'Last Chance' allows for the player to survive through an incorrect question and not be eliminated. If it is manually triggered, then the player will still have the same question, but have 5 seconds extra time!

An issue that I have not covered is having players of the same name! (_Quiz mode_) Ensure that players all have different names!

Check out my GitHub [here](https://github.com/sadgituser) and my [Etsy Shop](https://theprintedcraftuk.etsy.com)!

If you want to make an issue, then you can go to [Bug Report](https://github.com/sadgituser/Python-Quiz/issues/new?template=bug_report.md) or to [Feature Suggest](https://github.com/sadgituser/Python-Quiz/issues/new?template=suggest_feature.md)!


If you want to change this code, then make sure that you update stateVars.py (which contains all of the variables needed for main.py and quiz_defs.py) and quiz_defs.py (which contains all of the definitions/functions needed for the main window, CRT functionality and quiz functionality to work)!


![The icon of my Etsy shop](/Assets/photo3.png)


[Hackclub Assets](https://hackclub.com/brand) & [Music Assets](https://pixabay.com/sound-effects/technology-noisy-computer-hum-34737/) & Terra Fox was snipped and edited from the [Terra](terra.hackclub.com) website! Check it out along with other [HC](https://hackclub.com) projects!

Made for the [Hackclub Terra](https://terra.hackclub.com) project (originally) for [Hackclub](https://hackclub.com).
It started out with Terra, but it will now be moving onto _[Phantom](https://phantom.hackclub.com)_

</p>


<p align="center">

<img src="/Assets/photo1.png" width="150" height="150" alt="Hackclub Flag... yay!">          

<img src="/Assets/photo4.png" width="100" height="100" alt="Hackclub Phantom Logo... ooooohhh scary">          

<img src="/Assets/photo2.png" width="100" height="100" alt="Hackclub Terra Fox, old...]">

</p>
