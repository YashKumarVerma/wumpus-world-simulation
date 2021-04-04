
from util.logger import whumpusLogger,worldLogger, agentLogger
from util.interface import getInt
from util.block import Block

class WumpusWorld:
    # dimension of the world
    n = 0
    maze = []
    
    def playGame(self):
        self.n = getInt("Enter the dimension of the world (single number) : ")
        self.maze = []
        
        
        """
        maze = new Block[n][n];
        for(int i=0; i<n; i++) {
            maze[i] = new Block[n];
            for(int j=0; j<n; j++)
                maze[i][j] = new Block();
        }
        """
        # initialize the blocks of the world
        # for i in range(0, self.n):
        #     for j in range(0, self.n):
                
        
        for i in range(0, self.n):
            self.maze.append([])
            for j in range(0, self.n):
                self.maze[i].append(Block())
        
        """
        System.out.print("\nEnter the number of pits: ");
        int pits = sc.nextInt();
        
        for(int i=0; i<pits; i++) {
            System.out.print("Enter the location of pit " + (i+1) + ": ");
            addPit(n-sc.nextInt(), sc.nextInt()-1);
        }
        """
        pits = getInt("Enter the number of pits : ")
        for i in range(0, pits):
            
            x = getInt("Enter location of pit, x coordinate : ")
            y = getInt("Enter location of pit, y coordinate : ")
            
            self.addPit(self.n - x, y-1)
            
        """
        System.out.print("\nEnter the location of wumpus: ");
        addWumpus(n-sc.nextInt(), sc.nextInt()-1);
        """
        wumpusLocationX = getInt("Enter location of wumpus, x coordinate : ")
        wumpusLocationY = getInt("Enter location of wumpus, y coordinate : ")
        
        self.addWumpus(self.n - wumpusLocationX, wumpusLocationY-1)
        
        """
        System.out.print("\nEnter the location of gold: ");
        addGold(n-sc.nextInt(), sc.nextInt()-1);
        """
        goldLocationX = getInt("Enter location of gold, x coordinate :")
        goldLocationY = getInt("Enter location of gold, y coordinate :")
        
        self.addGold(self.n - goldLocationX, goldLocationY-1)
        
        
        """
        System.out.print("\nEnter the starting location: ");
        int r = n - sc.nextInt();
        int c = sc.nextInt() - 1;
        int rPrev = -1, cPrev = -1;
        """
        startLocationX = getInt("Enter location of start, x coordinate :")
        startLocationY = getInt("Enter location of start, y coordinate :")
            
        r = self.n - startLocationX
        c = startLocationY - 1
        rPrev = -1
        cPrev = -1
        
        """
        int moves = 0;
        System.out.println("\nInitial state:");
        printMaze(r, c);
        """
        moves = 0
        worldLogger.info("Initial State : ")
        self.printMaze(r, c)
        
        # search for gold
        while self.maze[r][c].hasGold == False :
            """
            maze[r][c].isVisited = true;
            maze[r][c].pitStatus = Block.NOT_PRESENT;
            maze[r][c].wumpusStatus = Block.NOT_PRESENT;
            """
            self.maze[r][c].isVisited = True
            self.maze[r][c].pitStatus = Block.NOT_PRESENT
            self.maze[r][c].wumpusStatus = Block.NOT_PRESENT
            
            """
            if(!maze[r][c].hasBreeze) {
                if(r >= 1 && maze[r-1][c].pitStatus == Block.UNSURE)
                    maze[r-1][c].pitStatus = Block.NOT_PRESENT;
                if(r <= (n-2) && maze[r+1][c].pitStatus == Block.UNSURE)
                    maze[r+1][c].pitStatus = Block.NOT_PRESENT;
                if(c >= 1 && maze[r][c-1].pitStatus == Block.UNSURE)
                    maze[r][c-1].pitStatus = Block.NOT_PRESENT;
                if(c <= (n-2) && maze[r][c+1].pitStatus == Block.UNSURE)
                    maze[r][c+1].pitStatus = Block.NOT_PRESENT;
            }
            """
            if self.maze[r][c].hasBreeze == False :
                if r >= 1 and self.maze[r-1][c].pitStatus == Block.UNSURE : 
                    self.maze[r-1][c].pitStatus = Block.NOT_PRESENT
                    
                if r <= (self.n-2) and self.maze[r+1][c].pitStatus == Block.UNSURE : 
                    self.maze[r+1][c].pitStatus = Block.NOT_PRESENT
                    
                if c >= 1 and self.maze[r][c-1].pitStatus == Block.UNSURE : 
                    self.maze[r][c-1].pitStatus = Block.NOT_PRESENT
                    
                if c <= (self.n-2) and self.maze[r][c+1].pitStatus == Block.UNSURE : 
                    self.maze[r][c+1].pitStatus = Block.NOT_PRESENT

            """"
             if(!maze[r][c].hasStench) {
                if(r >= 1 && maze[r-1][c].wumpusStatus == Block.UNSURE)
                    maze[r-1][c].wumpusStatus = Block.NOT_PRESENT;
                if(r <= (n-2) && maze[r+1][c].wumpusStatus == Block.UNSURE)
                    maze[r+1][c].wumpusStatus = Block.NOT_PRESENT;
                if(c >= 1 && maze[r][c-1].wumpusStatus == Block.UNSURE)
                    maze[r][c-1].wumpusStatus = Block.NOT_PRESENT;
                if(c <= (n-2) && maze[r][c+1].wumpusStatus == Block.UNSURE)
                    maze[r][c+1].wumpusStatus = Block.NOT_PRESENT;
            }
            """
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
            
            """
            if(r >= 1 && !((r-1) == rPrev && c == cPrev) && maze[r-1][c].isVisited == false && maze[r-1][c].pitStatus == Block.NOT_PRESENT && maze[r-1][c].wumpusStatus == Block.NOT_PRESENT) {
                rPrev = r;
                cPrev = c;
                
                r--;
                foundNewPath = true;
            }
            """
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
                
            """
            if(!foundNewPath) {
                int temp1 = rPrev;
                int temp2 = cPrev;

                rPrev = r;
                cPrev = c;

                r = temp1;
                c = temp2;
            }
            
            moves++;
            """
            if not foundNewPath:
                temp1 = rPrev
                temp2 = cPrev
                
                rPrev = r
                cPrev = c
                
                r = temp1
                c = temp2
            
            moves+=1
            
            """
            System.out.println("\n\nMove " + moves + ":");
            printMaze(r, c);

            if(moves > n*n) {
                System.out.println("\nNo solution found!");
                break;
            }
            """
            worldLogger.info(f"\n\n Move # {moves}")
            self.printMaze(r,c)
            
            if moves > self.n*self.n :
                agentLogger.info("No Solution Found")
                break
        
        """
        if(moves <= n*n)
            System.out.println("\nFound gold in " + moves + " moves.");
        """
        if moves <= self.n * self.n:
            agentLogger.info(f"Found gold in {moves} moves")
            
    
    
    def addPit(self, row, col):
        worldLogger.info(f"New Pit added to the world")
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
        whumpusLogger.info(f"A WumPus is added to the world")
        self.maze[row][col].hasWumpus = True
        
        if row >= 1 :
            self.maze[row-1][col].hasStench = True
    
        if row <= (self.n - 2):
            self.maze[row+1][col].hasStench = True
            
        if col >= 1:
            self.maze[row][col-1].hasStench = True
            
        if col <= (self.n-2):
            self.maze[row][col+1].hasStench = True
     
    def addGold(self, row, col):
        worldLogger.info(f"A Gold Chest Added to the world")
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


game = WumpusWorld()
game.playGame()