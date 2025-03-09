import tensorflow as tf

print("TensorFlow version:", tf.__version__)

# Sprawdzenie dostępnych GPU
gpus = tf.config.list_physical_devices('GPU')
print("Dostępne GPU:", gpus)

# Sprawdzenie, czy operacje są wykonywane na GPU
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)
    print("TensorFlow używa GPU!")
else:
    print("TensorFlow nie wykrył GPU.")

