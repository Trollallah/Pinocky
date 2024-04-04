# Pinocky
Capstone project for NCLab python course.

![Static Badge](https://img.shields.io/badge/-pygame--ce_2.4.0-blue)
![Static Badge](https://img.shields.io/badge/-Python_3.11.3-brightgreen)

I wanted to build a game for my capstone project. I looked to simplistic games with a lot of room for scaling. That
lead me to the game Vampire Survivors by Poncle. This game is a 2D roguelike with auto attacks and fairly simple enemies
that wouldn't require a ton of AI logic. The player can collect experience points that allow the player to unlock
upgrades for their player and attack stats.

I built a proof of concept to emulate Vampire survivors using Pygame-ce. Pinocky is in a playable state, but currently
only has the fundamentals necessary for a game loop. The player can attack and kill enemies who drop xp upon death, 
absorb the xp drops which count towards leveling up which results in the player picking up one of two upgrades. There
are currently only two enemies, and two types of drops, but the enemies, pickups, attacks, and upgrades were all written
in a way that makes them scalable. All of these systems use Enums to easily distinguish them in code and allow for more
of anyone of them to be added.