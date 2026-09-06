# 138. Copy List With Random Pointer

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/copy-list-with-random-pointer/>  
- **NeetCode:** <https://neetcode.io/problems/copy-linked-list-with-random-pointer>  
- **Video:** <https://www.youtube.com/watch?v=5Y2EiZST97Y>  
- **Video approach:** 2. Hash Map (Two Pass)  

[← Back to index](../INDEX.md)

## 1. Recursion + Hash Map

We must create a deep copy of a linked list where each node has both `next` and `random` pointers.  
The main difficulty: multiple nodes may point to the same `random` node, so we must ensure each original node is copied **exactly once**.

A hash map helps us remember the copied version of each original node.  
Using recursion, we:

- copy the current node,
- store it in the map,
- recursively copy its `next`,
- link its `random` using the map.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

class Solution {
public:
    unordered_map<Node*, Node*> map;

    Node* copyRandomList(Node* head) {
        if (head == nullptr) return nullptr;
        if (map.count(head)) return map[head];

        Node* copy = new Node(head->val);
        map[head] = copy;
        copy->next = copyRandomList(head->next);
        copy->random = map[head->random];
        return copy;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Hash Map (Two Pass) ▶ video

We want to copy a linked list where each node has both `next` and `random` pointers.  
The challenge is that the `random` pointer can point anywhere — forward, backward, or even `None`.  
So we must ensure every original node is copied **exactly once**, and all pointers are reconnected correctly.

A simple solution:

- **Pass 1:** Create a copy of every node (just values), and store the mapping:  
  `original_node → copied_node`
- **Pass 2:** Use this map to connect `next` and `random` pointers for each copied node.

This guarantees all pointers are valid and no node is duplicated.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> oldToCopy;
        oldToCopy[NULL] = NULL;

        Node* cur = head;
        while (cur != NULL) {
            Node* copy = new Node(cur->val);
            oldToCopy[cur] = copy;
            cur = cur->next;
        }

        cur = head;
        while (cur != NULL) {
            Node* copy = oldToCopy[cur];
            copy->next = oldToCopy[cur->next];
            copy->random = oldToCopy[cur->random];
            cur = cur->next;
        }

        return oldToCopy[head];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Map (One Pass)

We want to copy a linked list where every node has a `next` pointer and a `random` pointer.  
Normally we need two passes: one to create nodes, and another to connect pointers.  
But we can actually do both at the same time by using a hash map that **automatically creates a copy node whenever we access it**.

So when we say:

- `oldToCopy[cur]` → gives the copied node
- `oldToCopy[cur.next]` → gives the copy of `cur.next` (created if not present)
- `oldToCopy[cur.random]` → gives the copy of `cur.random`

This lets us fill `val`, `next`, and `random` in **one single pass**.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> oldToCopy;
        oldToCopy[nullptr] = nullptr;

        Node* cur = head;
        while (cur != nullptr) {
            if (oldToCopy.find(cur) == oldToCopy.end()) {
                oldToCopy[cur] = new Node(0);
            }
            oldToCopy[cur]->val = cur->val;
            if (oldToCopy.find(cur->next) == oldToCopy.end()) {
                oldToCopy[cur->next] = new Node(0);
            }
            oldToCopy[cur]->next = oldToCopy[cur->next];
            if (oldToCopy.find(cur->random) == oldToCopy.end()) {
                oldToCopy[cur->random] = new Node(0);
            }
            oldToCopy[cur]->random = oldToCopy[cur->random];
            cur = cur->next;
        }
        return oldToCopy[head];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Space Optimized - I

We want to copy the list without using extra space like a hash map.  
The trick is to **interleave copied nodes inside the original list**:

Original:  
**A → B → C**

After interleaving:  
**A → A' → B → B' → C → C'**

Now every copied node (`A'`, `B'`, `C'`) is right next to the original node, so we can easily:

- Set `random` of the copied node: `A'.random = A.random.next`
- Finally separate the two lists again.

This gives a perfect clone using **O(1) extra space**.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (head == nullptr) {
            return nullptr;
        }

        Node* l1 = head;
        while (l1 != nullptr) {
            Node* l2 = new Node(l1->val);
            l2->next = l1->next;
            l1->next = l2;
            l1 = l2->next;
        }

        Node* newHead = head->next;

        l1 = head;
        while (l1 != nullptr) {
            if (l1->random != nullptr) {
                l1->next->random = l1->random->next;
            }
            l1 = l1->next->next;
        }

        l1 = head;
        while (l1 != nullptr) {
            Node* l2 = l1->next;
            l1->next = l2->next;
            if (l2->next != nullptr) {
                l2->next = l2->next->next;
            }
            l1 = l1->next;
        }

        return newHead;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ for the output.

## 5. Space Optimized - II

This method also avoids extra space like a hash map, but instead of inserting copied nodes into the **next** pointer chain, we temporarily use the **random** pointer to store the copied nodes.

For every original node:

- We create its copy and store it in the original node’s `random` pointer.
- The copy’s `next` pointer initially points to whatever the original node’s `random` was pointing to.

This allows us to:

1. **Create all copies without extra memory.**
2. **Fix the random pointers** of the copied nodes using the original structure.
3. **Reconnect the next pointers** to build the final deep-copy list.
4. **Restore the original list.**

Everything happens using only pointer manipulations — no extra arrays, no hash map.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) {
            return nullptr;
        }

        Node* l1 = head;
        while (l1) {
            Node* l2 = new Node(l1->val);
            l2->next = l1->random;
            l1->random = l2;
            l1 = l1->next;
        }

        Node* newHead = head->random;

        l1 = head;
        while (l1) {
            Node* l2 = l1->random;
            l2->random = (l2->next != nullptr) ? l2->next->random : nullptr;
            l1 = l1->next;
        }

        l1 = head;
        while (l1) {
            Node* l2 = l1->random;
            l1->random = l2->next;
            l2->next = (l1->next != nullptr) ? l1->next->random : nullptr;
            l1 = l1->next;
        }

        return newHead;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ for the output.

## Standalone solution file (`cpp/0138-copy-list-with-random-pointer.cpp` in the NeetCode repo)

```cpp
/*
    Given linked list w/ also a random pointer, construct deep copy

    Hash map {old -> new}, O(n) space
    Optimize interweave old and new nodes, O(1) space
    A -> A' -> B -> B' -> C -> C', A'.random = A.random.next

    Time: O(n)
    Space: O(n) -> can optimize to O(1)
*/

/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;
    
    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

// class Solution {
// public:
//     Node* copyRandomList(Node* head) {
//         if (head == NULL) {
//             return NULL;
//         }
//         Node* oldNode = head;
//         Node* newNode = new Node(oldNode->val);
//         visited[oldNode] = newNode;
//         while (oldNode != NULL) {
//             newNode->next = getClonedNode(oldNode->next);
//             newNode->random = getClonedNode(oldNode->random);
//             oldNode = oldNode->next;
//             newNode = newNode->next;
//         }
//         return visited[head];
//     }
// private:
//     unordered_map<Node*, Node*> visited;
//     Node* getClonedNode(Node* node) {
//         if (node == NULL) {
//             return NULL;
//         }
//         if (visited.find(node) != visited.end()) {
//             return visited[node];
//         }
//         visited[node] = new Node(node->val);
//         return visited[node];
//     }
// };
/*
class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (head == NULL) {
            return NULL;
        }
        
        Node* ptr = head;
        while (ptr != NULL) {
            Node* newNode = new Node(ptr->val);
            newNode->next = ptr->next;
            ptr->next = newNode;
            ptr = newNode->next;
        }
        ptr = head;
        
        while (ptr != NULL) {
            if (ptr->random == NULL) {
                ptr->next->random == NULL;
            } else {
                ptr->next->random = ptr->random->next;
            }
            ptr = ptr->next->next;
        }
        
        Node* oldPtr = head;
        Node* newPtr = head->next;
        Node* oldHead = head->next;
        
        while (oldPtr != NULL) {
            oldPtr->next = oldPtr->next->next;
            if (newPtr->next == NULL) {
                newPtr->next = NULL;
            } else {
                newPtr->next = newPtr->next->next;
            }
            oldPtr = oldPtr->next;
            newPtr = newPtr->next;
        }
        
        return oldHead;
    }
};
*/

// class Solution {
// public:
//     Node* copyRandomList(Node* head) {
//         unordered_map<Node*, Node*> nodes;
//         Node* h = head;
        
//         while (h){
//             nodes[h] = new Node(h->val);
//             h = h->next;
//         }
//         h = head;
//         while (h){
//             Node* newNode = nodes[h];
//             newNode->next = nodes[h->next];
//             newNode->random = nodes[h->random];
//             h = h->next;
//         }
//         return nodes[head];
//     }
// };

class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> nodes;
        Node* curr = head;
        
        while (curr != NULL) {
            nodes[curr] = new Node(curr->val);
            curr = curr->next;
        }

        curr = head;
        while (curr != NULL) {
            nodes[curr]->next = nodes[curr->next];
            nodes[curr]->random = nodes[curr->random];
            curr = curr->next;
        }
        return nodes[head];
    }   
};
```
