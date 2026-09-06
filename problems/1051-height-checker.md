# 1051. Height Checker

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/height-checker/>  
- **NeetCode:** <https://neetcode.io/problems/height-checker>  
- **Video:** <https://www.youtube.com/watch?v=mQAoeYaE3Xk>  

[← Back to index](../INDEX.md)

## 1. Sorting

The problem asks us to count how many students are standing in the wrong position compared to where they should be if arranged by height.
If we sort the array, we get the "expected" order.
By comparing each position in the original array with the sorted version, we can count mismatches.

```cpp
class Solution {
public:
    int heightChecker(vector<int>& heights) {
        vector<int> expected = heights;
        sort(expected.begin(), expected.end());

        int res = 0;
        for (int i = 0; i < heights.size(); i++) {
            if (heights[i] != expected[i]) {
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Counting Sort

Since heights are constrained to a small range (`1` to `100`), we can use counting sort for a more efficient solution.
Instead of sorting the entire array, we count how many times each height appears.
Then we reconstruct the expected sorted order by iterating through possible heights and adding each one according to its count.
Finally, we compare the original array with this expected array.

```cpp
class Solution {
public:
    int heightChecker(vector<int>& heights) {
        int count[101] = {};
        for (int h : heights) {
            count[h]++;
        }

        vector<int> expected;
        for (int h = 1; h <= 100; h++) {
            int c = count[h];
            for (int i = 0; i < c; i++) {
                expected.push_back(h);
            }
        }

        int res = 0;
        for (int i = 0; i < heights.size(); i++) {
            if (heights[i] != expected[i]) {
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + k)$
- Space complexity: $O(n + k)$

> Where $n$ is the size of the input array, and $k$ is the range of numbers.
