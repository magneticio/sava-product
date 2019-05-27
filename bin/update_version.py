import getopt
import json
import re
import sys
from pathlib import Path


def main(argv):
    service_definition_file_path, tag = parse_options(argv)
    validate_tag(tag)
    json = read_json(service_definition_file_path)
    updated_json = update_version(json, tag)
    save_updated_json(service_definition_file_path, updated_json)


def parse_options(argv):
    try:
        opts, _ = getopt.getopt(argv, 'hf:t:', ['filePath=', 'tag='])
    except getopt.GetoptError:
        print('Usage: update_version.py -f <filePath> -t <tag>')
        sys.exit(1)

    service_definition_file_path = ''
    tag = ''
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: update_version.py -f <filePath> -t <tag>')
            sys.exit()
        elif opt in ('-f', '--filePath'):
            service_definition_file_path = arg.strip()
        elif opt in ('-t', '--tag'):
            tag = arg.strip()
    if service_definition_file_path == '':
        print('File path cannot be empty')
        sys.exit(1)
    if tag == '':
        print('Tag cannot be empty')
        sys.exit(1)
    return service_definition_file_path, tag


def validate_tag(tag):
    semantic_version_regex = '^(\d+)\.(\d+)\.(\d+)$'
    pattern = re.compile(semantic_version_regex)
    if None == pattern.match(tag):
        print('Tag not in semantic versioning format')
        sys.exit(1)


def read_json(service_definition_file_path):
    service_definition_file = Path(service_definition_file_path)
    if False == service_definition_file.is_file():
        print('Service definition file does not exist: {}'.format(
            service_definition_file_path))
        sys.exit(1)

    with open(service_definition_file_path, encoding='utf-8') as json_file:
        return json.load(json_file)


def update_version(json, tag):
    if None == json.get('versions') or len(json['versions']) == 0:
        json['versions'] = [{'tag': tag, 'dependencies': []}]
        return json

    versions = json['versions']
    if any(entry['tag'] != None and entry['tag'] == tag for entry in versions):
        print('Tag already exists')
        return json
    if len(versions) > 0:
        index, latest_version = search_latest_version(versions, tag)
        new_version = latest_version.copy()
        new_version['tag'] = tag
        versions.insert(index, new_version)
        return json


def search_latest_version(versions, tag):
    versions_copy = versions.copy()

    def get_tag(e):
        return e['tag']

    versions_copy.sort(key=get_tag)

    latest_version = None
    index = 0
    for current_version in versions_copy:
        if current_version['tag'] < tag:
            latest_version = current_version
            index += 1
            continue
        break

    if None == latest_version:
        return index, {'tag': tag, 'dependencies': []}

    return index, latest_version


def save_updated_json(service_definition_file_path, updated_json):
    with open(service_definition_file_path, 'w') as outfile:
        json.dump(updated_json, outfile, indent=4)


if __name__ == '__main__':
    main(sys.argv[1:])
