# 169. Majority Element

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/majority-element/>  
- **NeetCode:** <https://neetcode.io/problems/majority-element>  
- **Video:** <https://www.youtube.com/watch?v=7pnhv842keE>  
- **Video approach:** 5. Boyer-Moore Voting Algorithm  

[← Back to index](../INDEX.md)

## 1. Brute Force

The majority element appears more than `n/2` times. For each element, we can count how many times it appears in the array. If the count exceeds `n/2`, we've found our answer. This straightforward approach checks every element against every other element.

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int n = nums.size();
        for (int num : nums) {
            int count = 0;
            for (int i : nums) {
                if (i == num) {
                    count++;
                }
            }
            if (count > n / 2) {
                return num;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Map

We can avoid repeated counting by using a hash map to store the frequency of each element as we iterate through the array. We track the element with the maximum count seen so far. Once any element's count exceeds `n/2`, it must be the majority element.

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        unordered_map<int, int> count;
        int res = 0, maxCount = 0;

        for (int num : nums) {
            count[num]++;
            if (count[num] > maxCount) {
                res = num;
                maxCount = count[num];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sorting

If we sort the array, the majority element must occupy the middle position. Since it appears more than `n/2` times, no matter where the majority element's block starts, it will always include the index `n/2`. This gives us a simple one-liner solution after sorting.

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        return nums[nums.size() / 2];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Bit Manipulation

We can construct the majority element bit by bit. For each bit position, we count how many numbers have that bit set. If more than `n/2` numbers have the bit set, then the majority element must also have that bit set. We build the result by combining all the majority bits.

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int n = nums.size();
        vector<int> bit(32, 0);
        for (int num : nums) {
            for (int i = 0; i < 32; i++) {
                bit[i] += (num >> i) & 1;
            }
        }

        int res = 0;
        for (int i = 0; i < 32; i++) {
            if (bit[i] > n / 2) {
                res |= (1 << i);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 32)$
- Space complexity: $O(32)$

> $32$ represents the number of bits as the given numbers are integers.

## 5. Boyer-Moore Voting Algorithm ▶ video

The Boyer-Moore algorithm works by maintaining a candidate and a count. When we see the candidate, we increment the count; otherwise, we decrement it. When the count reaches `0`, we pick a new candidate. Since the majority element appears more than half the time, it will survive this elimination process and remain as the final candidate.

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int res = 0, count = 0;

        for (int num : nums) {
            if (count == 0) {
                res = num;
            }
            count += (num == res) ? 1 : -1;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 6. Randomization

Since the majority element appears more than `n/2` times, any random pick has greater than 50% chance of selecting it. We repeatedly pick a random element and check if it's the majority. On average, we need only about 2 picks to find the answer, making this surprisingly efficient in practice.

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int n = nums.size();

        while (true) {
            int candidate = nums[rand() % n];
            int count = 0;
            for (int num : nums) {
                if (num == candidate) {
                    count++;
                }
            }
            if (count > n / 2) {
                return candidate;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> The probability of randomly choosing the majority element is greater than $50\%$, so the expected number of iterations in the outer while loop is constant.

## Standalone solution file (`cpp/0169-majority-element.cpp` in the NeetCode repo)

```cpp
/*
Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.
*/

class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int count = 0;
        int res = 0;

        for (const int& num: nums) {
            if (count == 0) {
                res = num;
            } 
            count += (num == res) ? 1 : -1;
        }

        return res;
    }
};
```
