# Snek_Ai
Implementing a simple Ai using Q learning to play snake

Snake1 is an early version with simpler states, and uses a reward of -10 for death and +1 for apples, and 0 for movement. 
Ran into trouble surviving at longer snake lengths as it kept colliding into itself, likely due to the limited information its current states fed it.
Also has the habit of looping to avoid death due to dying having a heavy punishment.
