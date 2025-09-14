import plotly.express as px

def show_boxplots(results):
    for key in results[0].runs[0].keys():
        # No need for boxplots for these keys
        if key not in ['name','start', 'end']:
            bp_vals = {
                result.name: [] for result in results
            }

            for result in results:
                bp_vals[result.name.lower()] = [run.get(key) for run in result.runs]

            bp = px.box(bp_vals, title=key)
            bp.show()