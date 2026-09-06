# 2780. Minimum Index of a Valid Split

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-index-of-a-valid-split/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-index-of-a-valid-split>  
- **Video:** <https://www.youtube.com/watch?v=XemmMMz_0mU>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A valid split requires that the same element is dominant in both the left and right subarrays. The dominant element must appear more than half the time in each part.

The straightforward approach is to try every possible split point and, for each one, count element frequencies in both halves. We then check if any element satisfies the dominance condition on both sides.

```cpp
class Solution {
public:
    int minimumIndex(vector<int>& nums) {
        int n = nums.size();

        for (int i = 0; i < n - 1; i++) {
            unordered_map<int, int> leftCnt, rightCnt;
            for (int l = 0; l <= i; l++) {
                leftCnt[nums[l]]++;
            }
            for (int r = i + 1; r < n; r++) {
                rightCnt[nums[r]]++;
            }

            for (auto& [num, cnt] : leftCnt) {
                if (cnt > (i + 1) / 2 && rightCnt[num] > (n - i - 1) / 2) {
                    return i;
                }
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Hash Map

Instead of recounting from scratch at each split, we can maintain running counts. Start with all elements in the "right" map, then slide through the array moving one element at a time from right to left.

For each position, we only need to check if the current element is dominant in both parts. This works because if a valid split exists, the overall dominant element must be dominant on both sides.

```cpp
class Solution {
public:
    int minimumIndex(vector<int>& nums) {
        unordered_map<int, int> left, right;
        int n = nums.size();

        for (int num : nums) {
            right[num]++;
        }

        for (int i = 0; i < n; i++) {
            int num = nums[i];
            left[num]++;
            right[num]--;

            int leftLen = i + 1;
            int rightLen = n - i - 1;

            if (2 * left[num] > leftLen && 2 * right[num] > rightLen) {
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

## 3. Boyer-Moore Voting Algorithm

Since the problem guarantees a dominant element exists in the full array, we can first identify it using Boyer-Moore voting. This algorithm finds the majority element in O(n) time and O(1) space by maintaining a candidate and a counter.

Once we know the dominant element, we just need to track its count on each side as we scan through, checking if it remains dominant in both portions at each potential split.

```cpp
class Solution {
public:
    int minimumIndex(vector<int>& nums) {
        int majority = 0, count = 0;
        for (int num : nums) {
            if (count == 0) majority = num;
            count += (num == majority ? 1 : -1);
        }

        int leftCnt = 0, rightCnt = count_if(nums.begin(), nums.end(),
                                             [&](int x) { return x == majority; });

        int n = nums.size();
        for (int i = 0; i < n; i++) {
            if (nums[i] == majority) {
                leftCnt++;
                rightCnt--;
            }

            int leftLen = i + 1;
            int rightLen = n - i - 1;

            if (2 * leftCnt > leftLen && 2 * rightCnt > rightLen) {
                return i;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
