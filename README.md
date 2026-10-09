# Interactive Pyvis Graph for FOSS4GNA 2026

![Banner for FOSS4GNA with a logo with golden California poppies in the middle with a banner in light green wrapping around in a circle with the text FOSS4GNA 2026 on the top and Sacramento, CA on the right side. The background is blue with OpenStreetMap map data and a white quail on the bottom right. The text on the banner reads FOSS4G North America, Sacramento, CA, November 2-4, 2026.](images/foss4gna-2026-banner.png)

## Live demo

See the graph in action on my [portfolio site](https://rachelgugler.com/projects/2026-10-08_foss4gna_graph_map/).

The Whova schedule for [FOSS4GNA 2026 Conference](https://www.foss4gna.org) is packed full of interesting talks, workshops, and events, however it can sometimes feel like you are staring at a wall of text and stop absorbing what you are reading. I've found that adding the schedule to a visual interactive graph like you'll see in note taking apps like Notion or Obsidian, you can filter through topics better and identify programs you otherwise might have missed.

This was a slight rewrite of the project done for the 2025 conference. While that one was mostly done using AI for the data cleaning, hydration, and graph coding, this time it was done mostly by hand with minimal AI use for some data cleaning and troubleshooting.

![A picture of the graph with the legend up top, then the filters, and finally the section with the graph. The Topics are colorful rectangles and the node shapes depend on the Type. The background of the window is light green and the background of the legend, filters, and graph are a dark blue.](images/foss4gna-schedule-graph-2026.png)

## Using this project yourself

This project doesn't touch on the data cleaning side at all. The code expects your data to be ready to go, with an example CSV template included. If you need different titles, nodes, etc, it will take a little bit of refactoring, but I tried to comment everything and the [pyvis documentation](https://pyvis.readthedocs.io/en/latest/index.html) is very helpful. 

- It is currently set to create everything inline so it can be easily embedded. If you don't need to do that, commenting out `cdn_resources="in_line"` will have it create a separate folder instead.
- It expects topics to be separated by a semicolon (;). If you have it separated by something else you can change it, but make sure your topics don't also have a comma in it if you are separating by comma.

> [!NOTE]
> The background, session node, and text color global variables control the colors of the graph itself. The chosen colors are selected for a dark map with white text. If you want a light background, you'll want to adjust all the colors. It is currently not set up to adjust the CSS colors set in the html template either, so you will want to go in and adjust the legend and colors manually to match your graph color theme.


## Setup and install

This project uses [uv](https://docs.astral.sh/uv/) to manage Python and dependencies.

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it.
2. Clone the repo and move into it:
  ```bash
     git clone https://github.com/rgugs/foss4gna_graph_2026.git
     cd foss4gna_graph_2026
  ```
3. Install the dependencies:
  ```bash
     uv sync
  ```
4. Change variables to match your colors, input csv, etc.
5. Generate the graph:
  ```bash
     uv run main.py
  ```

The graph is saved as whatever you put in the output_file variable in the main() function. Open it in a browser to view it.

You can rerun the script as needed for changes, and view them by refreshing the page in your browser.