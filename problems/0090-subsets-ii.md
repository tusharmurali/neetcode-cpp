# 90. Subsets II

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/subsets-ii/>  
- **NeetCode:** <https://neetcode.io/problems/subsets-ii>  
- **Video:** <https://www.youtube.com/watch?v=Vn2v6ajA7U0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

This brute-force method generates **every possible subset** by making a binary choice at each index:

- **Include** the current number, or
- **Skip** the current number.

Since duplicates exist, many generated subsets may look identical.  
To avoid returning duplicates, we:

1. **Sort the array first**, so duplicates are next to each other.
2. **Store each subset as a tuple inside a set**, because:
    - Sets automatically remove duplicates.
    - Tuples are hashable (lists are not).

In the end, we convert the set of tuples back to a list of lists.

```cpp
class Solution {
    set<vector<int>> res;
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        backtrack(nums, 0, {});
        return vector<vector<int>>(res.begin(), res.end());
    }

    void backtrack(vector<int>& nums, int i, vector<int> subset) {
        if (i == nums.size()) {
            res.insert(subset);
            return;
        }

        subset.push_back(nums[i]);
        backtrack(nums, i + 1, subset);
        subset.pop_back();
        backtrack(nums, i + 1, subset);
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^n)$
- Space complexity: $O(2 ^ n)$

## 2. Backtracking - I

We want all subsets, but the array may contain duplicates.
If we blindly generate all subsets, we will produce repeated ones.
So we must **avoid picking the same value in the same decision level** more than once.

Key idea:

- At each index `i`, we make two choices:
    1. **Include** `nums[i]`
    2. **Exclude** `nums[i]`

But when excluding, if the next number is the same (`nums[i] == nums[i+1]`), then skipping it now and skipping it later produce the same subset.
So after exploring the "exclude" branch, we **skip over all duplicate values** to avoid generating duplicate subsets.

We also **sort the array first**, so duplicates become consecutive and easy to skip.

```cpp
class Solution {
    vector<vector<int>> res;
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        backtrack(0, {}, nums);
        return res;
    }

    void backtrack(int i, vector<int> subset, vector<int>& nums) {
        if (i == nums.size()) {
            res.push_back(subset);
            return;
        }

        subset.push_back(nums[i]);
        backtrack(i + 1, subset, nums);
        subset.pop_back();

        while (i + 1 < nums.size() && nums[i] == nums[i + 1]) {
            i++;
        }
        backtrack(i + 1, subset, nums);
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(2 ^ n)$ space for the output list.

## 3. Backtracking - II

We want to generate all subsets, but duplicates in the input can create repeated subsets.
To avoid duplicates cleanly, instead of making "pick / not pick" decisions, this approach builds subsets by **choosing each possible next element**—but **only once per unique value** at each recursion level.

Key idea:

- Sort the array so identical numbers are next to each other.
- At each recursion level, we loop `j` from the current index to the end.
- If `nums[j]` is the same as `nums[j-1]` and `j > i`, we skip it.
  This prevents generating the same subset starting with the same prefix.
- Every time we enter `backtrack`, we push the current subset into `res`.

This ensures:

- Each subset is generated exactly once.
- All valid subsets are included.
- No need for sets or extra data structures.

```cpp
class Solution {
public:
    vector<vector<int>> res;

    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        backtrack(0, {}, nums);
        return res;
    }

    void backtrack(int i, vector<int> subset, vector<int>& nums) {
        res.push_back(subset);
        for (int j = i; j < nums.size(); j++) {
            if (j > i && nums[j] == nums[j - 1]) {
                continue;
            }
            subset.push_back(nums[j]);
            backtrack(j + 1, subset, nums);
            subset.pop_back();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(2 ^ n)$ space for the output list.

## 4. Iteration

This iterative method builds subsets step by step.
Normally, for each new number, we **add it to every existing subset**.
But duplicates cause repeated subsets — so we must avoid recombining duplicates with all previous subsets.

Key idea:

- Sort the array so duplicates are next to each other.
- Maintain two indices:
    - `idx`: start point for generating new subsets.
    - `prev_idx`: end point (previous size of result list before adding this number).
- If the current number is **not a duplicate**, we start from the beginning (`idx = 0`).
- If it **is a duplicate**, we only combine it with subsets created in the **last round**.
  This prevents duplicate subsets from being generated.

Example:
For input `[1,2,2]`

- First `2` extends all subsets.
- Second `2` extends only the subsets added when first `2` was processed → no duplicates.

```cpp
class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res = {{}};
        int prevIdx = 0;
        int idx = 0;

        for (int i = 0; i < nums.size(); i++) {
            idx = (i >= 1 && nums[i] == nums[i - 1]) ? prevIdx : 0;
            prevIdx = res.size();
            for (int j = idx; j < prevIdx; j++) {
                std::vector<int> tmp = res[j];
                tmp.push_back(nums[i]);
                res.push_back(tmp);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(2 ^ n)$ space for the output list.

## Standalone solution file (`cpp/0090-subsets-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given an integer array of unique elements, return all possible subsets (the power set)
    Ex. nums = [1,2,2] -> [[],[1],[1,2],[1,2,2],[2],[2,2]]

    Backtracking, generate all combos, push/pop + to explore new combos, skip duplicates

    Time: O(n x 2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        
        vector<int> curr;
        vector<vector<int>> result;
        
        dfs(nums, 0, curr, result);
        return result;
    }
private:
    void dfs(vector<int>& nums, int start, vector<int>& curr, vector<vector<int>>& result) {
        result.push_back(curr);
        for (int i = start; i < nums.size(); i++) {
            if (i > start && nums[i] == nums[i - 1]) {
                continue;
            }
            curr.push_back(nums[i]);
            dfs(nums, i + 1, curr, result);
            curr.pop_back();
        }
    }
};
```
