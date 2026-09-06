# 1052. Grumpy Bookstore Owner

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/grumpy-bookstore-owner/>  
- **NeetCode:** <https://neetcode.io/problems/grumpy-bookstore-owner>  
- **Video:** <https://www.youtube.com/watch?v=pXFbNuEIn8Q>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Customers are satisfied when the owner is not grumpy. The owner can use a secret technique to suppress grumpiness for a consecutive window of `minutes`. We want to find the best position for this window to maximize total satisfied customers.

The idea is straightforward: first count all customers who are already satisfied (when grumpy is `0`), then try every possible window position and see how many additional customers we can save by suppressing grumpiness during that window.

```cpp
class Solution {
public:
    int maxSatisfied(vector<int>& customers, vector<int>& grumpy, int minutes) {
        int res = 0, n = customers.size();
        for (int i = 0; i < n; i++) {
            if (grumpy[i] == 0) {
                res += customers[i];
            }
        }

        int satisfied = res;
        for (int i = 0; i <= n - minutes; i++) {
            int cur = 0;
            for (int j = i; j < i + minutes; j++) {
                if (grumpy[j] == 1) {
                    cur += customers[j];
                }
            }
            res = max(res, satisfied + cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$

> Where $n$ is the size of the input array and $m$ is the number of minutes.

## 2. Sliding Window

Instead of recalculating the saved customers for each window position from scratch, we can use a sliding window to efficiently update the count. As the window moves one position to the right, we add the contribution of the new element entering the window and remove the contribution of the element leaving.

This reduces redundant computation since we only need to track customers at grumpy minutes within the current window.

```cpp
class Solution {
public:
    int maxSatisfied(vector<int>& customers, vector<int>& grumpy, int minutes) {
        int l = 0, window = 0, maxWindow = 0, satisfied = 0;

        for (int r = 0; r < customers.size(); r++) {
            if (grumpy[r] == 1) {
                window += customers[r];
            } else {
                satisfied += customers[r];
            }

            if (r - l + 1 > minutes) {
                if (grumpy[l] == 1) {
                    window -= customers[l];
                }
                l++;
            }

            maxWindow = max(window, maxWindow);
        }

        return satisfied + maxWindow;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
