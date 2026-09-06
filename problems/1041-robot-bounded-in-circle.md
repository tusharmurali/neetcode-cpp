# 1041. Robot Bounded In Circle

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/robot-bounded-in-circle/>  
- **NeetCode:** <https://neetcode.io/problems/robot-bounded-in-circle>  
- **Video:** <https://www.youtube.com/watch?v=nKv2LnC_g6E>  

[← Back to index](../INDEX.md)

## 1. Simulation

A robot executing the same instructions repeatedly will be bounded in a circle if and only if one of two conditions holds after one cycle: either it returns to the origin, or it is not facing north. If the robot returns to the origin, it will clearly repeat that pattern forever. If it ends up facing a different direction, the displacement vector will rotate with each cycle. After at most 4 cycles (for 90 degree turns) or 2 cycles (for 180 degree turns), the displacements cancel out and the robot returns to the origin.

```cpp
class Solution {
public:
    bool isRobotBounded(string instructions) {
        int dirX = 0, dirY = 1;
        int x = 0, y = 0;

        for (char d : instructions) {
            if (d == 'G') {
                x += dirX;
                y += dirY;
            } else if (d == 'L') {
                int temp = dirX;
                dirX = -dirY;
                dirY = temp;
            } else {
                int temp = dirX;
                dirX = dirY;
                dirY = -temp;
            }
        }

        return (x == 0 && y == 0) || (dirX != 0 || dirY != 1);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
