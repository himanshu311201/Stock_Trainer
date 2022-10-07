














import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    print(image_png)
    graph = base64.b64encode(image_png)
    print(graph)
    graph = graph.decode('utf-8')
    print(graph)
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(20,10))
    plt.title('sale of items')
    plt.plot(x,y)
    plt.xticks(rotation = 45)
    plt.xlabel('Item')
    plt.ylabel('Price')
    plt.tight_layout()
    graph = get_graph()
    return graph