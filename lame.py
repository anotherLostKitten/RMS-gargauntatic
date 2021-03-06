
# Import pandas, which is the library for the data structures being used
import pandas as pd

# Load train.csv into pandas dataframe and print the summary
df = pd.read_csv('train.csv')
df1 = pd.read_csv('test.csv')

# Show shapes of the data
print ("Train data shape:", df.shape)
print ("Test data shape:", df1.shape)
print list(df)
print list(df1)

# How many rows we are using for training (the rest are for evaluation)
num_training = 30000

# Get the labels as dataframes
labels_df = df.iloc[:num_training,0]ly because your Google account login access has expired or because third-party cookies are not allowed by your browser.

eval_labels_df = df.iloc[num_training:,0]
labels_df1 = df1.iloc[:,0]
      
# Get the features as dataframes
features_df = df.iloc[:num_training,1:]
eval_features_df = df.iloc[num_training:,1:]
features_df1 = df1.iloc[:,:]

# Make grey pixels black (to reduce complexity)
features_df[features_df > 0] = 1
eval_features_df[eval_features_df > 0] = 1
features_df1[features_df1 > 0] = 1

# Get the labels as lists
labels = labels_df.values
eval_labels = eval_labels_df.values
labels1 = labels_df1.values

print labels
print labels1

print features_df
print features_df1

# Import matplotlib (a graph library)
import matplotlib.pyplot as plt, matplotlib.image as mpimg

# Plot 25 training examples
my_dpi=96
plt.figure(figsize=(1200/my_dpi, 1200/my_dpi), dpi=my_dpi)

for i in range(25):
    img = features_df.iloc[i].as_matrix().reshape((28,28))
    plt.subplot(5, 5, i+1)
    plt.imshow(img, cmap='binary')
    plt.title(labels[i])
    plt.axis('off')
    
    # Import tensorflow
    import tensorflow as tf
    
    # Get and print the feature names
    headers = list(df)
    headers1 = list(df1)
    feature_names = headers[1:]
    feature_names1 = headers1[1:]
    
    print len(labels), labels
    print len(feature_names), feature_names
    
    !mkdir model_dir
    
    # Create a DNNClassifier with real-valued feature columns
    # (the number of columns = number of pixels in an image)
    
    features = [tf.contrib.layers.real_valued_column(f) for f in feature_names]
    # The hidden layers have 64, 32, and 16 neurons
    # The number of classes is 10 (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    classifier = tf.estimator.DNNClassifier(feature_columns=features,
                                            hidden_units=[64,32,16],
                                            n_classes=10,
                                            model_dir='model_dir')
    
    # How many examples are being processed at a time
    batch_size = 1000
    
    # Train 100 times
    for i in range(100):
        # Construct the training dataset
        def train_input_fn():
            return tf.data.Dataset.from_tensor_slices((dict(features_df), labels)).shuffle(batch_size*10).repeat().batch(batch_size)
        
        # Construct the evaluation dataset
        def eval_input_fn():
            return tf.data.Dataset.from_tensor_slices((dict(eval_features_df), eval_labels)).shuffle(batch_size*10).repeat().batch(batch_size)
        
        # Train for 100 steps each time
        classifier.train(input_fn=train_input_fn, steps=100)
        evaluation = classifier.evaluate(input_fn=eval_input_fn, steps=1)
        num_training_steps = evaluation.get('global_step', '?')
        loss = evaluation.get('loss', '?')
        
        !rm -r model_dir
        
        # Define the evaluation input function for predictions
        def eval_input_fn1():
            eval_dataset1 = tf.data.Dataset.from_tensor_slices((dict(features_df1)))
            #eval_dataset1 = eval_dataset1.shuffle(batch_size).repeat().batch(batch_size)
            eval_dataset1 = eval_dataset1.batch(len(features_df1))
            return eval_dataset1
        
        import matplotlib.pyplot as plt, matplotlib.image as mpimg
        
        #%matplotlib inline
        
        my_dpi=96
        plt.figure(figsize=(1200/my_dpi, 1200/my_dpi), dpi=my_dpi)
        
        # Get the models predictions
        predictions = classifier.predict(
            input_fn=eval_input_fn1)
        
        counter = 0
        counter1 = 0
        
        # Displays 25 test examples where the model was unsure of its prediction
        for pred_dict in predictions:
            counter1 += 1
            class_id = pred_dict['class_ids'][0]
            probability = pred_dict['probabilities'][class_id]
            if probability < .30:
                counter += 1
                img = features_df1.iloc[counter1 - 1].as_matrix().reshape((28,28))
                if counter <= 25:
                    plt.subplot(5, 5, counter)
                    plt.imshow(img, cmap='binary')
                    plt.title(str(class_id) + ', ' + str(probability))
                    plt.axis('off')
                else:
                    break
