# 238. Product of Array Except Self

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/product-of-array-except-self/>  
- **NeetCode:** <https://neetcode.io/problems/products-of-array-discluding-self>  
- **Video:** <https://www.youtube.com/watch?v=bNvIQI2wAjk>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each position in the array, we can compute the product of all other elements by multiplying every value except the one at the current index.
This directly follows the problem statement and is the most straightforward approach:
**for each index, multiply all elements except itself.**
Although simple, this method is inefficient because it repeats a full pass through the array for every element.

```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n);

        for (int i = 0; i < n; i++) {
            int prod = 1;
            for (int j = 0; j < n; j++) {
                if (i != j) {
                    prod *= nums[j];
                }
            }
            res[i] = prod;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## 2. Division

This approach works by using a simple idea:
If we know the **product of all non-zero numbers**, we can easily compute the answer for each position using division — as long as there are no division-by-zero issues.

So we first check how many zeros the array has:

- If there are **two or more zeros**, then every product will include at least one zero → the entire `res` is all zeros.
- If there is **exactly one zero**, then only the position containing that zero will get the product of all non-zero numbers. All other positions become `0`.
- If there are **no zeros**, we can safely do:
  **result[i] = total_product // nums[i]**

```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int prod = 1, zeroCount = 0;
        for (int num : nums) {
            if (num != 0) {
                prod *= num;
            } else {
                zeroCount++;
            }
        }

        if (zeroCount > 1) {
            return vector<int>(nums.size(), 0);
        }

        vector<int> res(nums.size());
        for (size_t i = 0; i < nums.size(); i++) {
            if (zeroCount > 0) {
                res[i] = (nums[i] == 0) ? prod : 0;
            } else {
                res[i] = prod / nums[i];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## 3. Prefix & Suffix

For each index, we need the product of all elements **before it** and all elements **after it**.
Instead of recomputing the product repeatedly, we can pre-compute two helpful arrays:

- **Prefix product**: `pref[i]` = product of all elements to the left of `i`
- **Suffix product**: `suff[i]` = product of all elements to the right of `i`

Then, the final answer for each index is simply:

**result[i] = pref[i] × suff[i]**

This works because:

- The `pref` handles everything before the index
- The `suff` handles everything after the index

Both pieces together form the product of all numbers except the one at that position.

```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n);
        vector<int> pref(n);
        vector<int> suff(n);

        pref[0] = 1;
        suff[n - 1] = 1;
        for (int i = 1; i < n; i++) {
            pref[i] = nums[i - 1] * pref[i - 1];
        }
        for (int i = n - 2; i >= 0; i--) {
            suff[i] = nums[i + 1] * suff[i + 1];
        }
        for (int i = 0; i < n; i++) {
            res[i] = pref[i] * suff[i];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Prefix & Suffix (Optimal)

We can compute the product of all elements except the current one **without using extra prefix and suffix arrays**.
Instead, we reuse the result array and build the answer in two simple passes:

- In the **first pass**, we fill `res[i]` with the product of all elements to the left of `i` (prefix product).
- In the **second pass**, we multiply each `res[i]` with the product of all elements to the right of `i` (`postfix` product).

By maintaining two running values — `prefix` and `postfix` — we avoid the need for separate `pref` and `suff` arrays.
This gives us the same logic as the previous method, but with **O(1) extra space**.

```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 1);

        for (int i = 1; i < n; i++) {
            res[i] = res[i - 1] * nums[i - 1];
        }

        int postfix = 1;
        for (int i = n - 1; i >= 0; i--) {
            res[i] *= postfix;
            postfix *= nums[i];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## Standalone solution file (`cpp/0238-product-of-array-except-self.cpp` in the NeetCode repo)

```cpp
/*
    Given an integer array nums, return an array such that:
    answer[i] is equal to the product of all elements of nums except nums[i]
    Ex. nums = [1,2,3,4] -> [24,12,8,6], nums = [-1,1,0,-3,3] -> [0,0,9,0,0]

    Calculate prefix products forward, then postfix backwards in a 2nd pass

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, 1);
        
        int prefix = 1;
        for (int i = 0; i < n; i++) {
            result[i] = prefix;
            prefix = prefix * nums[i];
        }
        
        int postfix = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] = result[i] * postfix;
            postfix = postfix * nums[i];
        }
        
        return result;
    }
};
```
