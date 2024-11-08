import pandas as pd
import zipfile
import os

# ���� �� ZIP-�����
zip_file_path = 'C:/Users/Notebook/P_Data_Extract_From_World_Development_Indicators (1).zip'
extracted_folder = 'C:/Users/Notebook/extracted_files'  # ����� ��� ������������ �����

# ����������
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
        print(f"����� ������ ����������� � �����: {extracted_folder}")

    # ����� CSV-����� � ����������� �����
    for file_name in os.listdir(extracted_folder):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(extracted_folder, file_name)
            print(f"�������� CSV-����: {csv_file_path}")

            # ���������� �����
            df = pd.read_csv(csv_file_path)

            # ������������ DataFrame � �������� ������� � ������
            df_melted = df.melt(id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
                                var_name='Year', value_name='Value')

            # ��������� ���������� ������� � ������� 'Year'
            df_melted['Year'] = df_melted['Year'].str.extract('(\d{4})').astype(int)

            # Գ�������� ����� ��� ������ � 1991 �� 2019 ����
            df_ukraine = df_melted[(df_melted['Country Name'] == 'Ukraine') & (df_melted['Year'].between(1991, 2019))]

            # ��������� ����� �� �����
            print(df_ukraine)

            # ����� ��������� � ������������ ������� ���������
            min_value = df_ukraine['Value'].min()
            max_value = df_ukraine['Value'].max()

            # ��������� ������ DataFrame ��� ������ ����������
            result_df = pd.DataFrame({
                '��������': ['̳������� ��������� �����', '����������� ��������� �����'],
                '��������': [min_value, max_value]
            })

            # ���������� ���������� � ����� CSV ����
            result_df.to_csv('����������_���������_�����.csv', index=False)

            print("���������� ��������� � ���� '����������_���������_�����.csv'.")
            break
    else:
        print("CSV-���� �� �������� � ����������� �����.")

except FileNotFoundError:
    print("�������: ZIP-���� �� ��������.")
except zipfile.BadZipFile:
    print("�������: ��������� ����������� ZIP-����.")
except pd.errors.EmptyDataError:
    print("�������: ���� �������.")
except pd.errors.ParserError:
    print("�������: ������� ������� �� ��� ������� �����.")
except KeyError as e:
    print(f"�������: ������� {e} �� �������� � CSV ����.")
except Exception as e:
    print(f"������� ��������������� �������: {e}")


