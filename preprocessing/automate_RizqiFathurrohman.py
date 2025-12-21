import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_data(path: str) -> pd.DataFrame:
    """
    Load dataset dari file CSV
    """
    df = pd.read_csv(path)
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menghapus data duplikat
    """
    return df.drop_duplicates()


def remove_outliers_iqr(df: pd.DataFrame, numerical_cols: list) -> pd.DataFrame:
    """
    Menghapus outlier menggunakan metode IQR
    """
    Q1 = df[numerical_cols].quantile(0.25)
    Q3 = df[numerical_cols].quantile(0.75)
    IQR = Q3 - Q1

    filtered_df = df[
        ~((df[numerical_cols] < (Q1 - 1.5 * IQR)) |
          (df[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)
    ]

    return filtered_df


def encode_categorical(df: pd.DataFrame, categorical_cols: list) -> pd.DataFrame:
    """
    Encoding data kategorikal menggunakan one-hot encoding
    """
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df_encoded


def scale_features(X: pd.DataFrame) -> pd.DataFrame:
    """
    Standarisasi fitur numerik menggunakan StandardScaler
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return pd.DataFrame(X_scaled, columns=X.columns)


def preprocess_pipeline(
    input_path: str,
    output_path: str
) -> None:
    """
    Pipeline preprocessing utama
    """

    # Load data
    df = load_data(input_path)

    # Remove duplicate data
    df = remove_duplicates(df)

    # Define columns
    numerical_cols = ["age", "bmi", "children", "charges"]
    categorical_cols = ["sex", "smoker", "region"]

    # Remove outliers
    df = remove_outliers_iqr(df, numerical_cols)

    # Encode categorical features
    df = encode_categorical(df, categorical_cols)

    # Split features and target
    X = df.drop("charges", axis=1)
    y = df["charges"]

    # Scale features
    X_scaled = scale_features(X)

    # Combine features and target
    final_df = X_scaled.copy()
    final_df["charges"] = y.values

    # Save preprocessed data
    final_df.to_csv(output_path, index=False)

    print("Preprocessing selesai. Dataset siap digunakan untuk training.")


if __name__ == "__main__":
    preprocess_pipeline(
        input_path="../insurance_raw/insurance.csv",
        output_path="../preprocessing/insurance_preprocessing/insurance_preprocessed.csv"
    )
