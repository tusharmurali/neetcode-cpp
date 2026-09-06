# 1929. Concatenation of Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/concatenation-of-array/>  
- **NeetCode:** <https://neetcode.io/problems/concatenation-of-array>  
- **Video:** <https://www.youtube.com/watch?v=68isPRHgcFQ>  

[← Back to index](../INDEX.md)

## 1. Iteration (Two Pass)

To concatenate an array with itself, we need to create a new array that contains all elements of the original array twice, maintaining the same order. The elements at indices $0$ to $n - 1$ are followed by the same elements at indices $n$ to $2n - 1$.

For example, if `nums = [1, 2, 3]`:

- The first three elements of `ans` will be `nums[0]`, `nums[1]`, `nums[2]` -> `[1, 2, 3]`
- The next three elements of `ans` will also be `nums[0]`, `nums[1]`, `nums[2]` -> `[1, 2, 3]`
- Result: `[1, 2, 3, 1, 2, 3]`

```cpp
class Solution {
public:
    vector<int> getConcatenation(vector<int>& nums) {
        vector<int> ans;
        for (int i = 0; i < 2; ++i) {
            for (int num : nums) {
                ans.push_back(num);
            }
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ where $n$ is the length of the input array. We iterate through the array twice, performing $2n$ operations.
- Space complexity: $O(n)$ if we consider the space required for the output array of size $2n$.

## 2. Iteration (One Pass)

The problem defines the result array `ans` such that `ans[i] == nums[i]` and `ans[i + n] == nums[i]` for `0 <= i < n`. Instead of looping through the input twice, we can fill both required positions in the result array simultaneously while iterating through the input array just once. This utilizes the index mapping `i` and `i + n` directly.

```cpp
class Solution {
public:
    vector<int> getConcatenation(vector<int>& nums) {
        int n = nums.size();
        vector<int> ans(2 * n);
        for (int i = 0; i < n; ++i) {
            ans[i] = ans[i + n] = nums[i];
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ where $n$ is the length of the input array. Although we iterate through the input once, we still perform $2n$ total writes to the output array.
- Space complexity: $O(n)$ as we must allocate an array of size $2n$ for the output.

## Standalone solution file (`cpp/1929-concatenation-of-array.cpp` in the NeetCode repo)

```cpp
class Solution{    
    public:    
        vector<int> getConcatenation(vector<int>& nums){            
            vector<int> ans;            
            int len;            
            len = nums.size();            
            for(int i = 0; i < 2 * len; i++){                
                ans.push_back(nums[i % len]);                
            }
            return ans;            
        }
};
```
