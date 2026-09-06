# 260. Single Number III

- **Difficulty:** Medium  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/single-number-iii/>  
- **NeetCode:** <https://neetcode.io/problems/single-number-iii>  
- **Video:** <https://www.youtube.com/watch?v=faoVORjd-T8>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check each element against every other element. If we find no duplicate for an element, it must be one of the two unique numbers. We collect these unique elements until we find both.

```cpp
class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        int n = nums.size();
        vector<int> res;

        for (int i = 0; i < n; i++) {
            bool flag = true;
            for (int j = 0; j < n; j++) {
                if (i != j && nums[i] == nums[j]) {
                    flag = false;
                    break;
                }
            }

            if (flag) {
                res.push_back(nums[i]);
                if (res.size() == 2) {
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Hash Map

We can count occurrences of each number using a hash map. Numbers that appear exactly once are our two unique elements. This trades space for time, reducing the time complexity from quadratic to linear.

```cpp
class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        vector<int> res;
        for (const auto& pair : count) {
            if (pair.second == 1) {
                res.push_back(pair.first);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Set

A hash set can track numbers we have seen. When we encounter a number for the first time, we add it. When we see it again, we remove it. After processing all numbers, only the two unique elements remain in the set.

```cpp
class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        unordered_set<int> seen;
        for (int& num : nums) {
            if (seen.count(num)) {
                seen.erase(num);
            } else {
                seen.insert(num);
            }
        }

        return vector<int>(seen.begin(), seen.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Sorting

Sorting the array groups duplicate numbers together. After sorting, each element should equal either its left or right neighbor if it has a duplicate. Elements that differ from both neighbors are the unique numbers we seek.

```cpp
class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<int> res;
        int n = nums.size();

        for (int i = 0; i < n; i++) {
            if ((i > 0 && nums[i] == nums[i - 1]) ||
                (i + 1 < n && nums[i] == nums[i + 1])) {
                continue;
            }
            res.push_back(nums[i]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 5. Bitwise XOR (Least Significant Bit)

XORing all numbers gives us `a ^ b` where `a` and `b` are the two unique numbers. Since `a != b`, at least one bit in the XOR result is set. This bit position represents where `a` and `b` differ. We can use this differing bit to partition all numbers into two groups: one containing `a` and one containing `b`. XORing within each group isolates the unique numbers.

```cpp
class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        int xor_all = 0;
        for (int& num : nums) {
            xor_all ^= num;
        }

        int diff_bit = 1;
        while ((xor_all & diff_bit) == 0) {
            diff_bit <<= 1;
        }

        int a = 0, b = 0;
        for (int& num : nums) {
            if (num & diff_bit) {
                a ^= num;
            } else {
                b ^= num;
            }
        }
        return {a, b};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 6. Bitwise XOR (Most Significant Bit)

This approach is similar to the previous one but uses a neat trick to find the rightmost set bit. The expression `x & (-x)` isolates the lowest set bit in `x`. Using this on the XOR of all numbers immediately gives us a differing bit between the two unique numbers without looping.

```cpp
class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        uint xor_all = 0;
        for (int& num : nums) {
            xor_all ^= num;
        }

        int diff_bit = xor_all & (-xor_all);

        int a = 0, b = 0;
        for (int& num : nums) {
            if (num & diff_bit) {
                a ^= num;
            } else {
                b ^= num;
            }
        }
        return {a, b};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
