# 287. Find The Duplicate Number

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/find-the-duplicate-number/>  
- **NeetCode:** <https://neetcode.io/problems/find-duplicate-integer>  
- **Video:** <https://www.youtube.com/watch?v=wjYnzkAhcNk>  

[← Back to index](../INDEX.md)

## 1. Sorting

If we sort the array, any duplicate numbers will appear **next to each other**.  
So after sorting, we just scan once and check if any two consecutive elements are equal.  
The first equal pair we find is the duplicate.

```cpp
class Solution {
public:
    int findDuplicate(std::vector<int>& nums) {
        sort(nums.begin(), nums.end());
        for (int i = 0; i < nums.size() - 1; i++) {
            if (nums[i] == nums[i + 1]) {
                return nums[i];
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Hash Set

We can detect duplicates by remembering which numbers we have already seen.  
As we scan the array, each new number is checked:

- If it's **not in the set**, we add it.
- If it **is already in the set**, that number must be the duplicate.

A set gives constant-time lookup, so this approach is simple and efficient.

```cpp
class Solution {
public:
    int findDuplicate(std::vector<int>& nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.find(num) != seen.end()) {
                return num;
            }
            seen.insert(num);
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Array

Since the values in the array are from **1 to n**, we can use an array to track whether we've seen a number before.
Each number directly maps to an index (`num - 1`).
- If that index is already marked, we've seen the number before → it's the duplicate.
- Otherwise, we mark it as seen.

This avoids using a hash set while still providing fast lookups.

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        vector<int> seen(nums.size(), 0);
        for (int num : nums) {
            if (seen[num - 1] == 1) {
                return num;
            }
            seen[num - 1] = 1;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Negative Marking

Since every value is between **1 and n**, each number corresponds to an index in the array (`num - 1`).  
We can use the array itself as a marking tool:

- When we see a number, we go to its corresponding index and **flip the sign** of the value there.
- If we ever visit an index that is **already negative**, it means we've visited this number before → it's the duplicate.

This method avoids extra memory and uses the input array as a tracking structure.

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        for (int num : nums) {
            int idx = abs(num) - 1;
            if (nums[idx] < 0) {
                return abs(num);
            }
            nums[idx] *= -1;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Binary Search

This method uses **binary search on the value range**, not on the array itself.

If all numbers from `1` to `mid` appeared **at most once**, then the count of numbers `<= mid` should be **<= mid**.
But if the count is **greater than `mid`**, it means the duplicate must be in the range `[1, mid]`, because too many numbers fall into that range.

So we repeatedly:
- Count how many values are `<= mid`.
- Shrink the search space based on whether this count is "too large."

Eventually, `low == high`, and that value is the duplicate.

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int n = nums.size();
        int low = 1, high = n - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            int lessOrEqual = 0;
            for (int i = 0; i < n; i++) {
                if (nums[i] <= mid) {
                    lessOrEqual++;
                }
            }

            if (lessOrEqual <= mid) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        return low;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$

## 6. Bit Manipulation

Every number from **1 to n−1** should appear exactly **once**, but in the array, one number appears **twice**.  
So for each **bit position**, we compare:

- How many times this bit is set among all numbers in the array.
- How many times this bit *should* be set among the numbers `1` to `n-1`.

If a bit appears **more times in the array** than expected, that bit must belong to the **duplicate number**.

By combining all such bits, we reconstruct the duplicate.

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int n = nums.size();
        int res = 0;
        for (int b = 0; b < 32; b++) {
            int x = 0, y = 0;
            int mask = 1 << b;
            for (int num : nums) {
                if (num & mask) {
                    x++;
                }
            }
            for (int num = 1; num < n; num++) {
                if (num & mask) {
                    y++;
                }
            }
            if (x > y) {
                res |= mask;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(32 * n)$
- Space complexity: $O(1)$

## 7. Fast And Slow Pointers

Treat the array like a **linked list**, where each index points to the next index given by its value.  
Because one number is duplicated, two indices will point into the **same chain**, creating a **cycle** — exactly like a linked list with a loop.

Using Floyd’s **Fast & Slow Pointer** technique:

1. The **slow** pointer moves one step at a time.
2. The **fast** pointer moves two steps at a time.
3. If there’s a cycle, they will eventually meet.

Once they meet, we start a new pointer from the beginning:
- Move both pointers one step at a time.
- The point where they meet again is the **duplicate number** (the entry point of the cycle).

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = 0, fast = 0;
        while (true) {
            slow = nums[slow];
            fast = nums[nums[fast]];
            if (slow == fast) {
                break;
            }
        }

        int slow2 = 0;
        while (true) {
            slow = nums[slow];
            slow2 = nums[slow2];
            if (slow == slow2) {
                return slow;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0287-find-the-duplicate-number.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, return the one repeated number
    Ex. nums = [1,3,4,2,2] -> 2, nums = [3,1,3,4,2] -> 3

    If there's duplicate, must be a cycle, find meeting point
    Take 1 back to start, they'll intersect at the duplicate

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0];
        int fast = nums[nums[0]];
        
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[nums[fast]];
        }
        
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};
```
