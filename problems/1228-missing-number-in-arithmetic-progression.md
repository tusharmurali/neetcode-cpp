# 1228. Missing Number In Arithmetic Progression

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/missing-number-in-arithmetic-progression/>  
- **NeetCode:** <https://neetcode.io/problems/missing-number-in-arithmetic-progression>  

[← Back to index](../INDEX.md)

## 1. Linear search

An arithmetic progression has a constant difference between consecutive elements. Since exactly one element is missing, we can compute what the common difference should be using the first and last elements: `difference = (arr[n-1] - arr[0]) / n`. Then we walk through the array, checking if each element matches the expected value. The first mismatch reveals the missing number.

```cpp
class Solution {
public:
    int missingNumber(vector<int> &arr) {
        int n = arr.size();

        // Get the difference `difference`.
        int difference = (arr.back() - arr.front()) / n;

        // The expected element equals the starting element.
        int expected = arr.front();

        for (int &val : arr) {
            // Return the expected value that doesn't match val.
            if (val != expected) return expected;

            // Next element will be expected element + `difference`.
            expected += difference;
        }
        return expected;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the length of array `arr`.

## 2. Binary Search

Since the array is sorted and follows an arithmetic progression, we can use binary search to locate the missing element faster. At any index `i`, the expected value is `arr[0] + i * difference`. If the actual value matches, all elements up to that index are correct, so the missing number is to the right. If there is a mismatch, the missing number is at or before that index. This allows us to narrow down the search space logarithmically.

```cpp
class Solution {
public:
    int missingNumber(vector<int> &arr) {
        int n = arr.size();

        // Get the difference `difference`.
        int difference = (arr.back() - arr.front()) / n;
        int lo = 0;
        int hi = n - 1;

        // Basic binary search template.
        while (lo < hi) {

            int mid = (lo + hi) / 2; // Note: int mid = lo + (hi - lo) / 2; is recommended to avoid potential overflow
            // All numbers upto `mid` have no missing number, so search on the right side.
            if (arr[mid] == arr.front() + mid * difference) {
                lo = mid + 1;
            }

            // A number is missing before `mid` inclusive of `mid` itself.
            else {
                hi = mid;
            }
        }

        // Index `lo` will be the position with the first incorrect number.
        // Return the value that was supposed to be at this index.
        return arr.front() + difference * lo;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the length of array `arr`.
