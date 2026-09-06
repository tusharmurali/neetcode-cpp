# 2053. Kth Distinct String in an Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/kth-distinct-string-in-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/kth-distinct-string-in-an-array>  
- **Video:** <https://www.youtube.com/watch?v=1KOnvGPv9Mo>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A string is distinct if it appears exactly once in the array. The simplest approach is to check each string against all other strings. For each position, we scan the entire array to see if that string appears anywhere else. If not, it's distinct, and we decrement our counter until we find the k-th one.

```cpp
class Solution {
public:
    string kthDistinct(vector<string>& arr, int k) {
        for (int i = 0; i < arr.size(); i++) {
            bool flag = true;
            for (int j = 0; j < arr.size(); j++) {
                if (i == j) continue;

                if (arr[i] == arr[j]) {
                    flag = false;
                    break;
                }
            }

            if (flag) {
                k--;
                if (k == 0) {
                    return arr[i];
                }
            }
        }
        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Map

Instead of repeatedly scanning the array, we can count occurrences upfront using a hash map. In the first pass, we count how many times each string appears. In the second pass, we iterate in order and check if each string has a count of exactly `1`. This reduces time complexity from `O(n^2)` to `O(n)`.

```cpp
class Solution {
public:
    string kthDistinct(vector<string>& arr, int k) {
        unordered_map<string, int> count;

        for (const string& s : arr) {
            count[s]++;
        }

        for (const string& s : arr) {
            if (count[s] == 1) {
                k--;
                if (k == 0) {
                    return s;
                }
            }
        }

        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Set

We can use two sets instead of a counting map. One set tracks strings that are currently distinct (seen exactly once), and another tracks strings we've already identified as duplicates. When we encounter a string, if it's in the `distinct` set, we move it to the `seen` set (it's no longer distinct). If it's not in either set, we add it to `distinct`. This achieves the same result with a slightly different data structure.

```cpp
class Solution {
public:
    string kthDistinct(vector<string>& arr, int k) {
        unordered_set<string> distinct, seen;

        for (const string& s : arr) {
            if (distinct.count(s)) {
                distinct.erase(s);
                seen.insert(s);
            } else if (!seen.count(s)) {
                distinct.insert(s);
            }
        }

        for (const string& s : arr) {
            if (distinct.count(s)) {
                k--;
                if (k == 0) {
                    return s;
                }
            }
        }

        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
