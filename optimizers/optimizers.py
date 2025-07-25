import numpy as np

class Optimizer_SGD:
    """Stochastic Gradient Descent Optimizer."""
    def __init__(self, learning_rate=1.0, decay=0.0, momentum=0.0):
        """Initialize with a learning rate."""
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.momentum = momentum

    def pre_update_params(self):
        """Prepare for parameter update."""
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1.0 / (1.0 + self.decay * self.iterations))

    def update_params(self, layer):
        """Update parameters of the layer."""
        # If we use momentum
        if self.momentum:
            # If layer does not contain momentum arrays, create them
            if not hasattr(layer, 'weight_momentums'):
                layer.weight_momentums = np.zeros_like(layer.weights)
                # If there is no momentum array for weights
                # The array doesn't exist for biases yet either
                layer.bias_momentums = np.zeros_like(layer.biases)
            # Build weight updates with momentum
            weight_updates = \
                self.momentum * layer.weight_momentums - \
                self.current_learning_rate * layer.dweights
            layer.weight_momentums = weight_updates
        
            # Build bias updates with momentum
            bias_updates = \
                self.momentum * layer.bias_momentums - \
                self.current_learning_rate * layer.dbiases
            layer.bias_momentums = bias_updates
            
            # Vanilla SGD updates with momentum
            layer.weights += weight_updates
            layer.biases += bias_updates
        # Vanilla SGD update (no momentum)
        else:
            layer.weights += -self.current_learning_rate * layer.dweights
            layer.biases += -self.current_learning_rate * layer.dbiases
       
    def post_update_params(self):
        """Increment the iteration count."""
        self.iterations += 1

class Optimizer_ADAGrad:
    """Adaptive Gradient Optimizer."""
    def __init__(self, learning_rate=1.0, decay=0.0, epsilon=1e-7):
        """Initialize with a learning rate."""
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon

    def pre_update_params(self):
        """Prepare for parameter update."""
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1.0 / (1.0 + self.decay * self.iterations))

    def update_params(self, layer):
        """Update parameters of the layer."""
        # If layer doesn't contain cache arrays, create them
        if not hasattr(layer, 'weight_cache'):
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_cache = np.zeros_like(layer.biases)

        # Update cache with squared current gradients
        layer.weight_cache += layer.dweights ** 2
        layer.bias_cache += layer.dbiases ** 2

        # Vanilla SGD update + normalization
        layer.weights += -self.current_learning_rate * \
            layer.dweights / \
            (np.sqrt(layer.weight_cache) + self.epsilon)
        layer.biases += -self.current_learning_rate * \
            layer.dbiases / \
            (np.sqrt(layer.bias_cache) + self.epsilon)
        
    def post_update_params(self):
        """Increment the iteration count."""
        self.iterations += 1

class Optimizer_RMSProp:
    """Root Mean Square Propagation Optimizer."""
    def __init__(self, learning_rate=1.0, decay=0.0, epsilon=1e-7, rho=0.9):
        """Initialize with a learning rate."""
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon
        self.rho = rho

    # Call once before any parameter updates
    def pre_update_params(self):
        """Prepare for parameter update."""
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1.0 / (1.0 + self.decay * self.iterations))

    def update_params(self, layer):
        """Update parameters of the layer."""
        # If layer doesn't contain cache arrays, create them
        if not hasattr(layer, 'weight_cache'):
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_cache = np.zeros_like(layer.biases)

        # Update cache with squared current gradients
        layer.weight_cache = self.rho * layer.weight_cache + \
            (1 - self.rho) * layer.dweights ** 2
        layer.bias_cache = self.rho * layer.bias_cache + \
            (1 - self.rho) * layer.dbiases ** 2

        # Vanilla SGD update + normalization
        # with square root of the cache 
        layer.weights += -self.current_learning_rate * \
            layer.dweights / \
            (np.sqrt(layer.weight_cache) + self.epsilon)
        layer.biases += -self.current_learning_rate * \
            layer.dbiases / \
            (np.sqrt(layer.bias_cache) + self.epsilon)
        
    def post_update_params(self):
        """Increment the iteration count."""
        self.iterations += 1

class Optimizer_ADAM:
    """Adaptive Momentum Optimizer (Most widely used)."""
    def __init__(self, learning_rate=1.0, decay=0.0, epsilon=1e-7, beta_1=0.9, beta_2=0.999):
        """Initialize with a learning rate."""
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon
        self.beta_1 = beta_1
        self.beta_2 = beta_2  

    # Call once before any parameter updates
    def pre_update_params(self):
        """Prepare for parameter update."""
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1.0 / (1.0 + self.decay * self.iterations))

    def update_params(self, layer):
        """Update parameters of the layer."""
        # If layer doesn't contain cache arrays, create them filled with zeros
        if not hasattr(layer, 'weight_cache'):
            layer.weight_momentums = np.zeros_like(layer.weights)
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_momentums = np.zeros_like(layer.biases)
            layer.bias_cache = np.zeros_like(layer.biases)

        # Update momentum with current gradients
        layer.weight_momentums = self.beta_1 * layer.weight_momentums + \
            (1 - self.beta_1) * layer.dweights
        layer.bias_momentums = self.beta_1 * layer.bias_momentums + \
            (1 - self.beta_1) * layer.dbiases
        
        # Get corrected momentum
        weight_momentums_corrected = layer.weight_momentums / \
            (1 - self.beta_1 ** (self.iterations + 1))
        bias_momentums_corrected = layer.bias_momentums / \
            (1 - self.beta_1 ** (self.iterations + 1))
        # Update cache with squared current gradients
        layer.weight_cache = self.beta_2 * layer.weight_cache + \
            (1 - self.beta_2) * layer.dweights ** 2
        layer.bias_cache = self.beta_2 * layer.bias_cache + \
            (1 - self.beta_2) * layer.dbiases ** 2
        # Get corrected cache
        weight_cache_corrected = layer.weight_cache / \
            (1 - self.beta_2 ** (self.iterations + 1))
        bias_cache_corrected = layer.bias_cache / \
            (1 - self.beta_2 ** (self.iterations + 1))

        # Vanilla SGD update + normalization
        # with square root of the cache 
        layer.weights += -self.current_learning_rate * \
            weight_momentums_corrected / \
            (np.sqrt(weight_cache_corrected) + self.epsilon)
        layer.biases += -self.current_learning_rate * \
            bias_momentums_corrected / \
            (np.sqrt(bias_cache_corrected) + self.epsilon)
        
    def post_update_params(self):
        """Increment the iteration count."""
        self.iterations += 1