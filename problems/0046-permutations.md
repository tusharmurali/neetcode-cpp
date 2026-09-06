# 46. Permutations

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/permutations/>  
- **NeetCode:** <https://neetcode.io/problems/permutations>  
- **Video:** <https://www.youtube.com/watch?v=FZe0UqISmUw>  
- **Video approach:** 1. Recursion  

[← Back to index](../INDEX.md)

## 1. Recursion ▶ video

The idea is to generate permutations by **building them from smaller permutations**.

- If the list is empty → the only permutation is `[]`.
- Otherwise:
    1. Take the first number of the list.
    2. Recursively get all permutations of the remaining numbers.
    3. For each smaller permutation, insert the first number into **every possible position**.
        - Example:
          If smaller permutation = `[2,3]` and new number = `1`,
          we create: `[1,2,3]`, `[2,1,3]`, `[2,3,1]`.

This works because inserting the new number in all positions ensures we build all unique permutations.

```cpp
class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        if (nums.empty()) {
            return {{}};
        }

        vector<int> tmp = vector<int>(nums.begin() + 1, nums.end());
        vector<vector<int>> perms = permute(tmp);
        vector<vector<int>> res;
        for (const auto& p : perms) {
            for (int i = 0; i <= p.size(); i++) {
                vector<int> p_copy = p;
                p_copy.insert(p_copy.begin() + i, nums[0]);
                res.push_back(p_copy);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n! * n ^ 2)$
- Space complexity: $O(n! * n)$ for the output list.

## 2. Iteration

We build permutations step-by-step using **iteration instead of recursion**.

Start with one empty permutation: `[]`.

For each number in `nums`, we take all existing permutations and **insert the new number into every possible position**.

Example building process for `[1,2,3]`:

- Start: `[]`
- Insert `1` → `[1]`
- Insert `2` into every position of `[1]` → `[2,1]`, `[1,2]`
- Insert `3` into every position of each permutation:
    - For `[2,1]` → `[3,2,1]`, `[2,3,1]`, `[2,1,3]`
    - For `[1,2]` → `[3,1,2]`, `[1,3,2]`, `[1,2,3]`

By inserting each number in all positions of all existing permutations, we generate all possible permutations.

```cpp
class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> perms = {{}};
        for (int num : nums) {
            vector<vector<int>> new_perms;
            for (const auto& p : perms) {
                for (int i = 0; i <= p.size(); i++) {
                    vector<int> p_copy = p;
                    p_copy.insert(p_copy.begin() + i, num);
                    new_perms.push_back(p_copy);
                }
            }
            perms = new_perms;
        }
        return perms;
    }
};
```

**Complexity**

- Time complexity: $O(n! * n ^ 2)$
- Space complexity: $O(n! * n)$ for the output list.

## 3. Backtracking

Backtracking builds permutations by **choosing numbers one-by-one** and exploring all possible orders.

At every step:

- We pick a number that has not been used yet.
- Add it to the current permutation.
- Recursively continue building.
- When we reach a full permutation (length == len(nums)), we save it.
- Then we **undo the last choice** (backtrack) and try a different number.

We use a `pick` array to mark which elements are already used, ensuring each number appears only once per permutation.

This method explores a decision tree where each level chooses the next number until all numbers are used.

```cpp
class Solution {
    vector<vector<int>> res;
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<bool> pick(nums.size(), false);
        vector<int> perm;
        backtrack(perm, nums, pick);
        return res;
    }

    void backtrack(vector<int>& perm, vector<int>& nums, vector<bool>& pick) {
        if (perm.size() == nums.size()) {
            res.push_back(perm);
            return;
        }
        for (int i = 0; i < nums.size(); i++) {
            if (!pick[i]) {
                perm.push_back(nums[i]);
                pick[i] = true;
                backtrack(perm, nums, pick);
                perm.pop_back();
                pick[i] = false;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the output list.

## 4. Backtracking (Bit Mask)

We want to generate all permutations, but instead of using a boolean `pick` array,
we use a **bitmask** (`mask`) to track which elements in `nums` have been used.

- Each bit in `mask` represents whether an index `i` is used.
- Example with 4 numbers:
    - `mask = 0101` means indices 0 and 2 are already chosen.
- This makes checking usage extremely fast using:
    - `(mask & (1 << i))` → checks if index `i` is used.
    - `(mask | (1 << i))` → marks index `i` as used for the next recursive call.

We build permutations by trying every unused index at each step until we've chosen all numbers.

```cpp
class Solution {
public:
    vector<vector<int>> res;

    vector<vector<int>> permute(vector<int>& nums) {
        backtrack({}, nums, 0);
        return res;
    }

    void backtrack(vector<int> perm, vector<int>& nums, int mask) {
        if (perm.size() == nums.size()) {
            res.push_back(perm);
            return;
        }
        for (int i = 0; i < nums.size(); i++) {
            if (!(mask & (1 << i))) {
                perm.push_back(nums[i]);
                backtrack(perm, nums, mask | (1 << i));
                perm.pop_back();
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the output list.

## 5. Backtracking (Optimal)

This approach generates permutations **in-place** by swapping elements.

Instead of creating new lists or tracking visited elements, we treat the array as divided into:

- **Fixed prefix** (positions `0` to `idx - 1`)
- **Free suffix** (positions `idx` to end)

At each step:

1. We choose which element should go into position `idx`.
2. We do this by swapping every element `i ≥ idx` with `idx`.
3. After placing a number at position `idx`, we recursively fill the next index.
4. When recursion returns, we **swap back** to restore the original list (backtracking).

This gives all permutations efficiently and uses **O(1) extra space** (besides recursion).

```cpp
class Solution {
    vector<vector<int>> res;
public:
    vector<vector<int>> permute(vector<int>& nums) {
        backtrack(nums, 0);
        return res;
    }

    void backtrack(vector<int>& nums, int idx) {
        if (idx == nums.size()) {
            res.push_back(nums);
            return;
        }
        for (int i = idx; i < nums.size(); i++) {
            swap(nums[idx], nums[i]);
            backtrack(nums, idx + 1);
            swap(nums[idx], nums[i]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the output list.

## Standalone solution file (`cpp/0046-permutations.cpp` in the NeetCode repo)

```cpp
/*
    Given array of distinct integers, return all the possible permutations
    Ex. nums = [1,2,3] -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

    Permute by swapping i/start, DFS from this point, backtrack to undo swap

    Time: O(n x n!)
    Space: O(n!)
*/

class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> result;
        dfs(nums, 0, result);
        return result;
    }
private:
    void dfs(vector<int>& nums, int start, vector<vector<int>>& result) {
        if (start == nums.size()) {
            result.push_back(nums);
            return;
        }
        for (int i = start; i < nums.size(); i++) {
            swap(nums[i], nums[start]);
            dfs(nums, start + 1, result);
            swap(nums[i], nums[start]);
        }
    }
};
```
