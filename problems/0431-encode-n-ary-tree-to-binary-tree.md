# 431. Encode N-ary Tree to Binary Tree

- **Difficulty:** Hard  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/encode-n-ary-tree-to-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/encode-n-ary-tree-to-binary-tree>  

[← Back to index](../INDEX.md)

## 1. BFS (Breadth-First Search) Traversal

To encode an N-ary tree into a binary tree, we need a consistent rule for representing multiple children. The standard approach is the "left-child right-sibling" representation: the first child of an N-ary node becomes the left child of the binary node, and subsequent siblings are chained as right children. Using BFS, we process nodes level by level, building the binary tree structure while maintaining the parent-child relationships through a queue.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> children;

    Node() {}

    Node(int _val) {
        val = _val;
    }

    Node(int _val, vector<Node*> _children) {
        val = _val;
        children = _children;
    }
};
*/

/*
// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};
*/

class Codec {
public:
    // Encodes an n-ary tree to a binary tree.
    TreeNode* encode(Node* root) {
        if (!root) return nullptr;

        TreeNode* rootNode = new TreeNode(root->val);
        queue<pair<TreeNode*, Node*>> q;
        q.push({rootNode, root});

        while (!q.empty()) {
            auto [parent, curr] = q.front();
            q.pop();

            TreeNode* prevBNode = nullptr;
            TreeNode* headBNode = nullptr;

            // Traverse each child one by one
            for (Node* child : curr->children) {
                TreeNode* newBNode = new TreeNode(child->val);
                if (prevBNode) {
                    prevBNode->right = newBNode;
                } else {
                    headBNode = newBNode;
                }
                prevBNode = newBNode;
                q.push({newBNode, child});
            }

            // Use the first child in the left node of parent
            parent->left = headBNode;
        }

        return rootNode;
    }

    // Decodes your binary tree to an n-ary tree.
    Node* decode(TreeNode* data) {
        if (!data) return nullptr;

        Node* rootNode = new Node(data->val, vector<Node*>());
        queue<pair<Node*, TreeNode*>> q;
        q.push({rootNode, data});

        while (!q.empty()) {
            auto [parent, curr] = q.front();
            q.pop();

            TreeNode* firstChild = curr->left;
            TreeNode* sibling = firstChild;

            while (sibling) {
                Node* newNode = new Node(sibling->val, vector<Node*>());
                parent->children.push_back(newNode);
                q.push({newNode, sibling});
                sibling = sibling->right;
            }
        }

        return rootNode;
    }
};
```

**Complexity**

- Time complexity: $O(N)$

- Space complexity:
    - `encode()` : $O(L)$.

    - `decode()` : $O(L)$.

    - Since $L$ is proportional to $N$ in the worst case, we could further generalize the space complexity to $O(N)$.

> Where $N$ is the number of nodes in the N-ary tree, and $L$ is the maximum number of nodes that reside at the same level.

## 2. DFS (Depth-First Search) Traversal

DFS offers a more elegant recursive solution using the same left-child right-sibling encoding. For each N-ary node, we recursively encode its first child and attach it as the left child of the binary node. The remaining children are encoded and linked as right siblings of the first child. Decoding reverses this: we traverse the left child's right chain to rebuild the children list.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> children;
    Node() {}
    Node(int _val) {
        val = _val;
    }
    Node(int _val, vector<Node*> _children) {
        val = _val;
        children = _children;
    }
};
*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */

class Codec {
public:
    // Encodes an n-ary tree to a binary tree.
    TreeNode* encode(Node* root) {
        if (!root) {
            return nullptr;
        }

        TreeNode* rootNode = new TreeNode(root->val);

        if (root->children.size() > 0) {
            Node* firstChild = root->children[0];
            rootNode->left = encode(firstChild);
        }

        // the parent for the rest of the children
        TreeNode* curr = rootNode->left;

        // encode the rest of the children
        for (int i = 1; i < root->children.size(); i++) {
            curr->right = encode(root->children[i]);
            curr = curr->right;
        }

        return rootNode;
    }

    // Decodes your binary tree to an n-ary tree.
    Node* decode(TreeNode* root) {
        if (!root) {
            return nullptr;
        }

        Node* rootNode = new Node(root->val);

        TreeNode* curr = root->left;
        while (curr) {
            rootNode->children.push_back(decode(curr));
            curr = curr->right;
        }

        return rootNode;
    }
};
```

**Complexity**

- Time complexity: $O(N)$

- Space complexity: $O(D)$
    - Since $D$ is proportional to $N$ in the worst case, we could further generalize the space complexity to $O(N)$

    - Unlike the BFS algorithm, we don't use the queue data structure in the DFS algorithm. However, implicitly the algorithm would consume more space in the function call stack due to the recursive function calls.

    - And this consumption of call stack space is the main space complexity for our DFS algorithm. As we can see, the size of the call stack at any moment is exactly the number of level where the currently visited node resides, e.g. for the root node (level 0), the recursive call stack is empty.

> Where $N$ is the number of nodes in the N-ary tree, and $D$ is the depth of the N-ary tree.
