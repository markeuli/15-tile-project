# 15 Tile Project
## By: Mark Ulicnik

# Installation

After installing the directory, navigate to the root directory and run:
```
$pip install -r requirements.txt
```
This will install the requirements to run the project.

Then run:
```
$python main.py
```
for the game.

Or:
```
$python test.py
```
to run the tests. 

# Future Plans
- Clean up pygame UI
UI not exactly clean or as informative as I would like, CLI required for understanding metrics
- Reconsider TreeSearch <-> State class structure
Something cool here. Being able to define the required functions used by TreeSearch for any game that utilized this State class is interesting.
Perhaps need to research more OO Principles and existing python libraries to find a better way to do this
- Implement Pattern Database Heuristics
Much more powerful heuristics exist for this puzzle, A* and IDA* searches benefit greatly from improved heuristics.
- Expand TreeSearch to be a homebrewed python library where I can experiment with other heuristics for different game types
I recently have been interested in Swarm Intelligence and specifically Ant Colony Optimization. This structure could be
adapted and expanded to help me experiment and implement different heuristics and metaheuristics for other games or types
of search spaces. 
