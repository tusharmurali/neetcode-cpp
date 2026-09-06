# 2958. Length of Longest Subarray With at Most K Frequency

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/>  
- **NeetCode:** <https://neetcode.io/problems/length-of-longest-subarray-with-at-most-k-frequency>  
- **Video:** <https://www.youtube.com/watch?v=W_KYZGp2QzU>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most direct approach is to examine every possible subarray and check if it satisfies the frequency constraint. For each starting position, we extend the subarray one element at a time, tracking element frequencies as we go. The moment any element appears more than `k` times, we stop extending and move to the next starting position.

```cpp
class Solution {
public:
    int maxSubarrayLength(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;

        for (int i = 0; i < n; i++) {
            unordered_map<int, int> count;
            for (int j = i; j < n; j++) {
                count[nums[j]]++;
                if (count[nums[j]] > k) {
                    break;
                }
                res = max(res, j - i + 1);
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

Instead of restarting from scratch for each position, we can maintain a sliding window that always represents a valid subarray. When adding an element causes a frequency violation, we shrink the window from the left until the constraint is satisfied again. This way, we only process each element twice at most: once when entering and once when leaving the window.

```cpp
class Solution {
public:
    int maxSubarrayLength(vector<int>& nums, int k) {
        int res = 0;
        unordered_map<int, int> count;
        int l = 0;

        for (int r = 0; r < nums.size(); r++) {
            count[nums[r]]++;
            while (count[nums[r]] > k) {
                count[nums[l]]--;
                l++;
            }
            res = max(res, r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sliding Window (Optimal)

We can optimize further by observing that we only care about finding the maximum window size. Once we find a valid window of size `w`, we never need a smaller one. So instead of shrinking the window completely when invalid, we just slide it: move both left and right pointers by one. The window size either stays the same or grows, never shrinks. This guarantees we find the maximum valid window.

```cpp
class Solution {
public:
    int maxSubarrayLength(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        int l = 0, cnt = 0; // count of numbers with freq > k
        for (int r = 0; r < nums.size(); r++) {
            count[nums[r]]++;
            cnt += count[nums[r]] > k;
            if (cnt > 0) {
                cnt -= count[nums[l]] > k;
                count[nums[l]]--;
                l++;
            }
        }
        return nums.size() - l;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
