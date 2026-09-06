# 349. Intersection of Two Arrays

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/intersection-of-two-arrays/>  
- **NeetCode:** <https://neetcode.io/problems/intersection-of-two-arrays>  
- **Video:** <https://www.youtube.com/watch?v=fwUTXaMom6U>  
- **Video approach:** 5. Hash Set (Optimal) (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to check every element in the first array against every element in the second array. When we find a match, we add it to our result set. Using a set ensures we only include each common element once, even if it appears multiple times in both arrays.

```cpp
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> res;
        for (int i : nums1) {
            for (int j : nums2) {
                if (i == j) {
                    res.insert(i);
                    break;
                }
            }
        }
        return vector<int>(res.begin(), res.end());
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 2. Sorting + Two Pointers

By sorting both arrays, we can use two pointers to efficiently find common elements. We advance the pointer pointing to the smaller element. When both pointers point to equal elements, we found an intersection. We skip duplicates to ensure each element appears only once in the result.

```cpp
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        sort(nums1.begin(), nums1.end());
        sort(nums2.begin(), nums2.end());

        int n = nums1.size(), m = nums2.size();
        vector<int> res;
        int i = 0, j = 0;

        while (i < n && j < m) {
            while (j < m && nums2[j] < nums1[i]) {
                ++j;
            }
            if (j < m) {
                if (nums1[i] == nums2[j]) {
                    res.push_back(nums1[i]);
                }
                ++i;
                while (i < n && nums1[i] == nums1[i - 1]) {
                    ++i;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m \log m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 3. Hash Set

Converting both arrays to sets removes duplicates and enables O(1) lookup. We then iterate through one set and check membership in the other. Any element present in both sets belongs to the intersection.

```cpp
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> set1(nums1.begin(), nums1.end());
        unordered_set<int> set2(nums2.begin(), nums2.end());

        vector<int> res;
        for (int num : set1) {
            if (set2.find(num) != set2.end()) {
                res.push_back(num);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 4. Hash Map

We use a hash map to track which elements from `nums1` we have seen. We mark each element with value `1`. When iterating through `nums2`, if we find a marked element, we add it to the result and set its value to `0` to prevent duplicates.

```cpp
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_map<int, int> seen;
        for (int num : nums1) {
            seen[num] = 1;
        }

        vector<int> res;
        for (int num : nums2) {
            if (seen[num] == 1) {
                seen[num] = 0;
                res.push_back(num);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 5. Hash Set (Optimal) ▶ video

We can improve on the two-set approach by using only one set. Store all elements from `nums1` in a set, then iterate through `nums2`. When we find a match, add it to the result and remove it from the set to avoid duplicates.

```cpp
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> seen(nums1.begin(), nums1.end());
        vector<int> res;

        for (int num : nums2) {
            if (seen.count(num)) {
                res.push_back(num);
                seen.erase(num);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 6. Built-In Functions

Most programming languages provide built-in set intersection operations. By converting both arrays to sets and using the intersection function, we get a clean one-liner solution. The implementation details are handled by the language's standard library.

```cpp
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        set<int> set1(nums1.begin(), nums1.end()), set2(nums2.begin(), nums2.end());
        vector<int> res;
        set_intersection(set1.begin(), set1.end(), set2.begin(), set2.end(), back_inserter(res));
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$ in average case, $O(n * m)$ in worst case.
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.
