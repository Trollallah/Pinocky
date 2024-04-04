# Pinocky
Capstone project for NCLab python course.

![Static Badge](https://img.shields.io/badge/-pygame--ce_2.4.0-blue)
![Static Badge](https://img.shields.io/badge/-Python_3.11.3-brightgreen)

## Description:
I wanted to build a game for my capstone project. I looked to simplistic games with a lot of room for scaling, so that 
I could create a prototype that could also function as a jumping off point for further development. That lead me to 
the game Vampire Survivors by Poncle. This game is a 2D roguelike with auto attacks and fairly simple enemies that
wouldn't require a ton of AI logic. The player can collect experience points that allow the player to unlock upgrades
for their player and attack stats.

I built a proof of concept to emulate Vampire survivors using Pygame-ce. Pinocky is in a playable state, but currently
only has the fundamentals necessary for a game loop. The player can attack and kill enemies who drop xp upon death, 
absorb the xp drops which count towards leveling up which results in the player picking up one of two upgrades. The end
condition is when the player dies. After death, the player is presented with a score, their time lived, and options to
be directed to the main menu or to exit the application.

There are currently only two enemies, and two types of drops, but the enemies, pickups, attacks, and upgrades were all 
written in a way that makes them scalable. All of these systems use Enums to easily distinguish them in code and allow 
for more of any one of them to be added.

### To run the game:
1. Install [Python 3.11](https://www.python.org/downloads/)
2. Install pygame-ce from command prompt/powershell
   >pip install pygame-ce or pip3 install pygame-ce for most people
3. Clone the repo to a folder/directory
4. Open either command prompt/powershell
5. Switch to the folder/directory containing main.py from this project
   >cd *folder/directory path*
6. Run main.py from the folder/directory containing it
   >python main.py
