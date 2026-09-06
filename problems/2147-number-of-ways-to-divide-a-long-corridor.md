# 2147. Number of Ways to Divide a Long Corridor

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-ways-to-divide-a-long-corridor>  
- **Video:** <https://www.youtube.com/watch?v=YOTjCd4Eyhc>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We need to divide the corridor so each section has exactly two seats. The key insight is that after placing two seats in a section, we have a choice: place the divider immediately after the second seat, or delay it through any number of plants. Each plant between the second seat of one section and the first seat of the next section represents a possible divider position.

```cpp
class Solution {
public:
    static constexpr int MOD = 1'000'000'007;
    vector<vector<int>> dp;

    int numberOfWays(string corridor) {
        int n = corridor.size();
        dp.assign(n, vector<int>(3, -1));
        return dfs(0, 0, corridor);
    }

    int dfs(int i, int seats, string& corridor) {
        if (i == corridor.size()) {
            return seats == 2 ? 1 : 0;
        }
        if (dp[i][seats] != -1) {
            return dp[i][seats];
        }

        int res = 0;
        if (seats == 2) {
            if (corridor[i] == 'S') {
                res = dfs(i + 1, 1, corridor);
            } else {
                res = (dfs(i + 1, 0, corridor) + dfs(i + 1, 2, corridor)) % MOD;
            }
        } else {
            if (corridor[i] == 'S') {
                res = dfs(i + 1, seats + 1, corridor);
            } else {
                res = dfs(i + 1, seats, corridor);
            }
        }

        return dp[i][seats] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Bottom-Up)

We can convert the top-down approach to bottom-up by iterating from the end of the corridor to the beginning. For each position, we compute the number of ways based on whether we have `0`, `1`, or `2` seats in the current section.

```cpp
class Solution {
public:
    int numberOfWays(string corridor) {
        int MOD = 1000000007;
        int n = corridor.size();
        vector<vector<int>> dp(n + 1, vector<int>(3, 0));
        dp[n][2] = 1;

        for (int i = n - 1; i >= 0; i--) {
            for (int seats = 0; seats < 3; seats++) {
                if (seats == 2) {
                    if (corridor[i] == 'S') {
                        dp[i][seats] = dp[i + 1][1];
                    } else {
                        dp[i][seats] = (dp[i + 1][0] + dp[i + 1][2]) % MOD;
                    }
                } else {
                    if (corridor[i] == 'S') {
                        dp[i][seats] = dp[i + 1][seats + 1];
                    } else {
                        dp[i][seats] = dp[i + 1][seats];
                    }
                }
            }
        }
        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Space Optimized)

Since each row of the DP table only depends on the next row, we can reduce space by maintaining just a single array of size `3` (for the three possible seat counts).

```cpp
class Solution {
public:
    int numberOfWays(string corridor) {
        const int MOD = 1000000007;
        vector<int> dp = {0, 0, 1};

        for (int i = corridor.length() - 1; i >= 0; i--) {
            vector<int> new_dp(3, 0);
            for (int seats = 0; seats < 3; seats++) {
                if (seats == 2) {
                    new_dp[seats] = (corridor[i] == 'S') ? dp[1] : (dp[0] + dp[2]) % MOD;
                } else {
                    new_dp[seats] = (corridor[i] == 'S') ? dp[seats + 1] : dp[seats];
                }
            }
            dp = new_dp;
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Combinatorics

Instead of DP, we can think combinatorially. First, collect all seat positions. If the count isn't even or is less than `2`, there's no valid way. Otherwise, between every pair of seats (the 2nd and 3rd, 4th and 5th, etc.), we can place the divider at any position including those occupied by plants. The number of choices at each gap is the distance between consecutive pairs of seats.

```cpp
class Solution {
public:
    int numberOfWays(string corridor) {
        int mod = 1'000'000'007;
        vector<int> seats;

        for (int i = 0; i < corridor.size(); i++) {
            if (corridor[i] == 'S') {
                seats.push_back(i);
            }
        }

        int length = seats.size();
        if (length < 2 || length % 2 == 1) {
            return 0;
        }

        long long res = 1;
        for (int i = 1; i < length - 1; i += 2) {
            res = (res * (seats[i + 1] - seats[i])) % mod;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Combinatorics (Optimal)

We can optimize the combinatorics approach by not storing all seat positions. Instead, we track the count of seats and the position of the previous seat. Whenever we complete a pair (seat count becomes even and greater than `2`), we multiply by the gap between the current seat and the previous one.

```cpp
class Solution {
public:
    int numberOfWays(string corridor) {
        int mod = 1'000'000'007, count = 0, res = 1, prev = -1;

        for (int i = 0; i < corridor.size(); i++) {
            if (corridor[i] == 'S') {
                count++;
                if (count > 2 && count % 2 == 1) {
                    res = (1LL * res * (i - prev)) % mod;
                }
                prev = i;
            }
        }

        return (count >= 2 && count % 2 == 0) ? res : 0;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
