import streamlit as st
import json
from streamlit.components.v1 import html
import pandas as pd

# Define custom CSS for the recommendation container
st.markdown("""
    <style>
    .recommendation-container {
        background-color: #f0f0f0; /* light grey */
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data  
def load_data():
    with open("data/network_data.json", "r") as f:
        G = json.load(f)
    
    with open("data/connections_31.json", "r") as f:
        Connections_31 = json.load(f)
    
    with open("data/connections_99.json", "r") as f:
        Connections_99 = json.load(f)
    
    cluster_df = pd.read_csv("data/cluster_processed.csv")
    
    return G, Connections_31, Connections_99, cluster_df

# load data
G, Connections_31, Connections_99, cluster_df = load_data()

def create_interactive_tree_viz(G, focus_node, cluster_df, connections):
    
    # Calculate toxicity range 
    nodes_to_show = set([focus_node])
    for conn in connections[:5]:
        nodes_to_show.add(conn['node_id'])
    
    toxicities = [cluster_df[cluster_df['cluster_id'] == node_id].iloc[0]['avg_toxicity'] 
                 for node_id in nodes_to_show]
    min_tox, max_tox = min(toxicities), max(toxicities)

    # Create nodes dictionary
    nodes_dict = {}
    for node in G["nodes"]:
        node_id = str(node["id"])
        nodes_dict[node_id] = {
            "keywords": node.get("keywords", []),
            "id": node_id,
            "toxicity": node.get("toxicity", 0)
        }

    # Calculate secondary connections
    secondary_connections = {}
    for conn in connections[:5]:
        primary_node = conn['node_id']
        secondary = []
        # Get up to 2 neighbors for each primary connection
        for node in G["nodes"]:
            if str(node["id"]) != focus_node and str(node["id"]) != primary_node:
                node_row = cluster_df[cluster_df['cluster_id'] == node["id"]].iloc[0]
                secondary.append({
                    'node_id': str(node["id"]),
                    'toxicity': node_row['avg_toxicity']
                })
        secondary.sort(key=lambda x: x['toxicity'], reverse=True)
        secondary_connections[primary_node] = secondary[:2]

    # Prepare the data
    graph_data = {
        "nodes": nodes_dict,
        "clusterDf": cluster_df.to_dict('records'),
        "connections": connections,
        "secondaryConnections": secondary_connections,
        "toxicityRange": {"min": min_tox, "max": max_tox},
        "spacing": {
            'xMain': 0.15,
            'xImmediate': 0.45,
            'xSecondaryLeft': 0.70,
            'xSecondaryRight': 0.80,
            'boxWidth': 0.18,
            'boxHeight': 0.07,
            'ySpacing': 0.20,
            'textPadding': 0.005
        }
    }

    # HTML template with matching aesthetics
    component_html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <script src="https://unpkg.com/react@17/umd/react.development.js"></script>
            <script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                .node-box {{
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                    transition: all 0.3s ease;
                }}
                .connection-line {{
                    stroke-dasharray: 5,5;
                }}
            </style>
        </head>
        <body>
            <div id="root"></div>
            <script type="text/javascript">
                const DEFAULT_DATA = {{
                    nodes: {{}},
                    clusterDf: [],
                    connections: []
                }};

                const graphData = {json.dumps(graph_data)};
                const focusNode = "{focus_node}";

                function getNodeColor(toxicity) {{
                    return `rgba(255,${{Math.floor(255 * (1 - toxicity))}},0,0.4)`;
                }}

                function createCurvedPath(start, end) {{
                    const midX = (start[0] + end[0]) / 2;
                    return `M${{start[0]}},${{start[1]}} C${{midX}},${{start[1]}} ${{midX}},${{end[1]}} ${{end[0]}},${{end[1]}}`;
                }}

                const InteractiveTreeVisualization = React.memo(function(props) {{
                    const {{graphData = DEFAULT_DATA, focusNode, width = 1200, height = 700}} = props;
                    const [expandedNodes, setExpandedNodes] = React.useState(new Set([focusNode]));
                    const [hoveredNode, setHoveredNode] = React.useState(null);

                    const spacing = {{
                        xMain: 0.15,
                        xImmediate: 0.45,
                        xSecondaryLeft: 0.70,
                        xSecondaryRight: 0.80,
                        boxWidth: 0.18,
                        boxHeight: 0.07,
                        ySpacing: 0.20,
                        textPadding: 0.005
                    }};

                    const Node = React.memo(function({{ nodeId, position, through = null }}) {{
                        const node = graphData.nodes[nodeId] || {{ keywords: [] }};
                        const clusterInfo = graphData.clusterDf.find(d => d.cluster_id.toString() === nodeId.toString());
                        const toxicity = clusterInfo?.avg_toxicity || 0;
                        
                        // Clean and wrap keywords like in original function
                        const cleanKeywords = (keywords) => {{
                            const cleaned = [];
                            const seen = new Set();
                            keywords.forEach(kw => {{
                                if (!seen.has(kw.toLowerCase())) {{
                                    seen.add(kw.toLowerCase());
                                    cleaned.push(kw === kw.toUpperCase() ? kw : kw.charAt(0).toUpperCase() + kw.slice(1));
                                }}
                            }});
                            return cleaned.slice(0, 4);
                        }};
                        
                        const keywords = cleanKeywords(node.keywords).join(', ');
                        
                        // Get period from temporal evolution
                        let period = 'N/A';
                        if (clusterInfo?.temporal_evolution) {{
                            try {{
                                const temporal = JSON.parse(clusterInfo.temporal_evolution);
                                const allMonths = [];
                                Object.entries(temporal).forEach(([year, months]) => {{
                                    Object.keys(months).forEach(month => allMonths.push(month));
                                }});
                                if (allMonths.length) {{
                                    period = `${{Math.min(...allMonths)}} to ${{Math.max(...allMonths)}}`;
                                }}
                            }} catch (e) {{
                                console.error('Error parsing temporal evolution:', e);
                            }}
                        }}

                        return React.createElement('div', {{
                            className: 'absolute node-box rounded-lg p-3',
                            style: {{
                                left: position[0] * width + 'px',
                                top: position[1] * height + 'px',
                                width: spacing.boxWidth * width + 'px',
                                height: spacing.boxHeight * height + 'px',
                                transform: 'translate(-50%, -50%)',
                                backgroundColor: getNodeColor(toxicity),
                                border: '1px solid rgba(128,128,128,0.5)',
                                cursor: 'pointer',
                                padding: spacing.textPadding * width + 'px'
                            }},
                            onClick: () => {{
                                setExpandedNodes(prev => {{
                                    const next = new Set(prev);
                                    if (next.has(nodeId)) next.delete(nodeId);
                                    else next.add(nodeId);
                                    return next;
                                }});
                            }},
                            onMouseEnter: () => setHoveredNode(nodeId),
                            onMouseLeave: () => setHoveredNode(null)
                        }}, [
                            React.createElement('div', {{
                                key: 'title',
                                className: 'text-center font-bold mb-2'
                            }}, keywords),
                            React.createElement('div', {{
                                key: 'details',
                                className: 'text-center text-sm'
                            }}, [
                                React.createElement('div', {{ key: 'toxicity' }}, `Toxicity: ${{toxicity.toFixed(3)}}`),
                                React.createElement('div', {{ key: 'period' }}, `Period: ${{period}}`),
                                through && React.createElement('div', {{ key: 'through' }}, 
                                    `via ${{graphData.nodes[through]?.keywords[0] || 'unknown'}}`)
                            ])
                        ]);
                    }});

                    // Add this function right after the Node component
                    const renderSecondaryConnections = (primaryNodeId, primaryPos) => {{
                        if (!graphData.secondaryConnections[primaryNodeId]) return null;
                        
                        return graphData.secondaryConnections[primaryNodeId].map((secConn, i) => {{
                            const xPos = i % 2 === 0 ? spacing.xSecondaryLeft : spacing.xSecondaryRight;
                            const yOffset = spacing.ySpacing * (0.3 * (i % 2 === 0 ? 1 : -1));
                            const yPos = primaryPos[1] + yOffset;
                            
                            return [
                                createConnection(
                                    [primaryPos[0] + spacing.boxWidth/2, primaryPos[1]],
                                    [xPos - spacing.boxWidth/2, yPos],
                                    0.3
                                ),
                                React.createElement(Node, {{
                                    key: secConn.node_id,
                                    nodeId: secConn.node_id,
                                    position: [xPos, yPos],
                                    through: primaryNodeId
                                }})
                            ];
                        }});
                    }};

                    return React.createElement('div', {{
                        className: 'relative bg-white rounded-lg shadow-lg',
                        style: {{ width, height }}
                    }}, [
                        React.createElement('svg', {{
                            key: 'svg',
                            className: 'absolute top-0 left-0',
                            width,
                            height,
                            style: {{ pointerEvents: 'none' }}
                        }}, expandedNodes.has(focusNode) && graphData.connections.slice(0, 5).map((conn, i) => {{
                            const start = [spacing.xMain + spacing.boxWidth/2, 0.5];
                            const end = [spacing.xImmediate - spacing.boxWidth/2, 0.9 - i * spacing.ySpacing];
                            return React.createElement('g', {{ key: `conn-${{i}}` }}, [
                                React.createElement('path', {{
                                    key: 'path',
                                    d: createCurvedPath(
                                        [start[0] * width, start[1] * height],
                                        [end[0] * width, end[1] * height]
                                    ),
                                    stroke: 'gray',
                                    strokeWidth: 1,
                                    fill: 'none',
                                    opacity: 0.5
                                }}),
                                expandedNodes.has(focusNode) && graphData.connections.slice(0, 5).map((conn, i) => {{
                                const primaryPos = [spacing.xImmediate, 0.9 - i * spacing.ySpacing];
                                return graphData.secondaryConnections[conn.node_id]?.map((secConn, j) => {{
                                    const xPos = j % 2 === 0 ? spacing.xSecondaryLeft : spacing.xSecondaryRight;
                                    const yOffset = spacing.ySpacing * (0.3 * (j % 2 === 0 ? 1 : -1));
                                    const yPos = primaryPos[1] + yOffset;
                                    
                                    return React.createElement('path', {{
                                        key: `secondary-path-${{secConn.node_id}}`,
                                        d: createCurvedPath(
                                            [primaryPos[0] + spacing.boxWidth/2, primaryPos[1]],
                                            [xPos - spacing.boxWidth/2, yPos]
                                        ),
                                        stroke: 'gray',
                                        strokeWidth: 1,
                                        fill: 'none',
                                        opacity: 0.3
                                    }});
                                }});
                            }})
                        ]),
                                React.createElement('text', {{
                                    key: 'text',
                                    x: (start[0] + end[0]) * width / 2,
                                    y: (start[1] + end[1]) * height / 2,
                                    textAnchor: 'middle',
                                    fill: 'gray',
                                    fontSize: 12
                                }}, `${{(conn.temporal_sim * 100).toFixed(1)}}%`)
                            ]);
                        }})),
                        React.createElement(Node, {{
                            key: 'main-node',
                            nodeId: focusNode,
                            position: [spacing.xMain, 0.5]
                        }}),
                        expandedNodes.has(focusNode) && graphData.connections.slice(0, 5).map((conn, i) =>
                            React.createElement(Node, {{
                                key: conn.node_id,
                                nodeId: conn.node_id,
                                position: [spacing.xImmediate, 0.9 - i * spacing.ySpacing]
                            }})
                        ),
                        expandedNodes.has(focusNode) && graphData.connections.slice(0, 5).map((conn, i) => {{
                            const primaryPos = [spacing.xImmediate, 0.9 - i * spacing.ySpacing];
                            return graphData.secondaryConnections[conn.node_id]?.map((secConn, j) => {{
                                const xPos = j % 2 === 0 ? spacing.xSecondaryLeft : spacing.xSecondaryRight;
                                const yOffset = spacing.ySpacing * (0.3 * (j % 2 === 0 ? 1 : -1));
                                const yPos = primaryPos[1] + yOffset;
                                
                                return React.createElement(Node, {{
                                    key: `secondary-${{secConn.node_id}}`,
                                    nodeId: secConn.node_id,
                                    position: [xPos, yPos],
                                    through: conn.node_id
                                }});
                            }});
                        }}),
                        React.createElement('div', {{
                            key: 'legend',
                            className: 'absolute top-4 right-4 bg-white p-4 rounded shadow-md'
                        }}, [
                            React.createElement('div', {{
                                key: 'title',
                                className: 'text-lg font-bold mb-2'
                            }}, 'Topic Relationship Analysis'),
                            React.createElement('div', {{
                                key: 'low',
                                className: 'flex items-center gap-2'
                            }}, [
                                React.createElement('div', {{
                                    key: 'color',
                                    className: 'w-4 h-4',
                                    style: {{ backgroundColor: getNodeColor(0.1) }}
                                }}),
                                React.createElement('span', {{ key: 'label' }}, 'Low Toxicity')
                            ]),
                            React.createElement('div', {{
                                key: 'high',
                                className: 'flex items-center gap-2'
                            }}, [
                                React.createElement('div', {{
                                    key: 'color',
                                    className: 'w-4 h-4',
                                    style: {{ backgroundColor: getNodeColor(0.9) }}
                                }}),
                                React.createElement('span', {{ key: 'label' }}, 'High Toxicity')
                            ])
                        ])
                    ]);
                }});

                ReactDOM.render(
                    React.createElement(InteractiveTreeVisualization, {{
                        graphData: graphData,
                        focusNode: focusNode,
                        width: 800,
                        height: 600
                    }}),
                    document.getElementById('root')
                );
            </script>
        </body>
    </html>
    """
    
    return html(component_html, height=600)

# Title and description
st.title("Reddit Content Analysis: Topic Deep Dive")

# Sidebar for Detailed Analysis options with "Police" as the default
st.sidebar.header("Detailed Analysis")
page_selection = st.sidebar.selectbox("Choose a topic for detailed analysis:", ["Police", "LGBTQ"], index=0)

# Layout setup based on selected topic
if page_selection == "Police":
    st.header("Detailed Analysis: Police-related Topics")
    st.markdown("In-depth analysis focusing on toxicity trends around police-related discussions.")
    
    # Technical Terms Explanation (at the top)
    with st.expander("Technical Terms Explanation"):
        st.write("""
        **Toxicity Score**: The toxicity score represents the likelihood of toxic content within discussions. 
        Higher scores indicate higher levels of toxic language.
        
        **Correlation Score**: The correlation score represents the strength of the relationship between topics.
        Higher scores indicate a stronger association between topics, suggesting that discussions in one topic
        may influence or correlate with discussions in another.
        """)

    # Create two main columns: one for stacked graphs and one for recommendations
    left_col, right_col = st.columns([3, 1])  # Left column wider than right column

    with left_col:
        tab1, tab2 = st.tabs(["Topic Relationship Tree", "Topic Relationship Trends Over Time"])

        with tab1:
            st.image('dashboard/graphs/police_tree.png', use_column_width=True)  # Fallback to static image

        with tab2:
            st.image('dashboard/graphs/police_temporal.png', use_column_width=True)

    with right_col:
    # Create tabs for insights and recommendations
        tab1, tab2 = st.tabs(["Insights", "Recommendations"])

        with tab1:
            st.markdown("""
            **Insights:**
            - High toxicity peaks are observed around **"Cops, Policeman, Arrest"**, especially between 2020-2021, with moderate correlation to topics like **"Accusations"** and **"Drugs"**.
            - Other sensitive topics like **"Burns"** and **"Filming, CCTV"** are also highly connected to police discussions.
            """)

        with tab2:
            # Container for recommendations with grey background
            st.markdown("""
            **Recommendations for Police-related Discussions:**
            1. <strong>Monitor keywords</strong> related to arrests and police actions (e.g., "arrest," "use of force," "riot") during sensitive periods to flag inflammatory content.
            2. <strong>Address sensitive topics</strong> like police accountability with fact-checking initiatives and encourage constructive, respectful discussions on legal rights and policing.
            """, unsafe_allow_html=True)



elif page_selection == "LGBTQ":
    st.header("Detailed Analysis: LGBTQ-related Topics")
    st.markdown("In-depth analysis focusing on toxicity trends around LGBTQ-related discussions.")

    # Technical Terms Explanation (at the top)
    with st.expander("Technical Terms Explanation"):
        st.write("""
        **Toxicity Score**: The toxicity score represents the likelihood of toxic content within discussions. 
        Higher scores indicate higher levels of toxic language.
        
        **Moderation Rate**: Percentage of content that has been flagged or moderated to maintain community standards.
        """)

    # Create two main columns: one for stacked graphs and one for recommendations
    left_col, right_col = st.columns([3, 1])  # Left column wider than right column

    with left_col:
        # Create Tabs for the left column (graphs)
        tab1, tab2 = st.tabs(["Topic Relationship Tree", "Topic Relationship Trends Over Time"])

        with tab1:
            st.image('dashboard/graphs/lgbtq_tree.png', use_column_width=True)

        with tab2:
            st.image('dashboard/graphs/lgbtq_temporal.png', use_column_width=True)

    with right_col:
    # Create tabs for insights and recommendations
        tab1, tab2 = st.tabs(["Insights", "Recommendations"])

        with tab1:
            st.markdown("""
            **Insights:**
            - High toxicity peaks are observed around **"Homosexual, Repeal, Homosexuality, Transgender"**, especially between 2020-2023, indicating heightened toxicity during sensitive events like legal debates on LGBTQ rights.
            - Topics such as **"Patriarchy, Masculinity, Feminists"**, **"Diversity, Racists, Ethnic"**, and **"Ballot, Voting, Voted"** show moderate correlation with LGBTQ discussions, suggesting connections to broader societal issues like gender equality and voting rights.
            """)

        with tab2:
            # Container for recommendations with grey background
            st.markdown("""
            **Recommendations for LGBTQ-related Discussions:**
            1. <strong>Monitor and moderate sensitive keywords</strong> related to LGBTQ topics (e.g., "homosexuality," "transgender," "gender rights") during high-intensity periods such as debates on LGBTQ rights.
            2. <strong>Promote respectful dialogue</strong> by providing factual information on LGBTQ issues like gender equality and transgender rights, and encourage community leaders to reduce harmful rhetoric.
            """, unsafe_allow_html=True)