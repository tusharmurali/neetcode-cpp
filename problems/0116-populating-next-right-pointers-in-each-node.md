# 116. Populating Next Right Pointers In Each Node

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/populating-next-right-pointers-in-each-node/>  
- **NeetCode:** <https://neetcode.io/problems/populating-next-right-pointers-in-each-node>  
- **Video:** <https://www.youtube.com/watch?v=U4hFQCa1Cq0>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

Level-order traversal naturally groups nodes by their depth, which is exactly what we need to connect nodes on the same level. As we process each level, the next node in the queue is the right neighbor of the current node.

By tracking the size of each level, we can connect all nodes within a level while avoiding connecting the last node of one level to the first node of the next.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* next;

    Node() : val(0), left(NULL), right(NULL), next(NULL) {}

    Node(int _val) : val(_val), left(NULL), right(NULL), next(NULL) {}

    Node(int _val, Node* _left, Node* _right, Node* _next)
        : val(_val), left(_left), right(_right), next(_next) {}
};
*/

class Solution {
public:
    Node* connect(Node* root) {
        if (!root) return nullptr;

        queue<Node*> q;
        q.push(root);

        while (!q.empty()) {
            int levelSize = q.size();
            while (levelSize > 0) {
                Node* node = q.front();
                q.pop();
                if (levelSize > 1) {
                    node->next = q.front();
                }
                if (node->left) {
                    q.push(node->left);
                }
                if (node->right) {
                    q.push(node->right);
                }
                levelSize--;
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(\log n)$

## 2. Depth First Search

Using `dfs`, we can traverse the tree and track the rightmost node seen at each depth. When we visit a node, we connect the previous rightmost node at that depth to the current node, then update the rightmost reference.

A hash map stores the most recently visited node at each depth, allowing us to build the `next` pointers as we traverse left to right.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* next;

    Node() : val(0), left(NULL), right(NULL), next(NULL) {}

    Node(int _val) : val(_val), left(NULL), right(NULL), next(NULL) {}

    Node(int _val, Node* _left, Node* _right, Node* _next)
        : val(_val), left(_left), right(_right), next(_next) {}
};
*/

class Solution {
public:
    Node* connect(Node* root) {
        unordered_map<int, Node*> mp;
        dfs(root, 0, mp);
        return root;
    }

private:
    void dfs(Node* node, int depth, unordered_map<int, Node*>& mp) {
        if (!node) return;

        if (mp.find(depth) == mp.end()) {
            mp[depth] = node;
        } else {
            mp[depth]->next = node;
            mp[depth] = node;
        }

        dfs(node->left, depth + 1, mp);
        dfs(node->right, depth + 1, mp);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(\log n)$

## 3. Depth First Search (Optimal)

In a perfect binary tree, every node has either zero or two children, and all leaves are at the same level. This structure lets us establish `next` pointers without extra space for tracking.

For any node with children, its `left` child's `next` is always its `right` child. And if the node has a `next` pointer, its `right` child's `next` is the `left` child of the node's `next` neighbor. This recursive pattern connects the entire tree.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* next;

    Node() : val(0), left(NULL), right(NULL), next(NULL) {}

    Node(int _val) : val(_val), left(NULL), right(NULL), next(NULL) {}

    Node(int _val, Node* _left, Node* _right, Node* _next)
        : val(_val), left(_left), right(_right), next(_next) {}
};
*/

class Solution {
public:
    Node* connect(Node* root) {
        if (!root) return root;

        if (root->left) {
            root->left->next = root->right;
            if (root->next) {
                root->right->next = root->next->left;
            }

            connect(root->left);
            connect(root->right);
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(\log n)$ for the recursion stack.

## 4. Breadth First Search (Optimal)

Instead of using a queue, we can leverage the `next` pointers we've already established to traverse each level. We process the tree level by level, using the current level's `next` pointers to iterate horizontally while setting up the connections for the next level.

Two pointers track our position: one for the current node being processed, and one for the leftmost node of the next level (so we know where to start the next iteration).

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* next;

    Node() : val(0), left(NULL), right(NULL), next(NULL) {}

    Node(int _val) : val(_val), left(NULL), right(NULL), next(NULL) {}

    Node(int _val, Node* _left, Node* _right, Node* _next)
        : val(_val), left(_left), right(_right), next(_next) {}
};
*/

class Solution {
public:
    Node* connect(Node* root) {
        if (!root) return nullptr;

        Node* cur = root, *nxt = root->left;

        while (cur && nxt) {
            cur->left->next = cur->right;
            if (cur->next) {
                cur->right->next = cur->next->left;
            }

            cur = cur->next;
            if (!cur) {
                cur = nxt;
                nxt = cur->left;
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0116-populating-next-right-pointers-in-each-node.cpp` in the NeetCode repo)

```cpp
/*
  You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:
  
  struct Node {
    int val;
    Node *left;
    Node *right;
    Node *next;
  }
  
  Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.
  Initially, all next pointers are set to NULL.

  Ex. Input: root = [1,2,3,4,5,6,7]
      Output: [1,#,2,3,#,4,5,6,7,#]
      Explanation: Given the above perfect binary tree (Figure A), your function should populate each next pointer to point to its next right node,
      just like in Figure B. The serialized output is in level order as connected by the next pointers, with '#' signifying the end of each level.

  Time  : O(N)
  Space : O(N)
*/

/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;
    Node* next;

    Node() : val(0), left(NULL), right(NULL), next(NULL) {}

    Node(int _val) : val(_val), left(NULL), right(NULL), next(NULL) {}

    Node(int _val, Node* _left, Node* _right, Node* _next)
        : val(_val), left(_left), right(_right), next(_next) {}
};
*/

class Solution {
public:
    Node* connect(Node* root) {
        if(root == NULL || (root -> right == NULL && root -> left == NULL))
            return root;
        queue <Node*>q;
        q.push(root);

        while(!q.empty()) {
            int size = q.size();
            Node* temp = NULL;

            for(int i = 0 ; i < size ; i++) {
                Node* front = q.front();

                if(temp != NULL)
                    temp -> next = front;
                temp = front;

                if(front -> left) {
                    q.push(front -> left);
                    q.push(front -> right);
                }
                q.pop();
            }
        }
        return root;
    }
};
```
