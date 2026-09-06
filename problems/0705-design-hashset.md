# 705. Design HashSet

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/design-hashset/>  
- **NeetCode:** <https://neetcode.io/problems/design-hashset>  
- **Video:** <https://www.youtube.com/watch?v=VymjPQUXjL8>  
- **Video approach:** 1. Brute Force  

[← Back to index](../INDEX.md)

## 1. Brute Force ▶ video

The simplest implementation uses a dynamic array to store all keys. For each operation, we search through the array linearly. This works correctly but is inefficient since every operation requires scanning potentially all stored elements.

```cpp
class MyHashSet {
private:
    vector<int> data;
public:
    MyHashSet() {}

    void add(int key) {
        if (find(data.begin(), data.end(), key) == data.end()) {
            data.push_back(key);
        }
    }

    void remove(int key) {
        auto it = find(data.begin(), data.end(), key);
        if (it != data.end()) {
            data.erase(it);
        }
    }

    bool contains(int key) {
        return find(data.begin(), data.end(), key) != data.end();
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for each function call.
- Space complexity: $O(n)$

## 2. Boolean Array

Since keys are constrained to [0, 1000000], we can use direct addressing with a boolean array. The index represents the key, and the boolean value indicates presence. This provides O(1) operations but uses fixed memory regardless of how many keys are stored.

```cpp
class MyHashSet {
private:
    vector<bool> data;
public:
    MyHashSet() : data(1000001, false) {}

    void add(int key) {
        data[key] = true;
    }

    void remove(int key) {
        data[key] = false;
    }

    bool contains(int key) {
        return data[key];
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each function call.
- Space complexity: $O(1000000)$ since the key is in the range $[0, 1000000]$.

## 3. Linked List

To reduce memory while handling collisions, we use separate chaining. An array of buckets stores linked lists, and keys are assigned to buckets using a hash function. Each operation traverses only the linked list in the relevant bucket, making average-case operations faster than the brute force approach.

```cpp
class MyHashSet {
private:
    struct ListNode {
        int key;
        ListNode* next;
        ListNode(int k) : key(k), next(nullptr) {}
    };

    vector<ListNode*> set;

    int hash(int key) {
        return key % set.size();
    }

public:
    MyHashSet() {
        set.resize(10000);
        for (auto& bucket : set) {
            bucket = new ListNode(0);
        }
    }

    void add(int key) {
        ListNode* cur = set[hash(key)];
        while (cur->next) {
            if (cur->next->key == key) {
                return;
            }
            cur = cur->next;
        }
        cur->next = new ListNode(key);
    }

    void remove(int key) {
        ListNode* cur = set[hash(key)];
        while (cur->next) {
            if (cur->next->key == key) {
                ListNode* temp = cur->next;
                cur->next = temp->next;
                delete temp;
                return;
            }
            cur = cur->next;
        }
    }

    bool contains(int key) {
        ListNode* cur = set[hash(key)];
        while (cur->next) {
            if (cur->next->key == key) {
                return true;
            }
            cur = cur->next;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(\frac{n}{k})$ for each function call.
- Space complexity: $O(k + m)$

> Where $n$ is the number of keys, $k$ is the size of the set ($10000$) and $m$ is the number of unique keys.

## 4. Binary Search Tree

Instead of linked lists for collision handling, we can use binary search trees (BSTs) in each bucket. This improves the worst-case time complexity from O(n/k) to O(log(n/k)) for each bucket, since BST operations are logarithmic in the number of nodes. The tradeoff is slightly more complex implementation.

```cpp
class BST {
private:
    struct TreeNode {
        int key;
        TreeNode* left;
        TreeNode* right;
        TreeNode(int k) : key(k), left(nullptr), right(nullptr) {}
    };

    TreeNode* insert(TreeNode* root, int key) {
        if (!root) return new TreeNode(key);
        if (key < root->key)
            root->left = insert(root->left, key);
        else if (key > root->key)
            root->right = insert(root->right, key);
        return root;
    }

    TreeNode* deleteNode(TreeNode* root, int key) {
        if (!root) return nullptr;
        if (key < root->key)
            root->left = deleteNode(root->left, key);
        else if (key > root->key)
            root->right = deleteNode(root->right, key);
        else {
            if (!root->left) {
                TreeNode* temp = root->right;
                delete root;
                return temp;
            }
            if (!root->right) {
                TreeNode* temp = root->left;
                delete root;
                return temp;
            }
            TreeNode* temp = minValueNode(root->right);
            root->key = temp->key;
            root->right = deleteNode(root->right, temp->key);
        }
        return root;
    }

    TreeNode* minValueNode(TreeNode* root) {
        while (root->left) root = root->left;
        return root;
    }

    bool search(TreeNode* root, int key) {
        if (!root) return false;
        if (key == root->key) return true;
        return key < root->key ? search(root->left, key) : search(root->right, key);
    }

    TreeNode* root;

public:
    BST() : root(nullptr) {}

    void add(int key) {
        root = insert(root, key);
    }

    void remove(int key) {
        root = deleteNode(root, key);
    }

    bool contains(int key) {
        return search(root, key);
    }
};

class MyHashSet {
private:
    const int size = 10000;
    vector<BST> buckets;

    int hash(int key) {
        return key % size;
    }

public:
    MyHashSet() : buckets(size) {}

    void add(int key) {
        int idx = hash(key);
        if (!contains(key)) {
            buckets[idx].add(key);
        }
    }

    void remove(int key) {
        int idx = hash(key);
        buckets[idx].remove(key);
    }

    bool contains(int key) {
        int idx = hash(key);
        return buckets[idx].contains(key);
    }
};
```

**Complexity**

- Time complexity: $O(\log (\frac{n}{k}))$ in average case, $O(\frac{n}{k})$ in worst case for each function call.
- Space complexity: $O(k + m)$

> Where $n$ is the number of keys, $k$ is the size of the set ($10000$) and $m$ is the number of unique keys.

## 5. Bit Manipulation

We can compress the boolean array approach by using individual bits instead of booleans. Each integer stores 32 bits, so we need only about 31251 integers to cover 1000000+ keys. We use bit operations to set, clear, and check individual bits. This reduces memory usage by a factor of 32 compared to a boolean array.

```cpp
class MyHashSet {
private:
    int set[31251];

    int getMask(int key) {
        return 1 << (key % 32);
    }

public:
    MyHashSet() {
        // key is in the range [0, 1000000]
        // 31251 * 32 = 1000032
        memset(set, 0, sizeof(set));
    }

    void add(int key) {
        set[key / 32] |= getMask(key);
    }

    void remove(int key) {
        if (contains(key)) {
            set[key / 32] ^= getMask(key);
        }
    }

    bool contains(int key) {
        return (set[key / 32] & getMask(key)) != 0;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each function call.
- Space complexity: $O(k)$

> Where $k$ is the size of the set $(31251)$.

## Standalone solution file (`cpp/0705-design-hashset.cpp` in the NeetCode repo)

```cpp
// Time: O(n)
// Space: O(n)

class MyHashSet {
public:
    void add(int key) {
        if (!contains(key)) {
            hashSet.push_back(key);
        }
    }

    void remove(int key) {
        auto k = find(hashSet.begin(), hashSet.end(), key);
        if (k != hashSet.end()) {
            hashSet.erase(k);
        }
    }

    bool contains(int key) {
        return (find(hashSet.begin(), hashSet.end(), key) != hashSet.end());
    }

private:
    vector<int> hashSet;
};
```
