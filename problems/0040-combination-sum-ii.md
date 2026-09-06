# 40. Combination Sum II

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/combination-sum-ii/>  
- **NeetCode:** <https://neetcode.io/problems/combination-target-sum-ii>  
- **Video:** <https://www.youtube.com/watch?v=FOyRpNUSFeA>  
- **Video approach:** 4. Backtracking (Optimal)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The brute-force approach tries **every possible subset** of the candidate numbers.

- We sort the array so duplicate combinations appear in the same order.
- At each index, we have two choices:
    1. **Include** the current number.
    2. **Skip** the current number.
- This produces all subsets (like a binary tree of choices).
- Whenever a subset’s sum equals the target, we store it.
- To avoid duplicate combinations, we store each result as a **tuple in a set**.

This method is easy to understand but slow because it explores _all_ subsets, even invalid or duplicate ones.

```cpp
class Solution {
public:
    set<vector<int>> res;

    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        res.clear();
        sort(candidates.begin(), candidates.end());
        vector<int> cur;
        generateSubsets(candidates, target, 0, cur, 0);
        return vector<vector<int>>(res.begin(), res.end());
    }

private:
    void generateSubsets(vector<int>& candidates, int target, int i, vector<int>& cur, int total) {
        if (total == target) {
            res.insert(cur);
            return;
        }
        if (total > target || i == candidates.size()) {
            return;
        }

        cur.push_back(candidates[i]);
        generateSubsets(candidates, target, i + 1, cur, total + candidates[i]);
        cur.pop_back();

        generateSubsets(candidates, target, i + 1, cur, total);
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(n * 2 ^ n)$

## 2. Backtracking

The goal is to choose numbers that sum to the target, but each number can be used **once**, and the list may contain **duplicates**.  
To avoid generating duplicate combinations, we:

1. **Sort the array** so duplicates appear next to each other.
2. Use **backtracking** to explore choices:
    - Take the current number.
    - Skip the current number.
3. When skipping, we **skip all duplicates in one jump** to avoid creating duplicate combinations like `[1,2,2]` multiple times.
4. If the running total exceeds the target, we stop exploring the current path early.

Sorting + skipping duplicates + backtracking ensures we only build valid and unique combinations.

```cpp
class Solution {
public:
    vector<vector<int>> res;
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        res.clear();
        sort(candidates.begin(), candidates.end());
        vector<int> cur;
        dfs(candidates, target, 0, cur, 0);
        return res;
    }

private:
    void dfs(vector<int>& candidates, int target, int i, vector<int>& cur, int total) {
        if (total == target) {
            res.push_back(cur);
            return;
        }
        if (total > target || i == candidates.size()) {
            return;
        }

        cur.push_back(candidates[i]);
        dfs(candidates, target, i + 1, cur, total + candidates[i]);
        cur.pop_back();

        while (i + 1 < candidates.size() && candidates[i] == candidates[i + 1]) {
            i++;
        }
        dfs(candidates, target, i + 1, cur, total);
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^n)$
- Space complexity: $O(n)$

## 3. Backtracking (Hash Map)

Instead of sorting and skipping duplicates, this method uses a **frequency map** that stores how many times each number appears.  
Example:  
If input is `[1,1,2,2,2,3]`, we convert it into:

- Unique list: `[1, 2, 3]`
- Count map: `{1: 2, 2: 3, 3: 1}`

Now each number can be chosen **up to its allowed count**, and we explore combinations using backtracking.  
This avoids duplicates because we never pick the same number more times than it appears.

At each index `i` (pointing to unique numbers):

- **Option 1: Take the number**  
  If its count is still > 0, we include it and reduce the count.
- **Option 2: Skip the number**  
  Move to next index.

We stop exploring a path when:

- `target == 0` → we found a valid combination
- `target < 0` or `i == len(nums)` → invalid path

This ensures we explore all valid combinations while preventing duplicates naturally.

```cpp
class Solution {
public:
    vector<vector<int>> res;
    unordered_map<int, int> count;
    vector<vector<int>> combinationSum2(vector<int>& nums, int target) {
        vector<int> cur;
        vector<int> A;
        for (int num : nums) {
            if (!count[num]) {
                A.push_back(num);
            }
            count[num]++;
        }
        backtrack(A, target, cur, 0);
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

        if (count[nums[i]]) {
            cur.push_back(nums[i]);
            count[nums[i]]--;
            backtrack(nums, target - nums[i], cur, i);
            count[nums[i]]++;
            cur.pop_back();
        }

        backtrack(nums, target, cur, i + 1);
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(n)$

## 4. Backtracking (Optimal) ▶ video

We need all unique combinations where each number can be used **at most once**, and duplicates in the input should not create duplicate combinations.

To handle duplicates safely, we:

1. **Sort the array**
   This groups equal numbers together, which helps us skip duplicates easily.

2. Use **backtracking** where at each index we decide:
    - Take the number
    - Skip the number

3. To avoid duplicate combinations:
    - If `candidates[i] == candidates[i - 1]` and we are still in the same level of recursion (`i > idx`),
      we **skip** that number.

4. We stop early if `current_sum + candidates[i] > target` because the list is sorted.

This approach explores each number only once per combination path and guarantees no repeated results.

```cpp
class Solution {
public:
    vector<vector<int>> res;
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        res.clear();
        sort(candidates.begin(), candidates.end());
        dfs(0, {}, 0, candidates, target);
        return res;
    }

private:
    void dfs(int idx, vector<int> path, int cur, vector<int>& candidates, int target) {
        if (cur == target) {
            res.push_back(path);
            return;
        }
        for (int i = idx; i < candidates.size(); i++) {
            if (i > idx && candidates[i] == candidates[i - 1]) {
                continue;
            }
            if (cur + candidates[i] > target) {
                break;
            }

            path.push_back(candidates[i]);
            dfs(i + 1, path, cur + candidates[i], candidates, target);
            path.pop_back();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0040-combination-sum-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given array & a target, find all unique combos that sum to target, nums can only be used once
    Ex. candidates = [10,1,2,7,6,1,5], target = 8 -> [[1,1,6],[1,2,5],[1,7],[2,6]]

    Backtracking, generate all combo sums, push/pop + index checking to explore new combos

    Time: O(2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        
        vector<int> curr;
        vector<vector<int>> result;
        
        dfs(candidates, target, 0, 0, curr, result);
        return result;
    }
private:
    void dfs(vector<int>& candidates, int target, int sum, int start, vector<int>& curr, vector<vector<int>>& result) {
        if (sum > target) {
            return;
        }
        if (sum == target) {
            result.push_back(curr);
            return;
        }
        for (int i = start; i < candidates.size(); i++) {
            if (i > start && candidates[i] == candidates[i - 1]) {
                continue;
            }
            curr.push_back(candidates[i]);
            dfs(candidates, target, sum + candidates[i], i + 1, curr, result);
            curr.pop_back();
        }
    }
};
```
