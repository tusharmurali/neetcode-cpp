# 55. Jump Game

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/jump-game/>  
- **NeetCode:** <https://neetcode.io/problems/jump-game>  
- **Video:** <https://www.youtube.com/watch?v=Yan0cv2cLy8>  
- **Video approach:** 4. Greedy  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks whether we can reach the **last index** of the array starting from the first index.

At every position `i`, the value `nums[i]` tells us the **maximum jump length** from that index.
So from index `i`, we can jump to **any index between `i + 1` and `i + nums[i]`**.

Using recursion, we try **all possible jumps** from the current index and see if **any path** eventually reaches the last index.

The recursive function represents:
**"Is it possible to reach the last index starting from index `i`?"**

If we ever reach the last index, we know the answer is `true`.

```cpp
class Solution {
public:
    bool canJump(vector<int>& nums) {
        return dfs(nums, 0);
    }

private:
    bool dfs(vector<int>& nums, int i) {
        if (i == nums.size() - 1) {
            return true;
        }
        int end = min((int)nums.size() - 1, i + nums[i]);
        for (int j = i + 1; j <= end; ++j) {
            if (dfs(nums, j)) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

This problem asks whether we can reach the **last index** of the array starting from index `0`.

At each index `i`, the value `nums[i]` tells us how far we can jump. From there, we can choose **any next index within that jump range**.

The plain recursive approach explores all possible jumps, but it repeats the same work many times.
To avoid this, we use **top-down dynamic programming (memoization)**.

The recursive function represents:
**"Can we reach the last index starting from index `i`?"**

Once we know the answer for an index, we store it so we never recompute it.

```cpp
class Solution {
public:
    bool canJump(vector<int>& nums) {
        unordered_map<int, bool> memo;
        return dfs(nums, 0, memo);
    }

private:
    bool dfs(vector<int>& nums, int i, unordered_map<int, bool>& memo) {
        if (memo.count(i)) {
            return memo[i];
        }
        if (i == nums.size() - 1) {
            return true;
        }
        if (nums[i] == 0) {
            return false;
        }

        int end = min((int)nums.size(), i + nums[i] + 1);
        for (int j = i + 1; j < end; j++) {
            if (dfs(nums, j, memo)) {
                memo[i] = true;
                return true;
            }
        }
        memo[i] = false;
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

We want to know if we can reach the **last index** starting from index `0`.

Instead of using recursion, we can solve this using **bottom-up dynamic programming** by working backwards from the end of the array.

The idea is simple:

- mark positions that can reach the end
- then check earlier positions to see if they can jump to any of those “good” positions

If index `i` can jump to **any index `j` that is already reachable**, then `i` is also reachable.

```cpp
class Solution {
public:
    bool canJump(vector<int>& nums) {
        int n = nums.size();
        vector<bool> dp(n, false);
        dp[n - 1] = true;

        for (int i = n - 2; i >= 0; i--) {
            int end = min((int)nums.size(), i + nums[i] + 1);
            for (int j = i + 1; j < end; j++) {
                if (dp[j]) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Greedy ▶ video

We want to check if we can reach the **last index** starting from index `0`.

Instead of trying all possible jumps, we can think about the problem **in reverse**:

- ask which positions can eventually reach the end
- then move backward to see if earlier positions can reach those positions

We keep a variable called `goal`:

- it represents the **leftmost index** that we must be able to reach
- initially, the goal is the last index itself

As we move backward through the array:

- if from index `i` we can jump to the current `goal` (or beyond), then index `i` becomes the new goal

At the end, if index `0` becomes the goal, it means we can reach the last index.

```cpp
class Solution {
public:
    bool canJump(vector<int>& nums) {
        int goal = nums.size() - 1;

        for (int i = nums.size() - 2; i >= 0; i--) {
            if (i + nums[i] >= goal) {
                goal = i;
            }
        }

        return goal == 0;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0055-jump-game.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, return true if can reach last index
    Ex. nums = [2,3,1,1,4] -> true, index 0 to 1 to last

    Greedy: At each point, determine furthest reachable index

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    bool canJump(vector<int>& nums) {
        int n = nums.size();
        int reachable = 0;
        
        for (int i = 0; i < n; i++) {
            if (i > reachable) {
                return false;
            }
            reachable = max(reachable, i + nums[i]);
            if (reachable >= n - 1) {
                break;
            }
        }
        
        return true;
    }
};
```
