# 209. Minimum Size Subarray Sum

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/minimum-size-subarray-sum/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-size-subarray-sum>  
- **Video:** <https://www.youtube.com/watch?v=aYqYMIqZx5s>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every possible subarray. For each starting index, we expand the subarray until the sum reaches or exceeds the target, then record the length. Since all numbers are positive, once we hit the target we can stop expanding from that starting point.

```cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int n = nums.size();
        int res =  INT_MAX;

        for (int i = 0; i < n; i++) {
            int curSum = 0, j = i;
            while (j < n) {
                curSum += nums[j];
                if (curSum >= target) {
                    res = min(res, j - i + 1);
                    break;
                }
                j++;
            }
        }

        return res == INT_MAX ? 0 : res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Sliding Window

Since all elements are positive, we can use a sliding window approach. We expand the window by moving the right pointer to increase the sum. Once the sum meets or exceeds the target, we try to shrink the window from the left to find the minimum length. This works because removing elements from the left will only decrease the sum, and we want the smallest window that still satisfies the condition.

```cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int l = 0, total = 0, res = INT_MAX;

        for (int r = 0; r < nums.size(); r++) {
            total += nums[r];
            while (total >= target) {
                res = min(r - l + 1, res);
                total -= nums[l];
                l++;
            }
        }

        return res == INT_MAX ? 0 : res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Prefix Sum + Binary Search

We can precompute prefix sums so that the sum of any subarray from index `i` to `j` is `prefixSum[j+1] - prefixSum[i]`. Since all numbers are positive, the prefix sum array is strictly increasing. For each starting index `i`, we can binary search for the smallest ending index `j` where the subarray sum is at least `target`.

```cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int n = nums.size();
        vector<int> prefixSum(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }

        int res = n + 1;
        for (int i = 0; i < n; i++) {
            int l = i, r = n;
            while (l < r) {
                int mid = (l + r) / 2;
                int curSum = prefixSum[mid + 1] - prefixSum[i];
                if (curSum >= target) {
                    r = mid;
                } else {
                    l = mid + 1;
                }
            }
            if (l != n) {
                res = min(res, l - i + 1);
            }
        }

        return res % (n + 1);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0209-minimum-size-subarray-sum.cpp` in the NeetCode repo)

```cpp
/* Given an array of positive integers nums and a positive integer target, 
return the minimal length of a contiguous subarray [numsl, numsl+1, ..., numsr-1, numsr] 
of which the sum is greater than or equal to target. 
If there is no such subarray, return 0 instead.
Ex.: target = 7, nums = [2,3,1,2,4,3] -> 2 
     target = 4, nums = [1,4,4] -> 1     
Sliding window (with two pointer). Keep adding elements to the SL. When Sum => target or SP points to end of the vector resize the SW. */

class Solution{    
    public:    
        int minSubArrayLen(int target, vector<int>& nums){            
            int min;            
            int fp, sp;            
            int sum;            
            fp = 0;            
            sp = 1;            
            sum = nums[0];            
            min = nums.size() + 1;            
            while(fp != sp){                
                if(Sum >= target){                    
                    min = min(sp - fp, min);                    
                    sum = Sìsum - nums[fp];                    
                    fp++;                    
                }
                else{                        
                    if(sp < nums.size()){                         
                        sum = sum + nums[sp];
                        sp++;                            
                    }
                    else{                            
                        fp++;                            
                    }                    
                }                  
            }            
            return min;
        }    
};
```
