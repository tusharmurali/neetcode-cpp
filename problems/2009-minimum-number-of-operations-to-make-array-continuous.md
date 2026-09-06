# 2009. Minimum Number of Operations to Make Array Continuous

- **Difficulty:** Hard  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-operations-to-make-array-continuous/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-operations-to-make-array-continuous>  
- **Video:** <https://www.youtube.com/watch?v=Dd-yJylrcOY>  

[← Back to index](../INDEX.md)

## 1. Brute Force

An array is continuous if it contains `n` unique elements where the difference between the maximum and minimum is exactly `n - 1`. This means a valid continuous array is just a range of consecutive integers. We can replace any element with any value, so the goal is to keep as many original elements as possible and replace the rest.

For each unique element, we treat it as the potential minimum of our final array. Then we count how many other unique elements fall within the valid range (from that minimum to `minimum + n - 1`). The elements outside this range need to be replaced.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums) {
        int N = nums.size();
        int res = INT_MAX;
        set<int> uniqueNums(nums.begin(), nums.end());
        vector<int> sortedNums(uniqueNums.begin(), uniqueNums.end());
        int n = sortedNums.size();

        for (int i = 0; i < n; i++) {
            int noChange = 1;
            for (int j = i + 1; j < n; j++) {
                if (sortedNums[j] < sortedNums[i] + N) {
                    noChange++;
                }
            }
            res = min(res, N - noChange);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Binary Search

Instead of using a nested loop to count elements in range, we can use binary search. Once the array is sorted, for each starting element, we binary search for the first element that exceeds the valid range. The number of valid elements is the difference between the found position and the starting `index`.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums) {
        int N = nums.size();
        int res = INT_MAX;
        set<int> uniqueNums(nums.begin(), nums.end());
        vector<int> sortedNums(uniqueNums.begin(), uniqueNums.end());
        int n = sortedNums.size();

        for (int i = 0; i < n; i++) {
            int l = i, r = n;
            while (l < r) {
                int mid = l + (r - l) / 2;
                if (sortedNums[mid] < sortedNums[i] + N) {
                    l = mid + 1;
                } else {
                    r = mid;
                }
            }
            int noChange = l - i;
            res = min(res, N - noChange);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Sliding Window

Since the sorted unique elements are in increasing order, we can use a sliding window instead of binary search. As the left pointer moves right, the right pointer only needs to move forward (never backward) because the valid range shifts up. This gives us an efficient two-pointer approach.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums) {
        int length = nums.size();
        set<int> uniqueNums(nums.begin(), nums.end());
        vector<int> sortedNums(uniqueNums.begin(), uniqueNums.end());
        int res = length, r = 0;

        for (int l = 0; l < sortedNums.size(); l++) {
            while (r < sortedNums.size() && sortedNums[r] < sortedNums[l] + length) {
                r++;
            }
            int window = r - l;
            res = min(res, length - window);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Sliding Window (Optimal)

We can optimize space by removing duplicates in-place after sorting. Instead of creating a new array, we overwrite the original array with unique elements. The sliding window logic remains the same, but we avoid allocating extra space for the deduplicated array.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums) {
        int length = nums.size();
        sort(nums.begin(), nums.end());
        int n = 1;

        for (int i = 1; i < length; i++) {
            if (nums[i] != nums[i - 1]) {
                nums[n] = nums[i];
                n++;
            }
        }

        int l = 0;
        for (int r = 0; r < n; r++) {
            if (nums[r] - nums[l] > length - 1) {
                l++;
            }
        }

        return length - (n - l);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.
