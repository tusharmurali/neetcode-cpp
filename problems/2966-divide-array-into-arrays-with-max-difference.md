# 2966. Divide Array Into Arrays With Max Difference

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/divide-array-into-arrays-with-max-difference/>  
- **NeetCode:** <https://neetcode.io/problems/divide-array-into-arrays-with-max-difference>  
- **Video:** <https://www.youtube.com/watch?v=XleOio1oJeo>  

[← Back to index](../INDEX.md)

## 1. Sorting

To minimize the difference within each group of three, we should place elements that are close in value together. Sorting the array achieves this naturally. After sorting, we greedily form groups of three consecutive elements. For each group, we only need to check if the difference between the largest and smallest element (first and third in the triplet) is within `k`. If any group fails this check, no valid division exists.

```cpp
class Solution {
public:
    vector<vector<int>> divideArray(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;

        for (int i = 0; i < nums.size(); i += 3) {
            if (nums[i + 2] - nums[i] > k) {
                return {};
            }
            res.push_back({nums[i], nums[i + 1], nums[i + 2]});
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$ for the output array.

## 2. Counting Sort

When the range of values is bounded, counting sort can be faster than comparison-based sorting. We count occurrences of each number, then iterate through possible values in order, building groups of three. As we form each group, we verify that the difference between the smallest and largest element in the group does not exceed `k`.

```cpp
class Solution {
public:
    vector<vector<int>> divideArray(vector<int>& nums, int k) {
        int maxNum = *max_element(nums.begin(), nums.end());
        vector<int> count(maxNum + 1, 0);

        for (int& num : nums) {
            count[num]++;
        }

        vector<vector<int>> res;
        vector<int> group;

        for (int num = 0; num <= maxNum; num++) {
            while (count[num] > 0) {
                group.push_back(num);
                count[num]--;

                if (group.size() == 3) {
                    if (group[2] - group[0] > k) {
                        return {};
                    }
                    res.push_back(group);
                    group.clear();
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in $nums$.
