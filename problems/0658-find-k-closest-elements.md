# 658. Find K Closest Elements

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/find-k-closest-elements/>  
- **NeetCode:** <https://neetcode.io/problems/find-k-closest-elements>  
- **Video:** <https://www.youtube.com/watch?v=o-YDQzHoaKM>  

[← Back to index](../INDEX.md)

## 1. Sorting (Custom Comparator)

The problem asks for the `k` elements closest to `x`. A straightforward approach is to sort all elements by their distance to `x`. If two elements have the same distance, we prefer the smaller one. After sorting, we simply take the first `k` elements and return them in sorted order.

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        sort(arr.begin(), arr.end(), [x](int a, int b) {
            int diff = abs(a - x) - abs(b - x);
            return diff == 0 ? a < b : diff < 0;
        });
        vector<int> result(arr.begin(), arr.begin() + k);
        sort(result.begin(), result.end());
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + k \log k)$
- Space complexity:
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.
    - $O(k)$ space for the output array.

> Where $n$ is the size of the input array and $k$ is the number of closest elements to find.

## 2. Linear Scan + Two Pointers

Since we need elements closest to `x`, we can first find the element nearest to `x` using a linear scan. Once we have this starting point, we expand outward using two pointers, picking the closer element at each step until we have `k` elements.

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int n = arr.size();
        int idx = 0;
        for (int i = 1; i < n; i++) {
            if (abs(x - arr[idx]) > abs(x - arr[i])) {
                idx = i;
            }
        }

        vector<int> res = {arr[idx]};
        int l = idx - 1, r = idx + 1;

        while (res.size() < k) {
            if (l >= 0 && r < n) {
                if (abs(x - arr[l]) <= abs(x - arr[r])) {
                    res.push_back(arr[l--]);
                } else {
                    res.push_back(arr[r++]);
                }
            } else if (l >= 0) {
                res.push_back(arr[l--]);
            } else if (r < n) {
                res.push_back(arr[r++]);
            }
        }

        sort(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + k \log k)$
- Space complexity:
    - $O(1)$ or $O(k)$ space depending on the sorting algorithm.
    - $O(k)$ space for the output array.

> Where $n$ is the size of the input array and $k$ is the number of closest elements to find.

## 3. Two Pointers

Since the array is already sorted, the `k` closest elements must form a contiguous subarray. We can use two pointers starting at the ends of the array and shrink the window by removing the element that is farther from `x` until only `k` elements remain.

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int l = 0, r = arr.size() - 1;
        while (r - l >= k) {
            if (abs(x - arr[l]) <= abs(x - arr[r])) {
                r--;
            } else {
                l++;
            }
        }
        return vector<int>(arr.begin() + l, arr.begin() + r + 1);
    }
};
```

**Complexity**

- Time complexity: $O(n - k)$
- Space complexity: $O(k)$ for the output array.

> Where $n$ is the size of the input array and $k$ is the number of closest elements to find.

## 4. Binary Search + Two Pointers

Instead of scanning linearly to find the starting point, we can use binary search to quickly locate where `x` would fit in the sorted array. From that position, we expand outward with two pointers to collect `k` closest elements.

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int l = 0, r = arr.size() - 1;
        while (l < r) {
            int mid = (l + r) / 2;
            if (arr[mid] < x) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }

        l = l - 1;
        r = l + 1;
        while (r - l - 1 < k) {
            if (l < 0) {
                r++;
            } else if (r >= arr.size()) {
                l--;
            } else if (abs(arr[l] - x) <= abs(arr[r] - x)) {
                l--;
            } else {
                r++;
            }
        }

        return vector<int>(arr.begin() + l + 1, arr.begin() + r);
    }
};
```

**Complexity**

- Time complexity: $O(\log n + k)$
- Space complexity: $O(k)$ for the output array.

> Where $n$ is the size of the input array and $k$ is the number of closest elements to find.

## 5. Binary Search

We can binary search directly for the starting index of the `k`-length window. For any starting index `m`, we compare the distances of `arr[m]` and `arr[m + k]` to `x`. If `arr[m + k]` is closer, the window should shift right; otherwise, it should stay or shift left. This narrows down the optimal starting position.

```cpp
class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int l = 0, r = arr.size() - k;
        while (l < r) {
            int m = (l + r) / 2;
            if (x - arr[m] > arr[m + k] - x) {
                l = m + 1;
            } else {
                r = m;
            }
        }
        return vector<int>(arr.begin() + l, arr.begin() + l + k);
    }
};
```

**Complexity**

- Time complexity: $O(\log (n - k) + k)$
- Space complexity: $O(k)$ for the output array.

> Where $n$ is the size of the input array and $k$ is the number of closest elements to find.
