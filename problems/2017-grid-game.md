# 2017. Grid Game

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/grid-game/>  
- **NeetCode:** <https://neetcode.io/problems/grid-game>  
- **Video:** <https://www.youtube.com/watch?v=N4wDSOw65hI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Robot 1 must go right along row `0`, drop down to row `1` at some column, then continue right. After Robot 1 collects its points (setting those cells to `0`), Robot 2 follows optimally. Robot 1 wants to minimize Robot 2's maximum possible score. We try every possible column where Robot 1 drops down and simulate Robot 2's best response.

```cpp
class Solution {
public:
    long long gridGame(vector<vector<int>>& grid) {
        int cols = grid[0].size();
        long long res = LLONG_MAX;

        long long top1 = 0;
        for (int i = 0; i < cols; i++) {
            top1 += grid[0][i];
            long long bottom1 = 0;
            for (int j = i; j < cols; j++) {
                bottom1 += grid[1][j];
            }

            long long top2 = 0, robot2 = 0;
            for (int j = 0; j < cols; j++) {
                if (j > i) {
                    top2 += grid[0][j];
                }

                long long bottom2 = 0;
                for (int k = j; k < i; k++) {
                    bottom2 += grid[1][k];
                }
                robot2 = max(robot2, top2 + bottom2);
            }

            res = min(res, robot2);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(1)$

## 2. Prefix Sum

After Robot 1 drops at column `i`, Robot 2 can only collect from two disjoint regions: the top row after column `i`, or the bottom row before column `i`. Robot 2 will choose whichever region has more points. Using prefix sums, we can compute these region totals in O(1) per column.

```cpp
class Solution {
public:
    long long gridGame(vector<vector<int>>& grid) {
        int N = grid[0].size();
        vector<long long> preRow1, preRow2;
        for (int i = 0; i < N; i++) {
            preRow1.push_back((long)grid[0][i]);
            preRow2.push_back((long)grid[1][i]);
        }

        for (int i = 1; i < N; i++) {
            preRow1[i] += preRow1[i - 1];
            preRow2[i] += preRow2[i - 1];
        }

        long long res = LLONG_MAX;
        for (int i = 0; i < N; i++) {
            long long top = preRow1[N - 1] - preRow1[i];
            long long bottom = i > 0 ? preRow2[i - 1] : 0;
            long long secondRobot = max(top, bottom);
            res = min(res, secondRobot);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Prefix Sum (Space Optimized)

We can avoid storing prefix arrays by maintaining running sums. Start with `topSum` as the total of the top row and `bottomSum` as `0`. As we iterate, subtract from `topSum` (simulating Robot 1 taking cells from the top) and add to `bottomSum` (accumulating what Robot 2 could take from below).

```cpp
class Solution {
public:
    long long gridGame(vector<vector<int>>& grid) {
        long long res = LLONG_MAX;
        long long topSum = accumulate(grid[0].begin(), grid[0].end(), 0LL);
        long long bottomSum = 0;

        for (int i = 0; i < grid[0].size(); i++) {
            topSum -= grid[0][i];
            res = min(res, max(topSum, bottomSum));
            bottomSum += grid[1][i];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/2017-grid-game.cpp` in the NeetCode repo)

```cpp
/* 
Approch:
    2nd robot can collect either all the bottom points
    before the break point (when 1st robot goes to bottom)
    or collect all the top points after that break point.
Time Complexity: O(N)
Space Complexity: O(1)
*/

class Solution {
public:
    long long gridGame(vector<vector<int>>& grid) {
  
        // prefix sum
        long long top = grid[0][0],bottom = 0, answer = LONG_MAX;
        for(int i =1;i<grid[0].size();i++){
            top += grid[0][i];
        }

        for(int i =0;i<grid[0].size();i++){
            // All the top points 2nd robot can collect
            top -= grid[0][i];

            // min because first robot wants to  minimize 
            answer = min(answer,max(top,bottom));

            // All the bootom points the robot could collect
            bottom += grid[1][i];
        }

        return answer;
    }
};
```
