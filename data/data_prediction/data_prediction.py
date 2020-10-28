import itertools
import json
from random import choice

from matplotlib import pyplot
from numpy import asarray, isnan
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Dropout


#################################
#################################


def generate_graphs_dict(countries_alphas2, data):
    d = dict()
    for x in countries_alphas2:
        d[x] = (get_data_country(data, x))
    return d


def read_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data


def get_data_country(data, country_alpha2):
    x, y = [], []
    for year in data:
        value = float(data[year]["areas"][country_alpha2.upper()]["value"])
        if not isnan(value):
            x.append(int(year)), y.append(value)
    return x, y


def get_countries(data):
    return union_sets([set(data[k]['areas'].keys()) for k in list(data.keys())])


def union_sets(args):
    return set(frozenset(itertools.chain.from_iterable(args)))


def draw_plot(x_pred_plot, yhat_plot, x_plot, y_plot):
    pyplot.scatter(x_pred_plot, yhat_plot, label='Predicted')
    pyplot.scatter(x_plot, y_plot, label='Actual')
    pyplot.title('Input (x) versus Output (y)')
    pyplot.xlabel('Input Variable (x)')
    pyplot.ylabel('Output Variable (y)')
    pyplot.legend()
    pyplot.show()


def get_model():
    model = Sequential()
    model.add(Dense(99, input_dim=1, activation='softmax', kernel_initializer='he_uniform'))
    model.add(Dense(120, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(256, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(90, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(20, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')
    return model


def data_preprocess(x, y, scale_y, scale_x):
    x = x.reshape((len(x), 1))
    y = y.reshape((len(y), 1))
    x = scale_x.fit_transform(x)
    y = scale_y.fit_transform(y)

    return x, y


def data_post_process(x, x_pred, y, yhat, scale_x, scale_y):
    x_plot = scale_x.inverse_transform(x)
    x_pred_plot = scale_x.inverse_transform(x_pred)
    y_plot = scale_y.inverse_transform(y)
    yhat_plot = scale_y.inverse_transform(yhat)
    return x_plot, x_pred_plot, y_plot, yhat_plot


def run_ai(x, y, x_pred):
    scale_x = MinMaxScaler()
    scale_y = StandardScaler()

    x, y = data_preprocess(x, y, scale_y, scale_x)
    model = get_model()
    model.fit(x, y, epochs=300, batch_size=10, verbose=0)

    x_pred = x_pred.reshape((len(x_pred), 1))
    x_pred = scale_x.transform(x_pred)

    yhat = model.predict(x_pred)
    print(yhat)
    x_plot, x_pred_plot, y_plot, yhat_plot = data_post_process(x, x_pred, y, yhat, scale_x, scale_y)
    draw_plot(x_pred_plot, yhat_plot, x_plot, y_plot)
    return yhat_plot


def get_prediction_country(c, r1, r2):
    data = read_json('co2.json')
    context = generate_graphs_dict(get_countries(data), data)
    print(c, '->', context[c])
    x1 = asarray(context[c][0])
    y11 = asarray(context[c][1])
    x_pred1 = asarray([i for i in range(r1, r2)])
    y_pred = run_ai(x1, y11, x_pred1)
    return dict(zip(x_pred1, y_pred))


def get_data_country_dict(data, country_alpha2):
    x = dict()
    for year in data:
        value = float(data[year]["areas"][country_alpha2.upper()]["value"])
        if not isnan(value):
            x[year] = value
    return x


def get_prediction_dict(countries, r1, r2):
    d = dict()
    for c in countries:
        try:
            c_pred = get_prediction_country(c, r1, r2)
            d[c] = c_pred
        except ValueError:
            pass
    return d


def clear_json(data, r1, r2):
    for i in range(r1, r2):
        if str(i) in data.keys():
            del data[str(i)]
    json.dump(data, open("co2.json", "w"), indent=4)



def edit_json():
    r1, r2 = 1980, 2025
    with open('co2.json', "r+") as f:
        data = json.load(f)
        clear_json(data, r1, r2)
        countries = get_countries(data)
        preds = get_prediction_dict(countries, r1, r2)
        exemplary_row = data[choice(data.keys())]
        for i in range(r1, r2):
            data[str(i)] = exemplary_row
            for country in countries:
                if i in preds.keys():
                    data[str(i)]['areas'][country]['value'] = preds[i]
        json.dump(data, open("co2.json", "w"), indent=4)


edit_json()
