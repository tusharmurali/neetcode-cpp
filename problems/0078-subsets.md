# 78. Subsets

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/subsets/>  
- **NeetCode:** <https://neetcode.io/problems/subsets>  
- **Video:** <https://www.youtube.com/watch?v=REOH22Xwdkk>  
- **Video approach:** 1. Backtracking  

[← Back to index](../INDEX.md)

## 1. Backtracking ▶ video

The idea is to build all possible subsets by making a choice at each step:
for every number, we have two options — **include it** or **exclude it**.
This naturally forms a decision tree.

Backtracking helps us explore both choices:

- Add the current number → explore further
- Remove it (undo) → explore without it

Whenever we reach the end of the array, the current list represents one
complete subset, so we store it.

This systematically generates all 2ⁿ subsets.

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> res;
        vector<int> subset;
        dfs(nums, 0, subset, res);
        return res;
    }

private:
    void dfs(const vector<int>& nums, int i, vector<int>& subset, vector<vector<int>>& res) {
        if (i >= nums.size()) {
            res.push_back(subset);
            return;
        }
        subset.push_back(nums[i]);
        dfs(nums, i + 1, subset, res);
        subset.pop_back();
        dfs(nums, i + 1, subset, res);
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(2 ^ n)$ for the output list.

## 2. Iteration

Start with just one subset: the empty set `[]`.

For every number in the array, we take all the subsets we have so far and
create **new subsets by adding the current number to each of them**.

Example:

- Start: `[[]]`
- Add `1` → `[[], [1]]`
- Add `2` → `[[], [1], [2], [1,2]]`
- Add `3` → `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]`

Each step doubles the number of subsets.

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> res = {{}};

        for (int num : nums) {
            int size = res.size();
            for (int i = 0; i < size; i++) {
                vector<int> subset = res[i];
                subset.push_back(num);
                res.push_back(subset);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(2 ^ n)$ for the output list.

## 3. Bit Manipulation

Every subset can be represented using bits.

For an array of length `n`, there are `2^n` possible subsets.
Each subset corresponds to a number from `0` to `2^n - 1`.

Example for `nums = [a, b, c]`:

- `000` → choose nothing → `[]`
- `001` → choose `c`
- `010` → choose `b`
- `011` → choose `b, c`
- `100` → choose `a`
- ...and so on.

Each bit tells us whether to _include_ the corresponding element.

So for every integer `i` from `0` to `(1 << n) - 1`:

- Check each bit `j` of `i`
- If bit `j` is `1`, include `nums[j]` in the current subset.

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> res;
        for (int i = 0; i < (1 << n); i++) {
            vector<int> subset;
            for (int j = 0; j < n; j++) {
                if (i & (1 << j)) {
                    subset.push_back(nums[j]);
                }
            }
            res.push_back(subset);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(2 ^ n)$ for the output list.

## Standalone solution file (`cpp/0078-subsets.cpp` in the NeetCode repo)

```cpp
/*
    Given an integer array of unique elements, return all possible subsets (the power set)
    Ex. nums = [1,2,3] -> [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

    Backtracking, generate all combinations, push/pop + index checking to explore new combos

    Time: O(n x 2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<int> curr;
        vector<vector<int>> result;
        dfs(nums, 0, curr, result);
        return result;
    }
private:
    void dfs(vector<int>& nums, int start, vector<int>& curr, vector<vector<int>>& result) {
        result.push_back(curr);
        for (int i = start; i < nums.size(); i++) {
            curr.push_back(nums[i]);
            dfs(nums, i + 1, curr, result);
            curr.pop_back();
        }
    }
};
```
