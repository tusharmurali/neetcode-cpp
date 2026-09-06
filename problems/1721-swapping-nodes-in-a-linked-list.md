# 1721. Swapping Nodes in a Linked List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/swapping-nodes-in-a-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/swapping-nodes-in-a-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=4LsrgMyQIjQ>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

Converting the linked list to an array gives us random access to any position. The `k`-th node from the beginning is at index `k-1`, and the `k`-th node from the end is at index `n-k` (where `n` is the length). After swapping values in the array, we simply copy them back to the original nodes. This approach is simple but uses extra space.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* swapNodes(ListNode* head, int k) {
        vector<int> arr;
        ListNode* cur = head;

        while (cur) {
            arr.push_back(cur->val);
            cur = cur->next;
        }

        int n = arr.size();
        swap(arr[k - 1], arr[n - k]);

        cur = head;
        int i = 0;
        while (cur) {
            cur->val = arr[i];
            cur = cur->next;
            i++;
        }

        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Recursion

Recursion naturally gives us access to positions from both ends. As we recurse, we can count from the start (using a variable incremented before the recursive call) to find the `k`-th node from the beginning. The recursive call returns a count from the end, allowing us to identify the `k`-th node from the end. Once both nodes are found, we swap their values.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* swapNodes(ListNode* head, int k) {
        ListNode* left = nullptr;
        ListNode* right = nullptr;
        int startIdx = 0;

        dfs(head, k, startIdx, left, right);

        if (left && right) {
            swap(left->val, right->val);
        }

        return head;
    }

private:
    int dfs(ListNode* node, int k, int& startIdx, ListNode*& left, ListNode*& right) {
        if (!node) {
            return 0;
        }

        startIdx++;
        if (startIdx == k) {
            left = node;
        }

        int endIdx = dfs(node->next, k, startIdx, left, right) + 1;
        if (endIdx == k) {
            right = node;
        }

        return endIdx;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iteration (Two Pass)

With two passes, we first determine the list length, then locate both target nodes. The `k`-th node from the beginning is found by advancing `k` nodes. The `k`-th node from the end is at position `n - k + 1` from the start. In the second pass, we find both positions and swap their values.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* swapNodes(ListNode* head, int k) {
        int n = 0;
        ListNode* cur = head;
        while (cur) {
            n++;
            cur = cur->next;
        }

        ListNode* left = nullptr;
        ListNode* right = nullptr;
        cur = head;
        for (int i = 1; i <= n; i++) {
            if (i == k) {
                left = cur;
            }
            if (i == (n - k + 1)) {
                right = cur;
            }
            cur = cur->next;
        }

        swap(left->val, right->val);
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Iteration (One Pass) - I

We can find both nodes in a single pass using the two-pointer technique. First, advance one pointer `k` steps to reach the `k`-th node from the start. Then, start a second pointer from the head and advance both pointers together until the first reaches the end. At that point, the second pointer will be at the `k`-th node from the end, since it trails by exactly `n - k` positions.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* swapNodes(ListNode* head, int k) {
        ListNode* cur = head;
        for (int i = 0; i < k - 1; i++) {
            cur = cur->next;
        }

        ListNode* left = cur;
        ListNode* right = head;

        while (cur->next) {
            cur = cur->next;
            right = right->next;
        }

        swap(left->val, right->val);
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Iteration (One Pass) - II

This variation uses a slightly different approach: we start `right` moving only after we have found the `k`-th node. By decrementing `k` during traversal, we know exactly when we reach the `k`-th position. At that moment, we initialize `right` at the head. From then on, both pointers move together, maintaining their fixed distance until the end.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* swapNodes(ListNode* head, int k) {
        ListNode* left = nullptr;
        ListNode* right = nullptr;
        ListNode* cur = head;

        while (cur) {
            if (right) {
                right = right->next;
            }
            if (k == 1) {
                left = cur;
                right = head;
            }
            k--;
            cur = cur->next;
        }

        swap(left->val, right->val);
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1721-swapping-nodes-in-a-linked-list.cpp` in the NeetCode repo)

```cpp
/*
  You are given the head of a linked list, and an integer k.
  Return the head of the linked list after swapping the values of the kth node from the beginning and the kth node from the end (the list is 1-indexed).

  Ex. Input: head = [1,2,3,4,5], k = 2
      Output: [1,4,3,2,5]

  Time  : O(N)
  Space : O(1)
*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* swapNodes(ListNode* head, int k) {
        if(head == NULL || head -> next == NULL) 
            return head;

        ListNode *ptr = head, *beg = head, *end = head;
        int a = 0;
        while(ptr != NULL) {
            a++;
            if(a == k) 
                beg = ptr;
            if(a >= k + 1) 
                end = end -> next;
            ptr = ptr -> next;
        }
        int temp = beg -> val;
        beg -> val = end -> val;
        end -> val = temp;
        return head;
    }
};
```
