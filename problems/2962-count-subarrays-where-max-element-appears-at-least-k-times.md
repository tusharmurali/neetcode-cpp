# 2962. Count Subarrays Where Max Element Appears at Least K Times

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/>  
- **NeetCode:** <https://neetcode.io/problems/count-subarrays-where-max-element-appears-at-least-k-times>  
- **Video:** <https://www.youtube.com/watch?v=CZ-z1ViskzE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to count subarrays where the maximum element of the entire array appears at least `k` times. The simplest approach is to check every possible subarray by trying all starting and ending positions, counting occurrences of the maximum element in each subarray.

```cpp
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {
        int n = nums.size();
        long long res = 0;
        int maxi = *max_element(nums.begin(), nums.end());

        for (int i = 0; i < n; i++) {
            int cnt = 0;
            for (int j = i; j < n; j++) {
                if (nums[j] == maxi) {
                    cnt++;
                }

                if (cnt >= k) {
                    res++;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Variable Size Sliding Window

Instead of checking all subarrays, we can use a sliding window. For each right endpoint, we find the smallest left endpoint such that the window contains exactly `k` occurrences of the max element with the max element at position `l`. All positions from `0` to `l` can serve as left endpoints for valid subarrays ending at `r`.

```cpp
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {
        int maxN = *max_element(nums.begin(), nums.end());
        int maxCnt = 0, l = 0;
        long long res = 0;

        for (int r = 0; r < nums.size(); r++) {
            if (nums[r] == maxN) {
                maxCnt++;
            }

            while (maxCnt > k || (l <= r && maxCnt == k && nums[l] != maxN)) {
                if (nums[l] == maxN) {
                    maxCnt--;
                }
                l++;
            }

            if (maxCnt == k) {
                res += l + 1;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Variable Size Sliding Window (Optimal)

We can simplify the sliding window by counting subarrays with fewer than `k` occurrences and subtracting from total, or equivalently, counting invalid prefixes. For each right endpoint, we maintain a window that has exactly `k` occurrences of the max element, then shrink it until we have fewer than `k`. The left pointer position tells us how many valid subarrays end at this right position.

```cpp
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {
        int max_n = *max_element(nums.begin(), nums.end());
        int max_cnt = 0, l = 0;
        long long res = 0;

        for (int r = 0; r < nums.size(); r++) {
            if (nums[r] == max_n) {
                max_cnt++;
            }
            while (max_cnt == k) {
                if (nums[l] == max_n) {
                    max_cnt--;
                }
                l++;
            }
            res += l;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Fixed Size Sliding Window + Math

We can collect all indices where the max element appears and then use combinatorics. For each window of `k` consecutive max element positions, the number of valid subarrays can be computed by multiplying the number of possible left endpoints (positions before the first max in the window) by the number of possible right endpoints (positions from the last max to the end of the array).

```cpp
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {
        int n = nums.size();
        int max_n = *max_element(nums.begin(), nums.end());
        vector<int> max_indexes = {-1};

        for (int i = 0; i < n; i++) {
            if (nums[i] == max_n) {
                max_indexes.push_back(i);
            }
        }

        long long res = 0;
        for (int i = 1; i <= int(max_indexes.size()) - k; i++) {
            long long cur = (max_indexes[i] - max_indexes[i - 1]);
            cur *= (n - max_indexes[i + k - 1]);
            res += cur;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Fixed Size Sliding Window (Optimal)

We maintain a sliding window containing exactly `k` indices of the max element. As we scan through the array, whenever we encounter the max element, we add its index to a queue. When the queue has more than `k` indices, we remove the oldest one. Whenever we have exactly `k` max element indices in our window, all positions from `0` to the first index in the queue are valid starting points for subarrays ending at the current position.

```cpp
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {
        int maxN = *max_element(nums.begin(), nums.end());
        queue<int> maxIndexes;
        long long res = 0;

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] == maxN) {
                maxIndexes.push(i);
            }

            if (maxIndexes.size() > k) {
                maxIndexes.pop();
            }

            if (maxIndexes.size() == k) {
                res += maxIndexes.front() + 1;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
