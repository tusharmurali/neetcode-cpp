# 1474. Delete N Nodes After M Nodes of a Linked List

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/delete-n-nodes-after-m-nodes-of-a-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/delete-n-nodes-after-m-nodes-of-a-linked-list>  

[← Back to index](../INDEX.md)

## 1. Traverse Linked List and Delete In Place

The problem asks us to keep the first `m` nodes, then delete the next `n` nodes, and repeat this pattern throughout the linked list. Since we are modifying the list in place, we need to track two key positions: the last node we want to keep (the `m`-th node in each group) and the node that comes after the `n` deleted nodes. By linking these two positions, we effectively skip over the deleted nodes.

```cpp
class Solution {
public:
    ListNode* deleteNodes(ListNode* head, int m, int n) {
        ListNode* currentNode = head;
        ListNode* lastMNode = head;

        while (currentNode != nullptr) {
            // initialize mCount to m and nCount to n
            int mCount = m, nCount = n;

            // traverse m nodes
            while (currentNode != nullptr && mCount != 0) {
                lastMNode = currentNode;
                currentNode = currentNode->next;
                mCount--;
            }

            // traverse n nodes
            while (currentNode != nullptr && nCount != 0) {
                currentNode = currentNode->next;
                nCount--;
            }

            // delete n nodes
            lastMNode->next = currentNode;
        }

        return head;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$

> Where $N$ is the length of the linked list pointed by `head`.
