#!/usr/bin/env python
# coding: utf-8

# In[7]:


pip install scikit-learn


# In[1]:


import pandas as pd

# Load the dataset
file_path = 'C:/Users/user/Desktop/exams.csv'
df = pd.read_csv(file_path)

# Display the first five rows of the dataframe
print(df.head())


# In[2]:


from sklearn.preprocessing import LabelEncoder

# Initialize the LabelEncoder
label_encoder = LabelEncoder()

# Encode categorical variables
df['gender'] = label_encoder.fit_transform(df['gender'])
df['race/ethnicity'] = label_encoder.fit_transform(df['race/ethnicity'])
df['parental level of education'] = label_encoder.fit_transform(df['parental level of education'])
df['lunch'] = label_encoder.fit_transform(df['lunch'])
df['test preparation course'] = label_encoder.fit_transform(df['test preparation course'])

# Display the first few rows of the transformed dataframe
print(df.head())


# In[3]:


# Define the target variable as the average score
df['average_score'] = df[['math score', 'reading score', 'writing score']].mean(axis=1)

# Define features (X) and target (y)
X = df.drop(columns=['math score', 'reading score', 'writing score', 'average_score'])
y = df['average_score']

# Display the first few rows of X and y
print(X.head())
print(y.head())


# In[4]:


from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Display the shape of the training and testing sets
print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)


# In[5]:


from sklearn.linear_model import LinearRegression

# Initialize the model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Display the model coefficients
print(model.coef_)


# In[6]:


from sklearn.metrics import mean_squared_error, r2_score

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

