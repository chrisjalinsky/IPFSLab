#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# mvn_xml: Update xpath properties in Maven XML namespaced pom.xml files.
# This is a modified Vince Gonzalez's hadoop_properties
# Copyright 2014, Vince Gonzalez
# Vince Gonzalez <vince.gonzalez@gmail.com>
#
# Copyright 2014, Red Hat, Inc.
# Tim Bielawa <tbielawa@redhat.com>
# Magnus Hedemark <mhedemar@redhat.com>
#
# This software may be freely redistributed under the terms of the GNU
# general public license version 2.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


DOCUMENTATION = '''
---
module: mvn_xml
short_description: Manage properties in Maven XML files.
description:
  - Update properties in Maven XML properties files.
version_added: "1.0"
options:
  file:
    description:
      - Path to the file to operate on. File must exist ahead of time.
    required: true
    default: null
  xpath:
    description:
      - Xpath to operate upon - requires the use of namespaces
    required: true
    default: null
  ns:
    description:
      - Namespace to search xpath with - defaults to Maven
    required: false
    default: http://maven.apache.org/POM/4.0.0
  value:
    description:
      - Desired string value of the property
    required: true
    default: null
requirements:
    - The remote end must have the Python C(lxml) library installed
author: Chris Jalinsky - based on a module by Tim Bielawa and Magnus Hedemark
'''


from io import BytesIO
from lxml import etree
try:
    import json
except:
    import simplejson as json
import lxml
import os

def modify_property(tree, xpath, value, module, ns):
    changed = False
    node = None

    try:
        node = tree.xpath(xpath, namespaces={'t': ns } )[0]
    except Exception as e:
        abort("Could not find xpath '%s': %s" % (xpath, e))

    if node.text != value:
        node.text = value
        changed = True

    finish(tree, xpath, module, changed=changed)

def abort(msg, m):
    m.fail_json(msg=msg)

def finish(tree, xpath, m, changed=False, msg="", hitcount=0):
    if changed:
        tree.write(m.params['file'], xml_declaration=True, encoding='UTF-8', pretty_print=True)
    m.exit_json(changed=changed,actions={"xpath": xpath, "tree": etree.tostring(tree, pretty_print=True), "changed": changed}, msg=msg, count=hitcount)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            file=dict(required=True, default=None),
            ns=dict(required=False, default="http://maven.apache.org/POM/4.0.0"),
            xpath=dict(required=True, default=None),
            value=dict(required=True, default=None)
        ),
        supports_check_mode=False,
        mutually_exclusive = [
        ]
    )

    xml_file = module.params['file']
    xpath = module.params['xpath']
    value = module.params['value']
    ns = module.params['ns']

    if os.path.isfile(xml_file):
        infile = file(xml_file, 'r')
    else:
        module.fail_json(
            msg="The target XML source does not exist: %s" %
            xml_file)

    try:
        parser = etree.XMLParser(remove_blank_text=False)
        x = etree.parse(infile, parser)
    except etree.XMLSyntaxError, e:
        module.fail_json(
            msg="Error while parsing file: %s" %
            str(e))

    modify_property(x, xpath, value, module, ns)

from ansible.module_utils.basic import *
main()
