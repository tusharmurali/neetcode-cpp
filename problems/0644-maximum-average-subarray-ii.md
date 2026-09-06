# 644. Maximum Average Subarray II

- **Difficulty:** Hard  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-average-subarray-ii/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-average-subarray-ii>  

[← Back to index](../INDEX.md)

## 1. Iterative

We need to find a contiguous subarray of length at least `k` with the maximum average. The brute force approach checks every possible subarray by trying all starting positions and all valid ending positions.

For each starting index, we extend the subarray one element at a time, maintaining a running sum. Once the length reaches `k` or more, we compute the average and update our result if it is larger.

```cpp
class Solution {
public:
    double findMaxAverage(vector<int>& nums, int k) {
        double res = -INFINITY;

        for (int s = 0; s < nums.size() - k + 1; s++) {
            long long sum = 0;
            for (int i = s; i < nums.size(); i++) {
                sum += nums[i];
                if (i - s + 1 >= k)
                    res = max(res, sum * 1.0 / (i - s + 1));
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n^2)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the number of elements in the array `nums`.

## 2. Binary Search

Instead of checking all subarrays, we can binary search on the answer. The key insight is that the maximum average lies between the minimum and maximum values in the array. For a candidate average `mid`, we can efficiently check if there exists a subarray of length at least `k` with average greater than or equal to `mid`.

To check this, we subtract `mid` from each element. Now we need to find a subarray of length at least `k` with non-negative sum. Using prefix sums and tracking the minimum prefix sum before the current window, we can do this in linear time.

```cpp
class Solution {
public:
    double findMaxAverage(vector<int>& nums, int k) {
        double max_val = INT_MIN;
        double min_val = INT_MAX;

        for (int n : nums) {
            max_val = max(max_val, (double)n);
            min_val = min(min_val, (double)n);
        }

        double prev_mid = max_val;
        double error = INT_MAX;

        while (error > 0.00001) {
            double mid = (max_val + min_val) * 0.5;
            if (check(nums, mid, k))
                min_val = mid;
            else
                max_val = mid;
            error = abs(prev_mid - mid);
            prev_mid = mid;
        }

        return min_val;
    }

private:
    bool check(vector<int>& nums, double mid, int k) {
        double sum = 0, prev = 0, min_sum = 0;

        for (int i = 0; i < k; i++)
            sum += nums[i] - mid;

        if (sum >= 0)
            return true;

        for (int i = k; i < nums.size(); i++) {
            sum += nums[i] - mid;
            prev += nums[i - k] - mid;
            min_sum = min(prev, min_sum);
            if (sum >= min_sum)
                return true;
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot \log_2 \frac{(\text{max\_val} - \text{min\_val})}{0.00001})$.
    - The algorithm consists of a binary search loop in the function of `findMaxAverage()`.
    - At each iteration of the loop, the `check()` function dominates the time complexity, which is of $O(N)$ for each invocation.
    - It now boils down to how many iterations the loop would run eventually. To calculate the number of iterations, let us break it down in the following steps.
    - After the first iteration, the error would be $\frac{\text{range}}{2}$, as one can see. Further on, at each iteration, the error would be reduced into half. For example, after the second iteration, we would have the error as $\frac{\text{range}}{2} \cdot \frac{1}{2}$.
    - As a result, after $K$ iterations, the error would become $\text{error} = \text{range} \cdot 2^{-K}$. Given the condition of the loop, i.e. $\text{error} < 0.00001$, we can deduct that $K > \log_2 \frac{\text{range}}{0.00001} = \log_2 \frac{(\text{max\_val} - \text{min\_val})}{0.00001}$.
    - To sum up, the time complexity of the algorithm would be $O(N \cdot K) = O(N \cdot \log_2 \frac{(\text{max\_val} - \text{min\_val})}{0.00001})$.
- Space complexity: $O(1)$ constant space

> Where $N$ is the number of elements in the array, and `range` is the difference between the maximal and minimal values in the array, i.e. `range = max_val - min_val`, and finally `error` is the precision required in the problem.
