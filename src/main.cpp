
#include <iostream>
#include <limits>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include "../include/BTree.h"
#include "../include/HashMap.h"
#include "../include/PriorityQueue.h"

using namespace std;

// Helper function to clear cin error state and buffer
void clearInputBuffer() {
    cin.clear(); // Clear error flags
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Clear buffer
}

// Helper function to safely read an integer
bool readInt(int& value, const string& prompt) {
    cout << prompt;
    if (cin >> value) {
        clearInputBuffer();
        return true;
    } else {
        cout << ">> ERROR: Please enter a valid number (integer)." << endl;
        clearInputBuffer();
        return false;
    }
}

// Helper function to safely read a double
bool readDouble(double& value, const string& prompt) {
    cout << prompt;
    if (cin >> value) {
        clearInputBuffer();
        return true;
    } else {
        cout << ">> ERROR: Please enter a valid number (decimal)." << endl;
        clearInputBuffer();
        return false;
    }
}

// Helper function to safely read a string
bool readString(string& value, const string& prompt) {
    cout << prompt;
    if (!getline(cin, value)) {
        clearInputBuffer();
        return false;
    }
    return true;
}

void showMenu() {
    cout << "\n=== AgriYield Core System ===" << endl;
    cout << "1. Add New Rice Batch" << endl;
    cout << "2. View All Batches (Sorted)" << endl;
    cout << "3. Search Batch by ID" << endl;
    cout << "4. Check Next Batch for Drying (Wettest)" << endl;
    cout << "5. Check Next Batch for Processing (Driest)" << endl;
    cout << "6. Exit" << endl;
    cout << "Select Option: ";
}

int main() {
    BTree db;
    SupplierMap suppliers;
    DryingQueue dryingQueue;
    
    // Load existing data from storage
    cout << "Loading data from storage..." << endl;
    db.loadFromStorage();
    
    // Populate dryingQueue with batches from storage
    ifstream storageFile("data/storage.txt");
    if (storageFile.is_open()) {
        string line;
        while (getline(storageFile, line)) {
            if (line.empty()) continue;
            istringstream iss(line);
            string token;
            vector<string> tokens;
            while (getline(iss, token, '|')) {
                tokens.push_back(token);
            }
            if (tokens.size() == 5) {
                try {
                    int bid = stoi(tokens[0]);
                    RiceBatch* found = db.search(bid);
                    if (found) {
                        dryingQueue.push(*found);
                    }
                } catch (...) {}
            }
        }
        storageFile.close();
    }
    
    // Pre-seed default data only if storage is empty
    if (db.search(101) == nullptr)
    {
        RiceBatch b1(101, "Ali Khan", 500.0, 24.5, "2025-12-01");
        db.insert(new RiceBatch(b1));
        dryingQueue.push(b1);

        RiceBatch b2(105, "Ghulam Rasool", 320.0, 21.0, "2025-12-02");
        db.insert(new RiceBatch(b2));
        dryingQueue.push(b2);

        RiceBatch b3(102, "Bashir Ahmed", 800.0, 23.2, "2025-12-03");
        db.insert(new RiceBatch(b3));
        dryingQueue.push(b3);

        cout << "Default batches loaded." << endl;
    }

    int choice;
    while (true)
    {
        showMenu();
        
        // Read choice with error handling
        if (!(cin >> choice))
        {
            cout << ">> ERROR: Invalid input. Please enter a number between 1-6." << endl;
            clearInputBuffer();
            continue;
        }
        clearInputBuffer();

        if (choice == 1)
        {
            int id;
            string name, date;
            double w, m;
            
            // Read Batch ID (must be a positive integer)
            if (!readInt(id, "Enter Batch ID: ")) {
                continue;
            }
            if (id <= 0) {
                cout << ">> ERROR: Batch ID must be a positive number. Please try again." << endl;
                continue;
            }
            
            // Check if ID already exists
            if (db.search(id) != nullptr) {
                cout << ">> ERROR: Batch ID " << id << " already exists. Please use a different ID." << endl;
                continue;
            }
            
            // Read Farmer Name
            if (!readString(name, "Enter Farmer Name: ")) {
                continue;
            }
            if (name.empty()) {
                cout << ">> ERROR: Farmer name cannot be empty. Please try again." << endl;
                continue;
            }
            
            // Read Weight (must be positive)
            if (!readDouble(w, "Enter Weight (kg): ")) {
                continue;
            }
            if (w <= 0) {
                cout << ">> ERROR: Weight must be a positive number. Please try again." << endl;
                continue;
            }
            
            // Read Moisture Level (must be between 0-100)
            if (!readDouble(m, "Enter Moisture (%): ")) {
                continue;
            }
            if (m < 0 || m > 100) {
                cout << ">> ERROR: Moisture level must be between 0-100. Please try again." << endl;
                continue;
            }
            
            // Read Date
            if (!readString(date, "Enter Date (YYYY-MM-DD): ")) {
                continue;
            }
            if (date.empty()) {
                cout << ">> ERROR: Date cannot be empty. Please try again." << endl;
                continue;
            }

            {
                RiceBatch batch(id, name, w, m, date);
                db.insert(new RiceBatch(batch));
                dryingQueue.push(batch);
                cout << ">> Batch Saved Successfully!" << endl;
            }
        } 
        else if (choice == 2)
        {
            cout << "\n--- Current Inventory ---" << endl;
            db.traverse();
        } 
        else if (choice == 3)
        {
            int searchId;
            if (!readInt(searchId, "Enter Batch ID to find: ")) {
                continue;
            }
            RiceBatch* result = db.search(searchId);
            if (result) {
                cout << ">> FOUND: ";
                result->printBatch();
            } else {
                cout << ">> ERROR: Batch ID not found." << endl;
            }
        } 
        else if (choice == 4)
        {
            if (dryingQueue.isEmpty()) {
                cout << ">> No batches queued for drying." << endl;
            } else {
                const RiceBatch& wettest = dryingQueue.peek();
                cout << ">> Next Batch for Drying (Wettest): ";
                wettest.printBatch();
            }
        } 
        else if (choice == 5)
        {
            if (dryingQueue.isEmpty()) {
                cout << ">> No batches available for processing." << endl;
            } else {
                const RiceBatch* driest = dryingQueue.findLowestMoistureBatch();
                cout << ">> Next Batch for Processing (Driest): ";
                driest->printBatch();
            }
        } 
        else if (choice == 6)
        {
            break;
        }
        else {
            cout << ">> ERROR: Invalid choice. Please select 1-6." << endl;
        }
    }
    return 0;
}