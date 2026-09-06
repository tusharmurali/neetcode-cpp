# 460. LFU Cache

- **Difficulty:** Hard  
- **Pattern:** Linked List  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/lfu-cache/>  
- **NeetCode:** <https://neetcode.io/problems/lfu-cache>  
- **Video:** <https://www.youtube.com/watch?v=bLEIHn-DgoA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

An LFU (Least Frequently Used) cache evicts the element that has been accessed the fewest times. When there's a tie in frequency, we evict the least recently used among them. The simplest approach stores each key's value, frequency, and a timestamp. On eviction, we scan all entries to find the one with the minimum frequency (and earliest timestamp for ties).

```cpp
class LFUCache {
    struct Node {
        int value, freq, timestamp;
        Node(int v, int f, int t) : value(v), freq(f), timestamp(t) {}
    };

    int capacity, timestamp;
    unordered_map<int, Node*> cache;

public:
    LFUCache(int capacity) : capacity(capacity), timestamp(0) {}

    int get(int key) {
        if (cache.find(key) == cache.end()) return -1;

        cache[key]->freq++;
        cache[key]->timestamp = ++timestamp;
        return cache[key]->value;
    }

    void put(int key, int value) {
        if (capacity <= 0) return;

        timestamp++;
        if (cache.find(key) != cache.end()) {
            cache[key]->value = value;
            cache[key]->freq++;
            cache[key]->timestamp = timestamp;
            return;
        }

        if (cache.size() >= capacity) {
            int minFreq = INT_MAX, minTimestamp = INT_MAX, lfuKey = -1;

            for (const auto& [k, node] : cache) {
                if (node->freq < minFreq || (node->freq == minFreq && node->timestamp < minTimestamp)) {
                    minFreq = node->freq;
                    minTimestamp = node->timestamp;
                    lfuKey = k;
                }
            }
            delete cache[lfuKey];
            cache.erase(lfuKey);
        }

        cache[key] = new Node(value, 1, timestamp);
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $get()$ function call.
    - $O(n)$ time for each $put()$ function call.
- Space complexity: $O(n)$

## 2. Doubly Linked List

To achieve O(1) operations, we need fast access to a key's current node and to the least recently used node inside each frequency group. We use a hash map from frequency to a doubly linked list of cache nodes, and a separate key-to-node map for direct access. Each linked list maintains recency order within one frequency bucket, so the head is the eviction candidate for ties. We also track the current minimum frequency to quickly find which list to evict from.

```cpp
class LFUCache {
    struct ListNode {
        int key;
        int val;
        int freq;
        ListNode* prev;
        ListNode* next;

        ListNode(int key, int val) : key(key), val(val), freq(1), prev(nullptr), next(nullptr) {}
    };

    struct LinkedList {
        ListNode* left;
        ListNode* right;
        int size;

        LinkedList() {
            left = new ListNode(0, 0);
            right = new ListNode(0, 0);
            left->next = right;
            right->prev = left;
            size = 0;
        }

        ~LinkedList() {
            delete left;
            delete right;
        }

        int length() {
            return size;
        }

        void pushRight(ListNode* node) {
            ListNode* prev = right->prev;
            prev->next = node;
            node->prev = prev;
            node->next = right;
            right->prev = node;
            size++;
        }

        void pop(ListNode* node) {
            ListNode* prev = node->prev;
            ListNode* next = node->next;
            prev->next = next;
            next->prev = prev;
            node->prev = nullptr;
            node->next = nullptr;
            size--;
        }

        ListNode* popLeft() {
            ListNode* node = left->next;
            pop(node);
            return node;
        }
    };

    int capacity;
    int lfuCount;
    unordered_map<int, ListNode*> nodeMap; // Map key -> node
    unordered_map<int, LinkedList*> listMap; // Map frequency -> linked list

    void counter(ListNode* node) {
        int count = node->freq;
        listMap[count]->pop(node);

        if (count == lfuCount && listMap[count]->length() == 0) {
            lfuCount++;
        }

        node->freq++;
        if (!listMap.count(node->freq)) {
            listMap[node->freq] = new LinkedList();
        }
        listMap[node->freq]->pushRight(node);
    }

public:
    LFUCache(int capacity) : capacity(capacity), lfuCount(0) {}

    ~LFUCache() {
        for (auto& pair : nodeMap) {
            delete pair.second;
        }
        for (auto& pair : listMap) {
            delete pair.second;
        }
    }

    int get(int key) {
        if (nodeMap.find(key) == nodeMap.end()) {
            return -1;
        }
        ListNode* node = nodeMap[key];
        counter(node);
        return node->val;
    }

    void put(int key, int value) {
        if (capacity == 0) {
            return;
        }

        if (nodeMap.find(key) != nodeMap.end()) {
            ListNode* node = nodeMap[key];
            node->val = value;
            counter(node);
            return;
        }

        if (nodeMap.size() == capacity) {
            ListNode* toRemove = listMap[lfuCount]->popLeft();
            nodeMap.erase(toRemove->key);
            delete toRemove;
        }

        ListNode* node = new ListNode(key, value);
        nodeMap[key] = node;
        if (!listMap.count(1)) {
            listMap[1] = new LinkedList();
        }
        listMap[1]->pushRight(node);
        lfuCount = 1;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $get()$ and $put()$ function calls.
- Space complexity: $O(n)$
