# 1122. Relative Sort Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/relative-sort-array/>  
- **NeetCode:** <https://neetcode.io/problems/relative-sort-array>  
- **Video:** <https://www.youtube.com/watch?v=OPvcR1e4lfg>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The straightforward approach is to process each element in `arr2` in order and find all matching elements in `arr1`. For each value in `arr2`, we scan through `arr1`, collect all occurrences, and mark them as used. After processing all elements from `arr2`, any remaining elements in `arr1` are sorted and appended to the result.

This approach directly mimics the problem requirements: first place elements in the order specified by `arr2`, then append the rest in sorted order.

```cpp
class Solution {
public:
    vector<int> relativeSortArray(vector<int>& arr1, vector<int>& arr2) {
        vector<int> res;

        for (int num2 : arr2) {
            for (int i = 0; i < arr1.size(); i++) {
                if (arr1[i] == num2) {
                    res.push_back(arr1[i]);
                    arr1[i] = -1;
                }
            }
        }

        sort(arr1.begin(), arr1.end());
        for (int i = res.size(); i < arr1.size(); i++) {
            res.push_back(arr1[i]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n + n \log n)$
- Space complexity:
    - $O(1)$ or $O(n)$ depending on the sorting algorithm.
    - $O(n)$ space for the output list.

> Where $n$ is the size of the array $arr1$, and $m$ is the size of the array $arr2$.

## 2. Hash Map

Instead of repeatedly scanning `arr1` for each element in `arr2`, we can first count the frequency of each element in `arr1` using a hash map. This allows O(1) lookups when building the result.

We also use a set to quickly identify which elements from `arr1` are not in `arr2`. These "extra" elements are collected separately, sorted, and appended to the end of the result.

```cpp
class Solution {
public:
    vector<int> relativeSortArray(vector<int>& arr1, vector<int>& arr2) {
        unordered_set<int> arr2Set(arr2.begin(), arr2.end());
        unordered_map<int, int> count;
        vector<int> end;

        for (int num : arr1) {
            if (!arr2Set.count(num)) end.push_back(num);
            count[num]++;
        }

        sort(end.begin(), end.end());
        vector<int> res;

        for (int num : arr2) {
            for (int i = 0; i < count[num]; i++) {
                res.push_back(num);
            }
        }

        res.insert(res.end(), end.begin(), end.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m + n \log n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $arr1$, and $m$ is the size of the array $arr2$.

## 3. Hash Map (Optimal)

This is a cleaner version of the hash map approach. Instead of tracking elements separately, we count all elements first, then process them in two phases: first by `arr2` order, then by remaining keys in sorted order.

By removing keys from the hash map as we process `arr2`, whatever remains in the map represents elements not in `arr2`. We sort these remaining keys and append their occurrences to complete the result.

```cpp
class Solution {
public:
    vector<int> relativeSortArray(vector<int>& arr1, vector<int>& arr2) {
        unordered_map<int, int> count;
        for (int num : arr1) {
            count[num]++;
        }

        vector<int> res;
        for (int num : arr2) {
            for (int i = 0; i < count[num]; i++) {
                res.push_back(num);
            }
            count.erase(num);
        }

        vector<int> remaining;
        for (auto& [num, freq] : count) {
            for (int i = 0; i < freq; i++) {
                remaining.push_back(num);
            }
        }

        sort(remaining.begin(), remaining.end());
        res.insert(res.end(), remaining.begin(), remaining.end());

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m + n \log n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $arr1$, and $m$ is the size of the array $arr2$.

## 4. Counting Sort

When the range of values in `arr1` is bounded and relatively small, counting sort becomes very efficient. We create an array where the index represents the value and the content represents the count.

The beauty of this approach is that the "remaining elements" are automatically sorted by simply iterating through the count array from index 0 to the maximum value. Elements that appear in `arr2` are handled first, then we sweep through the count array for everything else.

```cpp
class Solution {
public:
    vector<int> relativeSortArray(vector<int>& arr1, vector<int>& arr2) {
        int max_val = *max_element(arr1.begin(), arr1.end());
        vector<int> count(max_val + 1, 0);

        for (int num : arr1) count[num]++;

        vector<int> res;
        for (int num : arr2) {
            while (count[num]-- > 0) res.push_back(num);
        }

        for (int num = 0; num <= max_val; num++) {
            while (count[num]-- > 0) res.push_back(num);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m + M)$
- Space complexity:
    - $O(M)$ extra space.
    - $O(n)$ space for the output list.

> Where $n$ is the size of the array $arr1$, $m$ is the size of the array $arr2$, and $M$ is the maximum value in the array $arr1$.

## 5. Custom Sort

Instead of manually placing elements, we can leverage the built-in sorting algorithm with a custom comparator. The key insight is to assign each element a "priority" based on its position in `arr2`.

Elements in `arr2` get their index as priority (lower index = higher priority in the result). Elements not in `arr2` get a large priority (like 1000 + value) so they sort after all `arr2` elements, and among themselves they sort by their actual value.

```cpp
class Solution {
public:
    vector<int> relativeSortArray(vector<int>& arr1, vector<int>& arr2) {
        unordered_map<int, int> index;
        for (int i = 0; i < arr2.size(); i++) {
            index[arr2[i]] = i;
        }

        sort(arr1.begin(), arr1.end(), [&](int a, int b) {
            int ia = index.count(a) ? index[a] : 1000 + a;
            int ib = index.count(b) ? index[b] : 1000 + b;
            return ia < ib;
        });

        return arr1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m + n \log n)$
- Space complexity:
    - $O(m)$ extra space.
    - $O(n)$ space for the output list.

> Where $n$ is the size of the array $arr1$, and $m$ is the size of the array $arr2$.
