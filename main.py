# %% Imports
from pathlib import Path

import pandas as pd
from pyvis.network import Network

# %% Set Global variables

# These colors are all darker and meant to be readable with white text. Will need to adjust if using darker text
COLORS = [
    "#2563eb",  # Blue
    "#047857",  # Emerald
    "#a16207",  # Ochre
    "#db2777",  # Pink
    "#7c3aed",  # Violet
    "#0e7490",  # Cyan
    "#c2410c",  # Orange
    "#134e4a",  # Dark teal
    "#3730a3",  # Indigo
    "#4d7c0f",  # Lime
    "#9d174d",  # Berry
    "#86608e",  # Mauve
    "#1f2937",  # Charcoal
    "#0369a1",  # Sky
    "#14532d",  # Forest
    "#dc2626",  # Red
    "#a21caf",  # Fuchsia
    "#1e3a8a",  # Navy
    "#78350f",  # Brown
    "#64748b",  # Slate
    "#6b21a8",  # Purple
    "#7f1d1d",  # Maroon
    "#701a75",  # Plum
    "#6b6a0f",  # Olive
    "#9a3412",  # Rust
]

# Dictionary of session types and designated shapes for their nodes
SESSION_TYPES = {
    "Talk": "dot",
    "Pre-Conference Workshop": "triangle",
    "Conference Event": "hexagon",
    "Keynote": "star",
    "Poster": "square",
    "Lightning Talk": "diamond",
}


# Tuple of tracks
TRACKS = (
    "Technical",
    "Application",
    "Business of Open Source",
    "Community of Practice",
)

# Tuple of topics that speakers could pick
TOPICS = (
    "Cloud-Native Geo",
    "Commercialization Strategies",
    "Cybersecurity",
    "Disaster Response & Resilience",
    "Discrete Global Grid Systems",
    "Emerging Tech & Future Directions",
    "Environment, Climate & Sustainability",
    "Funding Models",
    "Geo AI & Machine Learning",
    "Geospatial Data Science",
    "Infrastructure & Resource Systems",
    "Open Data",
    "Open Geospatial Tools",
    "Research & Education",
    "Open Source Maintenance & Support",
    "Raster & Remote Sensing",
    "Spatial Databases & Interoperability",
    "Spatio-Temporal Asset Catalog",
    "State-of-Software",
    "User Accessibility",
    "Web Mapping & Geospatial Visualization",
    "Workflows & Reproducibility",
    "Field Data Collection",
    "Other",
)

# Set for dark blue background and white text, change as needed. You'll still need to go in and edit the template.html manually to match different colors
BACKGROUND_COLOR = "#214963"
SESSION_NODE_COLOR = "#bdc3c7"
FONT_COLOR = "white"

# True if using Jupyter Notebook, otherwise false
JUPYTER_NB = False


# Dates in the input data are saved as text the month/day/year format. Change as needed to fit input data
def read_csv(input_csv: str | Path) -> pd.DataFrame:
    """Load CSV into a pandas DataFrame."""
    return pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=["date"],
        date_format={"date": "%m/%d/%Y"},
        encoding="utf-8",
    )


# zips the topics and colors list together. Currently no randomness involved.
def get_topic_colors(topics: tuple, colors: list) -> dict[str, str]:
    """Return color mapping for topic categories."""
    if len(colors) < len(topics):
        raise ValueError(
            f"Not enough colors for all topics. {len(topics)} topics and only {len(colors)}"
        )
    return dict(zip(topics, colors))


def create_network() -> Network:
    """Create and configure a pyvis Network object."""
    net = Network(
        height="70vh",  # Makes it responsive vs setting px 
        width="100%",
        bgcolor=BACKGROUND_COLOR,
        # pyright will complain about font color not being a bool, but it can take a string or code color
        font_color=FONT_COLOR,
        notebook=JUPYTER_NB,
        # So it can be hosted in a Quarto generated website
        cdn_resources="in_line",
        # These create a built in filter and selection option, but they did not work for my purposes
        # filter_menu=True,
        # select_menu=True,
    )
    # net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=200)
    net.force_atlas_2based(
        gravity=-50,
        central_gravity=0.01,
        spring_length=100,
        spring_strength=0.08,
        damping=0.4,
        overlap=0,
    )
    return net


def add_topic_nodes(net: Network, topic_colors: dict[str, str]):
    """Add topic category nodes to the network."""
    for topic, color in topic_colors.items():
        net.add_node(
            topic,
            label=topic,
            shape="box",
            color=color,
            size=30,
            font={"size": 16},
            title=topic,
        )


def add_session_nodes(net: Network, df: pd.DataFrame, session_types: dict[str, str]):
    """Add session nodes and edges to the network."""
    # pyright will complain about the tuple access, but it works
    for row in df.itertuples():
        session_id = f"session_{row.Index}"
        title = row.proposal_title
        speakers = row.speaker_names
        type = row.session_type
        track = row.track
        date = row.date.strftime("%m/%d/%Y")  # strips time off end of date
        # topics are in a single column separated by semicolons due to one of the topics having a comma in it, splits then strips whitespace
        topics = [t.strip() for t in row.topics.split(";") if t.strip()]

        # Full set of information inside of hover
        title_text = f"{title}\nSpeaker(s): {speakers}\nType: {type}\nTrack: {track}\nDate: {date}"

        # Limits title so it doesn't overlap neighbors, full title in hover
        label = title[:30] + "..." if len(title) > 30 else title

        # Different shapes for different types
        shape = session_types[type]

        net.add_node(
            session_id,
            label=label,
            title=title_text,
            color=SESSION_NODE_COLOR,
            size=15,
            shape=shape,
            date=date,
            type=type,
            track=track,
        )

        # Connect sessions to topics
        for t in topics:
            net.add_edge(session_id, t, color="#95a5a6")


# %% Create Custom Filters

# Pyvis includes the options for built in filters, however I didn't like how they looked, so these are custom ones


def prepare_filter_data(df):
    """Prepare filter options from the dataframe."""
    filter_data = {
        "dates": sorted(df["date"].dt.strftime("%m/%d/%Y").unique().tolist()),
        "types": sorted(SESSION_TYPES.keys()),
        "tracks": sorted(TRACKS),
        "topics": sorted(TOPICS),
    }
    return filter_data


def generate_filter_html(filter_data, template_path="template.html"):
    """Generate HTML for filter controls from template file."""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    date_options = "".join(
        f'<option value="{d}">{d}</option>' for d in filter_data["dates"]
    )
    type_options = "".join(
        f'<option value="{t}">{t}</option>' for t in filter_data["types"]
    )
    track_options = "".join(
        f'<option value="{t}">{t}</option>' for t in filter_data["tracks"]
    )
    topic_options = "".join(
        f'<option value="{t}">{t}</option>' for t in filter_data["topics"]
    )

    return (
        template.replace("{date_options}", date_options)
        .replace("{type_options}", type_options)
        .replace("{track_options}", track_options)
        .replace("{topic_options}", topic_options)
    )


def inject_controls(html_path, control_html):
    """Inject filter controls into the generated HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        pyvis_html = f.read()

    # Extract CSS (between <style> and </style>)
    css_match = control_html[
        control_html.find("<style>") : control_html.find("</style>") + 8
    ]

    # Extract legend and controls (between body opening and mynetwork div)
    body_start = control_html.find("<body>") + 6
    mynetwork_pos = control_html.find('<div id="mynetwork"></div>')
    controls_section = control_html[body_start:mynetwork_pos].strip()

    # Extract just the JavaScript code (without <script> tags)
    script_start = control_html.find("<script>") + 8
    script_end = control_html.find("</script>")
    script_code = control_html[script_start:script_end].strip()

    # Inject CSS into head (before </head>)
    pyvis_html = pyvis_html.replace("</head>", f"{css_match}\n</head>", 1)

    # Inject controls at the beginning of body (after <body>)
    pyvis_html = pyvis_html.replace("<body>", f"<body>\n{controls_section}\n", 1)

    # Find the existing script tag and inject our code at the end
    last_script_pos = pyvis_html.rfind("</script>")
    if last_script_pos != -1:
        pyvis_html = (
            pyvis_html[:last_script_pos]
            + f"\n\n{script_code}\n"
            + pyvis_html[last_script_pos:]
        )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(pyvis_html)


# %% Generate Graph


def generate_graph(csv_path, output_path):
    """Main function to generate the interactive graph."""
    # Load data
    df = read_csv(csv_path)

    topic_color_dict = get_topic_colors(TOPICS, COLORS)

    # Generate Network
    net = create_network()

    # Add nodes and edges
    add_topic_nodes(net, topic_color_dict)
    add_session_nodes(net, df, SESSION_TYPES)

    net.toggle_physics(True)
    # net.show_buttons(filter_=["physics"])

    # Save initial graph
    net.save_graph(output_path)

    # Prepare and inject filter controls
    filter_data = prepare_filter_data(df)
    control_html = generate_filter_html(filter_data)
    inject_controls(output_path, control_html)

    print(f"Graph generated: {output_path}")
    print("This file can be embedded in Quarto or hosted on GitHub Pages.")


# %% Main script


def main():
    """Entry point for the script."""
    csv_file = Path(
        "/home/rgugs/Desktop/Code/projects/other/foss4gna_graph_2026/.ignore/foss4gna-2026-graph-input.csv"
    )

    output_file = "conference_graph_2026.html"

    generate_graph(csv_file, output_file)


if __name__ == "__main__":
    main()
