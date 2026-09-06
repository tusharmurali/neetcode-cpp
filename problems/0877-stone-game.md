# 877. Stone Game

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/stone-game/>  
- **NeetCode:** <https://neetcode.io/problems/stone-game>  
- **Video:** <https://www.youtube.com/watch?v=uhgdXOlGYqE>  

[← Back to index](../INDEX.md)

## 1. Recursion

This is a two-player game where Alice and Bob take turns picking from either end of the piles array. Both play optimally, meaning each player maximizes their own score. We can simulate this using recursion where we track the current range `[l, r]` and determine whose turn it is based on the range length. Alice wants to maximize her score, while Bob's moves affect what Alice can collect later.

```cpp
class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        int total = accumulate(piles.begin(), piles.end(), 0);
        int aliceScore = dfs(0, piles.size() - 1, piles);
        return aliceScore > total - aliceScore;
    }

private:
    int dfs(int l, int r, const vector<int>& piles) {
        if (l > r) {
            return 0;
        }
        bool even = (r - l) % 2 == 0;
        int left = even ? piles[l] : 0;
        int right = even ? piles[r] : 0;
        return max(dfs(l + 1, r, piles) + left, dfs(l, r - 1, piles) + right);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since the same `(l, r)` range can be reached through different sequences of moves. By memoizing results for each `(l, r)` pair, we avoid recomputing the same states and achieve polynomial time complexity.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    bool stoneGame(vector<int>& piles) {
        int n = piles.size();
        dp = vector<vector<int>>(n, vector<int>(n, -1));
        int total = accumulate(piles.begin(), piles.end(), 0);
        int aliceScore = dfs(0, n - 1, piles);
        return aliceScore > total - aliceScore;
    }

private:
    int dfs(int l, int r, const vector<int>& piles) {
        if (l > r) {
            return 0;
        }
        if (dp[l][r] != -1) {
            return dp[l][r];
        }
        bool even = (r - l) % 2 == 0;
        int left = even ? piles[l] : 0;
        int right = even ? piles[r] : 0;
        dp[l][r] = max(dfs(l + 1, r, piles) + left, dfs(l, r - 1, piles) + right);
        return dp[l][r];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion with memoization, we can fill the DP table iteratively. We process subproblems in order of increasing range length. For each range `[l, r]`, we compute Alice's optimal score based on already-solved smaller ranges `[l+1, r]` and `[l, r-1]`.

```cpp
class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        int n = piles.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));

        for (int l = n - 1; l >= 0; l--) {
            for (int r = l; r < n; r++) {
                bool even = (r - l) % 2 == 0;
                int left = even ? piles[l] : 0;
                int right = even ? piles[r] : 0;
                if (l == r) {
                    dp[l][r] = left;
                } else {
                    dp[l][r] = max(dp[l + 1][r] + left, dp[l][r - 1] + right);
                }
            }
        }

        int total = accumulate(piles.begin(), piles.end(), 0);
        int aliceScore = dp[0][n - 1];
        return aliceScore > total - aliceScore;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Space Optimized)

Looking at the DP transitions, `dp[l][r]` only depends on `dp[l+1][r]` and `dp[l][r-1]`. When iterating by increasing `l` from right to left and `r` from left to right, we only need values from the current row being built. This allows us to compress the 2D table into a 1D array.

```cpp
class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        int n = piles.size();
        vector<int> dp(n, 0);

        for (int l = n - 1; l >= 0; l--) {
            for (int r = l; r < n; r++) {
                bool even = (r - l) % 2 == 0;
                int left = even ? piles[l] : 0;
                int right = even ? piles[r] : 0;

                if (l == r) {
                    dp[r] = left;
                } else {
                    dp[r] = max(dp[r] + left, dp[r - 1] + right);
                }
            }
        }

        int total = accumulate(piles.begin(), piles.end(), 0);
        int aliceScore = dp[n - 1];
        return aliceScore > (total - aliceScore);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 5. Return TRUE

Here is the key insight: with an even number of piles and an odd total sum, Alice can always win. She can always choose to take all even-indexed piles or all odd-indexed piles. Since the total is odd, one of these sets must have a larger sum. Alice, moving first, can force the game to give her whichever set she prefers, guaranteeing a win.

```cpp
class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0877-stone-game.cpp` in the NeetCode repo)

```cpp
/*
  Alice and Bob play a game with piles of stones. There are an even number of piles arranged 
  in a row, and each pile has a positive integer number of stones piles[i].

  The objective of the game is to end with the most stones. The total number of stones across 
  all the piles is odd, so there are no ties.

  Alice and Bob take turns, with Alice starting first. Each turn, a player takes the entire pile 
  of stones either from the beginning or from the end of the row. This continues until there are 
  no more piles left, at which point the person with the most stones wins.

  Assuming Alice and Bob play optimally, return true if Alice wins the game, or false if Bob wins.
	
  Ex: Input: piles = [5,3,4,5]
  Output: true
  Explanation: 
  Alice starts first, and can only take the first 5 or the last 5.
  Say she takes the first 5, so that the row becomes [3, 4, 5].
  If Bob takes 3, then the board is [4, 5], and Alice takes 5 to win with 10 points.
  If Bob takes the last 5, then the board is [3, 4], and Alice takes 4 to win with 9 points.
  This demonstrated that taking the first 5 was a winning move for Alice, so we return true.

  Space: O(n/2)
  Time : O(1)
*/


class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        int alice = 0, bob = 0, size = piles.size();
        for(int i = 0 ; i < size/2; i++) {
            alice = alice + max( piles[i], piles[size - 1- i] );
            bob = bob + min( piles[i], piles[size - 1- i] );
        }
        if(alice > bob)  
            return true;
        return false;
    }
};
```
