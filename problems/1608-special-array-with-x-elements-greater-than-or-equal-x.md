# 1608. Special Array with X Elements Greater than or Equal X

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/special-array-with-x-elements-greater-than-or-equal-x/>  
- **NeetCode:** <https://neetcode.io/problems/special-array-with-x-elements-greater-than-or-equal-x>  
- **Video:** <https://www.youtube.com/watch?v=Z51jYCeBLVI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find a value `x` such that exactly `x` elements in the array are greater than or equal to `x`. The simplest approach is to try every possible value of `x` from `1` to `n` (the array length) and count how many elements satisfy the condition. If we find a match, we return that value. Since `x` must equal the count, `x` cannot exceed `n` (we can have at most `n` elements).

```cpp
class Solution {
public:
    int specialArray(vector<int>& nums) {
        for (int i = 1; i <= nums.size(); i++) {
            int count = 0;
            for (int num : nums) {
                if (num >= i) {
                    count++;
                }
            }
            if (count == i) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Binary Search

Instead of checking every value linearly, we can use binary search on the answer. The key observation is that as `x` increases, the count of elements greater than or equal to `x` decreases (or stays the same). This monotonic property allows us to binary search for the special value. If the count is less than `mid`, we need a smaller `x`. If the count is greater than `mid`, we need a larger `x`.

```cpp
class Solution {
public:
    int specialArray(vector<int>& nums) {
        int l = 1, r = nums.size();
        while (l <= r) {
            int mid = (l + r) / 2;
            int cnt = 0;
            for (int num : nums) {
                if (num >= mid) cnt++;
            }

            if (cnt == mid) return mid;

            if (cnt < mid) {
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$

## 3. Sorting

After sorting the array, we can efficiently determine how many elements are greater than or equal to any value. For each position `i` in the sorted array, there are `n - i` elements from index `i` to the end. We scan through the array and check if `totalRight` (the count of remaining elements) could be the special value. A valid special value must fall within a valid range defined by consecutive distinct elements.

```cpp
class Solution {
public:
    int specialArray(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int i = 0, prev = -1, totalRight = nums.size();

        while (i < nums.size()) {
            if (nums[i] == totalRight ||
               (prev < totalRight && totalRight < nums[i])) {
                return totalRight;
            }

            while (i + 1 < nums.size() && nums[i] == nums[i + 1]) {
                i++;
            }

            prev = nums[i];
            i++;
            totalRight = nums.size() - i;
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Sorting + Two Pointers

After sorting, we use two pointers: one for the candidate value `j` and another for the array index `i`. As we increase `j`, the number of elements greater than or equal to `j` can only decrease. We advance `i` to skip elements smaller than the current candidate and check if the remaining count matches `j`.

```cpp
class Solution {
public:
    int specialArray(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int i = 0, j = 1;

        while (i < n && j <= n) {
            while (i < n && j > nums[i]) i++;

            if (j == n - i) {
                return j;
            }
            j++;
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 5. Counting Sort

We can use a counting array to track how many elements have each value. Since any element greater than n is effectively the same as n for our purposes (they all contribute to counts for candidates 1 through n), we cap values at n. By iterating from the largest possible candidate down to 0 and accumulating counts, we can efficiently find when the running total equals the current index.

```cpp
class Solution {
public:
    int specialArray(vector<int>& nums) {
        vector<int> count(nums.size() + 1, 0);
        for (int num : nums) {
            int index = min(num, (int)nums.size());
            count[index]++;
        }

        int totalRight = 0;
        for (int i = nums.size(); i >= 0; --i) {
            totalRight += count[i];
            if (i == totalRight) {
                return totalRight;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
