# 4. Median of Two Sorted Arrays

- **Difficulty:** Hard  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/median-of-two-sorted-arrays/>  
- **NeetCode:** <https://neetcode.io/problems/median-of-two-sorted-arrays>  
- **Video:** <https://www.youtube.com/watch?v=q6IEA26hvXc>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to find the median of two sorted arrays is to **combine them into one array** and then sort it.  
Once everything is merged and sorted, finding the median becomes straightforward:

- If the total number of elements is odd → the middle element is the median.
- If even → the median is the average of the two middle elements.

This method is easy to understand but does not take advantage of the fact that the input arrays are already sorted.

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int len1 = nums1.size();
        int len2 = nums2.size();
        vector<int> merged(len1 + len2);
        copy(nums1.begin(), nums1.end(), merged.begin());
        copy(nums2.begin(), nums2.end(), merged.begin() + len1);
        sort(merged.begin(), merged.end());

        int totalLen = merged.size();
        if (totalLen % 2 == 0) {
            return (merged[totalLen / 2 - 1] + merged[totalLen / 2]) / 2.0;
        } else {
            return merged[totalLen / 2];
        }
    }
};
```

**Complexity**

- Time complexity: $O((n + m)\log (n + m))$
- Space complexity: $O(n + m)$

> Where $n$ is the length of $nums1$ and $m$ is the length of $nums2$.

## 2. Two Pointers

Since both arrays are already sorted, we don't need to fully merge them or sort again.
We can **simulate the merge process** using two pointers—just like in merge sort—but only advance until we reach the middle of the combined array.

Because the median depends only on the middle elements, we do not need to process the entire merged array.
We simply track the last one or two values seen while merging, and once we reach the halfway point, we can compute the median.

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int len1 = nums1.size(), len2 = nums2.size();
        int i = 0, j = 0;
        int median1 = 0, median2 = 0;

        for (int count = 0; count < (len1 + len2) / 2 + 1; count++) {
            median2 = median1;
            if (i < len1 && j < len2) {
                if (nums1[i] > nums2[j]) {
                    median1 = nums2[j];
                    j++;
                } else {
                    median1 = nums1[i];
                    i++;
                }
            } else if (i < len1) {
                median1 = nums1[i];
                i++;
            } else {
                median1 = nums2[j];
                j++;
            }
        }

        if ((len1 + len2) % 2 == 1) {
            return (double) median1;
        } else {
            return (median1 + median2) / 2.0;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ is the length of $nums1$ and $m$ is the length of $nums2$.

## 3. Binary Search

Instead of fully merging the two arrays, think about this question:

> “What is the **k-th smallest** element in the union of two sorted arrays?”

If we can find the k-th smallest element efficiently, then:

- The median is just the middle element (or the average of the two middle elements).

To find the k-th smallest:

- We compare the **k/2-th element** of each array.
- The smaller one (and everything before it in that array) **cannot** be the k-th element,
  because there are at least `k/2` elements smaller than or equal to it.
- So we discard that many elements from one array and **reduce k** accordingly.
- We repeat this process, shrinking the problem each time.

This is like a binary search on k: every step cuts off about half of the remaining elements, giving an `O(log(k))` (or `O(log(m + n))`) solution.

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int left = (nums1.size() + nums2.size() + 1) / 2;
        int right = (nums1.size() + nums2.size() + 2) / 2;
        return (getKth(nums1, nums1.size(), nums2, nums2.size(), left, 0, 0) +
                getKth(nums1, nums1.size(), nums2, nums2.size(), right, 0, 0)) / 2.0;
    }

    int getKth(vector<int>& a, int m, vector<int>& b, int n, int k, int aStart, int bStart) {
        if (m > n) {
            return getKth(b, n, a, m, k, bStart, aStart);
        }
        if (m == 0) {
            return b[bStart + k - 1];
        }
        if (k == 1) {
            return min(a[aStart], b[bStart]);
        }

        int i = min(m, k / 2);
        int j = min(n, k / 2);

        if (a[aStart + i - 1] > b[bStart + j - 1]) {
            return getKth(a, m, b, n - j, k - j, aStart, bStart + j);
        } else {
            return getKth(a, m - i, b, n, k - i, aStart + i, bStart);
        }
    }
};
```

**Complexity**

- Time complexity: $O(\log (m + n))$
- Space complexity: $O(\log (m + n))$ for recursion stack.

> Where $n$ is the length of $nums1$ and $m$ is the length of $nums2$.

## 4. Binary Search (Optimal)

We want the median of two **sorted** arrays without fully merging them.

Think of placing the two arrays side by side and making a **cut** (partition) so that:

- The left side of the cut contains exactly half of the total elements (or half + 1 if odd).
- All elements on the **left side** are `<=` all elements on the **right side**.

If we can find such a partition, then:

- The median must come from the **border elements** around this cut:
    - The largest element on the left side,
    - And the smallest element on the right side.

To find this cut efficiently, we:

- Only binary search on the **smaller array**.
- For a chosen cut in the smaller array, the cut in the larger array is fixed (so total elements on the left is half).
- Check if this partition is valid:
    - `Aleft <= Bright` and `Bleft <= Aright`
- If not valid:
    - Move the cut left or right (like normal binary search) until it becomes valid.

Once we have a valid partition, we compute the median using the max of left side and min of right side.

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        vector<int>& A = nums1;
        vector<int>& B = nums2;
        int total = A.size() + B.size();
        int half = (total + 1) / 2;

        if (B.size() < A.size()) {
            swap(A, B);
        }

        int l = 0;
        int r = A.size();
        while (l <= r) {
            int i = (l + r) / 2;
            int j = half - i;

            int Aleft = i > 0 ? A[i - 1] : INT_MIN;
            int Aright = i < A.size() ? A[i] : INT_MAX;
            int Bleft = j > 0 ? B[j - 1] : INT_MIN;
            int Bright = j < B.size() ? B[j] : INT_MAX;

            if (Aleft <= Bright && Bleft <= Aright) {
                if (total % 2 != 0) {
                    return max(Aleft, Bleft);
                }
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2.0;
            } else if (Aleft > Bright) {
                r = i - 1;
            } else {
                l = i + 1;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log (min(n, m)))$
- Space complexity: $O(1)$

> Where $n$ is the length of $nums1$ and $m$ is the length of $nums2$.

## Standalone solution file (`cpp/0004-median-of-two-sorted-arrays.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 sorted arrays of size m & n, return the median of these arrays
    Ex. nums1 = [1,3] nums2 = [2] -> 2, nums1 = [1,2] nums2 = [3,4] -> 2.5

    Binary search, partition each array until partitions are correct, get median
    [1,2,3,4,5]
    |  a|b    |
    [1,2,3,4,5,6,7,8]    -->    a <= d ? yes, c <= b ? no, so need to fix
    |      c|d      |

    Time: O(log min(m, n))
    Space: O(1)
*/

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int m = nums1.size();
        int n = nums2.size();
        
        if (m > n) {
            return findMedianSortedArrays(nums2, nums1);
        }
        
        int total = m + n;
        
        int low = 0;
        int high = m;
        
        double result = 0.0;
        
        while (low <= high) {
            // nums1
            int i = low + (high - low) / 2;
            // nums2
            int j = (total + 1) / 2 - i;
            
            int left1 = (i > 0) ? nums1[i - 1] : INT_MIN;
            int right1 = (i < m) ? nums1[i] : INT_MAX;
            int left2 = (j > 0) ? nums2[j - 1] : INT_MIN;
            int right2 = (j < n) ? nums2[j] : INT_MAX;
            
            // partition is correct
            if (left1 <= right2 && left2 <= right1) {
                // even
                if (total % 2 == 0) {
                    result = (max(left1, left2) + min(right1, right2)) / 2.0;
                // odd
                } else {
                    result = max(left1, left2);
                }
                break;
            } else if (left1 > right2) {
                high = i - 1;
            } else {
                low = i + 1;
            }
        }
        
        return result;
    }
};
```
