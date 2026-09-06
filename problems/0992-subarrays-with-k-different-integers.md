# 992. Subarrays with K Different Integers

- **Difficulty:** Hard  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/subarrays-with-k-different-integers/>  
- **NeetCode:** <https://neetcode.io/problems/subarrays-with-k-different-integers>  
- **Video:** <https://www.youtube.com/watch?v=etI6HqWVa8U>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every possible subarray and count those with exactly `k` distinct integers. For each starting index, we expand the subarray one element at a time, tracking distinct values using a set. Once we exceed `k` distinct values, we stop and move to the next starting position.

```cpp
class Solution {
public:
    int subarraysWithKDistinct(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;

        for (int i = 0; i < n; i++) {
            unordered_set<int> seen;
            for (int j = i; j < n; j++) {
                seen.insert(nums[j]);
                if (seen.size() > k) {
                    break;
                }
                if (seen.size() == k) {
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
- Space complexity: $O(n)$

## 2. Sliding Window

Counting subarrays with exactly `k` distinct values is tricky because adding an element can either increase or maintain the count of distinct values. A clever observation is that we can reframe the problem: subarrays with exactly `k` distinct = subarrays with at most `k` distinct minus subarrays with at most `k-1` distinct. Counting "at most k" is easier using a sliding window that shrinks whenever we exceed `k` distinct values.

```cpp
class Solution {
public:
    int subarraysWithKDistinct(vector<int>& nums, int k) {
        return atMostK(nums, k) - atMostK(nums, k - 1);
    }

private:
    int atMostK(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        int res = 0, l = 0;

        for (int r = 0; r < nums.size(); r++) {
            count[nums[r]]++;
            if (count[nums[r]] == 1) {
                k--;
            }

            while (k < 0) {
                count[nums[l]]--;
                if (count[nums[l]] == 0) {
                    k++;
                }
                l++;
            }

            res += (r - l + 1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sliding Window (One Pass) - I

Instead of computing "at most k" twice, we can count exactly `k` in a single pass by tracking a range of valid left boundaries. For any right pointer position with exactly `k` distinct values, there may be multiple valid starting positions. We maintain two left pointers: `l_far` marks the leftmost valid start, and `l_near` marks the rightmost valid start (where the leftmost element appears exactly once). The count of valid subarrays ending at `r` is `l_near - l_far + 1`.

```cpp
class Solution {
public:
    int subarraysWithKDistinct(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        int res = 0, l_far = 0, l_near = 0;

        for (int r = 0; r < nums.size(); r++) {
            count[nums[r]]++;

            while (count.size() > k) {
                count[nums[l_near]]--;
                if (count[nums[l_near]] == 0) {
                    count.erase(nums[l_near]);
                }
                l_near++;
                l_far = l_near;
            }

            while (count[nums[l_near]] > 1) {
                count[nums[l_near]]--;
                l_near++;
            }

            if (count.size() == k) {
                res += l_near - l_far + 1;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Sliding Window (One Pass) - II

This approach simplifies the previous one by using a single left pointer and a counter `cnt` to track how many positions we can extend the left boundary. When we have exactly `k` distinct values, we shrink the window from the left as long as the leftmost element has duplicates, incrementing `cnt` each time. The number of valid subarrays ending at the current position is `cnt + 1`.

```cpp
class Solution {
public:
    int subarraysWithKDistinct(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> count(n + 1, 0);
        int res = 0, l = 0, cnt = 0;

        for (int r = 0; r < n; r++) {
            count[nums[r]]++;
            if (count[nums[r]] == 1) {
                k--;
            }

            if (k < 0) {
                count[nums[l]]--;
                l++;
                k++;
                cnt = 0;
            }

            if (k == 0) {
                while (count[nums[l]] > 1) {
                    count[nums[l]]--;
                    l++;
                    cnt++;
                }

                res += (cnt + 1);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
