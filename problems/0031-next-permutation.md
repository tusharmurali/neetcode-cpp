# 31. Next Permutation

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/next-permutation/>  
- **NeetCode:** <https://neetcode.io/problems/next-permutation>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach generates all permutations of the array, sorts them in lexicographic order, finds the current permutation in that sorted list, and returns the next one. If we are at the last permutation, we wrap around to the first.

This approach is extremely inefficient for large arrays since the number of permutations is n!, but it demonstrates the concept of what "next permutation" means.

```cpp
class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        auto perms = permute(nums);
        sort(perms.begin(), perms.end());
        for (int i = 0; i < perms.size(); i++) {
            if (perms[i] == nums) {
                auto& next = perms[(i + 1) % perms.size()];
                nums = next;
                return;
            }
        }
    }

private:
    vector<vector<int>> permute(vector<int> nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        vector<int> path;
        vector<bool> used(nums.size(), false);
        function<void()> dfs = [&]() {
            if (path.size() == nums.size()) {
                res.push_back(path);
                return;
            }
            for (int i = 0; i < nums.size(); i++) {
                if (used[i]) continue;
                if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
                used[i] = true;
                path.push_back(nums[i]);
                dfs();
                path.pop_back();
                used[i] = false;
            }
        };
        dfs();
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n! * n)$
- Space complexity: $O(n! * n)$

## 2. Greedy

To find the next lexicographically greater permutation, we need to make the smallest possible change that increases the array's value. The key insight is to find the rightmost position where we can make an increase.

Scan from right to left to find the first element that is smaller than its right neighbor. This element (call it `pivot`) can be swapped with something larger to get a bigger permutation. We then find the smallest element to the right of `pivot` that is still larger than `pivot` and swap them.

After the swap, everything to the right of the `pivot` position is in descending order. To get the smallest possible permutation from this point, we reverse that suffix to ascending order.

If no such `pivot` exists (the array is fully descending), we are at the largest permutation, so we reverse the entire array to get the smallest.

```cpp
class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        int n = nums.size();
        int i = n - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) {
            i--;
        }
        if (i >= 0) {
            int j = n - 1;
            while (nums[j] <= nums[i]) {
                j--;
            }
            swap(nums[i], nums[j]);
        }
        int l = i + 1, r = n - 1;
        while (l < r) {
            swap(nums[l++], nums[r--]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
