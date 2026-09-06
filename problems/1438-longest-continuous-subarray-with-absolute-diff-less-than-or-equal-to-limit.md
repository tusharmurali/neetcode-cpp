# 1438. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/>  
- **NeetCode:** <https://neetcode.io/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit>  
- **Video:** <https://www.youtube.com/watch?v=V-ecDfY5xEw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A subarray is valid if the **difference between its maximum and minimum** is at most `limit`.
Brute force tries every possible starting index `i`, then extends the subarray to the right (`j`) while tracking the current `min` and `max`.
The moment `max - min` becomes greater than `limit`, extending further will only keep it invalid (or worse), so we **break** and move to the next `i`.

```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        int n = nums.size();
        int res = 1;

        for (int i = 0; i < n; i++) {
            int mini = nums[i], maxi = nums[i];
            for (int j = i + 1; j < n; j++) {
                mini = min(mini, nums[j]);
                maxi = max(maxi, nums[j]);
                if (maxi - mini > limit) {
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
- Space complexity: $O(1)$

## 2. Heap

We want to find the longest continuous subarray where the difference between the maximum and minimum elements is less than or equal to the given limit.

A simple way would be to check all subarrays, but that would be too slow. Instead, we can use a **sliding window** approach where we expand the window to the right and shrink it from the left only when the condition becomes invalid.

The key challenge is to **quickly know the maximum and minimum values** in the current window. To handle this efficiently, we use:

- a **max heap** to track the maximum value
- a **min heap** to track the minimum value

Each heap also stores indices so we can remove elements that move out of the window.

```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        priority_queue<pair<int,int>> maxHeap;
        priority_queue<
            pair<int,int>,
            vector<pair<int,int>>,
            greater<pair<int,int>>
        >   minHeap;

        int j = 0, res = 0;
        for (int i = 0; i < (int)nums.size(); ++i) {
            int v = nums[i];
            maxHeap.emplace(v, i);
            minHeap.emplace(v, i);

            while (maxHeap.top().first - minHeap.top().first > limit) {
                ++j;
                while (!maxHeap.empty() && maxHeap.top().second < j)
                    maxHeap.pop();
                while (!minHeap.empty() && minHeap.top().second < j)
                    minHeap.pop();
            }

            res = max(res, i - j + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Sorted Dict

We want the longest continuous subarray where the difference between the maximum and minimum elements is less than or equal to the given limit.

Using a sliding window helps us avoid checking all subarrays. As we expand the window to the right, we need a way to **always know the current minimum and maximum values** inside the window.

To do this efficiently, we use a **sorted data structure** that keeps all elements of the current window in order. This allows us to:

- get the minimum element from the beginning
- get the maximum element from the end

If the difference between these two values becomes greater than the limit, we shrink the window from the left until it becomes valid again.

```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        multiset<int> ms;
        int l = 0, res = 0;
        for (int r = 0; r < nums.size(); r++) {
            ms.insert(nums[r]);
            while (*ms.rbegin() - *ms.begin() > limit) {
                ms.erase(ms.find(nums[l]));
                l++;
            }
            res = max(res, r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Deque - I

We want to find the longest continuous subarray where the difference between the maximum and minimum elements does not exceed the given limit.

A sliding window is a natural choice here, but the main challenge is efficiently tracking the **current minimum and maximum** in the window as it moves.

To solve this, we use **two monotonic deques**:

- a **monotonically increasing deque** to keep track of the minimum values
- a **monotonically decreasing deque** to keep track of the maximum values

These deques are maintained in such a way that their front elements always represent the minimum and maximum of the current window.

```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        deque<int> minQ, maxQ;
        int l = 0, res = 0;
        for (int r = 0; r < nums.size(); r++) {
            while (!minQ.empty() && nums[r] < minQ.back()) {
                minQ.pop_back();
            }
            while (!maxQ.empty() && nums[r] > maxQ.back()) {
                maxQ.pop_back();
            }
            minQ.push_back(nums[r]);
            maxQ.push_back(nums[r]);
            while (maxQ.front() - minQ.front() > limit) {
                if (nums[l] == maxQ.front()) {
                    maxQ.pop_front();
                }
                if (nums[l] == minQ.front()) {
                    minQ.pop_front();
                }
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

## 5. Deque - II

We want the longest continuous subarray where the difference between the maximum and minimum values is at most `limit`.

A sliding window works well because the subarray must be continuous. As we expand the window to the right, we need to always know the **current minimum and maximum** in the window.

To track them efficiently, we maintain two monotonic deques:

- `inc` (increasing deque): keeps possible minimum values in increasing order, so the front is the current minimum
- `dec` (decreasing deque): keeps possible maximum values in decreasing order, so the front is the current maximum

Whenever the window becomes invalid (`max` - `min` > `limit`), we shrink it from the left by moving `j` forward and removing the left element from the deques if it matches their front.

```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        deque<int> inc, dec;
        inc.push_back(nums[0]);
        dec.push_back(nums[0]);
        int res = 1, j = 0, n = nums.size();

        for (int i = 1; i < n; i++) {
            while (!inc.empty() && inc.back() > nums[i]) {
                inc.pop_back();
            }
            while (!dec.empty() && dec.back() < nums[i]) {
                dec.pop_back();
            }

            inc.push_back(nums[i]);
            dec.push_back(nums[i]);
            if (dec.front() - inc.front() > limit) {
                if (dec.front() == nums[j]) {
                    dec.pop_front();
                }
                if (inc.front() == nums[j]) {
                    inc.pop_front();
                }
                j++;
            }
        }

        return n - j;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
