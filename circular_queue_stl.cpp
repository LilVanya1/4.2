#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

#include <list>

static std::list<int> queue;

extern "C" {

    EXPORT void lib_init() {
        queue.clear();
    }

    EXPORT int lib_add(int value) {
        queue.push_back(value);
        return 1;
    }

    EXPORT int lib_dequeue(int* value) {
        if (queue.empty()) {
            return 0;
        }

        *value = queue.front();
        queue.pop_front();
        return 1;
    }

    EXPORT int lib_peek(int* value) {
        if (queue.empty()) {
            return 0;
        }

        *value = queue.front();
        return 1;
    }

    EXPORT void lib_clear() {
        queue.clear();
    }

    EXPORT int lib_size() {
        return (int)queue.size();
    }

    EXPORT int lib_get_elements(int* buffer, int maxSize) {
        if (queue.empty() || maxSize <= 0) {
            return 0;
        }

        int count = 0;
        for (auto it = queue.begin(); it != queue.end() && count < maxSize; ++it) {
            buffer[count] = *it;
            count++;
        }

        return count;
    }

}