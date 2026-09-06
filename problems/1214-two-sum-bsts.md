# 1214. Two Sum BSTs

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/two-sum-bsts/>  
- **NeetCode:** <https://neetcode.io/problems/two-sum-bsts>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to collect all values from both trees and check every possible pair. If any pair sums to the target, we have found our answer.

```cpp
class Solution {
public:
    void dfs(TreeNode* currNode, vector<int>& nodeList) {
        if (currNode == nullptr) {
            return;
        }
        nodeList.push_back(currNode->val);
        dfs(currNode->left, nodeList);
        dfs(currNode->right, nodeList);
    }

    bool twoSumBSTs(TreeNode* root1, TreeNode* root2, int target) {
        vector<int> nodeList1, nodeList2;
        dfs(root1, nodeList1);
        dfs(root2, nodeList2);

        for (int a : nodeList1) {
            for (int b : nodeList2) {
                if (a + b == target) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot n)$
- Space complexity: $O(m+n)$

> Where $m$ and $n$ are the number of nodes in the two trees.

## 2. Binary Search

Since the second tree is a BST, we can leverage its sorted structure. For each node in the first tree, we compute the complement (`target - node.val`) and use binary search to check if that complement exists in the second tree.

```cpp
class Solution {
public:
    bool binarySearch(TreeNode* root2, int target2) {
        if (root2 == nullptr) {
            return false;
        }
        if (root2->val == target2) {
            return true;
        } else if (root2->val > target2) {
            return binarySearch(root2->left, target2);
        } else {
            return binarySearch(root2->right, target2);
        }
    }

    bool dfs(TreeNode* root1, TreeNode* root2, int target) {
        if (root1 == nullptr) {
            return false;
        }
        if (binarySearch(root2, target - root1->val)) {
            return true;
        }
        return dfs(root1->left, root2, target) || dfs(root1->right, root2, target);
    }

    bool twoSumBSTs(TreeNode* root1, TreeNode* root2, int target) {
        return dfs(root1, root2, target);
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot \log n)$
- Space complexity: $O(\log m + \log n)$

> Where $m$ and $n$ are the number of nodes in the two trees.

## 3. Hash Set

We can trade space for time by storing all values from one tree in a hash set. Then for each value in the other tree, we check if the complement exists in the set in O(1) time.

```cpp
class Solution {
public:
    void dfs(TreeNode* currNode, unordered_set<int>& nodeSet) {
        if (currNode == nullptr) {
            return;
        }
        dfs(currNode->left, nodeSet);
        nodeSet.insert(currNode->val);
        dfs(currNode->right, nodeSet);
    }

    bool twoSumBSTs(TreeNode* root1, TreeNode* root2, int target) {
        unordered_set<int> nodeSet1, nodeSet2;
        dfs(root1, nodeSet1);
        dfs(root2, nodeSet2);

        for (int value1 : nodeSet1) {
            if (nodeSet2.count(target - value1)) {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m + n)$

> Where $m$ and $n$ are the number of nodes in the two trees.

## 4. Two Pointers

An inorder traversal of a BST produces a sorted list. If we have sorted lists from both trees, we can use the classic two-pointer technique: one pointer starts at the beginning of the first list (smallest), and another starts at the end of the second list (largest). We adjust pointers based on whether the current sum is too small or too large.

```cpp
class Solution {
public:
    void dfs(TreeNode* currNode, vector<int>& nodeList) {
        if (currNode == nullptr) {
            return;
        }
        dfs(currNode->left, nodeList);
        nodeList.push_back(currNode->val);
        dfs(currNode->right, nodeList);
    }

    bool twoSumBSTs(TreeNode* root1, TreeNode* root2, int target) {
        vector<int> nodeList1, nodeList2;
        dfs(root1, nodeList1);
        dfs(root2, nodeList2);

        int pointer1 = 0, pointer2 = nodeList2.size() - 1;
        while (pointer1 < (int)nodeList1.size() && pointer2 >= 0) {
            if (nodeList1[pointer1] + nodeList2[pointer2] == target) {
                return true;
            } else if (nodeList1[pointer1] + nodeList2[pointer2] < target) {
                pointer1++;
            } else {
                pointer2--;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m + n)$

> Where $m$ and $n$ are the number of nodes in the two trees.

## 5. Morris Traversal

The two-pointer approach requires O(m + n) space to store the sorted lists. Morris traversal lets us iterate through a BST in sorted order using O(1) extra space by temporarily modifying tree pointers. We use forward Morris traversal on one tree and reverse Morris traversal on the other to simulate the two-pointer technique without extra space.

```cpp
class MorrisIterator {
private:
    TreeNode* current;
    TreeNode* pre;

public:
    MorrisIterator(TreeNode* root) : current(root), pre(nullptr) {}

    bool hasNext() {
        return current != nullptr;
    }

    int next() {
        int val = INT_MIN;
        while (current != nullptr) {
            if (current->left == nullptr) {
                val = current->val;
                current = current->right;
                break;
            } else {
                pre = current->left;
                while (pre->right != nullptr && pre->right != current) {
                    pre = pre->right;
                }
                if (pre->right == nullptr) {
                    pre->right = current;
                    current = current->left;
                } else {
                    pre->right = nullptr;
                    val = current->val;
                    current = current->right;
                    break;
                }
            }
        }
        return val;
    }
};

class ReversedMorrisIterator {
private:
    TreeNode* current;
    TreeNode* pre;

public:
    ReversedMorrisIterator(TreeNode* root) : current(root), pre(nullptr) {}

    bool hasNext() {
        return current != nullptr;
    }

    int next() {
        int val = INT_MIN;
        while (current != nullptr) {
            if (current->right == nullptr) {
                val = current->val;
                current = current->left;
                break;
            } else {
                pre = current->right;
                while (pre->left != nullptr && pre->left != current) {
                    pre = pre->left;
                }
                if (pre->left == nullptr) {
                    pre->left = current;
                    current = current->right;
                } else {
                    pre->left = nullptr;
                    val = current->val;
                    current = current->left;
                    break;
                }
            }
        }
        return val;
    }
};

class Solution {
public:
    bool twoSumBSTs(TreeNode* root1, TreeNode* root2, int target) {
        MorrisIterator iterator1(root1);
        ReversedMorrisIterator iterator2(root2);

        int value1 = iterator1.next();
        int value2 = iterator2.next();

        while (value1 != INT_MIN && value2 != INT_MIN) {
            if (value1 + value2 == target) {
                return true;
            } else if (value1 + value2 < target) {
                if (iterator1.hasNext()) {
                    value1 = iterator1.next();
                } else {
                    value1 = INT_MIN;
                }
            } else {
                if (iterator2.hasNext()) {
                    value2 = iterator2.next();
                } else {
                    value2 = INT_MIN;
                }
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$

> Where $m$ and $n$ are the number of nodes in the two trees.
