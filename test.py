import unittest
import random, time

class TestGui(unittest.TestCase):
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300 
    SNAKE_ICON_WIDTH = 15
    
    def __init__(self, queue):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = queue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15     #speed of snake updates (sec)
        while self.gameNotOver:
            #complete the method implementation below
            #pass #remove this line from your implemenation
            self.move()
            self.queue.put(('score', self.score))
            self.queue.put(('game_over', not self.gameNotOver))
            time.sleep(SPEED)

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        #complete the method implementation below
        if self.isPreyCaptured(NewSnakeCoordinates):
            self.score += 1
            self.createNewPrey()
        if self.isGameOver(NewSnakeCoordinates):
            self.gameNotOver = False
        else:
            self.snakeCoordinates.pop()
            self.snakeCoordinates.insert(0, NewSnakeCoordinates)



    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        #complete the method implementation below
        directionX, directionY = self.direction
        newX = lastX + directionX * SNAKE_ICON_WIDTH
        newY = lastY + directionY * SNAKE_ICON_WIDTH
        return (newX, newY)


    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        x, y = snakeCoordinates
        #complete the method implementation below
        if x < self.GRID_SIZE or x > self.WIDTH - 2 * self.GRID_SIZE or y < self.GRID_SIZE or y > self.HEIGHT - 2 * self.GRID_SIZE or snakeCoordinates[:-1].count(snakeCoordinates[-1]) > 0:
            self.gameNotOver = False
            self.queue.put("game_over")

    def createNewPrey(self) -> None:
        """ 
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). 
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
        THRESHOLD = 15   #sets how close prey can be to borders
        # Choose a random x and y coordinate for the prey. The coordinates should be THRESHOLD away from the wall.
        x = random.randint(THRESHOLD, WINDOW_WIDTH - THRESHOLD)
        y = random.randint(THRESHOLD,  WINDOW_HEIGHT- THRESHOLD)

        # Calculate the coordinates of the prey rectangle
        rectangleCoordinates = (x - 5, y - 5, x + 5, y + 5)

        # Add a "prey" task to the queue with the prey rectangle coordinates
        self.queue.put({"prey": rectangleCoordinates})
    
if __name__ == '__main__':
    unittest.main()
