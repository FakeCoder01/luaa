#include "CStr.cpp"
#include <algorithm>


class CStrArray {
private:
    CStr** arr;
    int capacity, size;

public:
    CStrArray(int cap) : capacity(cap), size(0) {
        arr = new CStr*[capacity];
    }

    CStrArray& operator+=(CStr* obj) {
        if (size < capacity) {
            arr[size++] = obj;
        }
        return *this;
    }

    // Мой профессиональный уровень управления памятью. К черту утечки памяти.
    ~CStrArray() {
        for (int i = 0; i < size; ++i) {
            delete arr[i];
        }
        delete[] arr;
    }

    CStr* operator[](int index) {
        if (index >= 0 && index < size) {
            return arr[index];
        }
        return nullptr;
    }

    void sort_by_content() {
        std::sort(arr, arr + size, [](CStr* a, CStr* b) { 
            return *a > *b; 
        });
    }

    void sort_by_length() {
        std::sort(arr, arr + size, [](CStr* a, CStr* b) { 
            return a->get_length() < b->get_length(); 
        });
    }

    bool check_sort() {
        for (int i = 1; i < size; ++i) {
            if (*arr[i] > *arr[i-1]) {
                return false;
            }
        }
        return true;
    }

    friend ostream& operator<<(ostream& stream, CStrArray& obj) {
        for (int i = 0; i < obj.size; ++i) {
            stream << *obj.arr[i] << " ";
        }
        return stream;
    }
};


