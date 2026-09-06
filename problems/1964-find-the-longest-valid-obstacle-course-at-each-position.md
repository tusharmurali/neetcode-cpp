# 1964. Find the Longest Valid Obstacle Course at Each Position

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-longest-valid-obstacle-course-at-each-position>  
- **Video:** <https://www.youtube.com/watch?v=Xq9VT7p0lic>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

For each position, we want the longest increasing subsequence ending at that position where each element is less than or equal to the next. This is a variant of the classic LIS problem. We can use memoization: for each index and the previous element chosen, we either include the current element in our sequence (if valid) or skip it.

```cpp
class Solution {
public:
    vector<vector<int>> dp;

    vector<int> longestObstacleCourseAtEachPosition(vector<int>& obstacles) {
        int n = obstacles.size();
        this->dp = vector<vector<int>>(n, vector<int>(n + 1, -1));

        dfs(n - 1, n, obstacles);

        vector<int> res(n, 1);
        for (int i = 1; i < n; i++) {
            res[i] = 1 + dp[i - 1][i];
        }
        return res;
    }

private:
    int dfs(int i, int prev, vector<int>& obstacles) {
        if (i < 0) {
            return 0;
        }
        if (dp[i][prev] != -1) {
            return dp[i][prev];
        }

        int res = dfs(i - 1, prev, obstacles);
        if (prev == obstacles.size() || obstacles[prev] >= obstacles[i]) {
            res = max(res, 1 + dfs(i - 1, i, obstacles));
        }
        return dp[i][prev] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Dynamic Programming (Binary Search) - I

We can optimize the LIS approach using binary search. Maintain a `dp` array where `dp[i]` represents the smallest ending value of all increasing subsequences of length `i + 1`. For each new element, we find where it fits using binary search (finding the first element greater than it), which tells us the longest subsequence we can extend. We then update that position with the current value to keep subsequences as extensible as possible.

```cpp
class Solution {
public:
    vector<int> longestObstacleCourseAtEachPosition(vector<int>& obstacles) {
        int n = obstacles.size();
        vector<int> res(n);
        vector<int> dp(n + 1, 1e8);

        for (int i = 0; i < n; i++) {
            int index = upper_bound(dp.begin(), dp.end(), obstacles[i]) - dp.begin();
            res[i] = index + 1;
            dp[index] = obstacles[i];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Binary Search) - II

This is a space-optimized version of the previous approach. Instead of preallocating an array of size `n + 1`, we start with an empty array and only grow it as needed. When a new element extends the longest sequence found so far, we append it; otherwise, we update an existing position. This uses only as much space as the length of the longest subsequence.

```cpp
class Solution {
public:
    vector<int> longestObstacleCourseAtEachPosition(vector<int>& obstacles) {
        int n = obstacles.size();
        vector<int> res(n);
        vector<int> dp;

        for (int i = 0; i < n; i++) {
            int index = upper_bound(dp.begin(), dp.end(), obstacles[i]) - dp.begin();
            res[i] = index + 1;

            if (index == dp.size()) {
                dp.push_back(obstacles[i]);
            } else {
                dp[index] = obstacles[i];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
