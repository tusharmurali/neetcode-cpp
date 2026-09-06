# 981. Time Based Key Value Store

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/time-based-key-value-store/>  
- **NeetCode:** <https://neetcode.io/problems/time-based-key-value-store>  
- **Video:** <https://www.youtube.com/watch?v=fu2cD_6E8Hw>  
- **Video approach:** 3. Binary Search (Array)  

[← Back to index](../INDEX.md)

## 1. Brute Force

We want to store values for a key along with timestamps, and when someone asks for a value at a given time, we must return the **latest value set at or before that timestamp**.

The brute-force idea is:
store everything as-is, and while retrieving, **look through all timestamps** for that key and pick the best match.
It's easy to implement, but slow because we scan all timestamps every time we call `get()`.

```cpp
class TimeMap {
public:
    unordered_map<string, unordered_map<int, vector<string>>> keyStore;
    TimeMap() {}

    void set(string key, string value, int timestamp) {
        keyStore[key][timestamp].push_back(value);
    }

    string get(string key, int timestamp) {
        if (keyStore.find(key) == keyStore.end()) {
            return "";
        }
        int seen = -1;
        for (const auto& [time, _] : keyStore[key]) {
            if (time <= timestamp) {
                seen = max(seen, time);
            }
        }
        return seen == -1 ? "" : keyStore[key][seen].back();
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $set()$ and $O(n)$ for $get()$.
- Space complexity: $O(m * n)$

> Where $n$ is the total number of unique timestamps associated with a key and $m$ is the total number of keys.

## 2. Binary Search (Sorted Map)

For each key, we store all its `(timestamp, value)` pairs in **sorted order by timestamp**.

When we call `get(key, timestamp)`, we don’t want to scan everything.  
Instead, we want to quickly find the **largest timestamp ≤ given timestamp** for that key.

Because the timestamps are sorted, we can use **binary search** to find this position in `O(log n)` time:

- If we find an exact match, return its value.
- Otherwise, return the value at the closest smaller timestamp.
- If there is no smaller or equal timestamp, return `""`.

So the idea is:

- Per key → keep timestamps sorted.
- On get → binary search over those timestamps.

```cpp
class TimeMap {
public:
    unordered_map<string, map<int, string>> m;

    TimeMap() {}

    void set(string key, string value, int timestamp) {
        m[key].insert({timestamp, value});
    }

    string get(string key, int timestamp) {
        auto it = m[key].upper_bound(timestamp);
        return it == m[key].begin() ? "" : prev(it)->second;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ or $O(\log n)$ for $set()$ depending on the language and $O(\log n)$ for $get()$.
- Space complexity: $O(m * n)$

> Where $n$ is the total number of values associated with a key and $m$ is the total number of keys.

## 3. Binary Search (Array) ▶ video

Each key stores its values in the order they were inserted, and timestamps are **guaranteed to be increasing** for each key.  
This means we can keep a simple list of `(value, timestamp)` pairs for every key.

To answer a `get(key, timestamp)` query, we only need to find the **latest timestamp that is ≤ the given timestamp**.  
Because timestamps are sorted, we can use **binary search** to quickly find this position instead of scanning everything.

This gives an efficient and clean approach:  
store values in arrays, then binary-search timestamps when retrieving.

```cpp
class TimeMap {
private:
    unordered_map<string, vector<pair<int, string>>> keyStore;

public:
    TimeMap() {}

    void set(string key, string value, int timestamp) {
        keyStore[key].emplace_back(timestamp, value);
    }

    string get(string key, int timestamp) {
        auto& values = keyStore[key];
        int left = 0, right = values.size() - 1;
        string result = "";

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (values[mid].first <= timestamp) {
                result = values[mid].second;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $set()$ and $O(\log n)$ for $get()$.
- Space complexity: $O(m * n)$

> Where $n$ is the total number of values associated with a key and $m$ is the total number of keys.

## Standalone solution file (`cpp/0981-time-based-key-value-store.cpp` in the NeetCode repo)

```cpp
/*
    Design time-based key-value structure, multiple vals at diff times

    Hash map, since timestamps are naturally in order, binary search

    Time: O(log n)
    Space: O(n)
*/

class TimeMap {
public:
    TimeMap() {
        
    }
    
    void set(string key, string value, int timestamp) {
        m[key].push_back({timestamp, value});
    }
    
    string get(string key, int timestamp) {
        if (m.find(key) == m.end()) {
            return "";
        }
        
        int low = 0;
        int high = m[key].size() - 1;
        
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (m[key][mid].first < timestamp) {
                low = mid + 1;
            } else if (m[key][mid].first > timestamp) {
                high = mid - 1;
            } else {
                return m[key][mid].second;
            }
        }
        
        if (high >= 0) {
            return m[key][high].second;
        }
        return "";
    }
private:
    unordered_map<string, vector<pair<int, string>>> m;
};

/**
 * Your TimeMap object will be instantiated and called as such:
 * TimeMap* obj = new TimeMap();
 * obj->set(key,value,timestamp);
 * string param_2 = obj->get(key,timestamp);
 */
```
