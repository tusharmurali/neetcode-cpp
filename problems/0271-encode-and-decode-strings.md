# 271. Encode and Decode Strings

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/encode-and-decode-strings/>  
- **NeetCode:** <https://neetcode.io/problems/string-encode-and-decode>  
- **Video:** <https://www.youtube.com/watch?v=B1k_sxOSgv8>  
- **Video approach:** 2. Encoding & Decoding (Optimal)  

[← Back to index](../INDEX.md)

## 1. Encoding & Decoding

To encode a list of strings into a single string, we need a way to store each string so that we can later separate them correctly during decoding.
A simple and reliable strategy is to record the **length of each string** first, followed by a special separator, and then append all the strings together.
During decoding, we can read the recorded lengths to know exactly how many characters to extract for each original string.
This avoids any issues with special characters, commas, or symbols inside the strings because the lengths tell us precisely where each string starts and ends.

```cpp
class Solution {
public:
    string encode(vector<string>& strs) {
        if (strs.empty()) return "";
        vector<int> sizes;
        string res;
        for (string& s : strs) {
            sizes.push_back(s.size());
        }
        for (int sz : sizes) {
            res.append(to_string(sz));
            res.push_back(',');
        }
        res.push_back('#');
        for (string& s : strs) {
            res.append(s);
        }
        return res;
    }

    vector<string> decode(string s) {
        if (s.empty()) return {};
        vector<int> sizes;
        vector<string> res;
        int i = 0;
        while (s[i] != '#') {
            int j = i;
            while (s[j] != ',') {
                j++;
            }
            sizes.push_back(stoi(s.substr(i, j - i)));
            i = j + 1;
        }
        i++;
        for (int sz : sizes) {
            res.push_back(s.substr(i, sz));
            i += sz;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$ for each $encode()$ and $decode()$ function calls.
- Space complexity: $O(m + n)$ for each $encode()$ and $decode()$ function calls.

> Where $m$ is the sum of lengths of all the strings and $n$ is the number of strings.

## 2. Encoding & Decoding (Optimal) ▶ video

Instead of storing all string lengths first and then appending the strings, we can directly attach each string to its length.  
For every string, we write **`length#string`**.  
The `#` character acts as a clear boundary between the length and the actual content, and using the length ensures we know exactly how many characters to read—no matter what characters appear in the string itself.  
During decoding, we simply read characters until we reach `#` to find the length, then extract exactly that many characters as the string.  
This approach is both simpler and more efficient because it avoids building separate sections for lengths and content.

```cpp
class Solution {
public:
    string encode(vector<string>& strs) {
        string res;
        for (const string& s : strs) {
            res.append(to_string(s.size()));
            res.push_back('#');
            res.append(s);
        }
        return res;
    }

    vector<string> decode(string s) {
        vector<string> res;
        int i = 0;
        while (i < s.size()) {
            int j = i;
            while (s[j] != '#') {
                j++;
            }
            int length = stoi(s.substr(i, j - i));
            i = j + 1;
            j = i + length;
            res.push_back(s.substr(i, length));
            i = j;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$ for each $encode()$ and $decode()$ function calls.
- Space complexity: $O(m + n)$ for each $encode()$ and $decode()$ function calls.

> Where $m$ is the sum of lengths of all the strings and $n$ is the number of strings.

## Standalone solution file (`cpp/0271-encode-and-decode-strings.cpp` in the NeetCode repo)

```cpp
/*
    Design algorithm to encode/decode: list of strings <-> string

    Encode/decode w/ non-ASCII delimiter: {len of str, "#", str}

    Time: O(n)
    Space: O(1)
*/

class Codec {
public:

    // Encodes a list of strings to a single string.
    string encode(vector<string>& strs) {
        string result;
        
        for (const string& str : strs) {
            result.append(to_string(str.size()));
            result.push_back('#');
            result.append(str);
        }
        
        return result;
    }

    // Decodes a single string to a list of strings.
    vector<string> decode(string s) {
        vector<string> result;
        
        int i = 0;
        while (i < s.size()) {
            int j = i;
            while (s[j] != '#') {
                j++;
            }
            int length = stoi(s.substr(i, j - i));
            string str = s.substr(j + 1, length);
            result.push_back(str);
            i = j + 1 + length;
        }
        
        return result;
    }
private:
};

// Your Codec object will be instantiated and called as such:
// Codec codec;
// codec.decode(codec.encode(strs));
```
