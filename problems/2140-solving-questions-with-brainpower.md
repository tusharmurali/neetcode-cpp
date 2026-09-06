# 2140. Solving Questions With Brainpower

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/solving-questions-with-brainpower/>  
- **NeetCode:** <https://neetcode.io/problems/solving-questions-with-brainpower>  
- **Video:** <https://www.youtube.com/watch?v=D7TD_ArkfkA>  

[← Back to index](../INDEX.md)

## 1. Recursion

At each question, we have two choices: solve it and skip the next few questions based on its brainpower requirement, or skip it entirely and move to the next question. This creates a decision tree where we want to maximize points. We recursively explore both choices at each position and return the maximum.

```cpp
class Solution {
public:
    long long mostPoints(vector<vector<int>>& questions) {
        return dfs(0, questions);
    }

private:
    long long dfs(int i, vector<vector<int>>& questions) {
        if (i >= questions.size()) return 0;
        return max(dfs(i + 1, questions), questions[i][0] + dfs(i + 1 + questions[i][1], questions));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The plain recursion has overlapping subproblems since we may compute the maximum points from the same index multiple times. By storing results in a memoization table, we avoid redundant calculations. Each index is computed at most once, giving us linear time complexity.

```cpp
class Solution {
    vector<long long> dp;

public:
    long long mostPoints(vector<vector<int>>& questions) {
        dp.assign(questions.size(), 0);
        return dfs(0, questions);
    }

private:
    long long dfs(int i, vector<vector<int>>& questions) {
        if (i >= questions.size()) return 0;
        if (dp[i] != 0) return dp[i];
        dp[i] = max(dfs(i + 1, questions), questions[i][0] + dfs(i + 1 + questions[i][1], questions));
        return dp[i];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion, we can fill a DP table iteratively from right to left. For each question, we compute the maximum points achievable starting from that position. Working backwards ensures that when we process question i, we already know the best outcomes for all questions after it.

```cpp
class Solution {
public:
    long long mostPoints(vector<vector<int>>& questions) {
        int n = questions.size();
        vector<long long> dp(n + 1, 0);

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = max(
                (long long)questions[i][0] + (i + 1 + questions[i][1] < n ? dp[i + 1 + questions[i][1]] : 0),
                dp[i + 1]
            );
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/2140-solving-questions-with-brainpower.cpp` in the NeetCode repo)

```cpp
// Time Complexity: O(n)
// Space Complexity: O(n)

class Solution
{
public:
    long long mostPoints(vector<vector<int>> &questions)
    {
        int n = questions.size();
        vector<long long> dp(n, 0);
        dp[n - 1] = questions[n - 1][0];
        long long ans = dp[n - 1];
        for (int i = n - 2; i >= 0; i--)
        {
            int k = i + questions[i][1] + 1;
            if (k < n)
            {
                dp[i] = (dp[k] + questions[i][0]) > dp[i + 1] ? (dp[k] + questions[i][0]) : dp[i + 1];
            }
            else
            {
                dp[i] = questions[i][0] > dp[i + 1] ? questions[i][0] : dp[i + 1];
            }
            ans = ans > dp[i] ? ans : dp[i];
        }
        return ans;
    }
};
```
