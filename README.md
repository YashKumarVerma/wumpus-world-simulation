# WumPus World 
- Yash Kumar Verma / 19BCE2669

This report documents the simulation of the classical Wumpus world problem. The constraints of the problem have been adapted from the document shared previously via VToP.


## Implementation
The implementation of the simulator has been done in Python (v3.7.5) and the entire project code has been upload on [this github repository](https://github.com/YashKumarVerma/wumpus-world-simulation), so that it is easier to reproduce and test locally. The code is attached at the end of this document.

## Project Structure
For simplicity, and to demonstrate the implementation of the agent clearly, the codebase has been written following the OOP principles and utility implementations like loggers, i/o classes have been kept in a separate directory.


![https://i.imgur.com/5bjB1qj.png](https://i.imgur.com/5bjB1qj.png)

- **world.py** -> contains main simulation and agent logic
- **util/block.py** -> contains implementation of a block in the wold
- **util/interface.py** -> provides function to take input from user and typecast it
- **util/logger.py** -> logger function to display output with context and color

and then all components are being included into the main world.py

![https://i.imgur.com/vGIuXhT.png](https://i.imgur.com/vGIuXhT.png)

## Running
- Step 1 : Clone the project to your local machine
  - `git clone https://github.com/YashKumarVerma/wumpus-world-simulation`
- Step 2 : Open and install the dependencies. (optional: do this in [virtualenv](https://pypi.org/project/virtualenv/))
  - `cd wumpus-world-simulation`
  - `pip3 install -r requirements.txt`
- Step 3 : Run the world.py file 

## Output
**Note**
1. The inputs are automated as described in the problem statement
2. The input coordinates are shifted as per the array indices automatically.
3. This means that the index of the boxes are (1,1) at the bottom left, therefore all the input coordinates are to be given as per this image.
![https://i.imgur.com/QDUdVcj.png](https://i.imgur.com/QDUdVcj.png)
4. For Utility and debugging purpose, the program would show the outputs in array-format (starting index 0 at top left)

### RunTime

Pits added automatically and runs automatically after adding the wumpus.

![https://i.imgur.com/9K1c4Vn.png](https://i.imgur.com/9K1c4Vn.png)
![https://i.imgur.com/i6ybkfp.png](https://i.imgur.com/i6ybkfp.png)
![https://i.imgur.com/kIu5gxX.png](https://i.imgur.com/kIu5gxX.png)

Since the game is dynamic, we get different output each time. The agent can also use the arrow at the cost of 10 points.
![https://i.imgur.com/gJmVLbs.png](https://i.imgur.com/gJmVLbs.png)
![https://i.imgur.com/GTqOe0B.png](https://i.imgur.com/GTqOe0B.png)
![https://i.imgur.com/k5oPi5A.png](https://i.imgur.com/k5oPi5A.png)

Shooting an arrow
![https://i.imgur.com/7ZYCqWL.png](https://i.imgur.com/7ZYCqWL.png)

Also shows last visited path if solution is not found
![https://i.imgur.com/umBa8FE.png](https://i.imgur.com/umBa8FE.png)


## Code
```py
# python libraries
from random import randint

# custom written libraries
from util.logger import whumpusLogger,worldLogger, agentLogger
from util.interface import getInt
from util.block import Block

class WumpusWorld:
    # dimension of the world
    n = 0
    maze = []
    occupiedBlocks = [[1,1]]
    path = []
    points = 0
    wumpusLocation = []
    arrowCount = 1
    solutionFound = False
    
    def playGame(self):
        self.n = getInt("Enter the dimension of the world (single number) : ")
        self.maze = []    
        
        for i in range(0, self.n):
            self.maze.append([])
            for j in range(0, self.n):
                self.maze[i].append(Block())
        
    
        # generating pits
        pits = randint(1,3)
        worldLogger.info(f"Generating {pits} pits randomly")
        for i in range(0, pits):
            pitTryCounter = 0
            x = 0
            y = 0
            
            # try 10 times before quitting
            while pitTryCounter < 10:
                x = randint(1, self.n)
                y = randint(1, self.n)
                
                if(self.isBlockFree(x,y)):
                    break
                
                if(pitTryCounter == 100):
                    worldLogger.info("Could not resolve pit location conflict after 100 tries")
                pitTryCounter+=1
            
            self.addPit(self.n - x, y-1)
            self.occupyBlock(x,y)
            
        wumpusLocationX = getInt("Enter location of wumpus, x coordinate : ")
        wumpusLocationY = getInt("Enter location of wumpus, y coordinate : ")
        self.addWumpus(self.n - wumpusLocationX, wumpusLocationY-1)
        self.occupyBlock(wumpusLocationX, wumpusLocationY)
        
       
        goldTryCounter = 0
        goldLocationX = 0
        goldLocationY = 0
            
        while(goldTryCounter < 10):
            goldLocationX = randint(1, self.n)
            goldLocationY = randint(1, self.n)
            if(self.isBlockFree(x,y)):
                break
            goldTryCounter += 1
            
            if goldTryCounter == 100:
                worldLogger.info("Could not resolve gold conflict after 100 tries")
                return False

        self.addGold(self.n - goldLocationX, goldLocationY-1)
        self.occupyBlock(goldLocationX, goldLocationY)
        
        
        #   always start from 1,1
        # startLocationX = getInt("Enter location of start, x coordinate :")
        # startLocationY = getInt("Enter location of start, y coordinate :")
        startLocationX = 1
        startLocationY = 1
            
        r = self.n - startLocationX
        c = startLocationY - 1
        rPrev = -1
        cPrev = -1
        
      
        moves = 0
        worldLogger.info("Initial State : ")
        self.printMaze(r, c)
        
        # search for gold
        while self.maze[r][c].hasGold == False :
          
            self.maze[r][c].isVisited = True
            self.maze[r][c].pitStatus = Block.NOT_PRESENT
            self.maze[r][c].wumpusStatus = Block.NOT_PRESENT
            
           
            if self.maze[r][c].hasBreeze == False :
                if r >= 1 and self.maze[r-1][c].pitStatus == Block.UNSURE : 
                    self.maze[r-1][c].pitStatus = Block.NOT_PRESENT
                    
                if r <= (self.n-2) and self.maze[r+1][c].pitStatus == Block.UNSURE : 
                    self.maze[r+1][c].pitStatus = Block.NOT_PRESENT
                    
                if c >= 1 and self.maze[r][c-1].pitStatus == Block.UNSURE : 
                    self.maze[r][c-1].pitStatus = Block.NOT_PRESENT
                    
                if c <= (self.n-2) and self.maze[r][c+1].pitStatus == Block.UNSURE : 
                    self.maze[r][c+1].pitStatus = Block.NOT_PRESENT

           
            if self.maze[r][c].hasStench == False :
                if r >= 1 and self.maze[r-1][c].wumpusStatus == Block.UNSURE :
                    self.maze[r-1][c].wumpusStatus = Block.NOT_PRESENT
                    
                if r <= (self.n-2) and self.maze[r+1][c].wumpusStatus == Block.UNSURE :
                    self.maze[r+1][c].wumpusStatus = Block.NOT_PRESENT
                    
                if c >= 1 and self.maze[r][c-1].wumpusStatus == Block.UNSURE :
                    self.maze[r][c-1].wumpusStatus = Block.NOT_PRESENT
                    
                if c <= (self.n-2) and self.maze[r][c+1].wumpusStatus == Block.UNSURE :
                    self.maze[r][c+1].wumpusStatus = Block.NOT_PRESENT
    
    
            #  boolean foundNewPath = false
            foundNewPath = False
            
            if r >= 1 and not ((r-1) == rPrev and c == cPrev) and self.maze[r-1][c].isVisited == False and self.maze[r-1][c].pitStatus == Block.NOT_PRESENT and self.maze[r-1][c].wumpusStatus == Block.NOT_PRESENT:
                rPrev = r
                cPrev = c
                r-=1
                foundNewPath = True
            
            elif r <= (self.n-2) and not ((r+1) == rPrev and c == cPrev) and self.maze[r+1][c].isVisited == False and self.maze[r+1][c].pitStatus == Block.NOT_PRESENT and self.maze[r+1][c].wumpusStatus == Block.NOT_PRESENT :
                rPrev = r
                cPrev = c
                r+= 1
                foundNewPath = True
            
            elif c >= 1 and not (r == rPrev and (c-1) == cPrev) and self.maze[r][c-1].isVisited == False and self.maze[r][c-1].pitStatus == Block.NOT_PRESENT and self.maze[r][c-1].wumpusStatus == Block.NOT_PRESENT :
                rPrev = r
                cPrev = c
                c-=1
                foundNewPath = True
            
            elif c <= (self.n-2) and not (r == rPrev and (c+1) == cPrev) and self.maze[r][c+1].isVisited == False and self.maze[r][c+1].pitStatus == Block.NOT_PRESENT and self.maze[r][c+1].wumpusStatus == Block.NOT_PRESENT :
                rPrev = r
                cPrev = c
                c+= 1
                foundNewPath = True
                
          
            if not foundNewPath:
                temp1 = rPrev
                temp2 = cPrev
                
                rPrev = r
                cPrev = c
                
                r = temp1
                c = temp2
            
            
            # one point for each step
            moves+=1
            self.points -= 1
            worldLogger.info(f"Move # {moves}")
            print("\n\n\n")
            self.path.append([r,c])
            
            # if passing by wumpus, means using arrow
            if([r,c] == self.wumpusLocation):
                # if arrow available, then kill and reduce points
                if self.arrowCount == 1:
                    self.arrowCount = 0
                    self.points -= 10
                    worldLogger.info("Shooting an arrow to wumpus")
                    whumpusLogger.info("KILLED")
                else:
                    # else die
                    self.points -= 1000
                    break
                
            self.printMaze(r,c)
            
            # deduct 1000 points for death
            if moves > self.n*self.n :
                self.points -= 1000
                break
        
        # 1000 points for finding gold
        if moves <= self.n * self.n:
            print("\n\n\n\n")
            agentLogger.info(f"Found gold in {moves} moves")
            self.solutionFound = True
            self.points += 1000
            
    def isBlockFree(self,x,y):
        givenBlock = [x,y]
        return givenBlock not in self.occupiedBlocks

    def occupyBlock(self, x, y):
        givenBlock = [x,y]
        self.occupiedBlocks.append(givenBlock)

    def addPit(self, row, col):
        worldLogger.info(f"New Pit added to the world at {row},{col}")
        self.maze[row][col].hasPit = True
        
        if row >= 1:
            self.maze[row-1][col].hasBreeze = True
        if row <= (self.n-2):
            self.maze[row+1][col].hasBreeze = True
        if col >= 1:
            self.maze[row][col-1].hasBreeze = True
        if col <= (self.n-2):
            self.maze[row][col+1].hasBreeze = True
    
    def addWumpus(self, row, col):
        whumpusLogger.info(f"A WumPus is added to the world at {row},{col}")
        self.maze[row][col].hasWumpus = True
        self.wumpusLocation = [row, col]
        
        if row >= 1 :
            self.maze[row-1][col].hasStench = True
    
        if row <= (self.n - 2):
            self.maze[row+1][col].hasStench = True
            
        if col >= 1:
            self.maze[row][col-1].hasStench = True
            
        if col <= (self.n-2):
            self.maze[row][col+1].hasStench = True
     
    def addGold(self, row, col):
        worldLogger.info(f"A Gold Chest Added to the world at {row},{col}")
        self.maze[row][col].hasGold = True
    
    def printMaze(self,r, c):
        print("\n")
        worldLogger.info(f"Visualizing World")        
        for i in range(0, self.n):
            for j in range(0, self.n):
                charToPrint = "〰"
                if r == i and c == j:
                    charToPrint = "👨"
                elif self.maze[i][j].hasPit:
                    charToPrint = "🕳"
                elif self.maze[i][j].hasWumpus:
                    charToPrint = "🐸"
                elif self.maze[i][j].hasGold:
                    charToPrint = "🏆"
                
                print(charToPrint, end="\t")
            print()


agentLogger.info("Welcome to WumPus World !")
agentLogger.info("simulator written by Yash Kumar Verma")


game = WumpusWorld()
game.playGame()

agentLogger.info(f"Final Points : {game.points} ")
if game.solutionFound : 
    agentLogger.info(f"Solution was found in {len(game.path)} turns.")
    for path in game.path:
        agentLogger.info(f"( {path[0]}, {path[1]} ) ")
else:
    agentLogger.info(f"Solution was not found.")
    agentLogger.info(f"Last visited coordinate : {game.path[len(game.path)-1]}")

```