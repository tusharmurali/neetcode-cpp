# 560. Subarray Sum Equals K

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/subarray-sum-equals-k/>  
- **NeetCode:** <https://neetcode.io/problems/subarray-sum-equals-k>  
- **Video:** <https://www.youtube.com/watch?v=fFVZt-6sgyo>  
- **Video approach:** 2. Hash Map  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to consider every possible subarray and check if its sum equals `k`. For each starting index, we extend the subarray element by element, maintaining a running sum. Whenever the sum equals `k`, we count it.

```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        int res = 0;
        for (int i = 0; i < nums.size(); i++) {
            int sum = 0;
            for (int j = i; j < nums.size(); j++) {
                sum += nums[j];
                if (sum == k) res++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Map ▶ video

The key insight is that if `prefixSum[j] - prefixSum[i] = k`, then the subarray from index `i+1` to `j` has sum `k`. This transforms the problem: for each position, we want to count how many earlier positions have a prefix sum equal to `currentPrefixSum - k`. A hash map lets us track prefix sum frequencies as we iterate, giving O(1) lookups.

```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        int res = 0, curSum = 0;
        unordered_map<int, int> prefixSums;
        prefixSums[0] = 1;

        for (int num : nums) {
            curSum += num;
            int diff = curSum - k;
            res += prefixSums[diff];
            prefixSums[curSum]++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0560-subarray-sum-equals-k.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int target) {
        int i=0,j=0,count=0,n=size(nums),sum=0;
        unordered_map<int,int>mp;
        while(j<n){
           sum+=nums[j];
           if(sum==target)count++;
           if(mp.find(sum-target)!=mp.end())count+=mp[sum-target];
           mp[sum]++;
           j++;
       } 
       return count;
    }
};
```
