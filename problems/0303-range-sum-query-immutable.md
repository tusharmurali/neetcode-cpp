# 303. Range Sum Query - Immutable

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/range-sum-query-immutable/>  
- **NeetCode:** <https://neetcode.io/problems/range-sum-query-immutable>  
- **Video:** <https://www.youtube.com/watch?v=2pndAmo_sMA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to iterate through the array from `left` to `right` and add up all the elements. This works correctly but is inefficient when we need to answer many queries, since each query requires scanning through the entire range.

```cpp
class NumArray {
private:
    const vector<int>& nums;

public:
    NumArray(const vector<int>& nums) : nums(nums) {}

    int sumRange(int left, int right) {
        int res = 0;
        for (int i = left; i <= right; i++) {
            res += nums[i];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for each $sumRange()$ query.
- Space complexity: $O(1)$ since we only make a reference to the input array.

## 2. Prefix Sum - I

We can precompute a prefix sum array where `prefix[i]` stores the sum of all elements from index `0` to `i`. To find the sum of any range `[left, right]`, we take `prefix[right]` and subtract `prefix[left - 1]` (if `left > 0`). This gives us constant-time queries after a linear-time preprocessing step.

```cpp
class NumArray {
private:
    vector<int> prefix;

public:
    NumArray(const vector<int>& nums) {
        int cur = 0;
        for (int num : nums) {
            cur += num;
            prefix.push_back(cur);
        }
    }

    int sumRange(int left, int right) {
        int rightSum = prefix[right];
        int leftSum = left > 0 ? prefix[left - 1] : 0;
        return rightSum - leftSum;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each $sumRange()$ query, $O(n)$ for building the prefix sum array.
- Space complexity: $O(n)$

## 3. Prefix Sum - II

This is a cleaner variation of the prefix sum approach. By creating an array of size `n + 1` where `prefix[0] = 0`, we avoid the edge case when `left = 0`. The value `prefix[i + 1]` represents the sum of the first `i + 1` elements. The range sum becomes simply `prefix[right + 1] - prefix[left]`.

```cpp
class NumArray {
private:
    vector<int> prefix;

public:
    NumArray(const vector<int>& nums) {
        prefix = vector<int>(nums.size() + 1, 0);
        for (int i = 0; i < nums.size(); i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }

    int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each $sumRange()$ query, $O(n)$ for building the prefix sum array.
- Space complexity: $O(n)$

## 4. Segment Tree

A segment tree is a binary tree where each node stores the sum of a range of elements. The root contains the sum of the entire array, and each leaf contains a single element. While this is overkill for an immutable array (prefix sums are simpler and faster), segment trees become essential when updates are needed. For this immutable version, queries still run in logarithmic time.

```cpp
class SegmentTree {
private:
    vector<int> tree;
    int n;

public:
    SegmentTree(const vector<int>& nums) {
        n = nums.size();
        tree.resize(2 * n);
        for (int i = 0; i < n; i++) {
            tree[n + i] = nums[i];
        }
        for (int i = n - 1; i > 0; i--) {
            tree[i] = tree[2 * i] + tree[2 * i + 1];
        }
    }

    int query(int left, int right) {
        int sum = 0;
        left += n;
        right += n + 1;
        while (left < right) {
            if (left % 2 == 1) sum += tree[left++];
            if (right % 2 == 1) sum += tree[--right];
            left /= 2;
            right /= 2;
        }
        return sum;
    }
};

class NumArray {
private:
    SegmentTree segTree;

public:
    NumArray(const vector<int>& nums) : segTree(nums) {}

    int sumRange(int left, int right) {
        return segTree.query(left, right);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$ for each $sumRange()$ query, $O(n)$ for building the Segment Tree.
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0303-range-sum-query-immutable.cpp` in the NeetCode repo)

```cpp
/*
Given an integer array nums, handle multiple queries of the following type:

Calculate the sum of the elements of nums between indices left and right inclusive where left <= right.

Implement the NumArray class:

  - NumArray(int[] nums) Initializes the object with the integer array nums.
  - int sumRange(int left, int right) Returns the sum of the elements of nums between indices left and right 
    inclusive (i.e. nums[left] + nums[left + 1] + ... + nums[right]).

*/


class NumArray {
public:
    vector<int> prefixSum;
    NumArray(vector<int>& nums) {
        int count=0;
        for(int i=0;i<nums.size();i++){
            count+=nums[i];
            prefixSum.push_back(count);
        }
    }
    
    int sumRange(int left, int right) {
        int answer=prefixSum[right];

        if(left-1>=0){
            answer-=prefixSum[left-1];
        }
        return answer;
    }
};

/**
 * Your NumArray object will be instantiated and called as such:
 * NumArray* obj = new NumArray(nums);
 * int param_1 = obj->sumRange(left,right);
 */
```
