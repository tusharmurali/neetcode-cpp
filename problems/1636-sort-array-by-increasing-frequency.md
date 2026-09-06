# 1636. Sort Array by Increasing Frequency

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sort-array-by-increasing-frequency/>  
- **NeetCode:** <https://neetcode.io/problems/sort-array-by-increasing-frequency>  
- **Video:** <https://www.youtube.com/watch?v=Evq1SfUbhBg>  

[← Back to index](../INDEX.md)

## 1. Custom Sort

We need to sort elements by how often they appear, with less frequent elements coming first. When two elements have the same frequency, the larger one should come first. A custom comparator lets us define this two-level sorting logic: primary sort by frequency (ascending), secondary sort by value (descending).

```cpp
class Solution {
public:
    vector<int> frequencySort(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        sort(nums.begin(), nums.end(), [&](int a, int b) {
            if (count[a] != count[b]) return count[a] < count[b];
            return a > b;
        });

        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
