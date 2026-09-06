# 904. Fruit into Basket

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/fruit-into-baskets/>  
- **NeetCode:** <https://neetcode.io/problems/fruit-into-baskets>  
- **Video:** <https://www.youtube.com/watch?v=yYtaV0G3mWQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force

This problem asks for the longest contiguous subarray containing at most two distinct values. We can check every possible starting position and extend as far as possible while keeping track of at most two fruit types.

For each starting index, we greedily expand until we encounter a third distinct type, then record the length.

```cpp
class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        int n = fruits.size(), res = 0;

        for (int i = 0; i < n; i++) {
            unordered_set<int> types;
            int j = i;

            while (j < n && (types.size() < 2 || types.count(fruits[j]))) {
                types.insert(fruits[j]);
                j++;
            }
            res = max(res, j - i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sliding Window - I

Instead of restarting from each position, we maintain a sliding window that always contains at most two fruit types. When we encounter a third type, we shrink the window from the left until only two types remain.

A hash map tracks the count of each fruit type in the current window. When a count drops to zero, we remove that type from the map.

```cpp
class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        unordered_map<int, int> count;
        int l = 0, total = 0, res = 0;

        for (int r = 0; r < fruits.size(); r++) {
            count[fruits[r]]++;
            total++;

            while (count.size() > 2) {
                int f = fruits[l];
                count[f]--;
                total--;
                if (count[f] == 0) {
                    count.erase(f);
                }
                l++;
            }
            res = max(res, total);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Sliding Window - II

Similar to the advanced sliding window for frequency problems, we only care about the maximum window size. Once we achieve a valid window of size `w`, we never need a smaller one.

When a third fruit type appears, instead of shrinking until valid, we just slide the window forward by one position. The window size only increases when we find valid configurations, and the final size equals our answer.

```cpp
class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        unordered_map<int, int> count;
        int l = 0;

        for (int r = 0; r < fruits.size(); r++) {
            count[fruits[r]]++;

            if (count.size() > 2) {
                count[fruits[l]]--;
                if (count[fruits[l]] == 0) {
                    count.erase(fruits[l]);
                }
                l++;
            }
        }

        return fruits.size() - l;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Sliding Window - III

Since we only track two fruit types, we can avoid using a hash map entirely. Instead, we store the two fruit types and the last index where each appeared. When a third type appears, we can immediately jump the left pointer to just after the earlier of the two last indices.

This approach uses `O(1)` space and handles the window adjustment in constant time by directly computing where the new window should start.

```cpp
class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        int l = 0, fruit1_lastIdx = 0, fruit2_lastIdx = -1;
        int fruit1 = fruits[0], fruit2 = -1, total = 1, res = 1;

        for (int r = 0; r < fruits.size(); r++) {
            int f = fruits[r];
            if (f == fruit1) {
                total++;
                fruit1_lastIdx = r;
            } else if (f == fruit2 || fruit2 == -1) {
                total++;
                fruit2_lastIdx = r;
                fruit2 = f;
            } else {
                if (fruit2_lastIdx == min(fruit1_lastIdx, fruit2_lastIdx)) {
                    swap(fruit1_lastIdx, fruit2_lastIdx);
                    swap(fruit1, fruit2);
                }
                total -= (fruit1_lastIdx - l + 1);
                l = fruit1_lastIdx + 1;
                fruit1 = f;
                fruit1_lastIdx = r;
            }
            res = max(res, r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0904-fruit-into-baskets.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        unordered_map<int, int> count;
        int l = 0, res = 0;

        for (int r = 0; r < fruits.size(); r++) {
            count[fruits[r]]++;

            while (count.size() > 2) {
                count[fruits[l]]--;
                if (count[fruits[l]] == 0)
                    count.erase(fruits[l]);
                l++;
            }
            res = max(res, r - l + 1);
        }
        return res;
    }
};
```
