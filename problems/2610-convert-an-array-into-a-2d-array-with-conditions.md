# 2610. Convert an Array Into a 2D Array With Conditions

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/convert-an-array-into-a-2d-array-with-conditions/>  
- **NeetCode:** <https://neetcode.io/problems/convert-an-array-into-a-2d-array-with-conditions>  
- **Video:** <https://www.youtube.com/watch?v=9pl1QiaGgmI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to distribute numbers into rows such that each row contains only distinct elements. For each number, we find the first row where it doesn't already exist and place it there. If no such row exists, we create a new row. This greedy placement ensures we use the minimum number of rows needed.

```cpp
class Solution {
public:
    vector<vector<int>> findMatrix(vector<int>& nums) {
        vector<vector<int>> res;

        for (int num : nums) {
            int r = 0;
            while (r < res.size()) {
                if (find(res[r].begin(), res[r].end(), num) == res[r].end()) {
                    break;
                }
                r++;
            }
            if (r == res.size()) {
                res.push_back({});
            }
            res[r].push_back(num);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$ for the output array.

> Where $n$ is the size of the array $nums$ and $m$ is the frequency of the most frequent element in the given array.

## 2. Sorting

By sorting the array first, all identical numbers become adjacent. This allows us to process each group of duplicates together. The number of rows needed equals the maximum frequency of any element, and by distributing each group of identical elements across consecutive rows starting from row `0`, we ensure each row has distinct values.

```cpp
class Solution {
public:
    vector<vector<int>> findMatrix(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;

        int i = 0;
        while (i < nums.size()) {
            int j = i, r = 0;
            while (j < nums.size() && nums[i] == nums[j]) {
                if (r == res.size()) {
                    res.push_back({});
                }
                res[r].push_back(nums[i]);
                r++;
                j++;
            }
            i = j;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$ for the output array.

## 3. Frequency Count

The frequency of each number tells us exactly which row it should go into. The first occurrence goes to row `0`, the second occurrence to row `1`, and so on. By tracking how many times we've seen each number, we can directly place it in the correct row without searching. This eliminates the need for both sorting and linear searching.

```cpp
class Solution {
public:
    vector<vector<int>> findMatrix(vector<int>& nums) {
        unordered_map<int, int> count;
        vector<vector<int>> res;

        for (int num : nums) {
            int row = count[num];
            if (res.size() == row) {
                res.push_back({});
            }
            res[row].push_back(num);
            count[num]++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
