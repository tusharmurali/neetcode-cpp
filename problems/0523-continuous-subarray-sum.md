# 523. Continuous Subarray Sum

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/continuous-subarray-sum/>  
- **NeetCode:** <https://neetcode.io/problems/continuous-subarray-sum>  
- **Video:** <https://www.youtube.com/watch?v=OKcrLfR-8mE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The straightforward approach is to check every possible subarray of size at least 2 and see if its sum is a multiple of `k`. A number is a multiple of `k` if dividing it by `k` leaves no remainder. We iterate through all starting and ending positions to examine every valid subarray.

```cpp
class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) {
        for (int i = 0; i < nums.size() - 1; i++) {
            int sum = nums[i];
            for (int j = i + 1; j < nums.size(); j++) {
                sum += nums[j];
                if (sum % k == 0) return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix Sum + Hash Map

The key insight is based on modular arithmetic. If the prefix sum up to index `i` has remainder `r` when divided by `k`, and the prefix sum up to index `j` also has remainder `r`, then the subarray from `i+1` to `j` has a sum that is a multiple of `k`. This is because `(prefixSum[j] - prefixSum[i]) % k = 0` when both have the same remainder. We use a hash map to store the first index where each remainder was seen.

```cpp
class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> remainder;
        remainder[0] = -1;
        int total = 0;

        for (int i = 0; i < nums.size(); i++) {
            total += nums[i];
            int r = total % k;
            if (remainder.find(r) == remainder.end()) {
                remainder[r] = i;
            } else if (i - remainder[r] > 1) {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(k)$

> Where $n$ is the size of the array $nums$ and $k$ is the number that a subarray sum needs to be multiple of.

## Standalone solution file (`cpp/0523-continuous-subarray-sum.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) {
        unordered_map<int,int>m;
        m[0] = -1;
        int sum = 0;

        for(int i = 0;i < nums.size();i++){
            sum += nums[i];
            if(k != 0){
                sum %= k;
            }

            if(m.count(sum) > 0){
                if(i - m[sum] > 1) return true;
            }
            else{
                m[sum] = i;
            }

        }
        return false;
    }
};
```
