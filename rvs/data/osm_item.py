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
'''Basic classes and functions for Wikigeo items.'''

import geopandas as gpd
import re
from typing import Text, Dict
from shapely.geometry.point import Point
import webcolors

import attr


@attr.s
class OSMEntity:
  """Construct a OSM entity.

  `osmid` is the osm id.
  `text` is the sample from tags.
  `name` is the name of the entity.
  `qid` is the Wikidata id assigned to this entity.
  `point` is the location.    
  """
  osmid: int = attr.ib()
  text: Text = attr.ib(init=False)
  name: Text = attr.ib(init=False)
  qid: Text = attr.ib(init=False)
  point: Point = attr.ib()
  raw: gpd.GeoSeries = attr.ib()

  def __attrs_post_init__(self):
    
    self.name = self.raw['name'] if 'name' in self.raw else ""
    self.qid = self.raw['wikidata'] if 'wikidata' in self.raw else str(
      self.osmid)

    wanted_col = ['name', 'amenity', 'colour', 'brand', 'tourism', 'leisure', 
    'historic', 'building', 'description', 'building:colour', 
    'building:material', 'roof:material', 'roof:shape', 'roof:colour', 'office', 
    'addr:street', 'diplomatic']
    col_included = [col for col in wanted_col if col in self.raw]
    self.raw = self.raw[col_included]
    self.text = concat_dictionary(self.raw.to_dict())

  @classmethod
  def from_osm(cls, row):
    """Construct an Entity from the Wikidata tags."""
    return OSMEntity(
      row['osmid'],
      row['centroid'],
      row)


def concat_dictionary(dictionary: Dict) -> Text:
  tag_list = []
  for k, v in dictionary.items():
    if isinstance(v, str):
      if 'colour' in k and v[0]=='#':
        v = get_colour_name(v)
      k = k.replace("_", " ")
      v = v.replace("_", " ")
      if k in ['building','historic', 'diplomatic']:  
        tag_list.append(k)
      elif v in ['yes']:
        tag_list.append(k)
      elif v in ['no']:
        continue
      else:
        tag_list.append(v)      

  return ' and '.join(tag_list) + "."


def closest_color(hex_color: Text) -> Text:
    '''Find the closest color in css21.
    Arguments:
      hex_color: The color in Hex format to be converted.
    Returns:
      The name of the color.
    '''
    rgb_color = webcolors.hex_to_rgb(hex_color)
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_color[0]) ** 2
        gd = (g_c - rgb_color[1]) ** 2
        bd = (b_c - rgb_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def get_colour_name(hex_color: Text) -> Text:
    '''Converts a color in Hex format to the closest color that has a name in 
    css21.
    Arguments:
      hex_color: The color in Hex format to be converted.
    Returns:
      The name of the color.
    '''

    try:
        closest_name = webcolors.CSS3_HEX_TO_NAMES[hex_color]  
    except KeyError:
        closest_name = closest_color(hex_color)
    return closest_name

