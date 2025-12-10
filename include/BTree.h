
#ifndef BTREE_H
#define BTREE_H

#include "RiceBatch.h"
#include <vector>
#include <iostream>

// Minimum degree (defines the range for number of keys)
// t=3 means every node must have at least 2 keys and at most 5 keys
const int T_DEGREE = 3; 

// A BTree Node
struct BTreeNode {
    RiceBatch* keys[2 * T_DEGREE - 1];  // Array of pointers to RiceBatches
    BTreeNode* children[2 * T_DEGREE];  // Array of pointers to children nodes
    int n;                              // Current number of keys
    bool leaf;                          // Is this a leaf node?

    BTreeNode(bool isLeaf);
    
    // Core B-Tree Operations
    void traverse();
    BTreeNode* search(int batchID);
    void insertNonFull(RiceBatch* k);
    void splitChild(int i, BTreeNode* y);
};

class BTree {
    BTreeNode* root; // Pointer to root node
    bool isLoading;   // Flag to prevent writing during load

public:
    BTree();
    void traverse();
    RiceBatch* search(int batchID);
    void insert(RiceBatch* k);
    void loadFromStorage(); // Load data from storage.txt
    void writeBatchToStorage(RiceBatch* batch); // Write a single batch to storage
};

#endif