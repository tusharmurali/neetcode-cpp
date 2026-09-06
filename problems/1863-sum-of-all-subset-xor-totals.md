# 1863. Sum of All Subsets XOR Total

- **Difficulty:** Easy  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/sum-of-all-subset-xor-totals/>  
- **NeetCode:** <https://neetcode.io/problems/sum-of-all-subset-xor-totals>  
- **Video:** <https://www.youtube.com/watch?v=LI7YR-bwNYY>  

[← Back to index](../INDEX.md)

## 1. Backtracking

We need to generate all possible subsets and compute the XOR total of each. The standard backtracking approach builds subsets by deciding for each element whether to include it or not. At each step, we compute the XOR of the current subset and add it to our running total.

```cpp
class Solution {
public:
    int subsetXORSum(vector<int>& nums) {
        int res = 0;
        vector<int> subset;

        function<void(int)> backtrack = [&](int i) {
            int xorr = 0;
            for (int num : subset) xorr ^= num;
            res += xorr;

            for (int j = i; j < nums.size(); ++j) {
                subset.push_back(nums[j]);
                backtrack(j + 1);
                subset.pop_back();
            }
        };

        backtrack(0);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(n)$

## 2. Recursion

A cleaner recursive approach avoids explicitly building subsets. For each element, we make a binary choice: include it in the XOR or skip it. We pass the running XOR total down the recursion tree. When we reach the end of the array, we return the accumulated XOR value. The sum of all returned values gives us the total.

```cpp
class Solution {
public:
    int subsetXORSum(vector<int>& nums) {
        return dfs(nums, 0, 0);
    }

private:
    int dfs(vector<int>& nums, int i, int total) {
        if (i == nums.size()) {
            return total;
        }
        return dfs(nums, i + 1, total ^ nums[i]) + dfs(nums, i + 1, total);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Bit Manipulation

Every subset can be represented by a bitmask where bit `i` indicates whether element `i` is included. With `n` elements, there are `2^n` subsets corresponding to masks from `0` to `2^n - 1`. We iterate through all masks, compute the XOR of selected elements for each mask, and sum them up.

```cpp
class Solution {
public:
    int subsetXORSum(vector<int>& nums) {
        int n = nums.size();
        int res = 0;

        for (int mask = 0; mask < (1 << n); mask++) {
            int xorr = 0;
            for (int i = 0; i < n; i++) {
                if ((mask & ( 1 << i)) != 0) {
                    xorr ^= nums[i];
                }
            }
            res += xorr;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(1)$ extra space.

## 4. Bit Manipulation (Optimal)

Each bit position in any number contributes independently to the XOR totals. For any bit that is set in at least one number, exactly half of all subsets will have that bit set in their XOR result (because each element either flips the bit or not, and the combinations balance out). The OR of all numbers gives us all bits that appear in at least one element. Each such bit contributes its value multiplied by `2^(n-1)` subsets.

```cpp
class Solution {
public:
    int subsetXORSum(vector<int>& nums) {
        int res = 0;
        for (int& num : nums) {
            res |= num;
        }
        return res << (nums.size() - 1);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
