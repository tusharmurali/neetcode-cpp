# 428. Serialize and Deserialize N-ary Tree

- **Difficulty:** Hard  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/serialize-and-deserialize-n-ary-tree>  

[← Back to index](../INDEX.md)

## 1. Parent Child relationships

One way to serialize an n-ary tree is to record each node along with a unique identifier and its parent's identifier. During serialization, we assign each node an `ID`, store its value, and record its parent's `ID`. During deserialization, we first create all nodes, then link children to their parents using the stored parent `ID`s. This approach explicitly encodes the tree structure through parent references.

```cpp
class Codec {
public:
    string serialize(Node* root) {
        string result;
        int identity = 1;
        serializeHelper(root, result, identity, -1);
        return result;
    }

    void serializeHelper(Node* root, string& result, int& identity, int parentId) {
        if (!root) return;

        result += (char)(identity + '0');
        result += (char)(root->val + '0');
        result += (parentId == -1) ? 'N' : (char)(parentId + '0');

        int currentId = identity;
        for (Node* child : root->children) {
            identity++;
            serializeHelper(child, result, identity, currentId);
        }
    }

    Node* deserialize(string data) {
        if (data.empty()) return nullptr;

        unordered_map<int, Node*> nodes;

        for (int i = 0; i < data.size(); i += 3) {
            int identity = data[i] - '0';
            int orgValue = data[i + 1] - '0';
            nodes[identity] = new Node(orgValue, vector<Node*>());
        }

        for (int i = 3; i < data.size(); i += 3) {
            int identity = data[i] - '0';
            int parentId = data[i + 2] - '0';
            nodes[parentId]->children.push_back(nodes[identity]);
        }

        return nodes[data[0] - '0'];
    }
};
```

**Complexity**

- Time complexity:
    - `Serialization` : $O(N)$. For every node, we add 3 different values to the final string and every node is processed exactly once.

    - `Deserialization` : $O(N)$. Technically, it is $3N$ for the first for loop and $N$ for the second one. However, constants are ignored in asymptotic complexity analysis. So, the overall time complexity for deserialization is $O(N)$.

- Space complexity:
    - `Serialization` : $O(N)$. The space occupied by the serialization helper function is through recursion stack and the final string that is produced. Usually, we don't take into consideration the space of the output. However, in this case, the output is something which is not fixed. For all we know, someone might be able to generate a string of size $N/2$. We don't know! So, the size of the final string is a part of the space complexity here. Overall, the space is $4N = O(N)$.

    - `Deserialization` : $O(N)$. The space occupied by the deserialization helper function is through the hash map. For each entry, we have 3 values. Thus, we can say the space is $3N$. But again, the constants don't really matter in asymptotic complexity. So, the overall space is $O(N)$.

> Where $N$ is the number of nodes in the tree.

## 2. Depth First Search with Children Sizes

Instead of storing parent IDs, we can store each node's value followed by its number of children. This gives us enough information to reconstruct the tree during DFS deserialization. When we encounter a node, we know exactly how many children to expect, so we can recursively build each subtree. This approach is more space-efficient since we only need 2 characters per node.

```cpp
class Codec {
public:
    string serialize(Node* root) {
        string result;
        serializeHelper(root, result);
        return result;
    }

    void serializeHelper(Node* root, string& result) {
        if (!root) return;

        result += (char)(root->val + '0');
        result += (char)(root->children.size() + '0');

        for (Node* child : root->children) {
            serializeHelper(child, result);
        }
    }

    Node* deserialize(string data) {
        if (data.empty()) return nullptr;
        int index = 0;
        return deserializeHelper(data, index);
    }

    Node* deserializeHelper(string& data, int& index) {
        if (index == data.size()) return nullptr;

        Node* node = new Node(data[index] - '0', vector<Node*>());
        index++;
        int numChildren = data[index] - '0';
        for (int i = 0; i < numChildren; i++) {
            index++;
            node->children.push_back(deserializeHelper(data, index));
        }

        return node;
    }
};
```

**Complexity**

- Time complexity:
    - `Serialization` : $O(N)$. For every node, we add 2 different values to the final string and every node is processed exactly once.

    - `Deserialization` : $O(N)$. For deserialization, we process the entire string, one character at a time and also construct the tree along the way. So, the overall time complexity for deserialization is $2N = O(N)$.

- Space complexity:
    - `Serialization` : $O(N)$. The space occupied by the serialization helper function is through recursion stack and the final string that is produced. We know the size of the final string to be $2N$. So, that is one part of the space complexity. The other part is the one occupied by the recursion stack which is $O(N)$. Overall, the space is $O(N)$.

    - `Deserialization` : $O(N)$. For deserialization, the space occupied is by the recursion stack only. We don't use any other intermediate data structures like we did in the previous approach and simply rely on the information in the string and recursion to work it's magic. So, the space complexity would be $O(N)$ since this is not a `balanced` tree of any sort. It's not even binary.

> Where $N$ is the number of nodes in the tree.

## 3. Depth First Search with a Sentinel

Another approach uses a sentinel character (like '#') to mark the end of a node's children. After serializing a node's value and all its children recursively, we append the sentinel. During deserialization, we read nodes and recursively build children until we hit the sentinel, which signals that all children for the current node have been processed.

```cpp
class Codec {
public:
    string serialize(Node* root) {
        string result;
        serializeHelper(root, result);
        return result;
    }

    void serializeHelper(Node* root, string& result) {
        if (!root) return;

        result += (char)(root->val + '0');

        for (Node* child : root->children) {
            serializeHelper(child, result);
        }

        result += '#';
    }

    Node* deserialize(string data) {
        if (data.empty()) return nullptr;
        int index = 0;
        return deserializeHelper(data, index);
    }

    Node* deserializeHelper(string& data, int& index) {
        if (index == data.size()) return nullptr;

        Node* node = new Node(data[index] - '0', vector<Node*>());
        index++;
        while (data[index] != '#') {
            node->children.push_back(deserializeHelper(data, index));
        }

        index++;
        return node;
    }
};
```

**Complexity**

- Time complexity:
    - `Serialization` : $O(N)$. For every node, we add 2 different values to the final string and every node is processed exactly once.

    - `Deserialization` : $O(N)$. For deserialization, we process the entire string, one character at a time and also construct the tree along the way. So, the overall time complexity for deserialization is $2N = O(N)$.

- Space complexity:
    - `Serialization` : $O(N)$. The space occupied by the serialization helper function is through recursion stack and the final string that is produced. We know the size of the final string to be $2N$. So, that is one part of the space complexity. The other part is the one occupied by the recursion stack which is $O(N)$. Overall, the space is $O(N)$.

    - `Deserialization` : $O(N)$. For deserialization, the space occupied is by the recursion stack only. We don't use any other intermediate data structures like we did in the previous approach and simply rely on the information in the string and recursion to work it's magic. So, the overall space complexity would be $O(N)$.

> Where $N$ is the number of nodes in the tree.

## 4. Level order traversal

We can serialize the tree level by level using BFS. We use two sentinel markers: '#' to indicate the end of a level, and '$' to indicate switching to a different parent's children on the same level. During deserialization, we track nodes at the current and previous levels, using the sentinels to know when to move to the next level or switch parents.

```cpp
class Codec {
private:
    void _serializeHelper(Node* root, string& serializedList) {
        deque<variant<Node*, char>> queue;
        queue.push_back(root);
        queue.push_back(nullptr);

        while (!queue.empty()) {

            // Pop a node
            auto front = queue.front();
            queue.pop_front();

            // If this is an "endNode", we need to add another one
            // to mark the end of the current level unless this
            // was the last level.
            if (holds_alternative<Node*>(front) && get<Node*>(front) == nullptr) {

                // We add a sentinel value of "#" here
                serializedList += "#,";
                if (!queue.empty()) {
                    queue.push_back(nullptr);
                }
            }
            // Add a sentinel value of "$" here to mark the switch to a
            // different parent.
            else if (holds_alternative<char>(front) && get<char>(front) == 'C') {
                serializedList += "$,";
            }
            else {

                // Add value of the current node and add all of its
                // children nodes to the queue.
                Node* node = get<Node*>(front);
                serializedList += to_string(node->val) + ",";
                for (Node* child : node->children) {
                    queue.push_back(child);
                }

                // If this node is NOT the last one on the current level,
                // add a childNode as well since we move on to processing
                // the next node.
                if (!queue.empty() &&
                    !(holds_alternative<Node*>(queue.front()) && get<Node*>(queue.front()) == nullptr)) {
                    queue.push_back('C');
                }
            }
        }
    }

    void _deserializeHelper(const string& data, Node* rootNode) {

        // We move one level at a time and at every level, we need access
        // to the nodes on the previous level as well so that we can form
        // the children arrays properly. Hence two arrays.
        deque<Node*> prevLevel, currentLevel;
        currentLevel.push_back(rootNode);
        Node* parentNode = rootNode;

        int i = 0;
        // Skip past first value (already parsed for rootNode)
        while (i < data.length() && data[i] != ',') i++;
        i++; // skip comma

        // Process the characters in the string one at a time.
        while (i < data.length()) {

            // Special processing for end of level. We need to swap the
            // array lists. Here, we simply re-initialize the "currentLevel"
            // arraylist rather than clearing it.
            if (data[i] == '#') {
                prevLevel = currentLevel;
                currentLevel = deque<Node*>();

                // Since we move one level down, we take the parent as the first
                // node on the current level.
                if (!prevLevel.empty()) {
                    parentNode = prevLevel.front();
                    prevLevel.pop_front();
                } else {
                    parentNode = nullptr;
                }
                i += 2; // skip "#,"
            }
            // Special handling for change in parent on the same level
            else if (data[i] == '$') {
                if (!prevLevel.empty()) {
                    parentNode = prevLevel.front();
                    prevLevel.pop_front();
                } else {
                    parentNode = nullptr;
                }
                i += 2; // skip "$,"
            }
            else {
                // Parse number (handles multi-digit values)
                int val = 0;
                while (i < data.length() && data[i] != ',') {
                    val = val * 10 + (data[i] - '0');
                    i++;
                }
                i++; // skip comma

                Node* childNode = new Node(val, vector<Node*>());
                currentLevel.push_back(childNode);
                parentNode->children.push_back(childNode);
            }
        }
    }

public:
    string serialize(Node* root) {
        if (root == nullptr) {
            return "";
        }

        string serializedList;
        _serializeHelper(root, serializedList);
        return serializedList;
    }

    Node* deserialize(string data) {
        if (data.empty()) {
            return nullptr;
        }

        // Parse first value (handles multi-digit values)
        int val = 0;
        int i = 0;
        while (i < data.length() && data[i] != ',') {
            val = val * 10 + (data[i] - '0');
            i++;
        }

        Node* rootNode = new Node(val, vector<Node*>());
        _deserializeHelper(data, rootNode);
        return rootNode;
    }
};
```

**Complexity**

- Time complexity:
    - `Serialization` : $O(N)$. For every node, we add 2 different values to the final string and every node is processed exactly once. We add the value of the node itself and we also add the child switch sentinel. Also, for the nodes that end a particular level, we add the level end sentinel.

    - `Deserialization` : $O(N)$. For deserialization, we process the entire string, one character at a time and also construct the tree along the way. So, the overall time complexity for deserialization is $2N = O(N)$.

- Space complexity:
    - `Serialization` : $O(N)$. The space occupied by the serialization helper function is through the queue and the final string that is produced. We know the size of the final string to be $2N$. So that is one part of the space complexity. The other part is the one occupied by the queue which is $O(N)$. Overall, the space is $O(N)$.

    - `Deserialization` : $O(N)$. For deserialization, the space is mostly occupied by the two lists that we use. The space complexity there is $O(N)$. Note that when we re-initialize a list, the memory that was allocated earlier is deallocated by the garbage collector and it's essentially equal to a single list of size $O(N)$.

> Where $N$ is the number of nodes in the tree.
