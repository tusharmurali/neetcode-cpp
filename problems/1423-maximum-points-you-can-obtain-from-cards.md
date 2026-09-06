# 1423. Maximum Points You Can Obtain From Cards

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-points-you-can-obtain-from-cards>  
- **Video:** <https://www.youtube.com/watch?v=TsA4vbtfCvo>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Since we can only take cards from the beginning or end, any valid selection forms two contiguous segments: one from the left and one from the right, totaling `k` cards. We can try all possible splits: take `0` from left and `k` from right, take `1` from left and `k-1` from right, and so on.

```cpp
class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        int n = cardPoints.size();
        int res = 0;

        for (int left = 0; left <= k; left++) {
            int leftSum = 0;
            for (int i = 0; i < left; i++) {
                leftSum += cardPoints[i];
            }

            int rightSum = 0;
            for (int i = n - (k - left); i < n; i++) {
                rightSum += cardPoints[i];
            }

            res = max(res, leftSum + rightSum);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(k ^ 2)$
- Space complexity: $O(1)$ extra space.

> Where $k$ is the number of cards to pick.

## 2. Prefix & Suffix Sums

Instead of recomputing sums for each split, we precompute prefix sums (sums from the left) and suffix sums (sums from the right). Then for any split, we can get the total in constant time by combining the appropriate prefix and suffix values.

```cpp
class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        int n = cardPoints.size();

        vector<int> prefix(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + cardPoints[i];
        }

        vector<int> suffix(n + 1, 0);
        for (int i = n - 1; i >= 0; i--) {
            suffix[i] = suffix[i + 1] + cardPoints[i];
        }

        int res = 0;
        for (int left = 0; left <= k; left++) {
            int right = k - left;
            res = max(res, prefix[left] + suffix[n - right]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sliding Window (Minimum Sum Window)

If we pick `k` cards total from the ends, we leave behind a contiguous subarray of size `n - k` in the middle. Maximizing the sum of picked cards is equivalent to minimizing the sum of the remaining window. We slide a window of size `n - k` across the array and find its minimum sum.

```cpp
class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        int n = cardPoints.size();
        int windowSize = n - k;

        if (windowSize == 0) {
            return accumulate(cardPoints.begin(), cardPoints.end(), 0);
        }

        int total = 0;
        int minWindowSum = INT_MAX;
        int curSum = 0;

        for (int i = 0; i < n; i++) {
            total += cardPoints[i];
            curSum += cardPoints[i];
            if (i >= windowSize - 1) {
                minWindowSum = min(minWindowSum, curSum);
                curSum -= cardPoints[i - windowSize + 1];
            }
        }

        return total - minWindowSum;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Sliding Window

We can directly maintain a sliding window of size `k` that wraps around the array. Start by taking all `k` cards from the right end. Then slide the window: remove one card from the right and add one from the left, tracking the maximum sum as we go.

```cpp
class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        int l = 0, r = cardPoints.size() - k;
        int total = 0;

        for (int i = r; i < cardPoints.size(); i++) {
            total += cardPoints[i];
        }

        int res = total;

        while (r < cardPoints.size()) {
            total += cardPoints[l] - cardPoints[r];
            res = max(res, total);
            l++;
            r++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(k)$
- Space complexity: $O(1)$ extra space.

> Where $k$ is the number of cards to pick.
