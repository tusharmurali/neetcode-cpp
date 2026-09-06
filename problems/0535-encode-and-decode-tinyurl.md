# 535. Encode and Decode TinyURL

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/encode-and-decode-tinyurl/>  
- **NeetCode:** <https://neetcode.io/problems/encode-and-decode-tinyurl>  
- **Video:** <https://www.youtube.com/watch?v=VyBOaboQLGc>  

[← Back to index](../INDEX.md)

## 1. List

The simplest way to create a URL shortener is to assign each long URL a unique integer ID based on its position in a list. The short URL is just the base URL plus this index. When decoding, we extract the index from the short URL and retrieve the original URL from the list. This approach is straightforward but the short URL length grows with the number of stored URLs.

```cpp
class Solution {
public:
    vector<string> urls;

    string encode(string longUrl) {
        urls.push_back(longUrl);
        return "http://tinyurl.com/" + to_string(urls.size() - 1);
    }

    string decode(string shortUrl) {
        int index = stoi(shortUrl.substr(shortUrl.find_last_of('/') + 1));
        return urls[index];
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $encode()$ and $decode()$.
- Space complexity: $O(n * m)$

> Where $n$ is the number of $longUrls$, $m$ is the average length of the URLs.

## 2. Hash Map - I

Instead of using a list with implicit indices, we use a hash map with an explicit incrementing ID. This offers more flexibility since we can use the ID as a key and don't rely on list indexing. Each new URL gets assigned the current ID, which then increments. The hash map allows constant-time lookup when decoding.

```cpp
class Solution {
    unordered_map<int, string> urlMap;
    int id;

public:
    Solution() : id(0) {}

    string encode(string longUrl) {
        urlMap[id] = longUrl;
        return "http://tinyurl.com/" + to_string(id++);
    }

    string decode(string shortUrl) {
        int urlId = stoi(shortUrl.substr(shortUrl.find_last_of('/') + 1));
        return urlMap[urlId];
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $encode()$ and $decode()$.
- Space complexity: $O(n * m)$

> Where $n$ is the number of $longUrls$, $m$ is the average length of the URLs.

## 3. Hash Map - II

This approach uses two hash maps to create a bidirectional mapping. One maps long URLs to short URLs, and the other maps short URLs back to long URLs. This ensures that encoding the same long URL twice returns the same short URL, avoiding duplicates. The trade-off is using more memory for the extra map.

```cpp
class Solution {
private:
    unordered_map<string, string> encodeMap;
    unordered_map<string, string> decodeMap;
    string base = "http://tinyurl.com/";

public:
    string encode(string longUrl) {
        if (encodeMap.find(longUrl) == encodeMap.end()) {
            string shortUrl = base + to_string(encodeMap.size() + 1);
            encodeMap[longUrl] = shortUrl;
            decodeMap[shortUrl] = longUrl;
        }
        return encodeMap[longUrl];
    }

    string decode(string shortUrl) {
        return decodeMap[shortUrl];
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $encode()$ and $decode()$.
- Space complexity: $O(n * m)$

> Where $n$ is the number of $longUrls$, $m$ is the average length of the URLs.

## Standalone solution file (`cpp/0535-encode-and-decode-tinyurl.cpp` in the NeetCode repo)

```cpp
class Solution {
private:
    map<string, string> encodeMap;
    map<string, string> decodeMap;
    string base = "http://tinyurl.com/";
public:
    // Encodes a URL to a shortened URL.
    string encode(string longUrl) {
        if(!encodeMap.count(longUrl)) {
            string shortUrl = base + to_string(encodeMap.size() + 1);
            encodeMap[longUrl] = shortUrl;
            decodeMap[shortUrl] = longUrl;
        }
        return encodeMap[longUrl];
    }

    // Decodes a shortened URL to its original URL.
    string decode(string shortUrl) {
        return decodeMap[shortUrl];
    }
};
```
