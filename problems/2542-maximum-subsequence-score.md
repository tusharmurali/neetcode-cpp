# 2542. Maximum Subsequence Score

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-subsequence-score/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-subsequence-score>  
- **Video:** <https://www.youtube.com/watch?v=ax1DKi5lJwk>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Recursion)

We need to select exactly `k` indices. The score is the sum of selected elements from `nums1` multiplied by the minimum of selected elements from `nums2`. Since we must choose exactly `k` elements, we can use recursion to try all combinations: for each index, either include it or skip it. When we include an element, we update the running sum and track the minimum from `nums2`.

```cpp
class Solution {
private:
    vector<int> nums1, nums2;
    int n;

public:
    long long maxScore(vector<int>& nums1, vector<int>& nums2, int k) {
        this->nums1 = nums1;
        this->nums2 = nums2;
        this->n = nums1.size();
        return dfs(0, k, INT_MAX, 0);
    }

private:
    long long dfs(int i, int k, int minVal, long long curSum) {
        if (k == 0) {
            return curSum * minVal;
        }
        if (i == n || (n - i) < k) {
            return INT_MIN;
        }
        if (minVal == 0) {
            return 0;
        }

        long long res = dfs(i + 1, k, minVal, curSum);
        res = max(res, dfs(i + 1, k - 1, min(minVal, nums2[i]), curSum + nums1[i]));
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Min-Heap - I

The key insight is that if we fix which element provides the minimum from `nums2`, we want the `k` largest corresponding values from `nums1` (among elements with `nums2` values >= our minimum). By sorting pairs by `nums2` in descending order and processing them one by one, each new element becomes the new minimum. We maintain the `k` largest `nums1` values seen so far using a min-heap.

```cpp
class Solution {
public:
    long long maxScore(vector<int>& nums1, vector<int>& nums2, int k) {
        int n = nums1.size();
        vector<pair<int, int>> pairs(n);

        for (int i = 0; i < n; i++) {
            pairs[i] = {nums1[i], nums2[i]};
        }

        sort(pairs.begin(), pairs.end(), [](const auto& a, const auto& b) {
            return b.second < a.second;
        });

        priority_queue<int, vector<int>, greater<int>> minHeap;
        long long n1Sum = 0, res = 0;

        for (auto& pair : pairs) {
            n1Sum += pair.first;
            minHeap.push(pair.first);

            if (minHeap.size() > k) {
                n1Sum -= minHeap.top();
                minHeap.pop();
            }

            if (minHeap.size() == k) {
                res = max(res, n1Sum * (long long)pair.second);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Min-Heap - II

This is a space-optimized version that packs both values into a single 64-bit integer. Since the problem constraints allow values up to `10^5`, we can use bit shifting to combine `nums2` (upper bits) and `nums1` (lower bits). Sorting these combined values gives us the same ordering as sorting by `nums2`, and we can extract both values using bitwise operations.

```cpp
class Solution {
public:
    long long maxScore(vector<int>& nums1, vector<int>& nums2, int k) {
        int n = nums1.size();
        vector<long long> arr(n);
        for (int i = 0; i < n; i++) {
            arr[i] = ((long long) nums2[i] << 30) | nums1[i];
        }

        sort(arr.rbegin(), arr.rend());
        priority_queue<int, vector<int>, greater<int>> minHeap;
        long long n1Sum = 0, res = 0;

        for (long long& num : arr) {
            int n1 = num & ((1LL << 30) - 1);
            int n2 = num >> 30;
            n1Sum += n1;
            minHeap.push(n1);

            if (minHeap.size() > k) {
                n1Sum -= minHeap.top();
                minHeap.pop();
            }
            if (minHeap.size() == k) {
                res = max(res, n1Sum * (long long)n2);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/2542-maximum-subsequence-score.cpp` in the NeetCode repo)

```cpp
// Time: O(NlogN)
// Space: O(N)

class Solution {
public:
    long long maxScore(vector<int>& nums1, vector<int>& nums2, int k) {
        int size = nums1.size();
        vector<pair<int, int>> pairs(size);

        // populating the array
        for(int i = 0; i < size; i++) {
            pairs.push_back(make_pair(nums1[i], nums2[i]));
        }
        
        // sorting the array using comparator lambda function
        sort(pairs.begin(), pairs.end(), [](pair<int, int> a, pair<int, int> b) {
            return (a.second > b.second);
        });

        priority_queue<int, vector<int>, greater<int>> minh;
        long long currSum = 0;
        long long maxSum = INT_MIN;

        for(int i = 0; i < size; i++) {
            currSum += pairs[i].first;
            minh.push(pairs[i].first);

            if(minh.size() > k) {
                currSum -= minh.top();
                minh.pop();
            }
            if(minh.size() == k) {
                maxSum = max(maxSum, (currSum * pairs[i].second));
            }
        }
        return maxSum;
    }
};
```
