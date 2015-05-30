# -*- coding: utf-8 -*-
# This file is a readaption of network.py of mu_autocaptcha
#
# Copyright 2009 Shaun Friedle
#
# This file is part of mu_autocaptcha.
# mu_autocaptcha is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mu_autocaptcha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mu_autocaptcha.  If not, see <http://www.gnu.org/licenses/>.
#
# URL: http://herecomethelizards.co.uk/mu_captcha/

from math import exp
from random import uniform

class Neuron(object):
    def __init__(self, num_inputs):
        """
        @param num_inputs: 输入次数，用以计算权值个数
        """
        self.activation = 0
        self.bias = -1
        self.threshold = 0
        self.weights = []
        self.error = 0
        self.last_weight_step = [0] * num_inputs

        self._init_weights(num_inputs)

    def _init_weights(self, num_inputs):
        """初始化权值
        """
        self.threshold = uniform(-1, 1)
        self.weights = [uniform(-1, 1) for _ in xrange(num_inputs)]

    def adjust_weights(self, inputs, learning_rate):
        """调整权值,学习阶段根据误差调整权值
        @param inputs: a list() or tuple() representing inputs
        @param learning_rate: learning rate
        """
        self.threshold += learning_rate * self.error * self.bias
        for i in xrange(len(inputs)):
            current_weight = self.weights[i]
            self.weights[i] += learning_rate * self.error * inputs[i]
            self.last_weight_step[i] = self.weights[i] - current_weight

    def feed(self, inputs):
        """处理输入
        @param inputs: a list() or tuple() representing inputs
        """
        self.activation = 0
        for i in xrange(len(inputs)):
            self.activation += inputs[i] * self.weights[i]
        self.activation += self.bias * self.threshold

    def output(self):
        """获取该神经元的输出结果
        @return: float number
        """
        return 1 / (1 + exp(-self.activation))
