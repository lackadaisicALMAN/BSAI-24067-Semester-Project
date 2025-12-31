#ifndef HASHMAP_H
#define HASHMAP_H

#include <string>
#include <vector>
#include <list>
#include <cstddef>

// SupplierMap: simple hash table for Farmer details using chaining.
struct Farmer {
    std::string name;
    std::string contactInfo;
    double totalRiceSold;

    Farmer(const std::string& n = "", const std::string& c = "", double t = 0.0)
        : name(n), contactInfo(c), totalRiceSold(t) {}
};

class SupplierMap {
public:
    explicit SupplierMap(std::size_t buckets = 101) : table(buckets) {}

    // Insert a supplier. If already present, update contact info.
    void insert(const std::string& name, const std::string& contact) {
        std::size_t idx = hash(name);
        for (auto &f : table[idx]) {
            if (f.name == name) {
                f.contactInfo = contact;
                return;
            }
        }
        table[idx].emplace_back(name, contact, 0.0);
    }

    // Retrieve pointer to Farmer; returns nullptr if not found.
    Farmer* get(const std::string& name) {
        std::size_t idx = hash(name);
        for (auto &f : table[idx]) {
            if (f.name == name) return &f;
        }
        return nullptr;
    }

    // Optionally increment total rice sold for a supplier (helper).
    bool addSales(const std::string& name, double amount) {
        Farmer* f = get(name);
        if (!f) return false;
        f->totalRiceSold += amount;
        return true;
    }

    std::size_t bucketCount() const { return table.size(); }

private:
    std::vector<std::list<Farmer>> table;

    // Polynomial rolling hash for strings
    std::size_t hash(const std::string& s) const {
        const unsigned long long p = 31ULL;
        unsigned long long h = 0ULL;
        for (unsigned char ch : s) {
            h = h * p + static_cast<unsigned long long>(ch);
        }
        return static_cast<std::size_t>(h % table.size());
    }
};

#endif
