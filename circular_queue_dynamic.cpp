#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

struct Uzl {
    int data;
    Uzl* next;
};

struct Sruct {
    Uzl* tail;
    int size;
};

static Sruct queue;

extern "C" {

EXPORT void lib_init() {
    queue.tail = nullptr;
    queue.size = 0;
}

EXPORT int lib_add(int value) {
    Uzl* newUzl = new Uzl;
    newUzl->data = value;

    if (queue.tail == nullptr) {
        newUzl->next = newUzl;
        queue.tail = newUzl;
    } else {
        newUzl->next = queue.tail->next;
        queue.tail->next = newUzl;
        queue.tail = newUzl;
    }

    queue.size++;
    return 1;
}

EXPORT int lib_dequeue(int* value) {
    if (queue.tail == nullptr) {
        return 0;
    }

    Uzl* head = queue.tail->next;
    *value = head->data;

    if (queue.tail == head) {
        queue.tail = nullptr;
    } else {
        queue.tail->next = head->next;
    }

    delete head;
    queue.size--;
    return 1;
}

EXPORT int lib_peek(int* value) {
    if (queue.tail == nullptr) {
        return 0;
    }

    *value = queue.tail->next->data;
    return 1;
}

EXPORT void lib_clear() {
    int value;
    while (queue.size > 0) {
        lib_dequeue(&value);
    }
}

EXPORT int lib_size() {
    return queue.size;
}

EXPORT int lib_get_elements(int* buffer, int maxSize) {
    if (queue.tail == nullptr || maxSize <= 0) {
        return 0;
    }

    Uzl* current = queue.tail->next;
    int count = 0;

    for (int i = 0; i < queue.size && i < maxSize; i++) {
        buffer[i] = current->data;
        current = current->next;
        count++;
    }

    return count;
}

}