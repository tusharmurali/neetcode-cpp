# 150. Evaluate Reverse Polish Notation

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/evaluate-reverse-polish-notation/>  
- **NeetCode:** <https://neetcode.io/problems/evaluate-reverse-polish-notation>  
- **Video:** <https://www.youtube.com/watch?v=iu0082c4HDE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Reverse Polish Notation (RPN) evaluates expressions without parentheses by applying each operator to the two most recent numbers.  
The brute-force idea is to repeatedly scan the list until we find an operator.  
When we do, we take the two numbers before it, compute the result, and replace all three tokens with the result.  
We continue compressing the list this way until only one value remains—the final answer.  
This approach works but is slow because we repeatedly rebuild and rescan the list.

```cpp
class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        while (tokens.size() > 1) {
            for (int i = 0; i < tokens.size(); i++) {
                if (tokens[i] == "+"
                    || tokens[i] == "-"
                    || tokens[i] == "*"
                    || tokens[i] == "/")
                {
                    int a = stoi(tokens[i - 2]);
                    int b = stoi(tokens[i - 1]);
                    int result = 0;
                    if (tokens[i] == "+") result = a + b;
                    else if (tokens[i] == "-") result = a - b;
                    else if (tokens[i] == "*") result = a * b;
                    else if (tokens[i] == "/") result = a / b;

                    tokens.erase(tokens.begin() + i - 2, tokens.begin() + i + 1);
                    tokens.insert(tokens.begin() + i - 2, to_string(result));
                    break;
                }
            }
        }
        return stoi(tokens[0]);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Doubly Linked List

In Reverse Polish Notation, every operator works on the two most recent numbers before it.  
A doubly linked list lets us move **both left and right** easily, so when we find an operator, we can quickly reach the two numbers before it.

The idea is:

- Build a doubly linked list of all tokens (numbers and operators).
- Walk through the list:
    - When we see an operator, we look at the previous two nodes (the two operands),
      compute the result, and **replace those three nodes** (`left`, `right`, `operator`)
      with a single node containing the result.
- We keep doing this until we've processed all operators and are left with just one value.

This behaves like the usual RPN evaluation but uses linked list navigation instead of a stack.

```cpp
class DoublyLinkedList {
public:
    string val;
    DoublyLinkedList* next;
    DoublyLinkedList* prev;

    DoublyLinkedList(string val, DoublyLinkedList* next = nullptr,
                        DoublyLinkedList* prev = nullptr) {
        this->val = val;
        this->next = next;
        this->prev = prev;
    }
};

class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        DoublyLinkedList* head = new DoublyLinkedList(tokens[0]);
        DoublyLinkedList* curr = head;

        for (int i = 1; i < tokens.size(); i++) {
            curr->next = new DoublyLinkedList(tokens[i], nullptr, curr);
            curr = curr->next;
        }

        int ans = 0;
        while (head != nullptr) {
            if (head->val == "+" ||
                 head->val == "-" ||
                 head->val == "*" ||
                 head->val == "/")
            {
                int l = stoi(head->prev->prev->val);
                int r = stoi(head->prev->val);
                int res = 0;
                if (head->val == "+") {
                    res = l + r;
                } else if (head->val == "-") {
                    res = l - r;
                } else if (head->val == "*") {
                    res = l * r;
                } else {
                    res = l / r;
                }

                head->val = to_string(res);
                head->prev = head->prev->prev->prev;
                if (head->prev != nullptr) {
                    head->prev->next = head;
                }
            }

            ans = stoi(head->val);
            head = head->next;
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Recursion

Reverse Polish Notation works naturally with recursion because every operator applies to the **two most recent values** that come before it.  
If we process the expression from the end, every time we see:

- a **number** → it is simply returned as a value
- an **operator** → we recursively evaluate the two values that belong to it

This creates a natural evaluation tree:

- Each operator becomes a recursive call,
- Each number becomes a base case,
- And the final return value is the fully evaluated expression.

This approach is clean, elegant, and mirrors the structure of RPN itself.

```cpp
class Solution {
public:
    int dfs(vector<string>& tokens) {
        string token = tokens.back();
        tokens.pop_back();

        if (token != "+" && token != "-" &&
             token != "*" && token != "/")
        {
            return stoi(token);
        }

        int right = dfs(tokens);
        int left = dfs(tokens);

        if (token == "+") {
            return left + right;
        } else if (token == "-") {
            return left - right;
        } else if (token == "*") {
            return left * right;
        } else {
            return left / right;
        }
    }

    int evalRPN(vector<string>& tokens) {
        return dfs(tokens);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Stack

A stack fits Reverse Polish Notation perfectly because the most recent numbers are always the ones used next.  
As we scan the tokens:

- When we see a **number**, we push it onto the stack.
- When we see an **operator**, we pop the top two numbers, apply the operation, and push the result back.

This way, the stack always holds the intermediate results, and the final remaining value is the answer.  
It is clean, efficient, and directly follows how RPN is meant to be evaluated.

```cpp
class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<int> stack;
        for (const string& c : tokens) {
            if (c == "+") {
                int a = stack.top(); stack.pop();
                int b = stack.top(); stack.pop();
                stack.push(b + a);
            } else if (c == "-") {
                int a = stack.top(); stack.pop();
                int b = stack.top(); stack.pop();
                stack.push(b - a);
            } else if (c == "*") {
                int a = stack.top(); stack.pop();
                int b = stack.top(); stack.pop();
                stack.push(b * a);
            } else if (c == "/") {
                int a = stack.top(); stack.pop();
                int b = stack.top(); stack.pop();
                stack.push(b / a);
            } else {
                stack.push(stoi(c));
            }
        }
        return stack.top();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0150-evaluate-reverse-polish-notation.cpp` in the NeetCode repo)

```cpp
/*
    Evaluate RPN, valid operators: +, -, *, /

    Stack, if num push, if operator apply to top 2 nums

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<int> stk;
        
        for (int i = 0; i < tokens.size(); i++) {
            string token = tokens[i];
            
            if (token.size() > 1 || isdigit(token[0])) {
                stk.push(stoi(token));
                continue;
            }
            
            int num2 = stk.top();
            stk.pop();
            int num1 = stk.top();
            stk.pop();
            
            int result = 0;
            if (token == "+") {
                result = num1 + num2;
            } else if (token == "-") {
                result = num1 - num2;
            } else if (token == "*") {
                result = num1 * num2;
            } else {
                result = num1 / num2;
            }
            stk.push(result);
        }
        
        return stk.top();
    }
};
```
