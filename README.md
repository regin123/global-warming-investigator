# Global warming investigator

## Table of contents

* [Introduction](#Introduction)
* [Launch](#launch)
* [Installation](#installation)
* [General info](#general-info)
* [Code Example](#code-example)
* [Artificial Intelligence](#artificial-intelligence)
* [Technologies](#technologies)

## Introduction
Application has been developed as a solution for hackathon organized by BEST HACKS. Subject of this event was air pollution and greenhouse gas emissions.
 Web application  visualizes CO2 emission and PM10 air content on whole world( by country) and accordingly poland(by voivodeship). Additionally application provides graph- statistics for each country.
  Simple CO2 emission calculator had been implemented to convince people about air pollution arisen by 
a transport choice. When we have data visualization we can check which country produce a lot of CO2 and which
does not. We are also able to notice which countries care about global warming by declining tendency of CO2 emission. 
On the other hand as long as we storage from data from past years we can predict next year emission. Our dataset is limited from 1960 thorugh 2015 so artificial intelligence was used to predict data between 2015 and 2025 year.
## Installation
```
pip install -r /path/to/requirements.txt
```
## Launch
```
python manage.py runserver
```
## General info
Application as in introduction mainly is a visualization of air pollution and global warming culprits. Our dataset storage
co2 emission data from 1960 through 2015. Each Map is interactive/ responsive. By a country click we can see relatively the diagram of 
co2 per person by past years for clicked country. We have implemented an calculator of the CO2 emission as comparison of choosing
one transport over another
### World Map
![IMG](static/images/world_map.png)
### Poland Map
![IMG](static/images/poland_map.png)
### Other
#### Route CO2 emission calculator
![IMG](static/images/compute_pm_ow.png)
#### Navigation bar
![IMG](static/images/menu.png)
## Code Example
Graph drawing on country click with canvasJS.
```python
        elemClick: function (elem) {
            var self = this;
            if (elem === undefined) return;
            if (!self.panning && elem.options.href !== undefined) {
                document.getElementById("graphPanel").classList.add("graph_window_style");
                document.getElementById("graphPanel").style.display="block";
                animateLeft(document.getElementById('graphPanel'), -600, 80);
                let alpha2 = elem.mapElem[0].getAttribute('data-id')
                let graph_values = document.getElementById(alpha2)
                let gv = graph_values.innerText.replaceAll(' ', '').split("],[")
                let X = gv[0].split(',')
                let Y = gv[1].split(',')
                X[0] = X[0].substring(2)
                Y[Y.length - 1] = Y[Y.length - 1].substring(0, Y[Y.length - 1].length - 2)
                let points = []
                for (let i = 0; i < Y.length; i++) {
                    if (Y[i] !== 'nan') {
                        points.push({x: parseInt(X[i]), y: parseFloat(Y[i])})
                    }
                }
                var chart = new CanvasJS.Chart("chartContainer", {
                    animationEnabled: true,
                    axisY: {title: "CO2 per person"},
                    axisX: {title: "Years"},
                    theme: "light2",
                    title: {
                        text: alpha2
                    },
                    data: [{
                        type: "line",
                        indexLabelFontSize: 16,
                        dataPoints: points
                    }]
                });
                chart.render();

                document.getElementById("graphPanel").onclick = function () {
                    this.style.display = "none"

                }

            }
        },
```
## Artificial Intelligence
Data between 2015 and 2024 had been predicted using neural network( tensorflow).
### Code example
#### Procedure
```
    x, y = data_preprocess(x, y, scale_y, scale_x)
    model = get_model()
    model.fit(x, y, epochs=300, batch_size=10, verbose=0)
    yhat = model.predict(x_pred)
    x_plot, x_pred_plot, y_plot, yhat_plot = data_post_process(x, x_pred, y, yhat, scale_x, scale_y)
    draw_plot(x_pred_plot, yhat_plot, x_plot, y_plot)
```
#### Model
```
    model = Sequential()
    model.add(Dense(99, input_dim=1, activation='softmax', kernel_initializer='he_uniform'))
    model.add(Dense(120, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(256, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(90, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(20, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='tanh', kernel_initializer='he_uniform'))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')
```
## Technologies
 - Python
 - Django
 - Tensorflow
 - CSS
 - HTML
 - Javascript
 - CanvasJS
 - RaphaelJS
 - JQuery
 

