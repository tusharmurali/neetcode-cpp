# 1490. Clone N-ary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/clone-n-ary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/clone-n-ary-tree>  

[← Back to index](../INDEX.md)

## 1. Recursion

Cloning an N-ary tree is a natural fit for recursion. For each node, we create a copy with the same value, then recursively clone all of its children. The recursive structure mirrors the tree structure itself, making the solution straightforward and elegant.

```cpp
class Solution {
public:
    Node* cloneTree(Node* root) {
        // Base case: empty node.
        if (!root) {
            return root;
        }
        
        // First, copy the node itself.
        Node* node_copy = new Node(root->val);
        
        // Then, recursively clone the sub-trees.
        for (Node* child : root->children) {
            node_copy->children.push_back(cloneTree(child));
        }
        
        return node_copy;
    }
};
```

**Complexity**

- Time complexity: $O(M)$
- Space complexity: $O(M)$

>  Where $M$ is the number of nodes in the input tree.

## 2. DFS with Iteration

We can avoid recursion by using an explicit stack. We maintain pairs of (original node, cloned node) on the stack. When we pop a pair, we iterate through the original node's children, create cloned children, link them to the cloned parent, and push the new pairs onto the stack for further processing.

```cpp
class Solution {
public:
    Node* cloneTree(Node* root) {
        if (!root) {
            return root;
        }
        
        Node* new_root = new Node(root->val);
        // Starting point to kick off the DFS visits.
        stack<pair<Node*, Node*>> st;
        st.push({root, new_root});
        
        while (!st.empty()) {
            auto [old_node, new_node] = st.top();
            st.pop();
            
            for (Node* child_node : old_node->children) {
                Node* new_child_node = new Node(child_node->val);
                // Make a copy for each child node.
                new_node->children.push_back(new_child_node);
                // Schedule a visit to copy the child nodes of each child node.
                st.push({child_node, new_child_node});
            }
        }
        
        return new_root;
    }
};
```

**Complexity**

- Time complexity: $O(M)$
- Space complexity: $O(\log_{n}{M})$

>  Where $M$ is the number of nodes in the input tree and $N$ is the maximum number of children that a node can have

## 3. BFS

Instead of depth-first traversal with a stack, we can use breadth-first traversal with a queue. This processes nodes level by level. The logic is the same as the iterative DFS approach, but we use a queue instead of a stack, removing from the front instead of the back.

```cpp
class Solution {
public:
    Node* cloneTree(Node* root) {
        if (!root) {
            return root;
        }
        
        Node* new_root = new Node(root->val);
        // Starting point to kick off the BFS visits.
        queue<pair<Node*, Node*>> q;
        q.push({root, new_root});
        
        while (!q.empty()) {
            // Get the element from the head of the queue.
            auto [old_node, new_node] = q.front();
            q.pop();
            
            for (Node* child_node : old_node->children) {
                Node* new_child_node = new Node(child_node->val);
                // Make a copy for each child node.
                new_node->children.push_back(new_child_node);
                // Schedule a visit to copy the child nodes of each child node.
                q.push({child_node, new_child_node});
            }
        }
        
        return new_root;
    }
};
```

**Complexity**

- Time complexity: $O(M)$
- Space complexity: $O(M)$

>  Where $M$ is the number of nodes in the input tree.
