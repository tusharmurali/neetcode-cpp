# 588. Design In-Memory File System

- **Difficulty:** Hard  
- **Pattern:** Tries  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-in-memory-file-system/>  
- **NeetCode:** <https://neetcode.io/problems/design-in-memory-file-system>  

[← Back to index](../INDEX.md)

## 1. Using separate Directory and File List

A file system has a natural tree structure where each directory can contain subdirectories and files. We model this by creating a `Dir` class that holds two hash maps: one for subdirectories and one for files. The root of the file system is a single `Dir` object. When we need to navigate to a path, we split it by "/" and traverse through the tree one directory at a time. This separation of directories and files makes it easy to distinguish between them when listing contents or reading file data.

```cpp
class FileSystem {
private:
    class Dir {
    public:
        unordered_map<string, Dir*> dirs;
        unordered_map<string, string> files;
    };
    
    Dir* root;
    
    vector<string> split(const string& path) {
        vector<string> result;
        string current = "";
        
        for (char c : path) {
            if (c == '/') {
                if (!current.empty()) {
                    result.push_back(current);
                    current = "";
                }
            } else {
                current += c;
            }
        }
        if (!current.empty()) {
            result.push_back(current);
        }
        
        return result;
    }
    
public:
    FileSystem() {
        root = new Dir();
    }
    
    vector<string> ls(string path) {
        Dir* t = root;
        vector<string> files;
        
        if (path != "/") {
            vector<string> d = split(path);
            
            for (int i = 0; i < d.size() - 1; i++) {
                t = t->dirs[d[i]];
            }
            
            if (t->files.find(d[d.size() - 1]) != t->files.end()) {
                files.push_back(d[d.size() - 1]);
                return files;
            } else {
                t = t->dirs[d[d.size() - 1]];
            }
        }
        
        for (auto& pair : t->dirs) {
            files.push_back(pair.first);
        }
        
        for (auto& pair : t->files) {
            files.push_back(pair.first);
        }
        
        sort(files.begin(), files.end());
        return files;
    }
    
    void mkdir(string path) {
        Dir* t = root;
        vector<string> d = split(path);
        
        for (int i = 0; i < d.size(); i++) {
            if (t->dirs.find(d[i]) == t->dirs.end()) {
                t->dirs[d[i]] = new Dir();
            }
            t = t->dirs[d[i]];
        }
    }
    
    void addContentToFile(string filePath, string content) {
        Dir* t = root;
        vector<string> d = split(filePath);
        
        for (int i = 0; i < d.size() - 1; i++) {
            t = t->dirs[d[i]];
        }
        
        t->files[d[d.size() - 1]] += content;
    }
    
    string readContentFromFile(string filePath) {
        Dir* t = root;
        vector<string> d = split(filePath);
        
        for (int i = 0; i < d.size() - 1; i++) {
            t = t->dirs[d[i]];
        }
        
        return t->files[d[d.size() - 1]];
    }
};
```

## 2. Using unified Directory and File List

Instead of maintaining separate maps for directories and files, we can use a single unified structure. Each node in our tree is a `File` object that can act as either a directory or a file. A boolean flag `isFile` tells us which role it plays. Directories store child nodes in a map, while files store their content in a string. This unified approach simplifies the data structure since we only need one type of node, and path traversal becomes more uniform.

```cpp
class FileSystem {
private:
    struct File {
        bool isfile = false;
        unordered_map<string, File*> files;
        string content = "";
    };

    File* root;

public:
    FileSystem() {
        root = new File();
    }

    vector<string> ls(string path) {
        File* t = root;
        vector<string> files;
        if (path != "/") {
            vector<string> d;
            stringstream ss(path);
            string item;
            while (getline(ss, item, '/')) {
                if (!item.empty()) d.push_back(item);
            }
            for (int i = 0; i < d.size(); i++) {
                t = t->files[d[i]];
            }
            if (t->isfile) {
                return {d[d.size() - 1]};
            }
        }
        for (auto& p : t->files) {
            files.push_back(p.first);
        }
        sort(files.begin(), files.end());
        return files;
    }

    void mkdir(string path) {
        File* t = root;
        vector<string> d;
        stringstream ss(path);
        string item;
        while (getline(ss, item, '/')) {
            if (!item.empty()) d.push_back(item);
        }
        for (int i = 0; i < d.size(); i++) {
            if (t->files.find(d[i]) == t->files.end()) {
                t->files[d[i]] = new File();
            }
            t = t->files[d[i]];
        }
    }

    void addContentToFile(string filePath, string content) {
        File* t = root;
        vector<string> d;
        stringstream ss(filePath);
        string item;
        while (getline(ss, item, '/')) {
            if (!item.empty()) d.push_back(item);
        }
        for (int i = 0; i < d.size() - 1; i++) {
            t = t->files[d[i]];
        }
        if (t->files.find(d[d.size() - 1]) == t->files.end()) {
            t->files[d[d.size() - 1]] = new File();
        }
        t = t->files[d[d.size() - 1]];
        t->isfile = true;
        t->content += content;
    }

    string readContentFromFile(string filePath) {
        File* t = root;
        vector<string> d;
        stringstream ss(filePath);
        string item;
        while (getline(ss, item, '/')) {
            if (!item.empty()) d.push_back(item);
        }
        for (int i = 0; i < d.size() - 1; i++) {
            t = t->files[d[i]];
        }
        return t->files[d[d.size() - 1]]->content;
    }
};
```
