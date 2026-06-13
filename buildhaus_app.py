import webview
import os

html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard.html')

window = webview.create_window(
    'Buildhaus Dashboard',
    url=f'file:///{html_path.replace(os.sep, "/")}',
    width=1200,
    height=800,
    min_size=(900, 600),
    background_color='#0d0d0d'
)

webview.start()
