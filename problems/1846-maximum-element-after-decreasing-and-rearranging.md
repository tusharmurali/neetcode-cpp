# 1846. Maximum Element After Decreasing and Rearranging

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-element-after-decreasing-and-rearranging>  
- **Video:** <https://www.youtube.com/watch?v=o_hVl8IXuIE>  

[← Back to index](../INDEX.md)

## 1. Greedy + Sorting

The constraints require the first element to be 1 and adjacent elements to differ by at most 1. Since we can only decrease values (not increase), we want to keep values as large as possible while satisfying the constraints. Sorting the array helps because we can then greedily assign each position the best possible value.

After sorting, we process elements left to right. Each element can be at most `previous + 1`. If the current value is larger, we reduce it; if it is smaller, we keep it as is. The final element gives us the maximum achievable value.

```cpp
class Solution {
public:
    int maximumElementAfterDecrementingAndRearranging(vector<int>& arr) {
        sort(arr.begin(), arr.end());
        int prev = 0;
        for (int num : arr) {
            prev = min(prev + 1, num);
        }
        return prev;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Greedy

We can avoid sorting by using counting sort. Since the maximum useful value is `n` (the array length), we count how many elements fall into each value bucket, capping values at `n`. Then we simulate the greedy process: at each target value from `1` to `n`, we have a certain number of elements available. The running count tells us how high we can reach.

This works because having more elements at value `v` means more flexibility to fill positions up to that value. The final running count gives the maximum element achievable.

```cpp
class Solution {
public:
    int maximumElementAfterDecrementingAndRearranging(vector<int>& arr) {
        int n = arr.size();
        vector<int> count(n + 1, 0);

        for (int num : arr) {
            count[min(num, n)]++;
        }

        int prev = 1;
        for (int num = 2; num <= n; num++) {
            prev = min(prev + count[num], num);
        }

        return prev;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
