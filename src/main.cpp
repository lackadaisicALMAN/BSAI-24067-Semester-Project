
#include <iostream>
#include <limits>
#include <string>
#include "../include/BTree.h"

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
    cout << "4. Exit" << endl;
    cout << "Select Option: ";
}

int main() {
    BTree db;
    
    // Load existing data from storage
    cout << "Loading data from storage..." << endl;
    db.loadFromStorage();
    
    // Pre-seed default data only if storage is empty
    if (db.search(101) == nullptr)
    {
        db.insert(new RiceBatch(101, "Ali Khan", 500.0, 24.5, "2025-12-01"));
        db.insert(new RiceBatch(105, "Ghulam Rasool", 320.0, 21.0, "2025-12-02"));
        db.insert(new RiceBatch(102, "Bashir Ahmed", 800.0, 23.2, "2025-12-03"));
        cout << "Default batches loaded." << endl;
    }

    int choice;
    while (true)
    {
        showMenu();
        
        // Read choice with error handling
        if (!(cin >> choice))
        {
            cout << ">> ERROR: Invalid input. Please enter a number between 1-4." << endl;
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

            db.insert(new RiceBatch(id, name, w, m, date));
            cout << ">> Batch Saved Successfully!" << endl;
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
            break;
        }
        else {
            cout << ">> ERROR: Invalid choice. Please select 1-4." << endl;
        }
    }
    return 0;
}