# 41. First Missing Positive

- **Difficulty:** Hard  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/first-missing-positive/>  
- **NeetCode:** <https://neetcode.io/problems/first-missing-positive>  
- **Video:** <https://www.youtube.com/watch?v=8g78yfzMlao>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to find the first missing positive is to just check each positive integer one by one.
We start with `1`, scan the entire array looking for it, and if we find it, move on to `2`, then `3`, and so on.
The first number we can't find in the array is our answer.

This works because we're guaranteed the answer exists somewhere between `1` and `n + 1` (where `n` is the array size). In the worst case, if the array contains exactly `[1, 2, 3, ..., n]`, the answer would be `n + 1`.

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int missing = 1;
        while (true) {
            bool flag = true;
            for (int& num : nums) {
                if (missing == num) {
                    flag = false;
                    break;
                }
            }
            if (flag) return missing;
            missing++;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Boolean Array

Here's a key observation: if the array has `n` elements, the answer must be in the range `[1, n + 1]`.
Why? Because even if the array contains `n` distinct positive integers, they can at most cover `1` through `n`, making `n + 1` the answer.

So we only care about numbers from `1` to `n`. We can create a boolean array of size `n` where `seen[i]` tells us whether `i + 1` exists in the input. Then we just find the first index that's still `false`.

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        vector<bool> seen(n, false);

        for (int num : nums) {
            if (num > 0 && num <= n) {
                seen[num - 1] = true;
            }
        }

        for (int i = 0; i < n; i++) {
            if (!seen[i]) {
                return i + 1;
            }
        }

        return n + 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sorting

If the array is sorted, finding the first missing positive becomes straightforward.
We walk through the sorted array while tracking the smallest positive integer we're looking for.
Whenever we see that number, we increment our target. The first target we don't find is the answer.

We skip negative numbers and zeros since they don't affect our search. Duplicates are also handled naturally since we only increment when we find an exact match.

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int missing = 1;
        for (int num : nums) {
            if (num > 0 && missing == num) {
                missing++;
            }
        }
        return missing;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Negative Marking

Can we achieve O(1) space without sorting? Yes, by using the input array itself as our hash map.

The idea is to use the sign of each element as a flag. If the value at index `i` is negative, it means `i + 1` exists in the array. But there's a catch: the array might already contain negative numbers or zeros, which would interfere with our marking scheme.

So we first convert all non-positive numbers to `0`. Then for each value `v` in the range `[1, n]`, we mark the element at index `v - 1` as negative. If it's already `0`, we use a special marker `-(n + 1)` to indicate presence while keeping it distinguishable.

Finally, the first non-negative index tells us which number is missing.

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();

        for (int i = 0; i < n; i++) {
            if (nums[i] < 0) {
                nums[i] = 0;
            }
        }

        for (int i = 0; i < n; i++) {
            int val = abs(nums[i]);
            if (val >= 1 && val <= n) {
                if (nums[val - 1] > 0) {
                    nums[val - 1] *= -1;
                } else if (nums[val - 1] == 0) {
                    nums[val - 1] = -1 * (n + 1);
                }
            }
        }

        for (int i = 1; i <= n; i++) {
            if (nums[i - 1] >= 0) {
                return i;
            }
        }

        return n + 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 5. Cycle Sort

Another way to use the array as its own hash map is through cycle sort. The goal is to place each number at its "correct" index: value `1` at index `0`, value `2` at index `1`, and so on.

We iterate through the array, and for each element, if it's a valid positive number in range `[1, n]` and not already in its correct position, we swap it to where it belongs. We keep swapping until the current position holds the right value or an out-of-range number.

After this rearrangement, we scan the array. The first position where `nums[i] != i + 1` gives us the missing number.

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        int i = 0;

        while (i < n) {
            if (nums[i] <= 0 || nums[i] > n) {
                i++;
                continue;
            }
            int index = nums[i] - 1;
            if (nums[i] != nums[index]) {
                swap(nums[i], nums[index]);
            } else {
                i++;
            }
        }

        for (i = 0; i < n; i++) {
            if (nums[i] != i + 1) {
                return i + 1;
            }
        }

        return n + 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0041-first-missing-positive.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        for(int i=0; i<nums.size(); i++){
            if(i+1==nums[i]) continue;
            int x = nums[i];
            while(x>=1 && x<=nums.size() && x!=nums[x-1]){
                swap(x, nums[x-1]);
            }
        }
        for(int i=0; i<nums.size(); i++){
            if(i+1!=nums[i])    return i+1;
        }
        return nums.size()+1;
    }
};
```
