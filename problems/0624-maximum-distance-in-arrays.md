# 624. Maximum Distance in Arrays

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-distance-in-arrays/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-distance-in-arrays>  
- **Video:** <https://www.youtube.com/watch?v=J0yYlj_oVTI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find the maximum absolute difference between elements from two different arrays. The naive approach is to compare every element from every array with every element from every other array. This guarantees we find the answer but is slow due to the nested iteration over all elements.

```cpp
class Solution {
public:
    int maxDistance(std::vector<std::vector<int>>& arrays) {
        int res = 0;
        int n = arrays.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < arrays[i].size(); j++) {
                for (int k = i + 1; k < n; k++) {
                    for (int l = 0; l < arrays[k].size(); l++) {
                        res = std::max(res, std::abs(arrays[i][j] - arrays[k][l]));
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O((n * x)^2)$
- Space complexity: $O(1)$ constant space used

> Where $n$ refers to the number of arrays in $arrays$ and $x$ refers to the average number of elements in each array in $arrays$.

## 2. Better Brute Force

Since each array is sorted, the minimum is always at the start and the maximum is always at the end. This means we only need to consider the first and last elements of each array. For any pair of arrays, the maximum distance is either `|min1 - max2|` or `|min2 - max1|`. This reduces the inner loops to constant time per pair.

```cpp
class Solution {
public:
    int maxDistance(std::vector<std::vector<int>>& arrays) {
        std::vector<int> array1, array2;
        int res = 0;
        int n = arrays.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                array1 = arrays[i];
                array2 = arrays[j];
                res = std::max(res, std::abs(array1[0] - array2[array2.size() - 1]));
                res = std::max(res, std::abs(array2[0] - array1[array1.size() - 1]));
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n^2)$
- Space complexity: $O(1)$ constant space used

> Where $n$ is the number of arrays in $arrays$

## 3. Single Scan

We can do better by making a single pass. As we scan through the arrays, we maintain the global minimum and maximum seen so far. For each new array, the best distance involving this array is either `current_max - global_min` or `global_max - current_min`. After checking, we update our global min and max to include the current array's values.

The key insight is that we compare the current array against all previous arrays implicitly through the running min and max. This guarantees the two elements come from different arrays.

```cpp
class Solution {
public:
    int maxDistance(std::vector<std::vector<int>>& arrays) {
        int res = 0;
        int n = arrays[0].size();
        int min_val = arrays[0][0];
        int max_val = arrays[0][arrays[0].size() - 1];
        for (int i = 1; i < arrays.size(); i++) {
            n = arrays[i].size();
            res = std::max(res, std::max(std::abs(arrays[i][n - 1] - min_val),
                                         std::abs(max_val - arrays[i][0])));
            min_val = std::min(min_val, arrays[i][0]);
            max_val = std::max(max_val, arrays[i][n - 1]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ constant space used

> Where $n$ is the number of arrays in $arrays$
