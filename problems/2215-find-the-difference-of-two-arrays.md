# 2215. Find the Difference of Two Arrays

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-difference-of-two-arrays/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-difference-of-two-arrays>  
- **Video:** <https://www.youtube.com/watch?v=a4wqKR-znBE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check each element in one array against every element in the other array. For each number in `nums1`, we scan through all of `nums2` to see if it exists there. If not found, it belongs in our result. We repeat the same process for `nums2`. Using sets ensures we only include each distinct value once.

```cpp
class Solution {
public:
    vector<vector<int>> findDifference(vector<int>& nums1, vector<int>& nums2) {
        set<int> res1, res2;

        for (int num1 : nums1) {
            bool found = false;
            for (int num2 : nums2) {
                if (num1 == num2) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                res1.insert(num1);
            }
        }

        for (int num2 : nums2) {
            bool found = false;
            for (int num1 : nums1) {
                if (num1 == num2) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                res2.insert(num2);
            }
        }

        return {vector<int>(res1.begin(), res1.end()),
                vector<int>(res2.begin(), res2.end())};
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 2. Sorting

By sorting both arrays, we can efficiently compare elements using a two-pointer technique. After sorting, elements are ordered, so we can walk through both arrays simultaneously. When we find an element in one array that doesn't have a match at the current position in the other, we know it's unique without needing to scan the entire array.

```cpp
class Solution {
public:
    vector<vector<int>> findDifference(vector<int>& nums1, vector<int>& nums2) {
        sort(nums1.begin(), nums1.end());
        sort(nums2.begin(), nums2.end());

        return {helper(nums1, nums2), helper(nums2, nums1)};
    }

private:
    vector<int> helper(vector<int>& A, vector<int>& B) {
        vector<int> res;
        int n = A.size(), m = B.size(), j = 0, prev = INT_MIN;

        for (int num : A) {
            if (num == prev) continue;
            while (j < m && B[j] < num) j++;
            if (j == m || B[j] != num) res.push_back(num);
            prev = num;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m \log m)$
- Space complexity: $O(1)$ or $O(n + m)$ depending on the sorting algorithm.

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 3. Hash Set

Hash sets provide O(1) average lookup time, making them ideal for membership testing. By converting both arrays to sets, we eliminate duplicates and can quickly check whether any element exists in the other array. This avoids the nested loops of the brute force approach.

```cpp
class Solution {
public:
    vector<vector<int>> findDifference(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> num1Set(nums1.begin(), nums1.end());
        unordered_set<int> num2Set(nums2.begin(), nums2.end());
        vector<int> res1, res2;

        for (int num : num1Set) {
            if (num2Set.find(num) == num2Set.end()) res1.push_back(num);
        }

        for (int num : num2Set) {
            if (num1Set.find(num) == num1Set.end()) res2.push_back(num);
        }

        return {res1, res2};
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## 4. Hash Set Difference

Many programming languages provide built-in set difference operations. The set difference A - B returns all elements in A that are not in B. This is exactly what the problem asks for, so we can leverage these optimized library functions for a clean, concise solution.

```cpp
class Solution {
public:
    vector<vector<int>> findDifference(vector<int>& nums1, vector<int>& nums2) {
        vector<int> res1, res2;
        set<int> numSet1(begin(nums1), end(nums1)), numSet2(begin(nums2), end(nums2));

        set_difference(begin(numSet1), end(numSet1), begin(numSet2), end(numSet2), back_inserter(res1));
        set_difference(begin(numSet2), end(numSet2), begin(numSet1), end(numSet1), back_inserter(res2));

        return {res1, res2};
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums1$ and $m$ is the size of the array $nums2$.

## Standalone solution file (`cpp/2215-find-the-difference-of-two-arrays.cpp` in the NeetCode repo)

```cpp
// Time Complexity: O(m + n), we check each element of nums1Set and nums2Set
// Space Complexity: O(m + n), where m and n are length sets in worst case.

class Solution
{
public:
    vector<vector<int>> findDifference(vector<int> &nums1, vector<int> &nums2)
    {
        unordered_set<int> nums1Set(nums1.begin(), nums1.end());
        unordered_set<int> nums2Set(nums2.begin(), nums2.end());

        vector<int> lst1;
        vector<int> lst2;

        for (const auto &num : nums1Set)
        {
            if (nums2Set.find(num) == nums2Set.end())
            {
                lst1.push_back(num);
            }
        }

        for (const auto &num : nums2Set)
        {
            if (nums1Set.find(num) == nums1Set.end())
            {
                lst2.push_back(num);
            }
        }

        return {lst1, lst2};
    }
};
```
