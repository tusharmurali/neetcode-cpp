# 1406. Stone Game III

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/stone-game-iii/>  
- **NeetCode:** <https://neetcode.io/problems/stone-game-iii>  
- **Video:** <https://www.youtube.com/watch?v=HsLG5QW9CFQ>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down) - I

Alice and Bob take turns picking `1`, `2`, or `3` stones from the front. Both play optimally: Alice maximizes her score while Bob minimizes Alice's score. We track the score difference (Alice minus Bob) throughout the game. At each state, we know whose turn it is and the current position. Alice adds stone values to the running score, while Bob subtracts them. The final result tells us who wins based on whether the difference is positive, negative, or zero.

```cpp
class Solution {
    vector<vector<int>> dp;
    int n;

public:
    string stoneGameIII(vector<int>& stoneValue) {
        n = stoneValue.size();
        dp.assign(n, vector<int>(2, INT_MIN));

        int result = dfs(0, 1, stoneValue);
        if (result == 0) return "Tie";
        return result > 0 ? "Alice" : "Bob";
    }

private:
    int dfs(int i, int alice, vector<int>& stoneValue) {
        if (i >= n) return 0;
        if (dp[i][alice] != INT_MIN) return dp[i][alice];

        int res = alice == 1 ? INT_MIN : INT_MAX;
        int score = 0;
        for (int j = i; j < min(i + 3, n); j++) {
            if (alice == 1) {
                score += stoneValue[j];
                res = max(res, score + dfs(j + 1, 0, stoneValue));
            } else {
                score -= stoneValue[j];
                res = min(res, score + dfs(j + 1, 1, stoneValue));
            }
        }

        dp[i][alice] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down) - II

We can simplify the recursion by treating both players symmetrically. At any position, the current player wants to maximize their advantage over the opponent. Since the game is zero-sum, if the current player takes some stones with total value `T`, and the opponent then plays optimally getting result `R`, the current player's relative advantage is `T - R`. This formulation eliminates the need to track whose turn it is.

```cpp
class Solution {
public:
    string stoneGameIII(vector<int>& stoneValue) {
        n = stoneValue.size();
        dp.assign(n, INT_MIN);

        int result = dfs(0, stoneValue);
        if (result == 0) return "Tie";
        return result > 0 ? "Alice" : "Bob";
    }

private:
    vector<int> dp;
    int n;

    int dfs(int i, vector<int>& stoneValue) {
        if (i >= n) return 0;
        if (dp[i] != INT_MIN) return dp[i];

        int res = INT_MIN, total = 0;
        for (int j = i; j < min(i + 3, n); j++) {
            total += stoneValue[j];
            res = max(res, total - dfs(j + 1, stoneValue));
        }

        dp[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Converting the recursive solution to iterative form, we fill the DP table from right to left. Each position stores the maximum advantage the current player can achieve from that point onward. Since each state only depends on the next three states, we process positions in reverse order to ensure dependencies are resolved.

```cpp
class Solution {
public:
    string stoneGameIII(vector<int>& stoneValue) {
        int n = stoneValue.size();
        vector<int> dp(n + 1, INT_MIN);
        dp[n] = 0;

        for (int i = n - 1; i >= 0; i--) {
            int total = 0;
            dp[i] = INT_MIN;
            for (int j = i; j < min(i + 3, n); j++) {
                total += stoneValue[j];
                dp[i] = max(dp[i], total - dp[j + 1]);
            }
        }

        int result = dp[0];
        if (result == 0) return "Tie";
        return result > 0 ? "Alice" : "Bob";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Since each state only depends on the next three states (`dp[i+1]`, `dp[i+2]`, `dp[i+3]`), we can reduce space from `O(n)` to `O(1)` by using a rolling array of size `4`. We use modulo arithmetic to cycle through the array indices as we process positions from right to left.

```cpp
class Solution {
public:
    string stoneGameIII(vector<int>& stoneValue) {
        int n = stoneValue.size();
        vector<int> dp(4, 0);

        for (int i = n - 1; i >= 0; --i) {
            int total = 0;
            dp[i % 4] = INT_MIN;
            for (int j = i; j < min(i + 3, n); ++j) {
                total += stoneValue[j];
                dp[i % 4] = max(dp[i % 4], total - dp[(j + 1) % 4]);
            }
        }

        if (dp[0] == 0) return "Tie";
        return dp[0] > 0 ? "Alice" : "Bob";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
