# 45. Jump Game II

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/jump-game-ii/>  
- **NeetCode:** <https://neetcode.io/problems/jump-game-ii>  
- **Video:** <https://www.youtube.com/watch?v=dJ7sWiOoK7g>  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks for the **minimum number of jumps** needed to reach the last index of the array.

From any index `i`, the value `nums[i]` tells us how far we can jump.
So at index `i`, we can choose to jump to **any index between `i + 1` and `i + nums[i]`**.

Using recursion, we try **all possible jumps** from the current index and choose the one that leads to the end using the **fewest total jumps**.

The recursive function represents:
**"What is the minimum number of jumps required to reach the last index starting from index `i`?"**

If we ever reach the last index, no more jumps are needed.
If we get stuck at an index with `0` jump length, that path is invalid.

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        return dfs(nums, 0);
    }

private:
    int dfs(vector<int>& nums, int i) {
        if (i == nums.size() - 1) {
            return 0;
        }
        if (nums[i] == 0) {
            return 1000000;
        }

        int res = 1000000;
        int end = min((int)nums.size() - 1, i + nums[i]);
        for (int j = i + 1; j <= end; ++j) {
            res = min(res, 1 + dfs(nums, j));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

This problem asks for the **minimum number of jumps** required to reach the last index.

At any index `i`, the value `nums[i]` tells us the **maximum jump length** from that position.
So from index `i`, we can try jumping to any index in the range `(i + 1)` to `(i + nums[i])`.

The pure recursive solution tries all possibilities, but it recomputes the same results for the same indices many times.
To avoid this repetition, we use **top-down dynamic programming (memoization)**.

The recursive function answers the question:
**"What is the minimum number of jumps needed to reach the end starting from index `i`?"**

Once we compute the answer for an index, we store it and reuse it whenever needed.

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        unordered_map<int, int> memo;
        return dfs(nums, 0, memo);
    }

private:
    int dfs(vector<int>& nums, int i, unordered_map<int, int>& memo) {
        if (memo.count(i)) {
            return memo[i];
        }
        if (i == nums.size() - 1) {
            return 0;
        }
        if (nums[i] == 0) {
            return 1000000;
        }

        int res = 1000000;
        int end = min((int)nums.size(), i + nums[i] + 1);
        for (int j = i + 1; j < end; j++) {
            res = min(res, 1 + dfs(nums, j, memo));
        }
        memo[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

This problem asks for the **minimum number of jumps** needed to reach the last index of the array.

Instead of using recursion, we can solve this using **bottom-up dynamic programming** by working backwards from the end.

The key idea is:

- for each index `i`, we want to know the minimum number of jumps needed to reach the end **starting from `i`**
- from index `i`, we can jump to any index in the range `[i + 1, i + nums[i]]`
- so the answer for `i` is: `1 + minimum(dp[j])` for all reachable `j`

By filling the DP array from right to left, all future states are already computed when needed.

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        int n = nums.size();
        vector<int> dp(n, 1000000);
        dp[n - 1] = 0;

        for (int i = n - 2; i >= 0; i--) {
            int end = min((int)nums.size(), i + nums[i] + 1);
            for (int j = i + 1; j < end; j++) {
                dp[i] = min(dp[i], 1 + dp[j]);
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Breadth First Search (Greedy)

This problem asks for the **minimum number of jumps** needed to reach the last index.

We can think of this problem as moving **level by level**, similar to **Breadth First Search (BFS)**:

- each “level” represents all positions we can reach using the same number of jumps
- from those positions, we compute how far we can reach in **one more jump**

Instead of explicitly using a queue, we use a **greedy window**:

- `[l, r]` represents the range of indices reachable with the current number of jumps
- from this range, we find the **farthest index** we can reach in the next jump

Once we finish scanning the current range, we move to the next range and increase the jump count.

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        int res = 0, l = 0, r = 0;

        while (r < nums.size() - 1) {
            int farthest = 0;
            for (int i = l; i <= r; i++) {
                farthest = max(farthest, i + nums[i]);
            }
            l = r + 1;
            r = farthest;
            res++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0045-jump-game-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, determine min jumps to reach last index
    Ex. nums = [2,3,1,1,4] -> 2, index 0 to 1 to last

    Greedy: At each point, determine furthest reachable, jump to it

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int jump(vector<int>& nums) {
        int n = nums.size();
        int result = 0;
        
        int i = 0;
        while (i < n - 1) {
            if (i + nums[i] >= n - 1) {
                result++;
                break;
            }
            int maxIndex = i + 1;
            int maxValue = 0;
            for (int j = i + 1; j < i + 1 + nums[i]; j++) {
                if (j + nums[j] > maxValue) {
                    maxIndex = j;
                    maxValue = j + nums[j];
                }
            }
            i = maxIndex;
            result++;
        }
        
        return result;
    }
};
```
