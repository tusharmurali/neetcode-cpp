# 146. LRU Cache

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/lru-cache/>  
- **NeetCode:** <https://neetcode.io/problems/lru-cache>  
- **Video:** <https://www.youtube.com/watch?v=7ABFKPK2hD4>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We store all `(key, value)` pairs in a list.  
To follow **LRU (Least Recently Used)** behavior:

- Whenever we **access** a key, we move it to the **end** of the list (most recently used).
- When inserting a new key:
    - If the key already exists → update its value and move it to the end.
    - If the cache is full → remove the **first** element (least recently used).
    - Then add the new key at the end.

```cpp
class LRUCache {
private:
    vector<pair<int, int>> cache;
    int capacity;

public:
    LRUCache(int capacity) {
        this->capacity = capacity;
    }

    int get(int key) {
        for (int i = 0; i < cache.size(); i++) {
            if (cache[i].first == key) {
                pair<int, int> tmp = cache[i];
                cache.erase(cache.begin() + i);
                cache.push_back(tmp);
                return tmp.second;
            }
        }
        return -1;
    }

    void put(int key, int value) {
        for (int i = 0; i < cache.size(); i++) {
            if (cache[i].first == key) {
                cache.erase(cache.begin() + i);
                cache.push_back({key, value});
                return;
            }
        }

        if (cache.size() == capacity) {
            cache.erase(cache.begin());
        }

        cache.push_back({key, value});
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for each $put()$ and $get()$ operation.
- Space complexity: $O(n)$

## 2. Doubly Linked List

We want all operations to be **O(1)** while still following **LRU (Least Recently Used)** rules.

To do that, we combine:

1. **Hash Map** -> quickly find a node by its key in O(1).
2. **Doubly Linked List** -> quickly move nodes to the **most recently used** position and remove the **least recently used** node from the other end in O(1).

We keep:

- The **most recently used** node near the **`right`** side.
- The **least recently used** node near the **`left`** side.

Whenever we:

- **Get** a key: move that node to the `right` (most recently used).
- **Put** a key:
    - If it exists: update value and move it to the `right`.
    - If it's new:
        - If at capacity: remove the leftmost real node (LRU).
        - Insert the new node at the `right`.

Dummy `left` and `right` nodes make insert/remove logic cleaner.

```cpp
class Node {
public:
    int key;
    int val;
    Node* prev;
    Node* next;

    Node(int k, int v) : key(k), val(v), prev(nullptr), next(nullptr) {}
};

class LRUCache {
private:
    int cap;
    unordered_map<int, Node*> cache;
    Node* left;
    Node* right;

    void remove(Node* node) {
        Node* prev = node->prev;
        Node* nxt = node->next;
        prev->next = nxt;
        nxt->prev = prev;
    }

    void insert(Node* node) {
        Node* prev = right->prev;
        prev->next = node;
        node->prev = prev;
        node->next = right;
        right->prev = node;
    }

public:
    LRUCache(int capacity) {
        cap = capacity;
        cache.clear();
        left = new Node(0, 0);
        right = new Node(0, 0);
        left->next = right;
        right->prev = left;
    }

    int get(int key) {
        if (cache.find(key) != cache.end()) {
            Node* node = cache[key];
            remove(node);
            insert(node);
            return node->val;
        }
        return -1;
    }

    void put(int key, int value) {
        if (cache.find(key) != cache.end()) {
            remove(cache[key]);
        }
        Node* newNode = new Node(key, value);
        cache[key] = newNode;
        insert(newNode);

        if (cache.size() > cap) {
            Node* lru = left->next;
            remove(lru);
            cache.erase(lru->key);
            delete lru;
        }
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each $put()$ and $get()$ operation.
- Space complexity: $O(n)$

## 3. Built-In Data Structure

Many languages provide a **built-in ordered map / dictionary** that:

- Stores key–value pairs
- Keeps track of the **order** in which keys were inserted or recently updated

This is perfect for an LRU cache:

- When we **access** a key (`get` or `put`), we mark it as **most recently used** by moving it to the "end" of the order.
- When the cache exceeds capacity, we remove the key that is at the **front** of the order (the least recently used).

So the ordered map itself handles:

- Fast lookups (like a normal hash map)
- Fast updates of usage order (moving keys to the end)
- Fast removal of the least recently used key (from the front)

This gives a clean and concise LRU implementation using library support.

```cpp
class LRUCache {
private:
    unordered_map<int, pair<int, list<int>::iterator>> cache;
    list<int> order;
    int capacity;

public:
    LRUCache(int capacity) {
        this->capacity = capacity;
    }

    int get(int key) {
        if (cache.find(key) == cache.end()) return -1;
        order.erase(cache[key].second);
        order.push_back(key);
        cache[key].second = --order.end();
        return cache[key].first;
    }

    void put(int key, int value) {
        if (cache.find(key) != cache.end()) {
            order.erase(cache[key].second);
        } else if (cache.size() == capacity) {
            int lru = order.front();
            order.pop_front();
            cache.erase(lru);
        }
        order.push_back(key);
        cache[key] = {value, --order.end()};
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each $put()$ and $get()$ operation.
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0146-lru-cache.cpp` in the NeetCode repo)

```cpp
/*
    Design data structure that follows constraints of an LRU cache

    Hash map + doubly linked list, left = LRU, right = MRU
    get: update to MRU, put: update to MRU, remove LRU if full

    Time: O(1)
    Space: O(capacity)
*/

class Node {
public:
    int k;
    int val;
    Node* prev;
    Node* next;
    
    Node(int key, int value) {
        k = key;
        val = value;
        prev = NULL;
        next = NULL;
    }
};

class LRUCache {
public:
    LRUCache(int capacity) {
        cap = capacity;
        
        left = new Node(0, 0);
        right = new Node(0, 0);
        
        left->next = right;
        right->prev = left;
    }
    
    int get(int key) {
        if (cache.find(key) != cache.end()) {
            remove(cache[key]);
            insert(cache[key]);
            return cache[key]->val;
        }
        return -1;
    }
    
    void put(int key, int value) {
        if (cache.find(key) != cache.end()) {
            remove(cache[key]);
            
            // Free allocated memory for the removed node
            delete cache[key];
        }
        cache[key] = new Node(key, value);
        insert(cache[key]);
        
        if (cache.size() > cap) {
            // remove from list & delete LRU from map
            Node* lru = left->next;
            remove(lru);
            cache.erase(lru->k);
            
            // Free allocated memory for the removed node
            delete lru;
        }
    }
private:
    int cap;
    unordered_map<int, Node*> cache; // {key -> node}
    Node* left;
    Node* right;
    
    // remove node from list
    void remove(Node* node) {
        Node* prev = node->prev;
        Node* next = node->next;
        
        prev->next = next;
        next->prev = prev;
    }
    
    // insert node at right
    void insert(Node* node) {
        Node* prev = right->prev;
        Node* next = right;
        
        prev->next = node;
        next->prev = node;
        
        node->prev = prev;
        node->next = next;
    }
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
```
