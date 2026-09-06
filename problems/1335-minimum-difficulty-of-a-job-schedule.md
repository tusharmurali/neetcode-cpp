# 1335. Minimum Difficulty of a Job Schedule

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-difficulty-of-a-job-schedule>  
- **Video:** <https://www.youtube.com/watch?v=DAAULrZFeLI>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We need to split `n` jobs across `d` days, where each day must have at least one job, and the difficulty of a day is the maximum difficulty among all jobs scheduled that day. This is a classic partitioning problem. At each step, we decide how many consecutive jobs to assign to the current day, then recursively solve for the remaining jobs and days. We track the maximum job difficulty seen so far for the current day and explore two choices: extend the current day by including the next job, or end the current day and start a new one.

```cpp
class Solution {
    vector<vector<vector<int>>> dp;

    int dfs(int i, int d, int curMax, const vector<int>& jobDifficulty) {
        if (i == jobDifficulty.size()) return d == 0 ? 0 : INT_MAX / 2;
        if (d == 0) return INT_MAX / 2;
        if (dp[i][d][curMax + 1] != -1) return dp[i][d][curMax + 1];

        int maxSoFar = max(curMax, jobDifficulty[i]);
        int res = min(
            dfs(i + 1, d, maxSoFar, jobDifficulty),
            maxSoFar + dfs(i + 1, d - 1, -1, jobDifficulty)
        );

        dp[i][d][curMax + 1] = res;
        return res;
    }

public:
    int minDifficulty(vector<int>& jobDifficulty, int d) {
        int n = jobDifficulty.size();
        if (n < d) return -1;

        int m = *max_element(jobDifficulty.begin(), jobDifficulty.end());
        dp = vector<vector<vector<int>>>(n, vector<vector<int>>(d + 1, vector<int>(m + 5, -1)));
        return dfs(0, d, -1, jobDifficulty);
    }
};
```

**Complexity**

- Time complexity: $O(n * d * m)$
- Space complexity: $O(n * d * m)$

> Where $n$ is the number of jobs, $d$ is the number of days, and $m$ is the maximum difficulty value among all the job difficulties.

## 2. Dynamic Programming (Top-Down Optimized)

The previous approach tracks `cur_max` as part of the state, which can lead to many states. We can optimize by restructuring: instead of tracking the current maximum, we iterate over all possible ending positions for the current day. For each starting position `i` and remaining days `d`, we try ending the day at positions `i, i+1, ..., n-d` (leaving enough jobs for remaining days). While iterating, we maintain a running maximum and take the best choice.

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    int minDifficulty(vector<int>& jobDifficulty, int d) {
        int n = jobDifficulty.size();
        if (n < d) return -1;

        dp.assign(n, vector<int>(d + 1, -1));
        return dfs(0, d, jobDifficulty);
    }

private:
    int dfs(int i, int d, vector<int>& jobDifficulty) {
        if (dp[i][d] != -1) return dp[i][d];

        int n = jobDifficulty.size();
        int maxi = jobDifficulty[i];
        if (d == 1) {
            for (int j = i; j < n; j++) {
                maxi = max(maxi, jobDifficulty[j]);
            }
            dp[i][d] = maxi;
            return maxi;
        }

        int res = INT_MAX / 2;
        for (int j = i + 1; j < n; j++) {
            res = min(res, maxi + dfs(j, d - 1, jobDifficulty));
            maxi = max(maxi, jobDifficulty[j]);
        }
        dp[i][d] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * d)$
- Space complexity: $O(n * d)$

> Where $n$ is the number of jobs and $d$ is the number of days.

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down recursion into an iterative bottom-up approach. Define `dp[i][day]` as the minimum difficulty to schedule jobs from index `i` onward using exactly `day` days. We fill the table starting from the last day and work backward. For each state, we try all valid partitions of jobs for the current day and combine with the precomputed result for remaining days.

```cpp
class Solution {
public:
    int minDifficulty(vector<int>& jobDifficulty, int d) {
        int n = jobDifficulty.size();
        if (n < d) return -1;

        vector<vector<int>> dp(n + 1, vector<int>(d + 1, INT_MAX / 2));
        dp[n][0] = 0;

        for (int day = 1; day <= d; day++) {
            for (int i = n - 1; i >= 0; i--) {
                int maxi = 0;
                for (int j = i; j <= n - day; j++) {
                    maxi = max(maxi, jobDifficulty[j]);
                    dp[i][day] = min(dp[i][day], maxi + dp[j + 1][day - 1]);
                }
            }
        }

        return dp[0][d];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * d)$
- Space complexity: $O(n * d)$

> Where $n$ is the number of jobs and $d$ is the number of days.

## 4. Dynamic Programming (Space Optimized)

Notice that when computing `dp[i][day]`, we only need values from `dp[j][day-1]` for `j > i`. This means we only need the previous day's row, not the entire 2D table. We can reduce space by using a single 1D array and updating it carefully. By processing positions from left to right within each day, we ensure that when we read `dp[j+1]`, it still holds the value from the previous day.

```cpp
class Solution {
public:
    int minDifficulty(vector<int>& jobDifficulty, int d) {
        int n = jobDifficulty.size();
        if (n < d) return -1;

        int INF = INT_MAX / 2;
        vector<int> dp(n + 1, INF);
        dp[n] = 0;

        for (int day = 1; day <= d; day++) {
            for (int i = 0; i <= n - day; i++) {
                int maxi = 0;
                dp[i] = INF;
                for (int j = i; j <= n - day; j++) {
                    maxi = max(maxi, jobDifficulty[j]);
                    dp[i] = min(dp[i], maxi + dp[j + 1]);
                }
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * d)$
- Space complexity: $O(n)$

> Where $n$ is the number of jobs and $d$ is the number of days.

## 5. Monotonic Decreasing Stack

The bottleneck in the previous approaches is finding the optimal partition for each day, which requires checking all possible ending positions. We can speed this up using a monotonic stack. The key insight is that when a new job has a higher difficulty than previous jobs in the current day, it becomes the new maximum and we can efficiently update our DP values. By maintaining a decreasing stack of job indices, we can quickly determine how previous partitions would change when extended to include the current job.

```cpp
class Solution {
public:
    int minDifficulty(vector<int>& jobDifficulty, int d) {
        int n = jobDifficulty.size();
        if (n < d) return -1;

        vector<int> dp(n, INT_MAX / 2);

        for (int day = 1; day <= d; day++) {
            vector<int> nextDp(n, INT_MAX / 2);
            stack<int> st;
            for (int i = day - 1; i < n; i++) {
                nextDp[i] = (i > 0 ? dp[i - 1] : 0) + jobDifficulty[i];
                while (!st.empty() && jobDifficulty[st.top()] <= jobDifficulty[i]) {
                    int j = st.top(); st.pop();
                    nextDp[i] = min(nextDp[i], nextDp[j] - jobDifficulty[j] + jobDifficulty[i]);
                }
                if (!st.empty()) {
                    nextDp[i] = min(nextDp[i], nextDp[st.top()]);
                }
                st.push(i);
            }
            dp = nextDp;
        }

        return dp[n - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n * d)$
- Space complexity: $O(n)$

> Where $n$ is the number of jobs and $d$ is the number of days.
