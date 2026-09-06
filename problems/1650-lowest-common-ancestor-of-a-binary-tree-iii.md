# 1650. Lowest Common Ancestor of a Binary Tree III

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/>  
- **NeetCode:** <https://neetcode.io/problems/lowest-common-ancestor-of-a-binary-tree-iii>  

[← Back to index](../INDEX.md)

## 1. Hash Set

Since each node has a parent pointer, we can trace the path from `p` to the root and store all visited nodes in a set. Then we trace from `q` upward until we find a node that already exists in the set. This intersection point is the lowest common ancestor.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* parent;
};
*/

class Solution {
public:
    Node* lowestCommonAncestor(Node* p, Node* q) {
        unordered_set<Node*> seen;
        while (p) {
            seen.insert(p);
            p = p->parent;
        }
        while (q) {
            if (seen.count(q)) return q;
            q = q->parent;
        }
        return nullptr;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration - I

If we know the depth of both nodes, we can align them first. We move the deeper node upward until both nodes are at the same depth. Then we move both nodes upward in lockstep until they meet. The meeting point is the LCA. This avoids using extra space for a hash set.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* parent;
};
*/

class Solution {
public:
    Node* lowestCommonAncestor(Node* p, Node* q) {
        int h1 = height(p), h2 = height(q);
        if (h2 < h1) {
            swap(p, q);
            swap(h1, h2);
        }
        int diff = h2 - h1;
        while (diff-- > 0) {
            q = q->parent;
        }
        while (p != q) {
            p = p->parent;
            q = q->parent;
        }
        return p;
    }

private:
    int height(Node* node) {
        int h = 0;
        while (node) {
            h++;
            node = node->parent;
        }
        return h;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Iteration - II

This approach is similar to finding the intersection of two linked lists. We use two pointers starting at `p` and `q`. When a pointer reaches the root (`null`), we redirect it to the other starting node. After at most two passes, both pointers will have traveled the same total distance and will meet at the LCA.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* parent;
};
*/

class Solution {
public:
    Node* lowestCommonAncestor(Node* p, Node* q) {
        Node* ptr1 = p;
        Node* ptr2 = q;
        while (ptr1 != ptr2) {
            ptr1 = ptr1 ? ptr1->parent : q;
            ptr2 = ptr2 ? ptr2->parent : p;
        }
        return ptr1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
