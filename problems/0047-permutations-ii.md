# 47. Permutations II

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/permutations-ii/>  
- **NeetCode:** <https://neetcode.io/problems/permutations-ii>  
- **Video:** <https://www.youtube.com/watch?v=qhBVWf0YafA>  
- **Video approach:** 2. Backtracking (Hash Map)  

[← Back to index](../INDEX.md)

## 1. Backtracking (Hash Set)

Since the input array may contain duplicates, generating all permutations naively would produce duplicate results. One straightforward way to handle this is to generate all permutations using standard backtracking and store them in a hash set, which automatically filters out duplicates.

We mark elements as "used" by temporarily replacing them with a sentinel value, ensuring each element is used exactly once per permutation.

```cpp
class Solution {
    set<vector<int>> res;
public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        vector<int> perm;
        backtrack(nums, perm);
        return vector<vector<int>>(res.begin(), res.end());
    }

private:
    void backtrack(vector<int>& nums, vector<int>& perm) {
        if (perm.size() == nums.size()) {
            res.insert(perm);
            return;
        }

        for (int i = 0; i < nums.size(); ++i) {
            if (nums[i] != INT_MIN) {
                int temp = nums[i];
                perm.push_back(temp);
                nums[i] = INT_MIN;
                backtrack(nums, perm);
                nums[i] = temp;
                perm.pop_back();
            }
        }

    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the hash set.

## 2. Backtracking (Hash Map) ▶ video

Instead of using a set to filter duplicates after the fact, we can prevent duplicates from being generated in the first place. By counting how many times each unique number appears, we only pick each distinct value once per position in the permutation.

When we decrement a count to zero, that number is no longer available for deeper recursion levels. This naturally avoids generating the same permutation multiple times.

```cpp
class Solution {
    vector<vector<int>> res;
    unordered_map<int, int> count;

public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        for (int& num : nums) {
            count[num]++;
        }
        vector<int> perm;
        dfs(nums, perm);
        return res;
    }

    void dfs(vector<int>& nums, vector<int>& perm) {
        if (perm.size() == nums.size()) {
            res.push_back(perm);
            return;
        }
        for (auto& [num, cnt] : count) {
            if (cnt > 0) {
                perm.push_back(num);
                cnt--;
                dfs(nums, perm);
                cnt++;
                perm.pop_back();
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the output list.

## 3. Backtracking (Boolean Array)

By sorting the array first, duplicate values become adjacent. This allows us to apply a simple rule: when we encounter a duplicate, only use it if the previous identical element has already been used in the current permutation path. This ensures each unique arrangement is generated exactly once.

A boolean array tracks which indices are currently in use during backtracking.

```cpp
class Solution {
    vector<vector<int>> res;
    vector<bool> visit;

public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        visit.assign(nums.size(), false);
        vector<int> perm;
        sort(nums.begin(), nums.end());
        dfs(nums, perm);
        return res;
    }

    void dfs(vector<int>& nums, vector<int>& perm) {
        if (perm.size() == nums.size()) {
            res.push_back(perm);
            return;
        }
        for (int i = 0; i < nums.size(); i++) {
            if (visit[i] || (i > 0 && nums[i] == nums[i - 1] && !visit[i - 1]))
                continue;

            visit[i] = true;
            perm.push_back(nums[i]);
            dfs(nums, perm);
            visit[i] = false;
            perm.pop_back();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the output list.

## 4. Backtracking (Optimal)

This approach generates permutations by swapping elements in place rather than building a separate permutation array. At each position `i`, we try placing each element from index `i` onward. By sorting first and skipping swaps that would place a duplicate value at position `i`, we avoid generating duplicate permutations.

After each recursive call, we restore the array to its sorted state for position `i` by reverse-swapping all elements back.

```cpp
class Solution {
    vector<vector<int>> res;

public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        dfs(0, nums);
        return res;
    }

    void dfs(int i, vector<int>& nums) {
        if (i == nums.size()) {
            res.push_back(nums);
            return;
        }

        for (int j = i; j < nums.size(); ++j) {
            if (j > i && nums[j] == nums[i]) continue;
            swap(nums[i], nums[j]);
            dfs(i + 1, nums);
        }

        for (int j = nums.size() - 1; j > i; --j) {
            swap(nums[i], nums[j]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the output list.

## 5. Iteration

This approach uses the "next permutation" algorithm to iterate through all permutations in lexicographic order. Starting from the smallest permutation (sorted array), we repeatedly find the next lexicographically larger permutation until we cycle back to the beginning.

Since we generate permutations in strict order, duplicates in the input naturally produce unique permutations without extra handling.

```cpp
class Solution {
public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        int n = nums.size();
        sort(nums.begin(), nums.end());
        vector<vector<int>> res = {nums};

        while (true) {
            int i = n - 2;
            while (i >= 0 && nums[i] >= nums[i + 1]) i--;

            if (i < 0) break;

            int j = n - 1;
            while (nums[j] <= nums[i]) j--;

            swap(nums[i], nums[j]);
            reverse(nums.begin() + i + 1, nums.end());
            res.push_back(nums);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$ for the output list.
