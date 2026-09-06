# 2149. Rearrange Array Elements by Sign

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/rearrange-array-elements-by-sign/>  
- **NeetCode:** <https://neetcode.io/problems/rearrange-array-elements-by-sign>  
- **Video:** <https://www.youtube.com/watch?v=SoPmcGzz9-E>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We process the array position by position. At each index, we check if the current element has the correct sign (positive at even indices, negative at odd indices). If not, we search forward for an element with the correct sign and shift all elements in between to make room for it.

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            if ((i % 2 == 0 && nums[i] > 0) || (i % 2 == 1 && nums[i] < 0)) {
                continue;
            }

            int j = i + 1;
            while (j < n && ((nums[j] > 0) == (nums[i] > 0))) {
                j++;
            }

            int temp = nums[j];
            while (j > i) {
                nums[j] = nums[j - 1];
                j--;
            }
            nums[i] = temp;
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Group Numbers Into Two Arrays

Since we need to alternate positive and negative numbers while preserving their relative order, we can first separate them into two lists. Then we interleave them back into the original array: positive numbers go to even indices, negative numbers go to odd indices.

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        vector<int> pos, neg;
        for (int num : nums) {
            if (num > 0) {
                pos.push_back(num);
            } else {
                neg.push_back(num);
            }
        }

        int i = 0;
        while (2 * i < nums.size()) {
            nums[2 * i] = pos[i];
            nums[2 * i + 1] = neg[i];
            i++;
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Two Pointers

We can build the result in a single pass using two pointers. One pointer tracks the next even index (for positive numbers), and the other tracks the next odd index (for negative numbers). As we scan through the input, we place each number at the appropriate position and advance the corresponding pointer by 2.

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        int i = 0, j = 1;
        vector<int> res(nums.size());
        for (int k = 0; k < nums.size(); k++) {
            if (nums[k] > 0) {
                res[i] = nums[k];
                i += 2;
            } else {
                res[j] = nums[k];
                j += 2;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output array.
