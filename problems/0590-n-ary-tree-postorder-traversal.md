# 590. N-ary Tree Postorder Traversal

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/n-ary-tree-postorder-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/n-ary-tree-postorder-traversal>  
- **Video:** <https://www.youtube.com/watch?v=GMUI91_pDmM>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Postorder traversal means we visit all children of a node before visiting the node itself. For an N-ary tree, this translates to recursively processing each child subtree from left to right, then adding the current node's value to the result. The recursive approach naturally handles this ordering since the node's value is appended only after all recursive calls on its children have completed.

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

class Solution {
public:
    vector<int> postorder(Node* root) {
        vector<int> res;
        dfs(root, res);
        return res;
    }

    void dfs(Node* node, vector<int>& res) {
        if (!node) return;
        for (auto child : node->children) {
            dfs(child, res);
        }
        res.push_back(node->val);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the recursion stack.

## 2. Iterative DFS

To convert the recursive solution to an iterative one, we use a stack. The key challenge is ensuring we process a node only after all its children have been processed. We achieve this by pushing each node onto the stack twice: once to signal that its children should be explored, and once to signal that it should be added to the result. A visited flag distinguishes between these two cases. When we pop a node that has been visited, we add it to the result. When we pop an unvisited node, we mark it as visited, push it back, then push all its children in reverse order.

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

class Solution {
public:
    vector<int> postorder(Node* root) {
        vector<int> res;
        if (!root) return res;

        stack<pair<Node*, bool>> st;
        st.push({root, false});

        while (!st.empty()) {
            auto [node, visited] = st.top();
            st.pop();

            if (visited) {
                res.push_back(node->val);
            } else {
                st.push({node, true});
                for (int i = (int)node->children.size() - 1; i >= 0; i--) {
                    st.push({node->children[i], false});
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
