from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([Dense(1, input_shape=(5,))])
plot_model(model, to_file="test.png", show_shapes=True)