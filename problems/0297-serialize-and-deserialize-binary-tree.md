# 297. Serialize And Deserialize Binary Tree

- **Difficulty:** Hard  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/serialize-and-deserialize-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/serialize-and-deserialize-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=u4JAi2JJhI8>  
- **Video approach:** 1. Depth First Search  

[← Back to index](../INDEX.md)

## 1. Depth First Search ▶ video

We want to turn a tree into a string (serialize) and then rebuild the same tree from that string (deserialize).
We use **preorder DFS (root → left → right)** because it naturally records a node before its children.

- When a node exists → record its value.
- When a child is missing → record `"N"` so we know where `null` pointers are.

Example:
`1,2,N,N,3,N,N` uniquely represents a tree.

During **deserialization**, we read the list in order:

- `"N"` → return `None`
- Otherwise → create node, then build left, then right.

This works because preorder always visits nodes in the exact structure order.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */

class Codec {
public:
    // Encodes a tree to a single string.
    string serialize(TreeNode* root) {
        vector<string> res;
        dfsSerialize(root, res);
        return join(res, ",");
    }

    // Decodes your encoded data to tree.
    TreeNode* deserialize(string data) {
        vector<string> vals = split(data, ',');
        int i = 0;
        return dfsDeserialize(vals, i);
    }

private:
    void dfsSerialize(TreeNode* node, vector<string>& res) {
        if (!node) {
            res.push_back("N");
            return;
        }
        res.push_back(to_string(node->val));
        dfsSerialize(node->left, res);
        dfsSerialize(node->right, res);
    }

    TreeNode* dfsDeserialize(vector<string>& vals, int& i) {
        if (vals[i] == "N") {
            i++;
            return NULL;
        }
        TreeNode* node = new TreeNode(stoi(vals[i]));
        i++;
        node->left = dfsDeserialize(vals, i);
        node->right = dfsDeserialize(vals, i);
        return node;
    }

    vector<string> split(const string &s, char delim) {
        vector<string> elems;
        stringstream ss(s);
        string item;
        while (getline(ss, item, delim)) {
            elems.push_back(item);
        }
        return elems;
    }

    string join(const vector<string> &v, const string &delim) {
        ostringstream s;
        for (const auto &i : v) {
            if (&i != &v[0])
                s << delim;
            s << i;
        }
        return s.str();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search

Instead of using DFS, we treat the tree like a queue (level order traversal).
BFS visits nodes level by level, so we simply record values in that order:

- If a node exists → record its value and push its children (even if they are `None`).
- If a node is missing → record `"N"` to mark empty spots.

This ensures the structure is preserved, because BFS processes nodes exactly how they appear in the tree layout.

During **deserialization**, we again use BFS:

- The first value is the root.
- Then for each node in the queue, assign its left and right children from the next values in the list.

This keeps the tree reconstruction aligned with the serialized order.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */

class Codec {
public:

    // Encodes a tree to a single string.
    string serialize(TreeNode* root) {
        if (!root) return "N";
        string res;
        queue<TreeNode*> queue;
        queue.push(root);

        while (!queue.empty()) {
            TreeNode* node = queue.front();
            queue.pop();
            if (!node) {
                res += "N,";
            } else {
                res += to_string(node->val) + ",";
                queue.push(node->left);
                queue.push(node->right);
            }
        }
        return res;
    }

    // Decodes your encoded data to tree.
    TreeNode* deserialize(string data) {
        stringstream ss(data);
        string val;
        getline(ss, val, ',');
        if (val == "N") return nullptr;
        TreeNode* root = new TreeNode(stoi(val));
        queue<TreeNode*> queue;
        queue.push(root);

        while (getline(ss, val, ',')) {
            TreeNode* node = queue.front();
            queue.pop();
            if (val != "N") {
                node->left = new TreeNode(stoi(val));
                queue.push(node->left);
            }
            getline(ss, val, ',');
            if (val != "N") {
                node->right = new TreeNode(stoi(val));
                queue.push(node->right);
            }
        }
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0297-serialize-and-deserialize-binary-tree.cpp` in the NeetCode repo)

```cpp
/*
    Design an algorithm to serialize & deserialize a binary tree

    Use stringstream to concisely handle negatives, nulls, etc.

    Time: O(n) serialize, O(n) deserialize
    Space: O(n) serialize, O(n) deserialize
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

    // Encodes a tree to a single string.
    string serialize(TreeNode* root) {
        ostringstream out;
        encode(root, out);
        return out.str();
    }

    // Decodes your encoded data to tree.
    TreeNode* deserialize(string data) {
        istringstream in(data);
        return decode(in);
    }
    
private:
    
    void encode(TreeNode* root, ostringstream& out) {
        if (root == NULL) {
            out << "N ";
            return;
        }
        
        out << root->val << " ";
        
        encode(root->left, out);
        encode(root->right, out);
    }
    
    TreeNode* decode(istringstream& in) {
        string value = "";
        in >> value;
        
        if (value == "N") {
            return NULL;
        }
        
        TreeNode* root = new TreeNode(stoi(value));
        
        root->left = decode(in);
        root->right = decode(in);
        
        return root;
    }
    
};

// Your Codec object will be instantiated and called as such:
// Codec ser, deser;
// TreeNode* ans = deser.deserialize(ser.serialize(root));
```
