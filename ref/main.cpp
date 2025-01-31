#include "CStrArray.cpp"



int main() {


    srand(static_cast<unsigned int>(time(nullptr)));


    CStr str1;
    cout << "Random string : " << str1 << endl;

    CStr str2("Hello");
    cout << "String from const char* : " << str2 << endl;

    CStr str3(10);
    cout << "Random string of length 10 : " << str3 << endl;

    CStr str4(str2);
    cout << "Copy of str2 : " << str4 << endl;

    str1 = str2;
    cout << "str1 after assignment : " << str1 << endl;

    str1 = "World";
    cout << "str1 after const char* assignment : " << str1 << endl;

    CStr str5 = str2 + str1;
    cout << "str2 + str1 : " << str5 << endl;

    str2 += str1;
    cout << "str2 after += str1 : " << str2 << endl;

    cout << "str1 > str2 : " << (str1 > str2) << endl;

    cout << "Third character of str1 : " << str1[2] << endl;

    cout << "Length of str1 : " << str1.get_length() << endl;

    cout << "Enter a string : ";
    cin >> str1;
    cout << "Entered string : " << str1 << endl;


    CStrArray arr(5);
    arr += new CStr("Apple");
    arr += new CStr("Banana");
    arr += new CStr("Cherry");
    arr += new CStr("Date");
    arr += new CStr("Elderberry");

    cout << "Original array : " << arr << endl;

    arr.sort_by_content();
    cout << "Sorted by content : " << arr << endl;

    arr.sort_by_length();
    cout << "Sorted by length : " << arr << endl;

    string if_array_sorted = arr.check_sort() ? "Yes" : "No";
    cout << "Is array sorted by content? : " << if_array_sorted << endl;

    cout << "Third element: " << *arr[2] << endl;

    return 0;
}