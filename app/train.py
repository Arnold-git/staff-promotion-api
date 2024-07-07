from pipeline import preprocess_data, save_model
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
from data_manager import load_data
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
import logging 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
from pathlib import Path
from config import __version__ as _version

PACKAGE_ROOT = "api"

TRAINED_MODEL_DIR = PACKAGE_ROOT + "/trained_models"

def run_training(train_date):
    df_train = load_data(train_date)
    cat_columns = [col for col in df_train.columns if df_train[col].dtype == "O" and col != "EmployeeNo"]

    X, encoders = preprocess_data(df_train.drop(columns=['EmployeeNo', "Promoted_or_Not"]), cat_columns)
    y = df_train['Promoted_or_Not']

    logging.info("Train test split")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    logging.info("Train test split ends")
    
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    logging.info("training begins")
    model = RandomForestClassifier(random_state=42)

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    }

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='f1', cv=5)
    grid_search.fit(X_resampled, y_resampled)
    best_model = grid_search.best_estimator_
    logging.info("training ends")

    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    logging.info(classification_report(y_test, y_pred))

    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)
    f1 = round(f1_score(y_test, y_pred), 2)
    precision = round(precision_score(y_test, y_pred), 2)
    recall = round(recall_score(y_test, y_pred), 2)
    auc = round(roc_auc_score(y_test, y_pred_proba),2)

    logging.info(f"Accuracy: {accuracy}")
    logging.info(f"Confusion Matrix:\n{conf_matrix}")
    logging.info(f"Classification Report:\n{class_report}")
    logging.info(f"F1 Score: {f1}")
    logging.info(f"Precision: {precision}")
    logging.info(f"Recall: {recall}")
    logging.info(f"AUC: {auc}")

    save_model(best_model, 'trained_model/', f"model_{_version}.joblib")


if __name__ == "__main__":
    data = "data/train.csv"
    run_training(data)



