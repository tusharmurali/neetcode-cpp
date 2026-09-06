# 353. Design Snake Game

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-snake-game/>  
- **NeetCode:** <https://neetcode.io/problems/design-snake-game>  

[← Back to index](../INDEX.md)

## 1. Queue and Hash Set

The snake game requires tracking the snake's body as it moves and grows. A deque (double-ended queue) is perfect because we add to the front (new head position) and remove from the back (tail moves forward). To quickly check whether the snake bites itself, we also maintain a hash set of all occupied cells. When the snake eats food, the tail stays in place so the snake grows. The score equals the number of food items eaten, which is the snake length minus `1`.

```cpp
class SnakeGame {
    unordered_set<string> snakeSet;
    deque<pair<int, int>> snake;
    vector<vector<int>> food;
    int foodIndex;
    int width;
    int height;

    string pairToString(int row, int col) {
        return to_string(row) + "," + to_string(col);
    }

public:
    SnakeGame(int width, int height, vector<vector<int>>& food) {
        this->width = width;
        this->height = height;
        this->food = food;
        this->foodIndex = 0;
        this->snakeSet.insert(pairToString(0, 0)); // initially at [0][0]
        this->snake.push_back({0, 0});
    }

    int move(string direction) {
        pair<int, int> snakeCell = this->snake.front();
        int newHeadRow = snakeCell.first;
        int newHeadColumn = snakeCell.second;

        if (direction == "U") {
            newHeadRow--;
        } else if (direction == "D") {
            newHeadRow++;
        } else if (direction == "L") {
            newHeadColumn--;
        } else if (direction == "R") {
            newHeadColumn++;
        }

        pair<int, int> newHead = {newHeadRow, newHeadColumn};
        pair<int, int> currentTail = this->snake.back();

        // Boundary conditions.
        bool crossesBoundary1 = newHeadRow < 0 || newHeadRow >= this->height;
        bool crossesBoundary2 = newHeadColumn < 0 || newHeadColumn >= this->width;

        // Checking if the snake bites itself.
        bool bitesItself = this->snakeSet.count(pairToString(newHeadRow, newHeadColumn)) &&
                          !(newHead.first == currentTail.first && newHead.second == currentTail.second);

        // If any of the terminal conditions are satisfied, then we exit with rcode -1.
        if (crossesBoundary1 || crossesBoundary2 || bitesItself) {
            return -1;
        }

        // If there's an available food item and it is on the cell occupied by the snake after the move,
        // eat it.
        if ((this->foodIndex < this->food.size())
            && (this->food[this->foodIndex][0] == newHeadRow)
            && (this->food[this->foodIndex][1] == newHeadColumn)) {
            this->foodIndex++;
        } else {
            this->snake.pop_back();
            this->snakeSet.erase(pairToString(currentTail.first, currentTail.second));
        }

        // A new head always gets added
        this->snake.push_front(newHead);

        // Also add the head to the set
        this->snakeSet.insert(pairToString(newHeadRow, newHeadColumn));

        return this->snake.size() - 1;
    }
};
```

**Complexity**

- Time Complexity:
    - The time complexity of the `move` function is $O(1)$.
    - The time taken to calculate `bites_itself` is constant since we are using a dictionary to search for the element.
    - The time taken to add and remove an element from the queue is also constant.

- Space Complexity: $O(W \times H + N)$
    - $O(N)$ is used by the `food` data structure.
    - $O(W \times H)$ is used by the `snake` and the `snake_set` data structures. At most, we can have snake that occupies all the cells of the grid.

> Where $W$ represents the width of the grid, $H$ represents the height of the grid, and $N$ represents the number of food items in the list.
