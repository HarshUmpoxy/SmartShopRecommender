import tensorflow as tf

# Check if TensorFlow is using GPU
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    print("GPU is being used by TensorFlow.")
    for device in physical_devices:
        print("Device:", device)
else:
    print("No GPU is being used by TensorFlow.")
