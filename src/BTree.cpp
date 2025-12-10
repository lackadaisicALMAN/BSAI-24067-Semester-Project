
#include "../include/BTree.h"
#include <fstream>
#include <sstream>
#include <string>
#include <set>

// Write a single batch to persistent storage
void BTree::writeBatchToStorage(RiceBatch* batch)
{
    if (batch == nullptr) return;
    
    std::ofstream file("data/storage.txt", std::ios::app); // Append mode
    if (!file.is_open()) {
        std::cerr << "Error: Could not open storage.txt for writing" << std::endl;
        return;
    }
    
    file << batch->batchID << "|"
         << batch->farmerName << "|"
         << batch->weight << "|"
         << batch->moistureLevel << "|"
         << batch->arrivalDate << "\n";
    
    file.close();
}

// Load data from storage.txt and rebuild the B-Tree
void BTree::loadFromStorage() {
    std::ifstream file("data/storage.txt");
    if (!file.is_open()) {
        // File doesn't exist yet, that's okay
        return;
    }
    
    isLoading = true; // Set flag to prevent writing during load
    
    std::string line;
    std::set<int> loadedIDs; // Track loaded IDs to avoid duplicates
    
    while (std::getline(file, line)) {
        if (line.empty()) continue;
        
        // Parse the line: batchID|farmerName|weight|moistureLevel|arrivalDate
        std::istringstream iss(line);
        std::string token;
        std::vector<std::string> tokens;
        
        while (std::getline(iss, token, '|')) {
            tokens.push_back(token);
        }
        
        // Validate we have all 5 fields
        if (tokens.size() != 5) {
            continue; // Skip malformed lines
        }
        
        try {
            int batchID = std::stoi(tokens[0]);
            std::string farmerName = tokens[1];
            double weight = std::stod(tokens[2]);
            double moistureLevel = std::stod(tokens[3]);
            std::string arrivalDate = tokens[4];
            
            // Skip entries with invalid data (like the corrupted ones)
            if (batchID <= 0 || weight < 0 || moistureLevel < 0 || farmerName.empty()) {
                continue;
            }
            
            // Skip if we've already loaded this ID (avoid duplicates)
            if (loadedIDs.find(batchID) != loadedIDs.end()) {
                continue;
            }
            
            // Insert into B-Tree
            insert(new RiceBatch(batchID, farmerName, weight, moistureLevel, arrivalDate));
            loadedIDs.insert(batchID);
        } catch (const std::exception& e) {
            // Skip lines that can't be parsed
            continue;
        }
    }
    
    file.close();
    isLoading = false; // Reset flag
}

// --- Node Implementation ---

BTreeNode::BTreeNode(bool isLeaf) {
    leaf = isLeaf;
    n = 0;
    // Initialize all pointers to nullptr for safety
    for (int i = 0; i < 2 * T_DEGREE - 1; i++) {
        keys[i] = nullptr;
    }
    for (int i = 0; i < 2 * T_DEGREE; i++) {
        children[i] = nullptr;
    }
}

// Traverse all nodes (In-order traversal)
void BTreeNode::traverse() {
    int i;
    for (i = 0; i < n; i++) {
        if (!leaf) children[i]->traverse();
        keys[i]->printBatch();
    }
    if (!leaf) children[i]->traverse();
}

// Search for a specific Batch ID
BTreeNode* BTreeNode::search(int batchID) {
    int i = 0;
    while (i < n && batchID > keys[i]->batchID)
        i++;

    if (i < n && keys[i]->batchID == batchID)
        return this;

    if (leaf)
        return nullptr;

    return children[i]->search(batchID);
}

// --- BTree Class Implementation ---

BTree::BTree() {
    root = nullptr;
    isLoading = false;
}

void BTree::traverse() {
    if (root != nullptr) root->traverse();
}

RiceBatch* BTree::search(int batchID) {
    if (root == nullptr) return nullptr;
    
    BTreeNode* resNode = root->search(batchID);
    if (resNode == nullptr) return nullptr;

    // Find the exact key within the node
    for(int i=0; i < resNode->n; i++) {
        if(resNode->keys[i]->batchID == batchID)
            return resNode->keys[i];
    }
    return nullptr;
}

void BTree::insert(RiceBatch* k) {
    if (root == nullptr) {
        root = new BTreeNode(true);
        root->keys[0] = k;
        root->n = 1;
    } else {
        if (root->n == 2 * T_DEGREE - 1) {
            BTreeNode* s = new BTreeNode(false);
            s->children[0] = root;
            s->splitChild(0, root);
            int i = 0;
            if (s->keys[0]->batchID < k->batchID)
                i++;
            s->children[i]->insertNonFull(k);
            root = s;
        } else {
            root->insertNonFull(k);
        }
    }
    
    // Write the new batch to storage (only when inserting, not during loading)
    if (!isLoading) {
        writeBatchToStorage(k);
    }
}

void BTreeNode::insertNonFull(RiceBatch* k) {
    int i = n - 1;

    if (leaf) {
        while (i >= 0 && keys[i]->batchID > k->batchID) {
            keys[i + 1] = keys[i];
            i--;
        }
        keys[i + 1] = k;
        n = n + 1;
    } else {
        while (i >= 0 && keys[i]->batchID > k->batchID)
            i--;
        if (children[i + 1]->n == 2 * T_DEGREE - 1) {
            splitChild(i + 1, children[i + 1]);
            if (keys[i + 1]->batchID < k->batchID)
                i++;
        }
        children[i + 1]->insertNonFull(k);
    }
}

void BTreeNode::splitChild(int i, BTreeNode* y) {
    BTreeNode* z = new BTreeNode(y->leaf);
    z->n = T_DEGREE - 1;

    for (int j = 0; j < T_DEGREE - 1; j++)
        z->keys[j] = y->keys[j + T_DEGREE];

    if (!y->leaf) {
        for (int j = 0; j < T_DEGREE; j++)
            z->children[j] = y->children[j + T_DEGREE];
    }

    y->n = T_DEGREE - 1;

    for (int j = n; j >= i + 1; j--)
        children[j + 1] = children[j];

    children[i + 1] = z;

    for (int j = n - 1; j >= i; j--)
        keys[j + 1] = keys[j];

    keys[i] = y->keys[T_DEGREE - 1];
    n = n + 1;
}