from dash import html

layout = html.Div([
       html.Div([
              html.H5([
                     
              ],id="loading_message")
       ],className="heading_container"),

       html.Div([
               html.Div(className="horizontal_loader1"),
               html.Div(className="horizontal_loader2"),
               html.Div(className="horizontal_loader3"),
               html.Div(className="horizontal_loader4"),
               html.Div(className="horizontal_loader5"),
       ],className="loading_container")
     
], className="animation_container",id="loading_screen")
