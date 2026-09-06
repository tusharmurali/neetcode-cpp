# 352. Data Stream as Disjoint Intervals

- **Difficulty:** Hard  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/data-stream-as-disjoint-intervals/>  
- **NeetCode:** <https://neetcode.io/problems/data-stream-as-disjoint-intervals>  
- **Video:** <https://www.youtube.com/watch?v=FavoZjPIWpo>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Sorting)

The simplest approach is to store all incoming numbers in a list and compute the intervals on demand. When `getIntervals()` is called, we sort the list and scan through it to identify consecutive sequences. Two numbers belong to the same interval if they differ by exactly `1`.

```cpp
class SummaryRanges {
private:
    vector<int> arr;

public:
    SummaryRanges() {}

    void addNum(int value) {
        arr.push_back(value);
    }

    vector<vector<int>> getIntervals() {
        vector<vector<int>> res;
        if (arr.empty()) return res;

        sort(arr.begin(), arr.end());
        int start = arr[0];
        for (int i = 1; i < arr.size(); i++) {
            if (arr[i] - arr[i - 1] > 1) {
                res.push_back({start, arr[i - 1]});
                start = arr[i];
            }
        }
        res.push_back({start, arr.back()});
        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $addNum()$ function call.
    - $O(n \log n)$ time for each $getIntervals()$ function call.
- Space complexity: $O(n)$

## 2. Hash Set + Sorting

The brute force approach stores duplicates, which wastes space and processing time during sorting. By using a hash set instead of a list, we automatically eliminate duplicates. This makes the interval computation cleaner since we only deal with unique values.

```cpp
class SummaryRanges {
private:
    set<int> arr;

public:
    SummaryRanges() {}

    void addNum(int value) {
        arr.insert(value);
    }

    vector<vector<int>> getIntervals() {
        vector<vector<int>> res;
        if (arr.empty()) return res;

        vector<int> lst(arr.begin(), arr.end());
        int start = lst[0];

        for (int i = 1; i < lst.size(); i++) {
            if (lst[i] - lst[i - 1] > 1) {
                res.push_back({start, lst[i - 1]});
                start = lst[i];
            }
        }
        res.push_back({start, lst.back()});
        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $addNum()$ function call.
    - $O(n \log n)$ time for each $getIntervals()$ function call.
- Space complexity: $O(n)$

## 3. Ordered Map

Using an ordered map (like TreeMap or SortedDict), we can maintain elements in sorted order as they are inserted. This eliminates the need to sort during `getIntervals()`. We simply iterate through the keys in order and merge consecutive numbers into intervals on the fly.

```cpp
class SummaryRanges {
private:
    map<int, bool> treeMap;

public:
    SummaryRanges() {}

    void addNum(int value) {
        treeMap[value] = true;
    }

    vector<vector<int>> getIntervals() {
        vector<vector<int>> res;
        for (auto& [n, _] : treeMap) {
            if (!res.empty() && res.back()[1] + 1 == n) {
                res.back()[1] = n;
            } else {
                res.push_back({n, n});
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(\log n)$ time for each $addNum()$ function call.
    - $O(n)$ time for each $getIntervals()$ function call.
- Space complexity: $O(n)$

## 4. Ordered Set

An ordered set provides the same benefits as an ordered map but with simpler semantics when we only need to track the presence of numbers. Elements are kept sorted automatically, and duplicates are ignored. The interval construction logic remains the same: iterate in order and merge consecutive numbers.

```cpp
class SummaryRanges {
private:
    set<int> orderedSet;

public:
    SummaryRanges() {}

    void addNum(int value) {
        orderedSet.insert(value);
    }

    vector<vector<int>> getIntervals() {
        vector<vector<int>> res;
        for (int n : orderedSet) {
            if (!res.empty() && res.back()[1] + 1 == n) {
                res.back()[1] = n;
            } else {
                res.push_back({n, n});
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(\log n)$ time for each $addNum()$ function call.
    - $O(n)$ time for each $getIntervals()$ function call.
- Space complexity: $O(n)$
