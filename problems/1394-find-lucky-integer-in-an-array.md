# 1394. Find Lucky Integer in an Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-lucky-integer-in-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-lucky-integer-in-an-array>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A lucky integer is one whose value equals its frequency in the array. The simplest approach is to check each number by counting how many times it appears. If the count matches the number itself, it's a lucky integer. We track the largest one found.

```cpp
class Solution {
public:
    int findLucky(vector<int>& arr) {
        int res = -1;

        for (int num : arr) {
            int cnt = 0;
            for (int a : arr) {
                if (num == a) {
                    cnt++;
                }
            }
            if (cnt == num) {
                res = max(res, num);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sorting

After sorting, identical numbers are grouped together. By traversing from right to left, we can count consecutive occurrences of each number. The first lucky integer we find (scanning from largest to smallest) is guaranteed to be the largest.

```cpp
class Solution {
public:
    int findLucky(vector<int>& arr) {
        sort(arr.begin(), arr.end());
        int streak = 0;

        for (int i = arr.size() - 1; i >= 0; i--) {
            streak++;
            if (i == 0 || arr[i] != arr[i - 1]) {
                if (arr[i] == streak) {
                    return arr[i];
                }
                streak = 0;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Hash Map

We can count the frequency of each number in one pass using a hash map. Then we iterate through the map to find numbers where the key equals its value (frequency). This avoids repeated counting and is more efficient than brute force.

```cpp
class Solution {
public:
    int findLucky(vector<int>& arr) {
        unordered_map<int, int> count;
        for (int num : arr) {
            count[num]++;
        }

        int res = -1;
        for (auto& [num, freq] : count) {
            if (num == freq) {
                res = max(res, num);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Negative Marking

If we can modify the input array, we can use it as a frequency counter without extra space. For a number `num`, we use index `num - 1` to store its frequency by making that position negative and decrementing it. After processing, a position `i` with value `-x` means the number `i + 1` appeared `x` times.

```cpp
class Solution {
public:
    int findLucky(vector<int>& arr) {
        int n = arr.size();
        for (int i = 0; i < n; i++) {
            int prev = i, num = arr[i];
            while (0 < num && num <= n) {
                int nxt = arr[num - 1];
                arr[num - 1] = min(0, arr[num - 1]) - 1;
                if (num - 1 <= i || num - 1 == prev) break;
                prev = num - 1;
                num = nxt;
            }
        }

        for (int i = n - 1; i >= 0; i--) {
            if (-arr[i] == i + 1) return i + 1;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Bit Manipulation

We can use bit manipulation to store both the original value and the frequency count in the same array element. Since values are at most `500`, they fit in 10 bits. We use the lower 10 bits for the original value and the upper bits for the count. This allows in-place frequency tracking.

```cpp
class Solution {
public:
    int findLucky(vector<int>& arr) {
        for (int num : arr) {
            int idx = num & ((1 << 10) - 1);
            if (idx <= arr.size()) {
                arr[idx - 1] += (1 << 10);
            }
        }

        for (int i = arr.size() - 1; i >= 0; i--) {
            int cnt = arr[i] >> 10;
            if (cnt == i + 1) return i + 1;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
