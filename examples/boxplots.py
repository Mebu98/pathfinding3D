import pandas as pd
import plotly.express as px

def show_boxplots(results):
    for key in results[0].runs[0].keys():
        if key not in ['name', 'start', 'end']:
            bp_vals = {
                result.name: [run.get(key) for run in result.runs]
                for result in results
            }

            # Convert to long-form DataFrame
            data = []
            for name, values in bp_vals.items():
                for v in values:
                    data.append({'name': name, key: v})
            df = pd.DataFrame(data)

            # Assign fixed colors
            color_map = {
                list(bp_vals.keys())[0]: 'blue'

            }

            bp = px.box(
                df,
                x='name',
                y=key,
                color='name',
                color_discrete_map=color_map,
                title=key
            )
            bp.show()
