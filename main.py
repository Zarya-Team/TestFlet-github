import flet as ft
import pandas as pd



def read_file(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx', '.xlsm')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")


def main(page: ft.Page):
    page.title = "Flet File Uploader"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Функция для обработки загруженного файла
    def on_upload_progress(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                df = read_file(file_path)
                data_table = ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(col)) for col in df.columns],
                    rows=[
                        ft.DataRow(
                            cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]
                        )
                        for row in df.values
                    ],
                )
                page.add(
                    ft.Column(
                        controls=[data_table],
                        auto_scroll=True,
                    )
                )
            except Exception as ex:
                page.add(ft.Text(f"Error: {ex}"))

    # Создание компонента для выбора файла
    file_picker = ft.FilePicker(on_result=on_upload_progress)
    page.overlay.append(file_picker)
    page.update()

    # Кнопка для запуска выбора файла
    upload_button = ft.ElevatedButton(
        "Upload File",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=['xls', 'xlsx', 'xlsm', 'csv']
        ),
    )

    page.add(upload_button)


# Запуск приложения
ft.app(target=main)
