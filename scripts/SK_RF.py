"""
    SK_RF.py  - This is a Random Forest example using SciKit Learn.

    Copyright (C) 2020 Adrian Bevan, Queen Mary University of London

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import seaborn as sns
import api

api.PrintGNULicense()


# Parameters
n_classes = 3
plot_colors = "ryb"
plot_step = 0.01

# Load data
print("\033[1mLoad the sklearn Iris data\033[0m\n")
iris = load_iris()

# split the data into test and train samples. The train sample will be used to learn
# the model, and the test sample will be used to evaluate module performance.
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=0)
print("Iris data have been split into test and train samples")
print("\tN(train) = ", len(X_train))
print("\tN(test)  = ", len(X_test))



print("\033[1mFitting a random forest classifier\033[0m")
RF_clf = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16)
RF_clf.fit(X_train, y_train)

compare_score=[]
rf_score=RF_clf.score(X_test, y_test)*100
compare_score.append(rf_score)

print('Test accuracy: {}%'.format(rf_score))

RFpredictions = RF_clf.predict(X_test)
RFcm = confusion_matrix(y_test, RFpredictions)
print("\nconfusion matrix (test) = \n", RFcm)
sns.heatmap(RFcm, center=True)
plt.show()
plt.clf()
print(RFpredictions)

print("... now compute the random forest scores")
train_score = RF_clf.score(X_train, y_train)
test_score  = RF_clf.score(X_test, y_test)

print("\nRandom Forest Classifier Score is:")
print("\tTrain Score = ", train_score, " (This measure of performance is biased)")
print("\tTest Score  = {:5.4f}".format(test_score))
print("\tNumber of mis-classified test data = {:2.1f}".format((1-test_score)*len(X_test)))

#
# Use the test data to compute a confusion matrix and to compare predictions against
# the ground truth labels.
#
print("Truth\tPrediction\tCorrect Prediction")
for i in range(len(RFpredictions)):
    Match = False
    if RFpredictions[i] == y_test[i]:
        Match = True
    print("{:}\t{:}\t{:}".format(y_test[i], RFpredictions[i], Match))

#
# Try cross validation with this sample - 5 splits of the data.  For this 
# look at the accuracy scores for each split in order to determine the
# mean performance.
#
print("\n\033[1mRun Cross Validation On the Sample\033[0m")
scores = cross_val_score(RF_clf, X_train, y_train, cv=5)
print("cross validation scores = ", scores)
print("\tmean = {:5.4f}".format(scores.mean()))
