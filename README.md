# Snek_Ai
Implementing a simple Ai using Q learning to play snake

Snake1 is an early version with simpler states, and uses a reward of -10 for death and +1 for apples, and 0 for movement. 
Ran into trouble surviving at longer snake lengths as it kept colliding into itself, likely due to the limited information its current states fed it.
Also has the habit of looping to avoid death due to dying having a heavy punishment.
After several days of training, it reached a meager high score of 27.

Snake2 came after many rounds of trial and error, trying to improve upon Snake1.
To fix the looping issue, I added a reward of -0.01 to each move it made that did not result in death or an apple, thus incentivizing it against looping endlessly to stay alive without actively chasing apples.

In an attempt to keep it alive longer at longer lengths, I tried many things to add more to its states. 
These include adding the relative distance of its head to its mid section and tails to give it an idea of its shape and also expanding the area around the ahead it could see was safe/unsafe.
This ended in failure, as the Q space became too large and its performance was worse than Snake1 even after several days of around the clock training.

Then, I tried the opposite of simplifying its Q table instead. Rather than the X/Y distance of the head to the apple ( which went from -9 to 9 ), I simplified it into a binary 1 or 0.
Was the apple to the left of the head? Was the apple to the right of the head? Was the apple above the head? Was the apple below the head?
I also removed the relative distances of the head to the mid sections and tails to reduce the Q space even further, and the result was a lot better than I expected.

While Snake1 reached a highscore of 27 after several days of training, Snake2 managed to reach 40 in a single afternoon, which is where I decided to stop training this version for now.


