# 707. Design Linked List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/design-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=Wf4QhpdVFQo>  

[← Back to index](../INDEX.md)

## 1. Singly Linked List

A singly linked list stores elements in nodes where each node points to the next one. We use a dummy head node to simplify edge cases like inserting at the beginning or deleting the first element. The dummy head always exists, so we never have to handle a null head pointer. We also track the size to quickly validate indices without traversing the entire list.

```cpp
class MyLinkedList {
    struct ListNode {
        int val;
        ListNode* next;
        ListNode(int val) : val(val), next(nullptr) {}
    };

public:
    ListNode* head;
    int size;
    MyLinkedList() {
        head = new ListNode(0);
        size = 0;
    }
    int get(int index) {
        if (index >= size) return -1;
        ListNode* cur = head->next;
        for (int i = 0; i < index; i++) {
            cur = cur->next;
        }
        return cur->val;
    }
    void addAtHead(int val) {
        ListNode* node = new ListNode(val);
        node->next = head->next;
        head->next = node;
        size++;
    }
    void addAtTail(int val) {
        ListNode* node = new ListNode(val);
        ListNode* cur = head;
        while (cur->next != nullptr) {
            cur = cur->next;
        }
        cur->next = node;
        size++;
    }
    void addAtIndex(int index, int val) {
        if (index > size) return;
        ListNode* cur = head;
        for (int i = 0; i < index; i++) {
            cur = cur->next;
        }
        ListNode* node = new ListNode(val);
        node->next = cur->next;
        cur->next = node;
        size++;
    }
    void deleteAtIndex(int index) {
        if (index >= size) return;
        ListNode* cur = head;
        for (int i = 0; i < index; i++) {
            cur = cur->next;
        }
        ListNode* temp = cur->next;
        cur->next = cur->next->next;
        delete temp;
        size--;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for $addAtHead()$.
    - $O(n)$ time for $get()$, $addAtTail()$, $addAtIndex()$, $deleteAtIndex()$.
- Space complexity: $O(n)$

## 2. Singly Linked List (Optimal)

This approach refactors the singly linked list by introducing a helper function `getPrev(index)` that returns the node immediately before the target index. Since insertion and deletion both require access to the predecessor node, centralizing this logic reduces code duplication. The `addAtHead()` and `addAtTail()` operations now simply call `addAtIndex()`, making the implementation cleaner and easier to maintain.

```cpp

class MyLinkedList {
    struct ListNode {
        int val;
        ListNode* next;
        ListNode(int val, ListNode* next) : val(val), next(next) {}
        ListNode(int val) : val(val), next(nullptr) {}
    };

public:
    MyLinkedList() {
        head = new ListNode(0, nullptr);
        size = 0;
    }

    int get(int index) {
        if (index >= size) return -1;
        return getPrev(index)->next->val;
    }

    void addAtHead(int val) {
        addAtIndex(0, val);
    }

    void addAtTail(int val) {
        addAtIndex(size, val);
    }

    void addAtIndex(int index, int val) {
        if (index > size) return;
        ListNode* prev = getPrev(index);
        ListNode* node = new ListNode(val, prev->next);
        prev->next = node;
        size++;
    }

    void deleteAtIndex(int index) {
        if (index >= size) return;
        ListNode* prev = getPrev(index);
        ListNode* toDelete = prev->next;
        prev->next = prev->next->next;
        delete toDelete;
        size--;
    }

private:
    ListNode* head;
    int size;

    ListNode* getPrev(int index) {
        ListNode* cur = head;
        for (int i = 0; i < index; i++) {
            cur = cur->next;
        }
        return cur;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for $addAtHead()$.
    - $O(n)$ time for $get()$, $addAtTail()$, $addAtIndex()$, $deleteAtIndex()$.
- Space complexity: $O(n)$

## 3. Doubly Linked List

A doubly linked list adds a `prev` pointer to each node, allowing traversal in both directions. We use two sentinel nodes: a dummy head and a dummy tail. These sentinels eliminate `null` checks when inserting or deleting at the boundaries. Any real node is always between the head and tail sentinels, so insertion and deletion operations become symmetric and straightforward.

```cpp
class MyLinkedList {
    struct ListNode {
        int val;
        ListNode* prev;
        ListNode* next;
        ListNode(int val) : val(val), prev(nullptr), next(nullptr) {}
    };
public:
	ListNode* head;
	ListNode* tail;

	MyLinkedList() {
		head = new ListNode(0);
		tail = new ListNode(0);
		head->next = tail;
		tail->prev = head;
	}

	int get(int index) {
		ListNode* cur = head->next;
		while (cur && index > 0) {
			cur = cur->next;
			index--;
		}
		if (cur && cur != tail && index == 0) {
			return cur->val;
		}
		return -1;
	}

	void addAtHead(int val) {
		ListNode* node = new ListNode(val);
		ListNode* next = head->next;
		ListNode* prev = head;
		prev->next = node;
		next->prev = node;
		node->next = next;
		node->prev = prev;
	}

	void addAtTail(int val) {
		ListNode* node = new ListNode(val);
		ListNode* next = tail;
		ListNode* prev = tail->prev;
		prev->next = node;
		next->prev = node;
		node->next = next;
		node->prev = prev;
	}

	void addAtIndex(int index, int val) {
		ListNode* cur = head->next;
		while (cur && index > 0) {
			cur = cur->next;
			index--;
		}
		if (cur && index == 0) {
			ListNode* node = new ListNode(val);
			ListNode* next = cur;
			ListNode* prev = cur->prev;
			prev->next = node;
			next->prev = node;
			node->next = next;
			node->prev = prev;
		}
	}

	void deleteAtIndex(int index) {
		ListNode* cur = head->next;
		while (cur && index > 0) {
			cur = cur->next;
			index--;
		}
		if (cur && cur != tail && index == 0) {
			ListNode* next = cur->next;
			ListNode* prev = cur->prev;
			next->prev = prev;
			prev->next = next;
			delete cur;
		}
	}
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for $addAtHead()$, $addAtTail()$.
    - $O(n)$ time for $get()$, $addAtIndex()$, $deleteAtIndex()$.
- Space complexity: $O(n)$

## 4. Doubly Linked List (Optimal)

This optimization improves traversal time by choosing the shorter path. For indices in the first half of the list, we traverse forward from the head. For indices in the second half, we traverse backward from the tail. The `getPrev(index)` helper returns the predecessor node using this bidirectional approach, cutting worst-case traversal roughly in half on average.

```cpp
class MyLinkedList {
    struct ListNode {
        int val;
        ListNode* next;
        ListNode* prev;
        ListNode(int val = 0, ListNode* next = nullptr, ListNode* prev = nullptr) {
            this->val = val;
            this->next = next;
            this->prev = prev;
        }
    };

public:
    ListNode* head;
    ListNode* tail;
    int size;

    MyLinkedList() {
        head = new ListNode(0);
        tail = new ListNode(0);
        head->next = tail;
        tail->prev = head;
        size = 0;
    }

    ListNode* getPrev(int index) {
        if (index <= size / 2) {
            ListNode* cur = head;
            for (int i = 0; i < index; i++) {
                cur = cur->next;
            }
            return cur;
        } else {
            ListNode* cur = tail;
            for (int i = 0; i < size - index + 1; i++) {
                cur = cur->prev;
            }
            return cur;
        }
    }

    int get(int index) {
        if (index >= size) return -1;
        return getPrev(index)->next->val;
    }

    void addAtHead(int val) {
        addAtIndex(0, val);
    }

    void addAtTail(int val) {
        addAtIndex(size, val);
    }

    void addAtIndex(int index, int val) {
        if (index > size) return;
        ListNode* node = new ListNode(val);
        ListNode* prev = getPrev(index);
        ListNode* next = prev->next;
        prev->next = node;
        node->prev = prev;
        node->next = next;
        next->prev = node;
        size++;
    }

    void deleteAtIndex(int index) {
        if (index >= size) return;
        ListNode* prev = getPrev(index);
        ListNode* cur = prev->next;
        ListNode* next = cur->next;
        prev->next = next;
        next->prev = prev;
        delete cur;
        size--;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for $addAtHead()$, $addAtTail()$.
    - $O(n)$ time for $get()$, $addAtIndex()$, $deleteAtIndex()$.
- Space complexity: $O(n)$
