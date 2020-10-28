from matplotlib import pyplot
from numpy import asarray
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense


def reshaper(x):
    return x.reshape((len(x), 1))


class Predictioner:
    def __init__(self):
        self.model = Sequential()
        self.setup_model()
        self.compile_model()

    def update_input(self, train_x, train_y):
        self.push_train_sets(train_x, train_y)
        self.y_scaler = MinMaxScaler()
        self.x_scaler = MinMaxScaler()
        self.reshape_train_sets()
        self.adjust_scalers()

    def push_train_sets(self, train_x, train_y):
        self.train_x = train_x
        self.train_y = train_y

    def reshape_train_sets(self):
        self.train_x = reshaper(self.train_x)
        self.train_y = reshaper(self.train_y)

    def adjust_scalers(self):
        self.train_x = self.x_scaler.fit_transform(self.train_x)
        self.train_y = self.y_scaler.fit_transform(self.train_y)

    def setup_model(self):
        self.model.add(Dense(99, input_dim=1, activation='softmax', kernel_initializer='he_uniform'))
        self.model.add(Dense(120, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(256, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(90, activation='relu', kernel_initializer='he_uniform'))
        self.model.add(Dense(20, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(10, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(1))

    def compile_model(self):
        self.model.compile(loss='mse', optimizer='adam')

    def fit_model(self):
        self.model.fit(self.train_x, self.train_y, epochs=300, batch_size=10, verbose=0)

    def predict(self, prediction_interval_x):
        prediction_interval_x = reshaper(prediction_interval_x)
        prediction_interval_x = self.x_scaler.transform(prediction_interval_x)\

        predicted_y = self.model.predict(prediction_interval_x)

        self.x_plot = self.x_scaler.inverse_transform(self.train_x)
        self.y_plot = self.y_scaler.inverse_transform(self.train_y)
        self.x_pred_plot = self.x_scaler.inverse_transform(prediction_interval_x)
        self.y_pred_plot = self.y_scaler.inverse_transform(predicted_y)
        return self.y_pred_plot

    def visualize(self):
        pyplot.scatter(self.x_pred_plot, self.y_pred_plot, label='Predicted')
        pyplot.scatter(self.x_plot, self.y_plot, label='Actual', s=0.1)
        pyplot.title('Input (x) versus Output (y)')
        pyplot.xlabel('Input Variable (x)')
        pyplot.ylabel('Output Variable (y)')
        pyplot.legend()
        pyplot.show()


x = asarray([i for i in range(-1000, 1000)])
predict_x = asarray([i for i in range(900, 1400)])
y = asarray([i ** 2.0 for i in range(-1000, 1000)])
y2 = asarray([i ** 3.0 for i in range(-1000, 1000)])

p = Predictioner()

p.update_input(x, y)
p.fit_model()
p.predict(predict_x)
p.visualize()

p.update_input(x, y2)
p.fit_model()
p.predict(predict_x)
p.visualize()
