# 1531. String Compression II

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/string-compression-ii/>  
- **NeetCode:** <https://neetcode.io/problems/string-compression-ii>  
- **Video:** <https://www.youtube.com/watch?v=ISIG3o-Xofg>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We want to delete at most k characters to minimize the run-length encoded length. The key observation is that the encoded length only increases at certain thresholds: going from 1 to 2 characters adds a digit, going from 9 to 10 adds another digit, and going from 99 to 100 adds yet another. We use recursion with memoization, tracking the current position, remaining deletions, the previous character, and its count. At each step, we either extend a run (if the current character matches the previous) or start a new run (keeping or deleting the current character).

```cpp
class Solution {
    static const int INF = INT_MAX / 2;
    vector<vector<vector<vector<int>>>> dp;

    int count(int i, int k, int prev, int prevCnt, string& s) {
        if (k < 0) return INF;
        if (i == s.size()) return 0;
        if (dp[i][k][prev][prevCnt] != -1) return dp[i][k][prev][prevCnt];

        int res;
        if (prev == s[i] - 'a') {
            int incr = (prevCnt == 1 || prevCnt == 9 || prevCnt == 99) ? 1 : 0;
            res = incr + count(i + 1, k, prev, prevCnt + 1, s);
        } else {
            res = 1 + count(i + 1, k, s[i] - 'a', 1, s); // don't delete
            if (k > 0) {
                res = min(res, count(i + 1, k - 1, prev, prevCnt, s)); // delete s[i]
            }
        }

        return dp[i][k][prev][prevCnt] = res;
    }

public:
    int getLengthOfOptimalCompression(string s, int k) {
        int n = s.size();
        dp = vector<vector<vector<vector<int>>>>(
            n + 1, vector<vector<vector<int>>>(k + 1, vector<vector<int>>(27, vector<int>(101, -1)))
        );
        return count(0, k, 26, 0, s);
    }
};
```

**Complexity**

- Time complexity: $O(k * n ^ 2)$
- Space complexity: $O(k * n ^ 2)$

> Where $n$ is the length of the string $s$ and $k$ is the maximum number of characters that can be deleted from the string.

## 2. Dynamic Programming (Top-Down Optimized)

Instead of tracking the previous character and its count explicitly, we can think of the problem differently. At each position, we decide to either delete the current character or make it the start of a new run. If we start a new run, we scan forward and try to extend it by keeping matching characters and deleting non-matching ones (within our deletion budget). This reduces the state space to just position and remaining deletions.

```cpp
class Solution {
private:
    int n;
    vector<vector<int>> dp;

    int dfs(int i, int k, const string& s) {
        if (n - i <= k) return 0;
        if (dp[i][k] != -1) return dp[i][k];

        int res = 150;
        if (k > 0) res = dfs(i + 1, k - 1, s);

        int freq = 0, delCnt = 0, comp_len = 1;
        for (int j = i; j < n; j++) {
            if (s[i] == s[j]) {
                if (freq == 1 || freq == 9 || freq == 99) comp_len++;
                freq++;
            } else {
                delCnt++;
                if (delCnt > k) break;
            }
            res = min(res, comp_len + dfs(j + 1, k - delCnt, s));
        }
        dp[i][k] = res;
        return res;
    }

public:
    int getLengthOfOptimalCompression(string s, int k) {
        n = s.size();
        dp = vector<vector<int>>(n + 1, vector<int>(k + 1, -1));
        return dfs(0, k, s);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * k)$
- Space complexity: $O(n * k)$

> Where $n$ is the length of the string $s$ and $k$ is the maximum number of characters that can be deleted from the string.

## 3. Dynamic Programming (Bottom-Up)

We convert the optimized top-down solution to bottom-up form. We process positions from right to left, computing for each position and deletion budget the minimum encoded length. This iterative approach fills the DP table systematically and avoids recursion overhead.

```cpp
class Solution {
public:
    int getLengthOfOptimalCompression(string s, int k) {
        int n = s.size();
        vector<vector<int>> dp(n + 1, vector<int>(k + 1, 150));

        for (int remK = 0; remK <= k; remK++) {
            dp[n][remK] = 0;
        }

        for (int i = n - 1; i >= 0; i--) {
            for (int remK = 0; remK <= k; remK++) {
                if (remK > 0) {
                    dp[i][remK] = dp[i + 1][remK - 1];
                }

                int freq = 0, delCnt = 0, compLen = 1;
                for (int j = i; j < n; j++) {
                    if (s[i] == s[j]) {
                        if (freq == 1 || freq == 9 || freq == 99) {
                            compLen++;
                        }
                        freq++;
                    } else {
                        delCnt++;
                        if (delCnt > remK) break;
                    }
                    dp[i][remK] = min(dp[i][remK], compLen + dp[j + 1][remK - delCnt]);
                }
            }
        }

        return dp[0][k];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * k)$
- Space complexity: $O(n * k)$

> Where $n$ is the length of the string $s$ and $k$ is the maximum number of characters that can be deleted from the string.
