# 1838. Frequency of The Most Frequent Element

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/frequency-of-the-most-frequent-element/>  
- **NeetCode:** <https://neetcode.io/problems/frequency-of-the-most-frequent-element>  
- **Video:** <https://www.youtube.com/watch?v=vgBrQ0NM5vE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We can only increment elements, so the target value for our frequent element must already exist in the array. For each element, we check how many smaller elements we can increment to match it using at most `k` operations.

Sorting the array helps because the elements closest in value to our target require the fewest increments. We greedily extend leftward from each position, incrementing elements until we run out of operations.

```cpp
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        int res = 1;

        for (int i = 0; i < nums.size(); i++) {
            int j = i - 1;
            long long tmpK = k;

            while (j >= 0 && (tmpK - (nums[i] - nums[j])) >= 0) {
                tmpK -= (nums[i] - nums[j]);
                j--;
            }
            res = max(res, i - j);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 + n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Prefix Sum + Binary Search

Instead of extending leftward one element at a time, we can use binary search to find the optimal left boundary. The cost to make all elements in a range equal to the rightmost element is: `(count * target) - sum_of_range`. Using prefix sums, we compute range sums in `O(1)`.

For each right boundary `i`, we binary search for the smallest left boundary `m` such that the cost is within budget `k`. The window size `i - m + 1` gives us the frequency.

```cpp
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        vector<long long> prefixSum(n + 1, 0);
        for (int i = 0; i < n; ++i) {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }

        int res = 1;
        for (int i = 0; i < n; ++i) {
            int l = 0, r = i;
            while (l <= r) {
                int m = (l + r) / 2;
                long long curSum = prefixSum[i + 1] - prefixSum[m];
                long long need = (i - m + 1) * 1LL * nums[i] - curSum;
                if (need <= k) {
                    r = m - 1;
                    res = max(res, i - m + 1);
                } else {
                    l = m + 1;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Sliding Window

Since the array is sorted, we can use a sliding window. As we expand the window by moving the right pointer, we add elements and check if the cost to make all elements equal to the rightmost exceeds `k`. If it does, we shrink from the left.

The cost for a window is `target * window_size - window_sum`. When this exceeds `k`, we need a smaller window. The window always represents a valid subarray that can be made uniform within budget.

```cpp
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        long long total = 0;
        int res = 0, l = 0;

        for (int r = 0; r < nums.size(); ++r) {
            total += nums[r];
            while ((long long)nums[r] * (r - l + 1) > total + k) {
                total -= nums[l];
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
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Advanced Sliding Window

We can optimize further by observing that we only care about the maximum window size. Once we find a valid window of size `w`, we never need a smaller window. So instead of shrinking until valid, we can just slide the window forward, maintaining its size when invalid.

If a new element causes the window to become invalid, we remove exactly one element from the left, keeping the window size the same. The window size only grows when we find a valid configuration.

```cpp
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        long long total = 0;
        int l = 0;

        for (int r = 0; r < nums.size(); ++r) {
            total += nums[r];
            if ((r - l + 1) * 1L * nums[r] > total + k) {
                total -= nums[l];
                l++;
            }
        }

        return nums.size() - l;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## Standalone solution file (`cpp/1838-frequency-of-the-most-frequent-element.cpp` in the NeetCode repo)

```cpp

/*
    Time: O(nlogn)
    Space: O(1)
*/
class Solution {
public:
    int maxFrequency(vector<int>& nums, long long k) {
        sort(nums.begin(),nums.end());
        int l=0;
        int r=0;
        int res=0;
        long long total=0;
        int n=nums.size();
        while(r<n){
            total+=nums[r];
            //invalid window

            while((long)(r-l+1)*nums[r] > total+k){
                total-=nums[l];
                l++;
            }
            
            res=max(res,r-l+1);
            r++;
        }
        return res;
    }
};
```
