#ifndef PRIORITYQUEUE_H
#define PRIORITYQUEUE_H

#include "RiceBatch.h"
#include <vector>
#include <stdexcept>

// DryingQueue: max-heap where higher moistureLevel has higher priority
// Uses a std::vector as the heap array and manual heapify operations.
class DryingQueue {
public:
    DryingQueue() = default;

    // Push a RiceBatch onto the heap
    void push(const RiceBatch& batch) {
        heap.push_back(batch);
        heapifyUp(heap.size() - 1);
    }

    // Pop and return the RiceBatch with highest moisture (top of max-heap)
    RiceBatch pop() {
        if (heap.empty()) throw std::out_of_range("DryingQueue is empty");
        RiceBatch top = heap.front();
        heap[0] = heap.back();
        heap.pop_back();
        if (!heap.empty()) heapifyDown(0);
        return top;
    }

    // Peek at the batch with highest moisture without removing
    const RiceBatch& peek() const {
        if (heap.empty()) throw std::out_of_range("DryingQueue is empty");
        return heap.front();
    }

    bool isEmpty() const { return heap.empty(); }
    std::size_t size() const { return heap.size(); }

private:
    std::vector<RiceBatch> heap;

    inline std::size_t parentIdx(std::size_t i) const { return (i - 1) / 2; }
    inline std::size_t leftIdx(std::size_t i) const { return 2 * i + 1; }
    inline std::size_t rightIdx(std::size_t i) const { return 2 * i + 2; }

    // Compare by moistureLevel: return true if a has higher priority than b
    static bool higherPriority(const RiceBatch& a, const RiceBatch& b) {
        return a.moistureLevel > b.moistureLevel; // higher moisture = higher priority
    }

    void heapifyUp(std::size_t idx) {
        while (idx > 0) {
            std::size_t p = parentIdx(idx);
            if (higherPriority(heap[idx], heap[p])) {
                std::swap(heap[idx], heap[p]);
                idx = p;
            } else break;
        }
    }

    void heapifyDown(std::size_t idx) {
        while (true) {
            std::size_t l = leftIdx(idx);
            std::size_t r = rightIdx(idx);
            std::size_t largest = idx;

            if (l < heap.size() && higherPriority(heap[l], heap[largest])) largest = l;
            if (r < heap.size() && higherPriority(heap[r], heap[largest])) largest = r;

            if (largest != idx) {
                std::swap(heap[idx], heap[largest]);
                idx = largest;
            } else break;
        }
    }
};

#endif
