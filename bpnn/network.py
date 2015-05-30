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

from bpnn.neuron import Neuron

class Network(object):
    """
        前向反馈神经网络
    """
    def __init__(self, num_inputs, num_h_neurons, num_o_neurons,
                 learning_rate = 0.1):
        """初始化设置
        @param num_inputs: 输入层神经元数量
        @param num_h_neurons: 隐藏层神经元数量
        @param num_o_neurons: 输出层神经元数量
        @param learning_rate: 学习速率
        """
        self.h_layer = self._new_layer(num_h_neurons, num_inputs)
        self.o_layer = self._new_layer(num_o_neurons, num_h_neurons)
        self.trained = False
        self.learning_rate = learning_rate
        self.error = 0

    def _new_layer(self, num_neurons, num_inputs):
        """创建向量
        """
        return [Neuron(num_inputs) for _ in xrange(num_neurons)]

    def feed(self, inputs):
        """传递输入向量
        @param inputs: a list or tuple containing inputs
        """
        h_outputs = []
        for neuron in self.h_layer:
            #各个神经元计算激活状态
            neuron.feed(inputs)
            #产生该层的输出
            h_outputs.append(neuron.output())

        for neuron in self.o_layer:
            #输出层计算激活状态
            neuron.feed(h_outputs)

    def output(self):
        """输出结果向量
        @return: a list() containing the value of the output neurons.
        """
        return [neuron.output() for neuron in self.o_layer]

    def test(self, inputs):
        """使用该网络进行识别

        This method is simply feed() followed by output().

        @param inputs: a list or tuple containing inputs
        @return: a list() containing the value of the output neurons.
        """
        self.feed(inputs)
        return self.output()

    def train(self, inputs, target):
        """训练该网络
        @param inputs: 样本集
        @param target: 预期结果集
        @return: 针对当前结果集的误差
        """
        self.feed(inputs)
        for i in xrange(len(self.o_layer)):
            o_neuron = self.o_layer[i]
            output = o_neuron.output()
            o_neuron.error = (target[i] - output) * output * (1 - output)
            h_outputs = [h_neuron.output() for h_neuron in self.h_layer]
            o_neuron.adjust_weights(h_outputs, self.learning_rate)

        for i in xrange(len(self.h_layer)):
            h_neuron = self.h_layer[i]
            h_neuron.error = 0
            for o_neuron in self.o_layer:
                h_neuron.error += o_neuron.weights[i] * o_neuron.error
            h_neuron.error *= h_neuron.output() * (1 - h_neuron.output())
            h_neuron.adjust_weights(inputs, self.learning_rate)

        self.error = 0

        for neuron in self.o_layer:
            self.error += abs(neuron.error)

        return self.error
