# 552. Student Attendance Record II

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/student-attendance-record-ii/>  
- **NeetCode:** <https://neetcode.io/problems/student-attendance-record-ii>  
- **Video:** <https://www.youtube.com/watch?v=BPIJ5ROX0i4>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down) - I

A valid attendance record has at most 1 absence (A) and no more than 2 consecutive late days (L). We can think of this as a state machine where each state tracks two things: how many absences used so far (0 or 1) and how many consecutive late days at the current position (0, 1, or 2). At each position, we decide whether to place P (present), A (absent), or L (late), and transition to the appropriate next state.

```cpp
class Solution {
    const int MOD = 1000000007;
    vector<vector<vector<int>>> cache;

public:
    int checkRecord(int n) {
        cache.assign(n + 1, vector<vector<int>>(2, vector<int>(3, -1)));
        return dfs(n, 0, 0);
    }

private:
    int dfs(int i, int cntA, int cntL) {
        if (i == 0) {
            return 1;
        }
        if (cache[i][cntA][cntL] != -1) {
            return cache[i][cntA][cntL];
        }

        int res = dfs(i - 1, cntA, 0) % MOD;

        if (cntA == 0) {
            res = (res + dfs(i - 1, 1, 0)) % MOD;
        }

        if (cntL < 2) {
            res = (res + dfs(i - 1, cntA, cntL + 1)) % MOD;
        }

        return cache[i][cntA][cntL] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down) - II

This approach reorganizes the state representation. Instead of tracking individual decisions, we store a 2D map keyed by (absence count, consecutive late count) for each length. The recursive function returns all six possible state counts for strings of length `n`, and we combine them when extending to longer strings.

```cpp
class Solution {
private:
    static constexpr int MOD = 1000000007;
    vector<vector<int>> baseCase = {{1, 1, 0}, {1, 0, 0}};
    vector<vector<vector<int>>> cache;

public:
    int checkRecord(int n) {
        cache.assign(n + 1, vector<vector<int>>(2, vector<int>(3, -1)));
        const vector<vector<int>>& result = count(n);
        int total = 0;
        for (const auto& row : result) {
            for (int val : row) {
                total = (total + val) % MOD;
            }
        }
        return total;
    }

private:
    const vector<vector<int>>& count(int n) {
        if (n == 1) {
            return baseCase;
        }

        if (cache[n][0][0] != -1) {
            return cache[n];
        }

        const vector<vector<int>>& prev = count(n - 1);
        auto& res = cache[n];

        // Choose P
        res[0][0] = ((prev[0][0] + prev[0][1]) % MOD + prev[0][2]) % MOD;
        res[1][0] = ((prev[1][0] + prev[1][1]) % MOD + prev[1][2]) % MOD;

        // Choose L
        res[0][1] = prev[0][0];
        res[0][2] = prev[0][1];
        res[1][1] = prev[1][0];
        res[1][2] = prev[1][1];

        // Choose A
        res[1][0] = (res[1][0] + ((prev[0][0] + prev[0][1]) % MOD + prev[0][2]) % MOD) % MOD;

        return cache[n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion, we iterate forward and build the DP table from length 0 to n. Each state `dp[i][cntA][cntL]` represents the number of valid records of length `i` that have used `cntA` absences and end with `cntL` consecutive lates.

```cpp
class Solution {
public:
    int checkRecord(int n) {
        const int MOD = 1000000007;
        vector<vector<vector<int>>> dp(n + 1, vector<vector<int>>(2, vector<int>(3, 0)));

        dp[0][0][0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int cntA = 0; cntA < 2; cntA++) {
                for (int cntL = 0; cntL < 3; cntL++) {
                    // Choose P
                    dp[i][cntA][0] = (dp[i][cntA][0] + dp[i - 1][cntA][cntL]) % MOD;

                    // Choose A
                    if (cntA > 0) {
                        dp[i][cntA][0] = (dp[i][cntA][0] + dp[i - 1][cntA - 1][cntL]) % MOD;
                    }

                    // Choose L
                    if (cntL > 0) {
                        dp[i][cntA][cntL] = (dp[i][cntA][cntL] + dp[i - 1][cntA][cntL - 1]) % MOD;
                    }
                }
            }
        }

        int result = 0;
        for (int cntA = 0; cntA < 2; cntA++) {
            for (int cntL = 0; cntL < 3; cntL++) {
                result = (result + dp[n][cntA][cntL]) % MOD;
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized) - I

Since each position only depends on the previous position, we can reduce space from O(n) to O(1) by keeping only two layers: the current and previous states. We store a 2x3 array representing all six possible (absence count, late count) combinations.

```cpp
class Solution {
public:
    int checkRecord(int n) {
        if (n == 1) return 3;

        const int MOD = 1000000007;
        vector<vector<int>> dp = {{1, 1, 0}, {1, 0, 0}};

        for (int i = 0; i < n - 1; i++) {
            vector<vector<int>> ndp(2, vector<int>(3, 0));

            // Choose P
            ndp[0][0] = ((dp[0][0] + dp[0][1]) % MOD + dp[0][2]) % MOD;
            ndp[1][0] = ((dp[1][0] + dp[1][1]) % MOD + dp[1][2]) % MOD;

            // Choose L
            ndp[0][1] = dp[0][0];
            ndp[1][1] = dp[1][0];
            ndp[0][2] = dp[0][1];
            ndp[1][2] = dp[1][1];

            // Choose A
            ndp[1][0] = (ndp[1][0] + ((dp[0][0] + dp[0][1]) % MOD + dp[0][2]) % MOD) % MOD;

            swap(dp, ndp);
        }

        int total = 0;
        for (auto& row : dp) {
            for (int val : row) {
                total = (total + val) % MOD;
            }
        }
        return total;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Dynamic Programming (Space Optimized) - II

This is an alternative space-optimized formulation that iterates forward from the empty state. We maintain a 2x3 DP array and update it in place, swapping between current and next arrays each iteration.

```cpp
class Solution {
public:
    int checkRecord(int n) {
        const int MOD = 1000000007;
        vector<vector<int>> dp(2, vector<int>(3, 0));

        dp[0][0] = 1;

        for (int i = 1; i <= n; i++) {
            vector<vector<int>> nextDp(2, vector<int>(3, 0));

            for (int cntA = 0; cntA < 2; cntA++) {
                for (int cntL = 0; cntL < 3; cntL++) {
                    // Choose P
                    nextDp[cntA][0] = (nextDp[cntA][0] + dp[cntA][cntL]) % MOD;

                    // Choose A
                    if (cntA > 0) {
                        nextDp[cntA][0] = (nextDp[cntA][0] + dp[cntA - 1][cntL]) % MOD;
                    }

                    // Choose L
                    if (cntL > 0) {
                        nextDp[cntA][cntL] = (nextDp[cntA][cntL] + dp[cntA][cntL - 1]) % MOD;
                    }
                }
            }

            dp = nextDp;
        }

        int result = 0;
        for (int cntA = 0; cntA < 2; cntA++) {
            for (int cntL = 0; cntL < 3; cntL++) {
                result = (result + dp[cntA][cntL]) % MOD;
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
