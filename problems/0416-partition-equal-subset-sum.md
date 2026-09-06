# 416. Partition Equal Subset Sum

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/partition-equal-subset-sum/>  
- **NeetCode:** <https://neetcode.io/problems/partition-equal-subset-sum>  
- **Video:** <https://www.youtube.com/watch?v=IsvocB5BJhw>  

[← Back to index](../INDEX.md)

## 1. Recursion

The problem asks whether we can split the array into **two subsets with equal sum**.

Key observation:

- If the total sum is **odd**, it’s impossible → return `False`.
- Otherwise, the problem becomes:
    > Can we pick a subset whose sum is `totalSum / 2`?

This is a classic **subset sum** decision problem.

Using recursion:

- At each index, we have **two choices**:
    1. Take the current number into the subset
    2. Skip the current number
- We keep reducing the target (`sum/2`) until:
    - Target becomes `0` → success
    - We run out of numbers or target becomes negative → failure

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        if (sum % 2 != 0) {
            return false;
        }

        return dfs(nums, 0, sum / 2);
    }

    bool dfs(vector<int>& nums, int i, int target) {
        if (i == nums.size()) {
            return target == 0;
        }
        if (target < 0) {
            return false;
        }

        return dfs(nums, i + 1, target) ||
               dfs(nums, i + 1, target - nums[i]);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

This is the same **subset sum** idea as the recursive approach, but optimized using **memoization**.

Key observations:

- If the total sum is **odd**, we can’t split it into two equal subsets.
- Otherwise, we only need to check if **some subset sums to `totalSum / 2`**.

In plain recursion, many subproblems repeat:

- Same index `i`
- Same remaining `target`

To avoid recomputing them, we store results in a **DP table**:

- `memo[i][t]` = whether it’s possible to form sum `t` using elements from index `i` onward.

This turns the exponential recursion into a **polynomial-time solution**.

```cpp
class Solution {
public:
    vector<vector<int>> memo;
    bool canPartition(vector<int>& nums) {
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        if (sum % 2 != 0) {
            return false;
        }
        memo.resize(nums.size(), vector<int>(sum / 2 + 1, -1));

        return dfs(nums, 0, sum / 2);
    }

    bool dfs(vector<int>& nums, int i, int target) {
        if (i == nums.size()) {
            return target == 0;
        }
        if (target < 0) {
            return false;
        }
        if (memo[i][target] != -1) {
            return memo[i][target];
        }

        memo[i][target] =  dfs(nums, i + 1, target) ||
                           dfs(nums, i + 1, target - nums[i]);
        return memo[i][target];
    }
};
```

**Complexity**

- Time complexity: $O(n * target)$
- Space complexity: $O(n * target)$

> Where $n$ is the length of the array $nums$ and $target$ is the sum of array elements divided by 2.

## 3. Dynamic Programming (Bottom-Up)

This is a classic **0/1 subset sum** DP.

We want to split `nums` into two subsets with equal sum. That’s only possible if:

- `total = sum(nums)` is **even**
- there exists a subset that sums to `target = total / 2`

Instead of trying all subsets (exponential), we build the answer gradually:

- Let `dp[i][j]` mean: using the **first `i` numbers**, can we form sum `j`?

For each number, we have two choices:

- **Skip it** → the possibility stays `dp[i-1][j]`
- **Take it** (only if `nums[i-1] <= j`) → check `dp[i-1][j - nums[i-1]]`

If either is true, then `dp[i][j]` is true.

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        if (sum % 2 != 0) {
            return false;
        }

        int target = sum / 2;
        int n = nums.size();
        vector<vector<bool>> dp(n + 1, vector<bool>(target + 1, false));

        for (int i = 0; i <= n; i++) {
            dp[i][0] = true;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= target; j++) {
                if (nums[i - 1] <= j) {
                    dp[i][j] = dp[i - 1][j] ||
                               dp[i - 1][j - nums[i - 1]];
                } else {
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }

        return dp[n][target];
    }
};
```

**Complexity**

- Time complexity: $O(n * target)$
- Space complexity: $O(n * target)$

> Where $n$ is the length of the array $nums$ and $target$ is the sum of array elements divided by 2.

## 4. Dynamic Programming (Space Optimized)

This is the same **subset sum** idea as before, but optimized to use **1D DP**.

Instead of keeping a full 2D table (`dp[i][j]`), we only track:

- `dp[j]` → whether sum `j` is achievable using numbers processed so far

At each number, we build a new state (`nextDp`) from the previous one:

- Either we **don’t take** the current number → `dp[j]`
- Or we **take** it (if possible) → `dp[j - nums[i]]`

This works because each state only depends on the previous row.

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        if (sum(nums) % 2 != 0) {
            return false;
        }

        int target = sum(nums) / 2;
        vector<bool> dp(target + 1, false);
        vector<bool> nextDp(target + 1, false);

        dp[0] = true;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = 1; j <= target; j++) {
                if (j >= nums[i]) {
                    nextDp[j] = dp[j] || dp[j - nums[i]];
                } else {
                    nextDp[j] = dp[j];
                }
            }
            swap(dp, nextDp);
        }

        return dp[target];
    }

private:
    int sum(vector<int>& nums) {
        int total = 0;
        for (int num : nums) {
            total += num;
        }
        return total;
    }
};
```

**Complexity**

- Time complexity: $O(n * target)$
- Space complexity: $O(target)$

> Where $n$ is the length of the array $nums$ and $target$ is the sum of array elements divided by 2.

## 5. Dynamic Programming (Hash Set)

This approach also solves **Partition Equal Subset Sum**, but instead of arrays, it uses a **Hash Set** to track all achievable sums.

At any point:

- `dp` contains **all subset sums** that can be formed using the processed numbers.

For each new number:

- Every existing sum `t` can either:
    - Stay the same (don’t pick the number)
    - Become `t + num` (pick the number)

If at any time we form `target`, we can stop early and return `True`.

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        if (sum % 2 != 0) {
            return false;
        }

        unordered_set<int> dp;
        dp.insert(0);
        int target = sum / 2;

        for (int i = nums.size() - 1; i >= 0; i--) {
            unordered_set<int> nextDP;
            for (int t : dp) {
                if (t + nums[i] == target) {
                    return true;
                }
                nextDP.insert(t + nums[i]);
                nextDP.insert(t);
            }
            dp = nextDP;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n * target)$
- Space complexity: $O(target)$

> Where $n$ is the length of the array $nums$ and $target$ is the sum of array elements divided by 2.

## 6. Dynamic Programming (Optimal)

This is the **most optimal DP solution** for _Partition Equal Subset Sum_.

We reduce the problem to:

> Can we pick some numbers whose sum equals `target = total_sum / 2`?

We use a **1D DP array** where:

- `dp[j] = True` means we can form sum `j` using some of the numbers so far.

Key idea:

- For each number, update the DP **from right to left** so that each number is used **only once**.
- This avoids overwriting results from the same iteration.

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        if (sum(nums) % 2 != 0) {
            return false;
        }

        int target = sum(nums) / 2;
        vector<bool> dp(target + 1, false);

        dp[0] = true;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = target; j >= nums[i]; j--) {
                dp[j] = dp[j] || dp[j - nums[i]];
            }
        }

        return dp[target];
    }

private:
    int sum(vector<int>& nums) {
        int total = 0;
        for (int num : nums) {
            total += num;
        }
        return total;
    }
};
```

**Complexity**

- Time complexity: $O(n * target)$
- Space complexity: $O(target)$

> Where $n$ is the length of the array $nums$ and $target$ is the sum of array elements divided by 2.

## 7. Dynamic Programming (Bitset)

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        if (sum % 2 != 0) {
            return false;
        }

        int target = sum / 2;
        bitset<10001> dp;
        dp[0] = 1;

        for (int num : nums) {
            dp |= dp << num;
        }

        return dp[target];
    }
};
```

**Complexity**

- Time complexity: $O(n * target)$
- Space complexity: $O(target)$

> Where $n$ is the length of the array $nums$ and $target$ is the sum of array elements divided by 2.

## Standalone solution file (`cpp/0416-partition-equal-subset-sum.cpp` in the NeetCode repo)

```cpp
/*
    Given non-empty, non-negative integer array nums, find if:
    Can be partitionined into 2 subsets such that sums are equal
    Ex. nums = [1,5,11,5] -> true, [1,5,5] & [11], both add to 11

    Maintain DP set, for each num, check if num in set + curr = target
    If not, add curr to every num in set we checked & iterate

    Time: O(n x sum(nums))
    Space: O(sum(nums))
*/

class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int target = 0;
        for (int i = 0; i < nums.size(); i++) {
            target += nums[i];
        }
        if (target % 2 != 0) {
            return false;
        }
        target /= 2;
        
        unordered_set<int> dp;
        dp.insert(0);
        
        for (int i = 0; i < nums.size(); i++) {
            unordered_set<int> dpNext;
            for (auto it = dp.begin(); it != dp.end(); it++) {
                if (*it + nums[i] == target) {
                    return true;
                }
                dpNext.insert(*it + nums[i]);
                dpNext.insert(*it);
            }
            dp = dpNext;
        }
        
        return false;
    }
};
```
