# coding=utf-8
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''Library to support graph embedding creation from Wikipedia and Wikidata.'''


from absl import app
from absl import flags
from absl import logging
import networkx as nx
import os
import pickle

from node2vec import Node2Vec


from rvs.geo import regions
from rvs.data.metagraph import utils

flags.DEFINE_enum(
  "region", None, regions.SUPPORTED_REGION_NAMES, regions.REGION_SUPPORT_MESSAGE)
flags.DEFINE_integer(
  "s2_level", None, "S2 level of the S2Cells.")
flags.DEFINE_multi_integer(
  "s2_node_levels",
  None,
  "Iterable of S2 cell levels (ints) to add to the graph." +
  "The flag can be specified more than once on the command line (the result is a Python list integers).")
flags.DEFINE_string(
  "base_osm_map_filepath", None, "Location of the map_structure.Map to be loaded.")

flags.DEFINE_string(
  "save_embedding_path", None, "Location of the embedding to be saved.")

flags.DEFINE_string(
  "save_graph_dir", None, "Location of the graph to be saved.")

flags.DEFINE_integer(
  'dimensions', default=224,
  help=('dimensions of Node2Vec.'))

flags.DEFINE_integer(
  'walk_length', default=30,
  help=('walk length of Node2Vec: How many nodes are in each random walk.'))

flags.DEFINE_integer(
  'num_walks', default=200,
  help=(
    'num of walks of Node2Vec: Number of random walks to be generated from each node in the graph'))

flags.DEFINE_integer(
  'window', default=10,
  help=('context window size of Node2Vec.'))

flags.DEFINE_integer(
  'workers', default=1,
  help=('number of threads for Node2Vec.'))

flags.DEFINE_integer(
  'n_epochs', default=5,
  help=('number of epochs of Node2Vec.'))


flags.DEFINE_bool(
  'is_draw_graph', default=True,
  help=('Draw the constructed graph'))

# Required flags.
flags.mark_flag_as_required("s2_node_levels")
flags.mark_flag_as_required("base_osm_map_filepath")
flags.mark_flag_as_required("region")
flags.mark_flag_as_required("s2_level")
flags.mark_flag_as_required("save_embedding_path")

FLAGS = flags.FLAGS

def main(argv):
  del argv  # Unused.

  graph = utils.construct_metagraph(
                            region=regions.get_region(FLAGS.region),
                            s2_level=FLAGS.s2_level,
                            s2_node_levels=FLAGS.s2_node_levels,
                            base_osm_map_filepath=FLAGS.base_osm_map_filepath,
                            )

  # Save graph to dir
  if FLAGS.save_graph_dir and os.path.exists(FLAGS.save_graph_dir):
    path_to_save_graph = os.path.join(FLAGS.save_graph_dir, f'graph_{FLAGS.region}.pickle')
    with open(path_to_save_graph, "wb") as f:
    # Pickle the object to the file
      pickle.dump(graph, f)
    logging.info(f"Saved graph to path => {path_to_save_graph}")

    path_to_save_drawing_graph = os.path.join(FLAGS.save_graph_dir, f'graph_draw_{FLAGS.region}.png')
    if utils.is_draw_graph:
      utils.draw_graph(graph, path_to_save_drawing_graph)

  # Precompute probabilities and generate walks

  node2vec = Node2Vec(
    graph,
    dimensions=FLAGS.dimensions,
    walk_length=FLAGS.walk_length,
    num_walks=FLAGS.num_walks, workers=FLAGS.workers)

  # Embed nodes
  # Any keywords acceptable by gensim.Word2Vec can be passed,
  # `dimensions` and `workers` are automatically passed (from the Node2Vec constructor)
  model = node2vec.fit(window=FLAGS.window, min_count=1, batch_words=4, epochs=FLAGS.n_epochs)

  # Save embeddings for later use
  model.wv.save_word2vec_format(FLAGS.save_embedding_path)

  logging.info(f"Saved graph embedding to => {FLAGS.save_embedding_path}")

if __name__ == '__main__':
  app.run(main)
