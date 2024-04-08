# Pinocky
Capstone project for NCLab python course.

![Static Badge](https://img.shields.io/badge/-pygame--ce_2.4.0-blue)
![Static Badge](https://img.shields.io/badge/-Python_3.11.3-brightgreen)

![pinocky gameplay](assets/pinocky_vid.gif)

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

### Objective and directions for Pinocky:
As of now the objective is just to last as long as possible. You control the penguin character by either using WASD or
the arrow keys. You take damage if the enemies touch you, so it's your job to maneuver your penguin around all the 
enemies. The attack is on a timer and automatically fires, so all you have to do is avoid touching the enemies. 
The attack deals damage to the enemies and stuns them momentarily. Once you have dealt enough damage to the enemies they
die and drop a bowling shoe. The bowling shoes are actually experience, and collecting them will go towards filling a
bar at the bottom of the screen up. Once that fills up you get to pick an upgrade. Watch out though... Everytime you
fill the bar you get an upgrade, but the enemies will start spawning more frequently and the chances of spawning the 
strong pins increases. The pins will also occasionally get buffs that make them more dangerous.

### Attacks:
1. The straight ball. It might not be the most glamorous, but it's definitely useful.

### Enemies:
1. Weak pin - A little bowling pin that chases you around. Drops a red bowling shoe that's not worth much experience.
2. Strong pin - A much tougher and larger pin that chases you around. Drops a yellow bowling shoe that is worth a lot 
more experience than the red shoes.

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

