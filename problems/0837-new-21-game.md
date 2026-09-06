# 837. New 21 Game

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/new-21-game/>  
- **NeetCode:** <https://neetcode.io/problems/new-21-game>  
- **Video:** <https://www.youtube.com/watch?v=zKi4LzjK27k>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

This problem asks for the probability of ending with a score between `k` and `n` (inclusive). Alice draws cards with values 1 to `maxPts` with equal probability until her score reaches `k` or more.

We can think recursively: from a given score, what is the probability of eventually ending at or below `n`? If our score is already >= `k`, we stop drawing. The outcome is successful (probability `1`) if `score <= n`, and failed (probability `0`) if `score > n`.

For scores below `k`, we draw one of `maxPts` values with equal probability `1/maxPts`, so the probability at score `s` is the average of probabilities at scores `s+1`, `s+2`, ..., `s+maxPts`.

```cpp
class Solution {
private:
    vector<double> dp;

public:
    double new21Game(int n, int k, int maxPts) {
        dp.resize(k, -1.0);
        return dfs(0, n, k, maxPts);
    }

private:
    double dfs(int score, int n, int k, int maxPts) {
        if (score >= k) {
            return score <= n ? 1.0 : 0.0;
        }
        if (dp[score] != -1.0) {
            return dp[score];
        }

        double prob = 0;
        for (int i = 1; i <= maxPts; i++) {
            prob += dfs(score + i, n, k, maxPts);
        }

        dp[score] = prob / maxPts;
        return dp[score];
    }
};
```

**Complexity**

- Time complexity: $O(k * m)$
- Space complexity: $O(k)$

> Where $k$ is the threshold score, $m$ is the maximum points per draw and $n$ is the upper bound on score.

## 2. Dynamic Programming (Top-Down Optimized)

The basic top-down approach sums over `maxPts` values at each state, leading to O(k \* maxPts) time. We can optimize by noticing that consecutive states have overlapping sums.

The probability at score `s` equals the sum of probabilities from `s+1` to `s+maxPts` divided by `maxPts`. The probability at `s` can be expressed in terms of `s+1`'s probability using a sliding window technique: `dp[s] = dp[s+1]` minus the difference caused by the window shifting.

The boundary at `k-1` needs special handling since it is the last score where we still draw cards.

```cpp
class Solution {
private:
    vector<double> dp;

public:
    double new21Game(int n, int k, int maxPts) {
        dp.resize(k + maxPts, -1.0);
        return dfs(0, n, k, maxPts);
    }

private:
    double dfs(int score, int n, int k, int maxPts) {
        if (score == k - 1) {
            return min(n - k + 1, maxPts) / (double)maxPts;
        }
        if (score > n) {
            return 0.0;
        }
        if (score >= k) {
            return 1.0;
        }
        if (dp[score] != -1.0) {
            return dp[score];
        }

        dp[score] = dfs(score + 1, n, k, maxPts);
        dp[score] -= (dfs(score + 1 + maxPts, n, k, maxPts) - dfs(score + 1, n, k, maxPts)) / maxPts;
        return dp[score];
    }
};
```

**Complexity**

- Time complexity: $O(k + m)$
- Space complexity: $O(n)$

> Where $k$ is the threshold score, $m$ is the maximum points per draw and $n$ is the upper bound on score.

## 3. Dynamic Programming (Bottom-Up)

Instead of computing probabilities of success from each score, we compute the probability of reaching each score. `dp[score]` represents the probability of landing on exactly that score at some point during the game.

We start at score `0` with probability `1`. For each score from `0` to `k-1` (the scores where we keep drawing), we distribute probability to scores reachable by drawing `1` to `maxPts`. Each draw has probability `1/maxPts`.

The answer is the sum of `dp[score]` for all scores from `k` to `n` (valid ending scores).

```cpp
class Solution {
public:
    double new21Game(int n, int k, int maxPts) {
        vector<double> dp(n + 1, 0.0);
        dp[0] = 1.0;

        for (int score = 1; score <= n; score++) {
            for (int draw = 1; draw <= maxPts; draw++) {
                if (score - draw >= 0 && score - draw < k) {
                    dp[score] += dp[score - draw] / maxPts;
                }
            }
        }

        double result = 0.0;
        for (int i = k; i <= n; i++) {
            result += dp[i];
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $k$ is the threshold score, $m$ is the maximum points per draw and $n$ is the upper bound on score.

## 4. Dynamic Programming (Sliding Window)

We can optimize the bottom-up approach using a sliding window. Notice that `dp[i]` depends on the sum of `dp` values from `dp[i-maxPts]` to `dp[i-1]`, but only those in the range `[0, k-1]`. Instead of recomputing this sum each time, we maintain a running window sum.

Working backwards from `k-1` to `0`, we compute `dp[i]` as `windowSum / maxPts`. The window initially covers scores from `k` to `k+maxPts-1`. For scores >= `k` and <= `n`, the probability of success is `1` (we already stopped and the score is valid). As we move the window, we add the newly computed `dp` value and remove the value that slides out.

```cpp
class Solution {
public:
    double new21Game(int n, int k, int maxPts) {
        if (k == 0) {
            return 1.0;
        }
        double windowSum = 0.0;
        for (int i = k; i < k + maxPts; i++) {
            windowSum += (i <= n) ? 1.0 : 0.0;
        }
        unordered_map<int, double> dp;
        for (int i = k - 1; i >= 0; i--) {
            dp[i] = windowSum / maxPts;
            double remove = 0.0;
            if (i + maxPts <= n) {
                remove = (dp.find(i + maxPts) != dp.end()) ? dp[i + maxPts] : 1.0;
            }
            windowSum += dp[i] - remove;
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(k + m)$
- Space complexity: $O(n)$

> Where $k$ is the threshold score, $m$ is the maximum points per draw and $n$ is the upper bound on score.
