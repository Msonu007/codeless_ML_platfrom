import base64
import io
import pandas as pd

import dash
from dash import html
from dash import dcc, State
from dash.dependencies import Output, Input
import sqlite3

connection = sqlite3.connect("../backend/database.db")
upload_image_link = "https://www.lifewire.com/thmb/G9NUSqx8NhyEL3x0lkXmWNXuaNk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/cloud-upload-a30f385a928e44e199a62210d578375a.jpg"
app = dash.Dash("myapp")
server = app.server
upload_child = dcc.Upload(
    id="dataset-upload",
    children=html.Button("Upload file"),
    multiple=True
)

app.layout = html.Div([
    html.Center(html.H2("Codeless Machine Learning platform")),
    html.H3("Dataset Upload"),
    html.P("Hi welcome to my codeless machinelearning platform, please upload your dataset using the below option"),
    html.Img(src=upload_image_link),
    dcc.Loading(id="upload-loading", children=upload_child, type="graph"),
    html.Div(id="upload errors"),
    html.Div(id="upload_status"),
    html.Button("Data Visualisation", id="page2"),
])


@app.callback([Output(component_id="upload_errors",component_property="children"),
               Output(component_id="upload_status",component_property="children")],
              [Input(component_id="dataset_upload", component_property="children")],
              [State("dataset_upload", "filename")])
def upload_dataset(dataset, file_name):
    if dataset is not None:
        data_type, data_string = dataset.split(",")
        decoded = base64.b64decode(data_string)
        name_ = file_name.split(".")[0]
        print("the function entered")
        try:
            if 'csv' in file_name:
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
                print("dataset read")
            elif "xls" in file_name:
                df = pd.read_excel(io.StringIO(decoded.decode("utf-8")))
            else:
                return f"filetype is not supported for file {file_name}","Failed upload"
            try:
                df.to_sql(name_,connection,if_exists='replace',index=False)
            except Exception as e:
                return f"Error occoured while pushing to sql database with error {e}","Failed upload"
            return "No upload Errors","Sucesss uploading"
        except Exception as e:
            return None,f"Error occoured while uploading {e}"
    return "None","Failed to upload"


if __name__ == "__main__":
    app.run("0.0.0.0", port=8000,debug=True)
