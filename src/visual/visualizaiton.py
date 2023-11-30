import plotly.express as px
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.io as pio



class Visual:
    def __init__(self):
        pass
    
    def simple_3D(self,df):
        fig = px.scatter_3d(df, x='x', y='y', z='z', color='z', size_max=18, opacity=0.7)

        # Adding labels and title
        fig.update_layout(title='3D Scatter Plot', scene=dict(
                            xaxis_title='X axis',
                            yaxis_title='Y axis',
                            zaxis_title='Z axis'))

        # Showing the plot
        fig.show()

    def simple_3D_matplotlib(self,df):
        # Creating a new figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Scatter plot
        scatter = ax.scatter(df['x'], df['y'], df['z'], marker='o')

        # Adding labels and title
        ax.set_title('3D Scatter Plot')
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        # Showing the plot
        plt.show() 
    
    def plot_3d_scatter_with_label(self, df,clusters):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Define a color map with a specific color for each label value
        colors = ['red', 'green', 'yellow', 'purple', 'blue']
        color_map = {label: color for label, color in zip(df['Label'].unique(), colors)}

        # Get the color for each point
        point_colors = df['Label'].map(color_map)

        # Create a scatter plot
        scatter = ax.scatter(df['x'], df['y'], df['z'], c=point_colors)

        # Create a custom legend
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                        for label, color in color_map.items()]
        ax.legend(handles=legend_elements, title="Labels")

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title(f'Clustered Point Cloud Data with {clusters} labels')
        plt.savefig(f'{clusters} clusters.png')
        plt.show()
        
    def plot_cluster_centroids(self, x_train, y_pred, model, num_cols):
    
        fig = sp.make_subplots(rows=1, cols=num_cols, subplot_titles=[f'Cluster {i}' for i in range(num_cols)])

        sz = x_train.shape[1]  # Assuming you want the second dimension of x_train

        for yi in range(num_cols):
            # Check if there are any data points in this cluster
            if not any(y_pred == yi):
                print(f"No data points found for cluster {yi}")
                continue

            for xx in x_train[y_pred == yi]:
                fig.add_trace(
                    go.Scatter(y=xx.ravel(), mode='lines', line=dict(width=1, color='gray'), showlegend=False),
                    row=1, col=yi + 1
                )

            fig.add_trace(
                go.Scatter(y=model.cluster_centers_[yi].ravel(), mode='lines', line=dict(color='red', width=2), showlegend=False),
                row=1, col=yi + 1
            )

            fig.update_yaxes(range=[-4, 4], row=1, col=yi + 1)
            fig.update_xaxes(range=[0, sz], row=1, col=yi + 1)

        if num_cols > 1:
            fig.update_layout(title_text="Centroid of all the clusters")

        # Set the size of the plot
        fig.update_layout(autosize=False, width=900, height=500)

        # Dynamically set the file name
        file_name = f'cluster_centroid_plot_{num_cols}.png'

        # Save the plot as PNG
        pio.write_image(fig, file_name)

        # Optionally, you can also display the plot
        fig.show()
        


            