import tensorflow as tf
import time

# Sprawdzenie dostępnych GPU
print("Dostępne GPU:", tf.config.list_physical_devices('GPU'))

# Testowe obliczenia
print("Uruchamianie testu na GPU...")
with tf.device('/GPU:0'):
    a = tf.random.normal([1000, 1000])
    b = tf.random.normal([1000, 1000])
    
    start = time.time()
    c = tf.matmul(a, b)
    print("Czas wykonania:", time.time() - start)

print("Test zakończony.")

