#include <iostream>
#include <cstring>
#include <cstdlib>
#include <ctime>

using namespace std;

class CStr {
private:
    char* string;

    char* generate(int length) {
        const char charset[] = "abcdefghijklmnopqrstuvwxyz";
        char* result = new char[length + 1];
        for (int i = 0; i < length; ++i) {
            result[i] = charset[rand() % 26];
        }
        result[length] = '\0';
        return result;
    }

public:
    CStr() {
        int length = rand() % 20 + 1;
        string = generate(length);
    }

    CStr(const char* str) {
        string = new char[strlen(str) + 1];
        strcpy(string, str);
    }

    CStr(int length) {
        if (length > 20) length = 20;
        if (length < 1) length = 1;
        string = generate(length);
    }

    CStr(const CStr& obj) {
        string = new char[strlen(obj.string) + 1];
        strcpy(string, obj.string);
    }

    ~CStr() {
        delete[] string;
    }

    CStr& operator=(CStr& obj) {
        if (this != &obj) {
            delete[] string;
            string = new char[strlen(obj.string) + 1];
            strcpy(string, obj.string);
        }
        return *this;
    }

    CStr& operator=(const char* str) {
        delete[] string;
        string = new char[strlen(str) + 1];
        strcpy(string, str);
        return *this;
    }

    CStr operator+(CStr& obj) {
        CStr result;
        delete[] result.string;
        result.string = new char[strlen(string) + strlen(obj.string) + 1];
        strcpy(result.string, string);
        strcat(result.string, obj.string);
        return result;
    }

    CStr& operator+=(CStr& obj) {

        char* temp = new char[strlen(string) + strlen(obj.string) + 1];
        strcpy(temp, string);
        strcat(temp, obj.string);
        delete[] string;
        string = temp;
        return *this;
    }


    bool operator>(CStr& obj) {
        return strcmp(string, obj.string) > 0;
    }

    char& operator[](int index) {
        return string[index];
    }

    int get_length() {
        return strlen(string);
    }

    friend ostream& operator<<(ostream& stream, CStr& obj) {
        stream << obj.string;
        return stream;
    }

    friend istream& operator>>(istream& stream, CStr& obj) {
        char buffer[1000];
        stream >> buffer;
        delete[] obj.string;
        obj.string = new char[strlen(buffer) + 1];
        strcpy(obj.string, buffer);
        return stream;
    }
};

// class header file
// cmake
