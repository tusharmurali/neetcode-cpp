# 2971. Find Polygon with the Largest Perimeter

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-polygon-with-the-largest-perimeter/>  
- **NeetCode:** <https://neetcode.io/problems/find-polygon-with-the-largest-perimeter>  
- **Video:** <https://www.youtube.com/watch?v=Yk9Mor-Y488>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A valid polygon requires that the longest side be strictly smaller than the sum of all other sides. We can try each element as the largest side and check if this condition holds. For each candidate, we sum all elements that are less than or equal to it (excluding itself) and verify whether that sum exceeds the candidate. If it does, we have a valid polygon and can compute its perimeter.

```cpp
class Solution {
public:
    long long largestPerimeter(vector<int>& nums) {
        int n = nums.size();
        long long res = -1;

        for (int i = 0; i < n; i++) {
            long long large = nums[i];
            long long cur = 0;

            for (int j = 0; j < n; j++) {
                if (i != j && nums[j] <= large) {
                    cur += nums[j];
                }
            }

            if (cur > large) {
                res = max(res, cur + large);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Sorting

If we sort the array, we can efficiently check the polygon condition. After sorting, as we iterate through each element, all previous elements are smaller or equal. The key insight is that if the running sum of all previous elements exceeds the current element, we have a valid polygon. Since we want the largest perimeter, we keep updating our answer as we find valid configurations, and the last valid one will be the largest.

```cpp
class Solution {
public:
    long long largestPerimeter(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        long long res = -1;
        long long total = 0;

        for (int& num : nums) {
            if (total > num) {
                res = total + num;
            }
            total += num;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Max Heap

Instead of sorting, we can use a max heap to process elements from largest to smallest. We start with the total sum and repeatedly extract the maximum element. If the remaining sum (after removing the max) is greater than the max element, we found the largest valid polygon. Otherwise, we subtract that element from our total and try the next largest. This approach can be faster in practice since we often find the answer before processing all elements.

```cpp
class Solution {
public:
    long long largestPerimeter(vector<int>& nums) {
        priority_queue<int> maxHeap(nums.begin(), nums.end());
        long long total = accumulate(nums.begin(), nums.end(), 0LL);

        while (maxHeap.size() > 2) {
            int largest = maxHeap.top();
            maxHeap.pop();
            total -= largest;
            if (largest < total) {
                return total + largest;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n + (30\log n))$ in Python, C++, JS.
    - $O(n \log n)$ in Java.
- Space complexity: $O(n)$
