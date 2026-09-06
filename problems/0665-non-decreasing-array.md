# 665. Non Decreasing Array

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/non-decreasing-array/>  
- **NeetCode:** <https://neetcode.io/problems/non-decreasing-array>  
- **Video:** <https://www.youtube.com/watch?v=RegQckCegDk>  

[← Back to index](../INDEX.md)

## 1. Greedy

When we find a "violation" where `nums[i] > nums[i + 1]`, we need to fix it by modifying one element. The key insight is deciding which element to change. We have two options: decrease `nums[i]` to match `nums[i + 1]`, or increase `nums[i + 1]` to match `nums[i]`. The greedy choice is to prefer decreasing `nums[i]` when possible, because a smaller value is less likely to cause future violations. However, we can only do this if `nums[i + 1]` is at least as large as `nums[i - 1]` (the element before the violation). Otherwise, we must increase `nums[i + 1]`. If we encounter more than one violation, the answer is `false`.

```cpp
class Solution {
public:
    bool checkPossibility(vector<int>& nums) {
        bool changed = false;

        for (int i = 0; i < nums.size() - 1; i++) {
            if (nums[i] <= nums[i + 1]) {
                continue;
            }
            if (changed) {
                return false;
            }
            if (i == 0 || nums[i + 1] >= nums[i - 1]) {
                nums[i] = nums[i + 1];
            } else {
                nums[i + 1] = nums[i];
            }
            changed = true;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0665-non-decreasing-array.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool checkPossibility(vector<int>& nums) {
        bool changed = false;

        for(int i = 0; i < nums.size() - 1; i++){
            if(nums[i] <= nums[i+1]){
                continue;
            }
            if(changed){
                return false;
            }
        
            if(i == 0 || nums[i+1] >= nums[i-1]){
                nums[i] = nums[i+1];
            }
            else{
                nums[i+1] = nums[i];
            }
            changed = true;
        }

        return true;
    }
};
```
