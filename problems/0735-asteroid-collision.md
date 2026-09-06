# 735. Asteroid Collision

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/asteroid-collision/>  
- **NeetCode:** <https://neetcode.io/problems/asteroid-collision>  
- **Video:** <https://www.youtube.com/watch?v=LN7KjRszjk4>  
- **Video approach:** 1. Stack  

[← Back to index](../INDEX.md)

## 1. Stack ▶ video

Collisions only happen when a right-moving asteroid (positive) meets a left-moving one (negative). A stack naturally models this: we process asteroids left to right, and when we see a negative asteroid, it can only collide with positive asteroids already on the stack. We keep popping and comparing until either the new asteroid is destroyed, destroys all opposing asteroids, or there are no more collisions possible.

```cpp
class Solution {
public:
    vector<int> asteroidCollision(vector<int>& asteroids) {
        vector<int> stack;
        for (int& a : asteroids) {
            while (!stack.empty() && a < 0 && stack.back() > 0) {
                int diff = a + stack.back();
                if (diff < 0) {
                    stack.pop_back();
                } else if (diff > 0) {
                    a = 0;
                } else {
                    a = 0;
                    stack.pop_back();
                }
            }
            if (a != 0) {
                stack.push_back(a);
            }
        }
        return stack;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Without Stack

We can simulate the stack behavior using the input array itself. We maintain a pointer `j` that tracks the "top" of our virtual stack within the array. When collisions occur, we decrement `j` (like popping). Surviving asteroids are written to position `j + 1`. This gives us O(1) extra space while maintaining the same logic.

```cpp
class Solution {
public:
    vector<int> asteroidCollision(vector<int>& asteroids) {
        int n = asteroids.size();
        int j = -1;

        for (int& a : asteroids) {
            while (j >= 0 && asteroids[j] > 0 && a < 0) {
                if (asteroids[j] > abs(a)) {
                    a = 0;
                    break;
                } else if (asteroids[j] == abs(a)) {
                    j--;
                    a = 0;
                    break;
                } else {
                    j--;
                }
            }
            if (a != 0) {
                asteroids[++j] = a;
            }
        }

        asteroids.resize(j + 1);
        return asteroids;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output array.

## Standalone solution file (`cpp/0735-asteroid-collision.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    vector<int> asteroidCollision(vector<int>& asteroids) {
        vector<int> stk;

        for (auto ast: asteroids)
        {
            while (!stk.empty() && stk.back() > 0 && ast < 0)
            {
                int diff = ast + stk.back();
                if (diff > 0)
                {
                    ast = 0;
                }
                else if (diff < 0)
                {
                    stk.pop_back();
                }
                else
                {
                    ast = 0;
                    stk.pop_back();
                } 
            }
            if (ast != 0)
                stk.push_back(ast);
        }
        return stk;
    }
};
```
