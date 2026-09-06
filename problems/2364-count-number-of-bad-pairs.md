# 2364. Count Number of Bad Pairs

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-number-of-bad-pairs/>  
- **NeetCode:** <https://neetcode.io/problems/count-number-of-bad-pairs>  
- **Video:** <https://www.youtube.com/watch?v=h13Y9sDbQ6w>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A bad pair is defined as `i < j` where `j - i != nums[j] - nums[i]`. We can check every possible pair of indices and count how many satisfy this condition.

```cpp
class Solution {
public:
    long long countBadPairs(vector<int>& nums) {
        int n = nums.size();
        long long res = 0;
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (j - i != nums[j] - nums[i]) {
                    res++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Map

Rearranging the bad pair condition `j - i != nums[j] - nums[i]` gives us `nums[j] - j != nums[i] - i`. This means a pair is "good" when both elements have the same value of `nums[k] - k`. Instead of counting bad pairs directly, we count the total pairs and subtract the good pairs. Elements with the same transformed value form good pairs among themselves.

```cpp
class Solution {
public:
    long long countBadPairs(vector<int>& nums) {
        unordered_map<int, int> count;
        long long total = 0, good = 0;
        for (int i = 0; i < nums.size(); i++) {
            int key = nums[i] - i;
            good += count[key];
            count[key]++;
            total += i;
        }
        return total - good;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
