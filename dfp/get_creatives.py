#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from googleads import dfp

from dfp.client import get_client


logger = logging.getLogger(__name__)


def get_creatives_by_advertiser_id_and_name(advertiser_id, creative_name):
  """
  Gets a creative by advertiser_id and name from DFP.

  Args:
    advertiser_id : the id of the advertiser
    order_name (str): the name of the DFP creative
  Returns:
    a DFP creative, or None
  """

  dfp_client = get_client()
  creative_service = dfp_client.GetService('CreativeService', version='v201802')

  # Filter by name.
  query = 'WHERE name = :name AND advertiserId = :advertiser_id'
  values = [{
    'key': 'name',
    'value': {
      'xsi_type': 'TextValue',
      'value': creative_name
    },
  }, {
    'key': 'advertiser_id',
    'value': {
      'xsi_type': 'NumberValue',
      'value': advertiser_id
    }
  }]
  statement = dfp.FilterStatement(query, values)
  response = creative_service.getCreativesByStatement(statement.ToStatement())

  no_creative_found = False
  try:
    no_creative_found = True if len(response['results']) < 1 else False
  except (AttributeError, KeyError):
    no_creative_found = True

  if no_creative_found:
    return None
  else:
    creative = response['results'][0]
    logger.info(u'Found a creative with ID "{id}" and name "{name}".'.format(
      id=creative['id'], name=creative['name']))
    return creative

def get_creatives_by_advertiser_id(advertiser_id, print_creatives=False):
  """
  Logs all creatives in DFP.

  Returns:
      None
  """

  dfp_client = get_client()

  # Initialize appropriate service.
  creative_service = dfp_client.GetService('CreativeService', version='v201802')

  query = 'WHERE advertiserId = :advertiser_id'
  values = [{
    'key': 'advertiser_id',
    'value': {
      'xsi_type': 'NumberValue',
      'value': advertiser_id
    }
  }]

  # Create a statement to select creatives.
  statement = dfp.FilterStatement(query, values)

  # Retrieve a small amount of creatives at a time, paging
  # through until all orders have been retrieved.
  all_creatives = []
  while True:
    response = creative_service.getCreativesByStatement(statement.ToStatement())
    if 'results' in response:
      all_creatives = all_creatives + response['results']
      if print_creatives:
	for creative in response['results']:
	  msg = u'Found a creative with ID "{id}" and name "{name}".'.format(
	    id=creative['id'], name=creative['name'])
	  print(msg)
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break
  return all_creatives

def main():
  get_creatives_by_advertiser_id(sys.argv[1], print_creatives=True)

if __name__ == '__main__':
  main()
