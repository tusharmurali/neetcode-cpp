# 39. Combination Sum

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/combination-sum/>  
- **NeetCode:** <https://neetcode.io/problems/combination-target-sum>  
- **Video:** <https://www.youtube.com/watch?v=GBKI9VSKdGg>  
- **Video approach:** 1. Backtracking  

[← Back to index](../INDEX.md)

## 1. Backtracking ▶ video

We want to build all combinations of numbers that add up to the target.  
Each number can be used multiple times, so at every index we have two choices:

1. **Include the current number** - stay at the same index (because we can reuse it).
2. **Skip the current number** - move to the next index.

We explore all possible choices using backtracking.  
Whenever the running total equals the target, we store that combination.  
If the total becomes greater than the target or we run out of numbers, we stop exploring that path.

```cpp
class Solution {
public:
    vector<vector<int>> res;
    vector<vector<int>> combinationSum(vector<int>& nums, int target) {
        vector<int> cur;
        backtrack(nums, target, cur, 0);
        return res;
    }

    void backtrack(vector<int>& nums, int target, vector<int>& cur, int i) {
        if (target == 0) {
            res.push_back(cur);
            return;
        }
        if (target < 0 || i >= nums.size()) {
            return;
        }

        cur.push_back(nums[i]);
        backtrack(nums, target - nums[i], cur, i);
        cur.pop_back();
        backtrack(nums, target, cur, i + 1);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ \frac{t}{m})$
- Space complexity: $O(\frac{t}{m})$

> Where $t$ is the given $target$ and $m$ is the minimum value in $nums$.

## 2. Backtracking (Optimal)

This optimized backtracking solution avoids exploring useless paths by using **sorting + early stopping**.

- We sort the numbers so that once a number makes the sum exceed the target,
  **all numbers after it will also exceed the target** - we can safely stop exploring further (break / return).
- At each position, we try every number starting from index `i`, allowing reuse of the same number.
- We build combinations step-by-step, and whenever the running total equals the target, we record the current list.

Sorting + pruning significantly reduces unnecessary recursion.

```cpp
class Solution {
public:
    vector<vector<int>> res;
    vector<vector<int>> combinationSum(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        dfs(0, {}, 0, nums, target);
        return res;
    }

    void dfs(int i, vector<int> cur, int total, vector<int>& nums, int target) {
        if (total == target) {
            res.push_back(cur);
            return;
        }

        for (int j = i; j < nums.size(); j++) {
            if (total + nums[j] > target) {
                return;
            }
            cur.push_back(nums[j]);
            dfs(j, cur, total + nums[j], nums, target);
            cur.pop_back();
        }
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ \frac{t}{m})$
- Space complexity: $O(\frac{t}{m})$

> Where $t$ is the given $target$ and $m$ is the minimum value in $nums$.

## Standalone solution file (`cpp/0039-combination-sum.cpp` in the NeetCode repo)

```cpp
/*
    Given distinct int array & a target, return list of all unique combos that sum to target
    Ex. candidates = [2,3,6,7] target = 7 -> [[2,2,3],[7]]

    Backtracking, generate all combo sums, push/pop + index checking to explore new combos

    Time: O(2^target)
    Space: O(target)
*/

class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        std::vector<int> curr;
        std::vector<std::vector<int>> res;
        helper(candidates, target, 0, curr, res);
        return res;
    }
private:
    void helper(std::vector<int>& cands, int target, int i, std::vector<int>& curr,  std::vector<std::vector<int>>& res) {
        if (i >= cands.size() || target < 0)
            return;

        if (target == 0) {
            res.push_back(curr);
            return;
        }

        curr.push_back(cands[i]);
        
        helper(cands, target - cands[i], i, curr, res);

        curr.pop_back();

        helper(cands, target, i + 1, curr, res);
    }
};
```
