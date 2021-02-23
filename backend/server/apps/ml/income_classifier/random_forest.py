import joblib
import pandas as pd


class RandomForestClassifier:
    def __init__(self):
        path_to_artifacts = "../../research/"
        self.values_fill_missing = joblib.load(
            path_to_artifacts + "train_mode.joblib")
        self.encoders = joblib.load(path_to_artifacts + 'encoders.joblib')
        self.model = joblib.load(path_to_artifacts + "random_forest.joblib")

    def preprocessing(self, input_data):

        # JSON to pandas dataframe
        input_data = pd.DataFrame(input_data, index=[0])

        # Fill missing values
        input_data = input_data.fillna(self.values_fill_missing)

        # Convert categoricals
        for column in [
            "workclass",
            "education",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "native-country",
        ]:
            categorical_convert = self.encoders[column]
            input_data[column] = categorical_convert.transform(
                input_data[column])

        return input_data

    def predict(self, preproessed_data):
        return self.model.predict_proba(preproessed_data)

    def postprocessing(self, predictions):
        label = "<=50K"
        proba = predictions[0][1]
        print(predictions)
        if proba > 0.5:
            label = ">50K"
        return {"probability": proba, "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            preprocessed_data = self.preprocessing(input_data)
            prediction = self.predict(preprocessed_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            print(e)
            return {"status": "Error", "message": str(e)}

        return prediction
