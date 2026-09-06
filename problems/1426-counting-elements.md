# 1426. Counting Elements

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/counting-elements/>  
- **NeetCode:** <https://neetcode.io/problems/counting-elements>  

[← Back to index](../INDEX.md)

## 1. Search with Array

For each element `x` in the array, we need to check whether `x + 1` also exists in the array. The straightforward approach is to scan through the entire array for each element to verify if its successor is present. While this works correctly, it requires a linear search for every element.

```cpp
class Solution {
public:
    int countElements(vector<int>& arr) {
        int count = 0;
        for (auto x : arr) {
            if (integerInArray(arr, x + 1)) {
                count++;
            }
        }
        return count;
    }

    bool integerInArray(vector<int>& arr, int target) {
        for (auto x : arr) {
            if (x == target) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(N^2)$
- Space complexity: $O(1)$ constant space

> Where $N$ is the length of the input array `arr`.

## 2. Search with HashSet

The brute force approach is slow because checking if `x + 1` exists requires scanning the entire array. A hash set provides `O(1)` lookup time, so we can first store all elements in a set, then check for each element's successor in constant time.

```cpp
class Solution {
public:
    int countElements(vector<int>& arr) {
        unordered_set<int> hashSet(arr.begin(), arr.end());
        int count = 0;
        for (int x : arr) {
            if (hashSet.find(x + 1) != hashSet.end()) {
                count++;
            }
        }
        return count;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the length of the input array `arr`.

## 3. Search with Sorted Array

Sorting brings equal elements together and places consecutive values next to each other. After sorting, we can traverse the array once and track "runs" of identical values. When we encounter a new value that is exactly one more than the previous value, all elements in the previous run satisfy the condition.

```cpp
class Solution {
public:
    int countElements(vector<int>& arr) {
        std::sort(arr.begin(), arr.end());
        int count = 0;
        int runLength = 1;
        for (int i = 1; i < arr.size(); i++) {
            if (arr[i - 1] != arr[i]) {
                if (arr[i - 1] + 1 == arr[i]) {
                    count += runLength;
                }
                runLength = 0;
            }
            runLength++;
        }
        return count;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: varies from $O(N)$ to $O(1)$
    - The overall space complexity is dependent on the space complexity of the sorting algorithm you're using. The space complexity of sorting algorithms built into programming languages are generally anywhere from $O(N)$ to $O(1)$.

> Where $N$ is the length of the input array `arr`.
