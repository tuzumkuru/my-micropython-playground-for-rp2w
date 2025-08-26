import math

class WindowedSensorDataAnalyzer:
    def __init__(self, window_size):
        self.window_size = window_size
        self.data = []
        self.timestamps = []

    def feed_data(self, value, timestamp):
        self.data.append((value, timestamp))
        self.data = self.data[-self.window_size:]

    def derivative(self):
        if len(self.data) < 2:
            return None
        derivatives = [(self.data[i+1][0] - self.data[i][0]) / (self.data[i+1][1] - self.data[i][1]) for i in range(len(self.data)-1)]
        return derivatives

    def jerk(self):
        if len(self.data) < 3:
            return None
        jerks = [(self.data[i+2][0] - 2*self.data[i+1][0] + self.data[i][0]) / ((self.data[i+2][1] - self.data[i+1][1]) * (self.data[i+1][1] - self.data[i][1])) for i in range(len(self.data)-2)]
        return jerks

    def std_deviation(self):
        if len(self.data) < 2:
            return None
        mean = sum(x[0] for x in self.data) / len(self.data)
        variance = sum((x[0] - mean) ** 2 for x in self.data) / len(self.data)
        return math.sqrt(variance)

# Example usage:
# Create an instance with a window size of 5
sensor = WindowedSensorDataAnalyzer(5)

# Feed some data
sensor.feed_data(10, 1)  # Value of 10 at timestamp 1
sensor.feed_data(12, 2)  # Value of 12 at timestamp 2
sensor.feed_data(15, 3)  # Value of 15 at timestamp 3
sensor.feed_data(13, 4)  # Value of 13 at timestamp 4
sensor.feed_data(11, 5)  # Value of 11 at timestamp 5

# Calculate and print the derivative
print("Derivative:", sensor.derivative())

# Calculate and print the jerk
print("Jerk:", sensor.jerk())

# Calculate and print the standard deviation
print("Standard Deviation:", sensor.std_deviation())
