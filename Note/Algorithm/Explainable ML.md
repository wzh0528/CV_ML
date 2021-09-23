### Explainable ML

#### Local explanation

basic idea : removing or modifying the values of the components, observing the change of decision

**Saliency Map**   

存在问题1：Gradient Saturation

改进方法：Global attribution （Integrated gradient、DeepLIFT）

存在问题2：Noisy gradient

改进方法：SmoothGrad



#### Global explanation

activation maximization 

"regularization" from Generator

#### Using a model to explain another

**LIME**(Local Interpretable Model-Agnostic Explanations)

1. given a data point you want to explain
2. Sample at the nearby
3. Fit with linear model (or other interpretable model)
4. Interpret the linear model

