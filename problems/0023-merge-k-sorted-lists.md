# 23. Merge K Sorted Lists

- **Difficulty:** Hard  
- **Pattern:** Linked List  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/merge-k-sorted-lists/>  
- **NeetCode:** <https://neetcode.io/problems/merge-k-sorted-linked-lists>  
- **Video:** <https://www.youtube.com/watch?v=q5a5OiGbT6Q>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to merge all linked lists is to **ignore the list structure**, collect every value, sort them, and then rebuild a single sorted linked list.
This doesn't use any clever merging logic — it is purely based on gathering and sorting.
It's easy to implement but not efficient because sorting dominates the runtime.

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
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        vector<int> nodes;
        for (ListNode* lst : lists) {
            while (lst) {
                nodes.push_back(lst->val);
                lst = lst->next;
            }
        }
        sort(nodes.begin(), nodes.end());

        ListNode* res = new ListNode(0);
        ListNode* cur = res;
        for (int node : nodes) {
            cur->next = new ListNode(node);
            cur = cur->next;
        }
        return res->next;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Iteration

We repeatedly pick the **smallest head node** among all the lists and attach it to our result list.
At every step:

- Look at the first node of each non-empty list.
- Choose the one with the smallest value.
- Move that list's pointer forward.
- Append the chosen node to our merged list.

This is similar to merging `k` sorted arrays by always picking the smallest available element.

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
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        ListNode* res = new ListNode(0);
        ListNode* cur = res;

        while (true) {
            int minNode = -1;
            for (int i = 0; i < lists.size(); i++) {
                if (!lists[i]) continue;
                if (minNode == -1 || lists[minNode]->val > lists[i]->val) {
                    minNode = i;
                }
            }

            if (minNode == -1) break;
            cur->next = lists[minNode];
            lists[minNode] = lists[minNode]->next;
            cur = cur->next;
        }
        return res->next;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(1)$

> Where $k$ is the total number of lists and $n$ is the total number of nodes across $k$ lists.

## 3. Merge Lists One By One

Instead of merging all `k` lists at once, we can **merge them one by one**.

- First merge list `0` and list `1` → get a sorted list.
- Then merge that result with list `2`.
- Then merge that result with list `3`.
- Repeat until all lists are merged.

Each merge operation is just like the standard **"merge two sorted linked lists"** problem:

- Compare the heads.
- Attach the smaller one.
- Move that list's pointer forward.
- Continue until one list is empty, then attach the rest of the other list.

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
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if (lists.empty()) return nullptr;

        for (int i = 1; i < lists.size(); i++) {
            lists[i] = merge(lists[i], lists[i - 1]);
        }
        return lists.back();
    }

private:
    ListNode* merge(ListNode* l1, ListNode* l2) {
        ListNode* dummy = new ListNode(0);
        ListNode* curr = dummy;

        while (l1 != nullptr && l2 != nullptr) {
            if (l1->val <= l2->val) {
                curr->next = l1;
                l1 = l1->next;
            } else {
                curr->next = l2;
                l2 = l2->next;
            }
            curr = curr->next;
        }

        if (l1 != nullptr) {
            curr->next = l1;
        } else {
            curr->next = l2;
        }

        return dummy->next;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(1)$

> Where $k$ is the total number of lists and $n$ is the total number of nodes across $k$ lists.

## 4. Heap

We want to always pick the **smallest current node** among all `k` lists as efficiently as possible.

Instead of scanning all heads every time (which is slow), we can use a **min-heap (priority queue)**:

- Push the head of each non-empty list into the heap.
- The heap always gives us the node with the **smallest value** on top.
- We pop that node, attach it to our result list, and then push its `next` node (if it exists) into the heap.
- Repeat until the heap is empty.

This way, at every step we choose the globally smallest node in **O(log k)** time, where `k` is the number of lists.

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
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if (lists.empty()) return nullptr;

        auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> minHeap(cmp);

        for (ListNode* list : lists) {
            if (list != nullptr) {
                minHeap.push(list);
            }
        }

        ListNode* res = new ListNode(0);
        ListNode* cur = res;
        while (!minHeap.empty()) {
            ListNode* node = minHeap.top();
            minHeap.pop();
            cur->next = node;
            cur = cur->next;

            node = node->next;
            if (node != nullptr) {
                minHeap.push(node);
            }
        }
        return res->next;
    }
};
```

**Complexity**

- Time complexity: $O(n \log k)$
- Space complexity: $O(k)$

> Where $k$ is the total number of lists and $n$ is the total number of nodes across $k$ lists.

## 5. Divide And Conquer (Recursion)

Instead of merging all k lists at once or one by one in order, we can use a **divide and conquer** strategy, similar to how **merge sort** works.

Idea:

- Split the list of linked lists into two halves.
- Recursively merge the left half into one sorted list.
- Recursively merge the right half into one sorted list.
- Finally, merge these two sorted lists into a single sorted list.

By always merging **pairs** of lists, we reduce the total work compared to merging k lists sequentially.  
Each merge of two lists is linear in their total length, and we do about `log k` levels of merging.

This makes the approach both clean and efficient.

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
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if (lists.empty()) {
            return nullptr;
        }
        return divide(lists, 0, lists.size() - 1);
    }

private:
    ListNode* divide(vector<ListNode*>& lists, int l, int r) {
        if (l > r) {
            return nullptr;
        }
        if (l == r) {
            return lists[l];
        }

        int mid = l + (r - l) / 2;
        ListNode* left = divide(lists, l, mid);
        ListNode* right = divide(lists, mid + 1, r);

        return conquer(left, right);
    }

    ListNode* conquer(ListNode* l1, ListNode* l2) {
        ListNode dummy(0);
        ListNode* curr = &dummy;

        while (l1 && l2) {
            if (l1->val <= l2->val) {
                curr->next = l1;
                l1 = l1->next;
            } else {
                curr->next = l2;
                l2 = l2->next;
            }
            curr = curr->next;
        }

        if (l1) {
            curr->next = l1;
        } else {
            curr->next = l2;
        }

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n \log k)$
- Space complexity: $O(\log k)$

> Where $k$ is the total number of lists and $n$ is the total number of nodes across $k$ lists.

## 6. Divide And Conquer (Iteration)

This is the **same idea as divide and conquer**, but done **iteratively** instead of using recursion.

We repeatedly merge the lists in **pairs**:

- In one pass:
    - Merge list 0 and list 1 -> get M0
    - Merge list 2 and list 3 -> get M1
    - Merge list 4 and list 5 -> get M2
    - ... and so on.
- After this pass, we have fewer lists (about half as many).
- Repeat this process on the new list of merged lists until only **one** list remains.

Each pairwise merge is just the usual **merge of two sorted linked lists**.
By always merging lists two at a time, the total work is efficient and structured, similar to the merge step in merge sort.

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
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if (lists.empty()) {
            return nullptr;
        }

        while (lists.size() > 1) {
            vector<ListNode*> mergedLists;
            for (int i = 0; i < lists.size(); i += 2) {
                ListNode* l1 = lists[i];
                ListNode* l2 = (i + 1) < lists.size() ? lists[i + 1] : nullptr;
                mergedLists.push_back(mergeList(l1, l2));
            }
            lists = mergedLists;
        }
        return lists[0];
    }

private:
    ListNode* mergeList(ListNode* l1, ListNode* l2) {
        ListNode dummy;
        ListNode* tail = &dummy;

        while (l1 && l2) {
            if (l1->val < l2->val) {
                tail->next = l1;
                l1 = l1->next;
            } else {
                tail->next = l2;
                l2 = l2->next;
            }
            tail = tail->next;
        }

        if (l1) {
            tail->next = l1;
        }
        if (l2) {
            tail->next = l2;
        }

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n \log k)$
- Space complexity: $O(k)$

> Where $k$ is the total number of lists and $n$ is the total number of nodes across $k$ lists.

## Standalone solution file (`cpp/0023-merge-k-sorted-lists.cpp` in the NeetCode repo)

```cpp
/*
    Given array of k sorted linked-lists, merge all into 1 sorted list
    Ex. lists = [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]

    Min heap -> optimize space w/ divide-and-conquer, merge 2 each time

    Time: O(n log k)
    Space: O(n) -> O(1)
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

// class Solution {
// public:
//     ListNode* mergeKLists(vector<ListNode*>& lists) {
//         priority_queue<int, vector<int>, greater<int>> pq;
//         for (int i = 0; i < lists.size(); i++) {
//             ListNode* node = lists[i];
//             while (node != NULL) {
//                 pq.push(node->val);
//                 node = node->next;
//             }
//         }
//         if (pq.empty()) {
//             return NULL;
//         }
//         ListNode* node = new ListNode(pq.top());
//         pq.pop();
//         ListNode* head = node;
//         while (!pq.empty()) {
//             node->next = new ListNode(pq.top());
//             pq.pop();
//             node = node->next;
//         }
//         return head;
//     }
// };

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        int n = lists.size();
        if (n == 0) {
            return NULL;
        }
        
        while (n > 1) {
            for (int i = 0; i < n / 2; i++) {
                lists[i] = mergeTwoLists(lists[i], lists[n - i - 1]);
            }
            n = (n + 1) / 2;
        }
        
        return lists.front();
    }
private:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (list1 == NULL && list2 == NULL) {
            return NULL;
        }
        if (list1 == NULL) {
            return list2;
        }
        if (list2 == NULL) {
            return list1;
        }
        
        ListNode* head = NULL;
        if (list1->val <= list2->val) {
            head = list1;
            list1 = list1->next;
        } else {
            head = list2;
            list2 = list2->next;
        }
        ListNode* curr = head;
        
        while (list1 != NULL && list2 != NULL) {
            if (list1->val <= list2->val) {
                curr->next = list1;
                list1 = list1->next;
            } else {
                curr->next = list2;
                list2 = list2->next;
            }
            curr = curr->next;
        }
        
        if (list1 == NULL) {
            curr->next = list2;
        } else {
            curr->next = list1;
        }
        
        return head;
    }
};
```
