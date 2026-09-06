# 496. Next Greater Element I

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/next-greater-element-i/>  
- **NeetCode:** <https://neetcode.io/problems/next-greater-element-i>  
- **Video:** <https://www.youtube.com/watch?v=68a1Dc_qVq4>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each element in `nums1`, we need to find it in `nums2` and then look for the first larger element to its right. The simplest approach scans `nums2` from right to left: track the largest element seen so far that is greater than our target. When we hit the target element, we have our answer.

This works but is inefficient since we repeat the scan for every element in `nums1`.

```cpp
class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        int n = nums2.size();
        vector<int> res;
        for (int num : nums1) {
            int nextGreater = -1;
            for (int i = n - 1; i >= 0; i--) {
                if (nums2[i] > num) {
                    nextGreater = nums2[i];
                } else if (nums2[i] == num) {
                    break;
                }
            }
            res.push_back(nextGreater);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$

> The output array is not counted towards space complexity, as the [standard convention](https://en.wikipedia.org/wiki/DSPACE) measures only auxiliary working space.

> Where $m$ is the size of the array $nums1$ and $n$ is the size of the array $nums2$.

## 2. Hash Map

Instead of scanning from the end each time, we can iterate through `nums2` from left to right. For each element that appears in `nums1`, we look ahead to find the next greater element. A hash map stores the index of each `nums1` element, so we can quickly check if a number from `nums2` is one we care about.

This is still O(m \* n) in the worst case, but we skip elements not in `nums1`.

```cpp
class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        unordered_map<int, int> nums1Idx;
        for (int i = 0; i < nums1.size(); i++) {
            nums1Idx[nums1[i]] = i;
        }

        vector<int> res(nums1.size(), -1);

        for (int i = 0; i < nums2.size(); i++) {
            if (nums1Idx.find(nums2[i]) == nums1Idx.end()) {
                continue;
            }
            for (int j = i + 1; j < nums2.size(); j++) {
                if (nums2[j] > nums2[i]) {
                    int idx = nums1Idx[nums2[i]];
                    res[idx] = nums2[j];
                    break;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m)$

> Where $m$ is the size of the array $nums1$ and $n$ is the size of the array $nums2$.

## 3. Stack

A monotonic stack solves this problem in linear time. We iterate through `nums2` and maintain a stack of elements that have not yet found their next greater element. When we encounter a larger element, it becomes the "next greater" for all smaller elements on the stack.

The stack maintains decreasing order from bottom to top. When a new element is larger than the stack top, we pop elements and record the current element as their next greater. We only push elements that are in `nums1` since those are the only ones we need answers for.

```cpp
class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        unordered_map<int, int> nums1Idx;
        for (int i = 0; i < nums1.size(); i++) {
            nums1Idx[nums1[i]] = i;
        }

        vector<int> res(nums1.size(), -1);
        stack<int> stack;

        for (int num : nums2) {
            while (!stack.empty() && num > stack.top()) {
                int val = stack.top();
                stack.pop();
                int idx = nums1Idx[val];
                res[idx] = num;
            }
            if (nums1Idx.find(num) != nums1Idx.end()) {
                stack.push(num);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m)$

> Where $m$ is the size of the array $nums1$ and $n$ is the size of the array $nums2$.

## Standalone solution file (`cpp/0496-next-greater-element-i.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        // O (n + m)
        map<int, int> nums1Idx; {
            int idx = 0;
            for(int n: nums1)
                nums1Idx[n] = idx++;
        }
        vector<int> res;
        for(int i = 0; i < nums1.size(); i++)
            res.push_back(-1);
        
        stack<int> stack;
        for(int i = 0; i < nums2.size(); i++) {
            int cur = nums2[i];
            
            // while stack has elements and current is greater than the top of the stack
            while(stack.size() && cur > stack.top()) {
                int val = stack.top(); // take top val
                stack.pop();
                int idx = nums1Idx[val];
                res[idx] = cur;
            }
            
            if(nums1Idx.count(cur))
                stack.push(cur);
        }
        
        return res;
    }
};
```
