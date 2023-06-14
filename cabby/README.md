# Rendezvous(RVS): Location Finding using Nearby Landmarks

### (1) Creating an OSM-based graph
```
bazel-bin/cabby/geo/map_processing/map_processor --region REGION --min_s2_level LEVEL --directory DIRECTORY_TO_MAP
```
### (2) Connecting the S2-Cells to the graph (1) and calculating the environment embedding 
```
bazel-bin/cabby/data/metagraph/create_graph_embedding  --region REGION --s2_level LEVEL --s2_node_levels LEVEL --s2_node_levels LEVEL+1 --s2_node_levels LEVEL-1  --base_osm_map_filepath DIRECTORY_TO_MAP --save_embedding_path PATH_TO_SAVE --dimensions EMBED_DIM
```
### (3) Generating spatial samples based on the graph (1)
```
bazel-bin/cabby/geo/sample_poi --region REGION --min_s2_level LEVEL --directory DIRECTORY_TO_MAP --path PATH_TO_SPATIAL_ITEMS.gpkg --n_samples NUMBER_OF_SAMPLES_TO_GENERATE
```
