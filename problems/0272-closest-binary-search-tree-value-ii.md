# 272. Closest Binary Search Tree Value II

- **Difficulty:** Hard  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/closest-binary-search-tree-value-ii/>  
- **NeetCode:** <https://neetcode.io/problems/closest-binary-search-tree-value-ii>  

[← Back to index](../INDEX.md)

## 1. Sort With Custom Comparator

The simplest approach is to collect all node values from the tree and then sort them based on their distance to the target. Once sorted, the first k elements are the closest values. This works because we just need the k values closest to the target, regardless of their original position in the tree.

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
class Solution {
public:
    vector<int> closestKValues(TreeNode* root, double target, int k) {
        vector<int> arr;
        dfs(root, arr);

        sort(arr.begin(), arr.end(), [&](int a, int b) {
            return abs(a - target) < abs(b - target);
        });

        return vector<int>(arr.begin(), arr.begin() + k);
    }

    void dfs(TreeNode* node, vector<int>& arr) {
        if (!node) return;
        arr.push_back(node->val);
        dfs(node->left, arr);
        dfs(node->right, arr);
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log n)$
- Space complexity: $O(n)$

>  Where $n$ is the number of nodes in the tree

## 2. Traverse With Heap

Instead of sorting all values, we can use a max-heap of size k to track the k closest values seen so far. As we traverse the tree, we compare each node's distance to the target with the farthest element in our heap. If the current node is closer, we replace the farthest element. This avoids sorting the entire array.

```cpp
class Solution {
public:
    vector<int> closestKValues(TreeNode* root, double target, int k) {
        auto cmp = [&](int a, int b) {
            return abs(a - target) < abs(b - target);
        };
        priority_queue<int, vector<int>, decltype(cmp)> heap(cmp);

        function<void(TreeNode*)> dfs = [&](TreeNode* node) {
            if (!node) return;

            heap.push(node->val);
            if (heap.size() > k) {
                heap.pop();
            }

            dfs(node->left);
            dfs(node->right);
        };

        dfs(root);

        vector<int> res;
        while (!heap.empty()) {
            res.push_back(heap.top());
            heap.pop();
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log k)$
- Space complexity: $O(n+k)$

>  Where $n$ is the number of nodes in the tree and $k$ is the size of our heap

## 3. Inorder Traversal + Sliding Window

Since this is a BST, an inorder traversal gives us values in sorted order. With a sorted array, the `k` closest values to the target form a contiguous subarray. We can use binary search to find the position closest to the target, then expand outward using two pointers to collect the `k` nearest values.

```cpp
class Solution {
public:
    vector<int> closestKValues(TreeNode* root, double target, int k) {
        vector<int> arr;
        dfs(root, arr);

        int left = lower_bound(arr.begin(), arr.end(), target) - arr.begin() - 1;
        int right = left + 1;
        vector<int> ans;

        while (ans.size() < k) {
            if (left < 0) {
                ans.push_back(arr[right++]);
            } else if (right >= arr.size()) {
                ans.push_back(arr[left--]);
            } else if (abs(arr[left] - target) <= abs(arr[right] - target)) {
                ans.push_back(arr[left--]);
            } else {
                ans.push_back(arr[right++]);
            }
        }

        return ans;
    }

    void dfs(TreeNode* node, vector<int>& arr) {
        if (!node) return;
        dfs(node->left, arr);
        arr.push_back(node->val);
        dfs(node->right, arr);
    }
};
```

**Complexity**

- Time complexity: $O(n+k)$
- Space complexity: $O(n)$

>  Where $n$ is the number of nodes in the tree and $k$ is the size of our sliding window

## 4. Binary Search The Left Bound

Since the inorder traversal produces a sorted array and we need a contiguous subarray of size `k`, we can binary search for the optimal starting position of this window. For any starting position, we compare the distances of the leftmost and rightmost elements in the window to decide if shifting right would improve our answer.

```cpp
class Solution {
public:
    vector<int> closestKValues(TreeNode* root, double target, int k) {
        vector<int> arr;
        dfs(root, arr);

        int left = 0;
        int right = arr.size() - k;

        while (left < right) {
            int mid = (left + right) / 2;
            if (abs(target - arr[mid + k]) < abs(target - arr[mid])) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return vector<int>(arr.begin() + left, arr.begin() + left + k);
    }

    void dfs(TreeNode* node, vector<int>& arr) {
        if (!node) return;
        dfs(node->left, arr);
        arr.push_back(node->val);
        dfs(node->right, arr);
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ in Java
    - $O(n+k)$ in Python
- Space complexity: $O(n)$

>  Where $n$ is the number of nodes in the tree and $k$ is the number of closest values to return

## 5. Build The Window With Deque

During inorder traversal, values are visited in sorted order. We can maintain a sliding window of size `k` using a deque. As we visit each node, we add it to the window. When the window exceeds `k` elements, we compare the distances of the first and last elements and remove the one farther from the target. Once the first element is closer, all subsequent elements will be even farther, so we can stop early.

```cpp
class Solution {
public:
    vector<int> closestKValues(TreeNode* root, double target, int k) {
        deque<int> queue;
        dfs(root, queue, k, target);
        return vector<int>(queue.begin(), queue.end());
    }
    
private:
    void dfs(TreeNode* node, deque<int>& queue, int k, double target) {
        if (node == nullptr) {
            return;
        }
        
        dfs(node->left, queue, k, target);
        
        queue.push_back(node->val);
        if (queue.size() > k) {
            if (abs(target - queue.front()) <= abs(target - queue.back())) {
                queue.pop_back();
                return;
            } else {
                queue.pop_front();
            }
        }
        
        dfs(node->right, queue, k, target);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n+k)$

>  Where $n$ is the number of nodes in the tree and $k$ is the number of closest values to return
