
#ifndef RICEBATCH_H
#define RICEBATCH_H

#include <string>
#include <iostream>

using namespace std;

// This represents one "Row" in your database
struct RiceBatch {
    int batchID;            // The Key for the B-Tree
    string farmerName;
    double weight;          // In kg
    double moistureLevel;   // e.g., 24.5
    string arrivalDate;     // "2025-12-09"

    // Constructor
    RiceBatch(int id = 0, string name = "", double w = 0.0, double m = 0.0, string date = "") 
        : batchID(id), farmerName(name), weight(w), moistureLevel(m), arrivalDate(date) {}

    // Utility to display batch info
    void printBatch() const {
        cout << "[ID: " << batchID << "] | Farmer: " << farmerName 
             << " | Weight: " << weight << "kg | Moisture: " << moistureLevel << "%" << endl;
    }
};

#endif