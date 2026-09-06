# 312. Burst Balloons

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/burst-balloons/>  
- **NeetCode:** <https://neetcode.io/problems/burst-balloons>  
- **Video:** <https://www.youtube.com/watch?v=VFskby7lUbw>  
- **Video approach:** 3. Dynamic Programming (Bottom-Up)  

[← Back to index](../INDEX.md)

## 1. Brute Force (Recursion)

This problem asks us to find the **maximum coins** we can collect by bursting balloons in the best possible order.

When we burst a balloon, the number of coins we gain depends on its **current neighbors**. Since bursting one balloon changes the neighbors of others, the order of bursting matters a lot.

A brute-force way to solve this is to **try every possible balloon as the last one to burst** in the current array:

- If we choose a balloon to burst now, we earn coins based on its left and right neighbors.
- Then the problem reduces to bursting the remaining balloons.

The recursive function represents:  
**“What is the maximum number of coins we can collect from the current list of balloons?”**

To simplify edge cases, we add `1` to both ends of the array so every balloon always has two neighbors.

```cpp
class Solution {
public:
    int maxCoins(vector<int>& nums) {
        nums.insert(nums.begin(), 1);
        nums.push_back(1);

        return dfs(nums);
    }

    int dfs(vector<int>& nums) {
        if (nums.size() == 2) return 0;

        int maxCoins = 0;
        for (int i = 1; i < nums.size() - 1; i++) {
            int coins = nums[i - 1] * nums[i] * nums[i + 1];
            vector<int> newNums = nums;
            newNums.erase(newNums.begin() + i);
            coins += dfs(newNums);
            maxCoins = max(maxCoins, coins);
        }
        return maxCoins;
    }
};
```

**Complexity**

- Time complexity: $O(n*2^n)$
- Space complexity: $O(n*2^n)$

## 2. Dynamic Programming (Top-Down)

The brute-force recursion tries every possible bursting order, which repeats the same work many times.

A useful way to think about this problem is:
instead of choosing the **first** balloon to burst, choose the **last** balloon to burst in a subarray.

Why this helps:

- If balloon `i` is the last one to burst between indices `l` and `r`, then at that moment:
    - everything inside `(l..r)` except `i` is already gone
    - the neighbors of `i` are fixed: `nums[l - 1]` on the left and `nums[r + 1]` on the right
- So the coins gained from bursting `i` last are:
    - `nums[l - 1] * nums[i] * nums[r + 1]`
- And the remaining work splits cleanly into two independent parts:
    - best coins from `(l..i-1)`
    - best coins from `(i+1..r)`

This creates overlapping subproblems, so we store results in a memo table `dp` keyed by `(l, r)`.

```cpp
class Solution {
public:
    int maxCoins(vector<int>& nums) {
        int n = nums.size();
        vector<int> newNums(n + 2, 1);
        for (int i = 0; i < n; i++) {
            newNums[i + 1] = nums[i];
        }

        vector<vector<int>> dp(n + 2, vector<int>(n + 2, -1));
        return dfs(newNums, 1, newNums.size() - 2, dp);
    }

    int dfs(vector<int>& nums, int l, int r, vector<vector<int>>& dp) {
        if (l > r) return 0;
        if (dp[l][r] != -1) return dp[l][r];

        dp[l][r] = 0;
        for (int i = l; i <= r; i++) {
            int coins = nums[l - 1] * nums[i] * nums[r + 1];
            coins += dfs(nums, l, i - 1, dp) + dfs(nums, i + 1, r, dp);
            dp[l][r] = max(dp[l][r], coins);
        }
        return dp[l][r];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up) ▶ video

We want the maximum coins we can get by bursting balloons in the best order.
The key trick is to think in reverse:

Instead of choosing which balloon to burst first, we choose which balloon is **burst last** in a range.

If we are only looking at balloons between `l` and `r`, and balloon `i` is the last one burst in that range, then:

- all balloons inside `(l..r)` except `i` are already gone
- so the neighbors of `i` are fixed as `new_nums[l - 1]` and `new_nums[r + 1]`
- coins gained from bursting `i` last are:
    - `new_nums[l - 1] * new_nums[i] * new_nums[r + 1]`

After bursting `i` last, the remaining problem splits into two independent subproblems:

- best coins for `[l .. i-1]`
- best coins for `[i+1 .. r]`

This makes the problem perfect for interval DP.

```cpp
class Solution {
public:
    int maxCoins(vector<int>& nums) {
        int n = nums.size();
        vector<int> newNums(n + 2, 1);
        for (int i = 0; i < n; i++) {
            newNums[i + 1] = nums[i];
        }

        vector<vector<int>> dp(n + 2, vector<int>(n + 2, 0));
        for (int l = n; l >= 1; l--) {
            for (int r = l; r <= n; r++) {
                for (int i = l; i <= r; i++) {
                    int coins = newNums[l - 1] * newNums[i] * newNums[r + 1];
                    coins += dp[l][i - 1] + dp[i + 1][r];
                    dp[l][r] = max(dp[l][r], coins);
                }
            }
        }

        return dp[1][n];
    }
};
```

**Complexity**

- Time complexity: $O(n^3)$
- Space complexity: $O(n^2)$

## Standalone solution file (`cpp/0312-burst-balloons.cpp` in the NeetCode repo)

```cpp
/*
    Given array of balloons w/ coins, if burst ith, get (i-1) + i + (i+1) coins
    Return max coins can collect by bursting the balloons wisely

    DP to return max coins obtainable in each interval [left, right]
    Divide & conquer left & right depends on previous bursts, so think backwards
    Instead of which one to burst first, need to think which one to burst last

    Time: O(n^3) -> O(n^2) states, for each states, determining max coins is O(n)
    Space: O(n^2) -> O(n^2) to store all states
*/

class Solution {
public:
    int maxCoins(vector<int>& nums) {
        // add 1 before & after nums
        nums.insert(nums.begin(), 1);
        nums.insert(nums.end(), 1);
        int n = nums.size();
        
        // cache results of dp
        vector<vector<int>> memo(n, vector<int>(n, 0));
        
        // 1 & n - 2 since we can't burst our fake balloons
        return dp(nums, memo, 1, n - 2);
    }
private:
    int dp(vector<int>& nums, vector<vector<int>>& memo, int left, int right) {
        // base case interval is empty, yields 0 coins
        if (right - left < 0) {
            return 0;
        }
        
        // we've already seen this, return from cache
        if (memo[left][right] > 0) {
            return memo[left][right];
        }
        
        // find the last burst in nums[left]...nums[right]
        int result = 0;
        for (int i = left; i <= right; i++) {
            // nums[i] is the last burst
            int curr = nums[left - 1] * nums[i] * nums[right + 1];
            // nums[i] is fixed, recursively call left & right sides
            int remaining = dp(nums, memo, left, i - 1) + dp(nums, memo, i + 1, right);
            result = max(result, curr + remaining);
        }
        // add to cache
        memo[left][right] = result;
        return result;
    }
};
```
