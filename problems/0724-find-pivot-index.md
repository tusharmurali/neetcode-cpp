# 724. Find Pivot Index

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-pivot-index/>  
- **NeetCode:** <https://neetcode.io/problems/find-pivot-index>  
- **Video:** <https://www.youtube.com/watch?v=u89i60lYx8U>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The pivot index is where the sum of elements to the left equals the sum of elements to the right. The most straightforward approach is to check each index by computing both sums from scratch. For every potential pivot, sum all elements before it and all elements after it, then compare.

```cpp
class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            int leftSum = 0, rightSum = 0;
            for (int l = 0; l < i; l++) {
                leftSum += nums[l];
            }
            for (int r = i + 1; r < n; r++) {
                rightSum += nums[r];
            }
            if (leftSum == rightSum) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix Sum

We can avoid recomputing sums repeatedly by precomputing a prefix sum array. The prefix sum at index `i` represents the sum of all elements from index `0` to `i-1`. With this, the left sum at any index is simply `prefixSum[i]`, and the right sum is `prefixSum[n] - prefixSum[i+1]`. This reduces each lookup to constant time.

```cpp
class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        int n = nums.size();
        vector<int> prefixSum(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }

        for (int i = 0; i < n; i++) {
            int leftSum = prefixSum[i];
            int rightSum = prefixSum[n] - prefixSum[i + 1];
            if (leftSum == rightSum) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Prefix Sum (Optimal)

We can eliminate the need for a separate prefix sum array by maintaining a running left sum and computing the right sum on the fly. First, calculate the total sum of the array. As we iterate, the right sum at any index equals `total - leftSum - nums[i]`. We update `leftSum` after each comparison, keeping space usage constant.

```cpp
class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        int total = 0;
        for (int num : nums) {
            total += num;
        }

        int leftSum = 0;
        for (int i = 0; i < nums.size(); i++) {
            int rightSum = total - leftSum - nums[i];
            if (leftSum == rightSum) {
                return i;
            }
            leftSum += nums[i];
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0724-find-pivot-index.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
  int pivotIndex(vector<int>& nums) {
    int total;
    for(int x: nums){
      total += x;
    }
    
    int leftSum = 0;
    int rightSum;

    for(int i = 0; i < nums.size(); i++){
        rightSum = total - nums[i] - leftSum;

        if(leftSum == rightSum){
            return i;
        }

        leftSum += nums[i];
      }

      return -1;
    }
};
```
