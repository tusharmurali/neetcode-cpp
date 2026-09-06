# 706. Design HashMap

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/design-hashmap/>  
- **NeetCode:** <https://neetcode.io/problems/design-hashmap>  
- **Video:** <https://www.youtube.com/watch?v=cNWsgbKwwoU>  
- **Video approach:** 2. Linked List  

[← Back to index](../INDEX.md)

## 1. Array

Since keys are constrained to the range [0, 1000000], we can use direct addressing. We allocate an array where the index represents the key and the value at that index is the stored value. We use -1 to indicate that a key is not present. This gives O(1) time for all operations at the cost of fixed memory usage regardless of how many keys are actually stored.

```cpp
class MyHashMap {
private:
    vector<int> map;

public:
    MyHashMap() : map(1000001, -1) {}

    void put(int key, int value) {
        map[key] = value;
    }

    int get(int key) {
        return map[key];
    }

    void remove(int key) {
        map[key] = -1;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each function call.
- Space complexity: $O(1000000)$ since the key is in the range $[0, 1000000]$.

## 2. Linked List ▶ video

To reduce memory usage, we use a hash table with separate chaining. We create an array of buckets (smaller than the key range) and use a hash function (key modulo bucket count) to determine which bucket a key belongs to. Each bucket is a linked list that stores key-value pairs. This handles collisions by chaining multiple entries in the same bucket.

```cpp
class MyHashMap {
private:
    struct ListNode {
        int key, val;
        ListNode* next;

        ListNode(int key = -1, int val = -1, ListNode* next = nullptr)
            : key(key), val(val), next(next) {}
    };

    vector<ListNode*> map;
    int hash(int key) {
        return key % map.size();
    }

public:
    MyHashMap() {
        map.resize(1000);
        for (auto& bucket : map) {
            bucket = new ListNode(0);
        }
    }

    void put(int key, int value) {
        ListNode* cur = map[hash(key)];
        while (cur->next) {
            if (cur->next->key == key) {
                cur->next->val = value;
                return;
            }
            cur = cur->next;
        }
        cur->next = new ListNode(key, value);
    }

    int get(int key) {
        ListNode* cur = map[hash(key)]->next;
        while (cur) {
            if (cur->key == key) {
                return cur->val;
            }
            cur = cur->next;
        }
        return -1;
    }

    void remove(int key) {
        ListNode* cur = map[hash(key)];
        while (cur->next) {
            if (cur->next->key == key) {
                ListNode* tmp = cur->next;
                cur->next = cur->next->next;
                delete tmp;
                return;
            }
            cur = cur->next;
        }
    }
};
```

**Complexity**

- Time complexity: $O(\frac{n}{k})$ for each function call.
- Space complexity: $O(k + m)$

> Where $n$ is the number of keys, $k$ is the size of the map ($1000$) and $m$ is the number of unique keys.

## Standalone solution file (`cpp/0706-design-hashmap.cpp` in the NeetCode repo)

```cpp
/*
    Design a HashMap without using any built-in hash table libraries.

    Designing a hash table using the chaining method, where a vector holds a list of pairs representing the key-value mappings.

    Time: O(n)
    Space: O(n)
*/

class MyHashMap {
public:
    const int N = 10010;
    vector<list<pair<int, int>>> h; 

    /** Initialize your data structure here. */
    MyHashMap() {
        h = vector<list<pair<int, int>>>(N);
    }
    
    list<pair<int, int>>::iterator find(int key) {
        int t = key % N;
        for (auto it = h[t].begin(); it != h[t].end(); it ++ ) {
            if (it->first == key)
                return it;
        }
        return h[t].end();
    }

    /** value will always be non-negative. */
    void put(int key, int value) {
        auto t = key % N;
        auto it = find(key);
        if (it == h[t].end()) h[t].push_back({key, value});
        else it->second = value;
    }
    
    /** Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key */
    int get(int key) {
        auto t = key % N;
        auto it = find(key);
        if (it != h[t].end()) return it->second;
        return -1;
    }
    
    /** Removes the mapping of the specified value key if this map contains a mapping for the key */
    void remove(int key) {
        auto t = key % N;
        auto it = find(key);
        if (it != h[t].end()) h[t].erase(it);
    }
};

/**
 * Your MyHashMap object will be instantiated and called as such:
 * MyHashMap* obj = new MyHashMap();
 * obj->put(key,value);
 * int param_2 = obj->get(key);
 * obj->remove(key);
 */
```
