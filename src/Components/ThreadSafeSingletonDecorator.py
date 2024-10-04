import threading

### Allows only one oppened connection to GPT we used it to reduce costs. 
### In multi-threaded applications, I need to ensure that the Singleton is thread-safe. 


def thread_safe_singleton(cls):
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


