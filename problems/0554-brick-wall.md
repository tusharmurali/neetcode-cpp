# 554. Brick Wall

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/brick-wall/>  
- **NeetCode:** <https://neetcode.io/problems/brick-wall>  
- **Video:** <https://www.youtube.com/watch?v=Kkmv2h48ekw>  
- **Video approach:** 2. Hash Map (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The goal is to draw a vertical line through the wall that crosses the fewest bricks. A line crosses a brick only if it doesn't pass through a gap between bricks. So we need to find the vertical position where the most gaps align across all rows.

The brute force approach is straightforward: for every possible vertical position (from 1 to wall width minus 1), count how many rows do NOT have a gap at that position. The position with the fewest cuts is our answer.

```cpp
class Solution {
public:
    int leastBricks(vector<vector<int>>& wall) {
        int n = wall.size();
        int m = 0;
        for (int brick : wall[0]) {
            m += brick;
        }

        vector<vector<int>> gaps(n);
        for (int i = 0; i < n; i++) {
            int gap = 0;
            for (int brick : wall[i]) {
                gap += brick;
                gaps[i].push_back(gap);
            }
        }

        int res = n;
        for (int line = 1; line < m; line++) {
            int cuts = 0;
            for (int i = 0; i < n; i++) {
                if (find(gaps[i].begin(), gaps[i].end(), line) == gaps[i].end()) {
                    cuts++;
                }
            }
            res = min(res, cuts);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * g)$
- Space complexity: $O(n * g)$

> Where $m$ is the sum of widths of the bricks in the first row, $n$ is the number of rows and $g$ is the average number of gaps in each row.

## 2. Hash Map ▶ video

Instead of checking every possible vertical position, we can think about this differently. We want to maximize the number of gaps we pass through, because each gap means we avoid cutting a brick. If we count how many times each gap position appears across all rows, the position with the most gaps is the best place to draw our line. The answer is then total rows minus the maximum gap count.

```cpp
class Solution {
public:
    int leastBricks(vector<vector<int>>& wall) {
        unordered_map<int, int> countGap;
        countGap[0] = 0;

        for (const auto& row : wall) {
            int total = 0;
            for (size_t i = 0; i < row.size() - 1; ++i) {
                total += row[i];
                countGap[total]++;
            }
        }

        int maxGaps = 0;
        for (const auto& [key, value] : countGap) {
            maxGaps = max(maxGaps, value);
        }

        return wall.size() - maxGaps;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(g)$

> Where $N$ is the total number of bricks in the wall and $g$ is the total number of gaps in all the rows.

## Standalone solution file (`cpp/0554-brick-wall.cpp` in the NeetCode repo)

```cpp
 /*
    Approach: 
    Store the count of the end of the brick for each row in a hash and keep the track
    of max number of brick that ends at same position, return rows - max.
    
    Time complexity : O(n x m)
    Space complexity: O(n x m)

    n is number of rows, m is max brick in a row.
*/

class Solution {
public:
    int leastBricks(vector<vector<int>>& wall) {

        map<int,int> end_count;
        int end_of_brick, max_end_count=0;

        int rows = wall.size(),cols;

        for(int i =0;i<rows;i++){
            end_of_brick = 0;

            // '-1' because edge of the wall is not considered
            cols = wall[i].size() -1;
            for(int j =0;j<cols;j++){
                end_of_brick += wall[i][j];

                if(end_count.find(end_of_brick)!=end_count.end())
                {
                    end_count[end_of_brick]++;
                }
                else{
                    end_count[end_of_brick] = 1;
                }
                max_end_count = max(max_end_count,end_count[end_of_brick]);
            }
        }

        return rows - max_end_count;
    }
};
```
