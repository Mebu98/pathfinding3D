import plotly.express as px

def show_boxplots(results):
    def boxplot_operations():
        bp_operations = {
            result.name: [] for result in results
        }
        # [[run.operations for run in result.runs] for result in results]
        for result in results:
            bp_operations[result.name.lower()] = [run.operations for run in result.runs]

        boxplots = px.box(bp_operations, title="Operations")

        boxplots.show()

    boxplot_operations()