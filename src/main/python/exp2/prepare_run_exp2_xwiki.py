import sys

import os
from os import listdir

SCRIPT_DIR = os.path.abspath('./src/main/python/utils/')
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.cmd.git_cmd import *
from utils.cmd.io_cmd import *
from utils.cmd.mvn_cmd import *
from utils.cmd.json_cmd import *
from utils.constants import *
from utils.args.run_exp2_args import *
from utils.utils import *
from utils.statitics import *

import clone

from xml.dom import minidom

if __name__ == '__main__':
    
    modules = [
        '/tmp/v1',
        '/tmp/v1/xwiki-commons-tools',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-verification-resources',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-pom',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-remote-resource-plugin',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-license-resources',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-enforcers',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-enforcers/xwiki-commons-tool-enforcer-dependencies',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-spoon',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-spoon/xwiki-commons-tool-spoon-checks',
        '/tmp/v1/xwiki-commons-pom',
        '/tmp/v1/xwiki-commons-core',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-test',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-test/xwiki-commons-tool-test-simple',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-stability',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-text',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-component',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-component/xwiki-commons-component-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-observation',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-observation/xwiki-commons-observation-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-component/xwiki-commons-component-observation',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-component/xwiki-commons-component-default',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-context',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-configuration',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-configuration/xwiki-commons-configuration-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-environment',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-environment/xwiki-commons-environment-api',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-test/xwiki-commons-tool-test-component',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-blame',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-blame/xwiki-commons-blame-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-logging',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-logging/xwiki-commons-logging-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-diff',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-diff/xwiki-commons-diff-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-diff/xwiki-commons-diff-display',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-script',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-blame/xwiki-commons-blame-script',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-cache',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-cache/xwiki-commons-cache-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-cache/xwiki-commons-cache-tests',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-cache/xwiki-commons-cache-infinispan',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-classloader',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-classloader/xwiki-commons-classloader-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-collection',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-component/xwiki-commons-component-archetype',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-common',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-cipher',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-password',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-signer',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-pkix',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-store',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-store/xwiki-commons-crypto-store-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-crypto/xwiki-commons-crypto-store/xwiki-commons-crypto-store-filesystem',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-xml',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-diff/xwiki-commons-diff-xml',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-diff/xwiki-commons-diff-script',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-displayer',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-environment/xwiki-commons-environment-common',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-environment/xwiki-commons-environment-standard',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-environment/xwiki-commons-environment-servlet',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-properties',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-xstream',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-logging/xwiki-commons-logging-common',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-observation/xwiki-commons-observation-local',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-job',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-job/xwiki-commons-job-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-job/xwiki-commons-job-default',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-logging/xwiki-commons-logging-logback',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-maven',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-handlers',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-handlers/xwiki-commons-extension-handler-jar',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-repositories',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-repositories/xwiki-commons-extension-repository-http',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-repositories/xwiki-commons-extension-repository-maven',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-repository',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-repository/xwiki-commons-repository-model',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-repository/xwiki-commons-repository-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-repositories/xwiki-commons-extension-repository-xwiki',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-extension/xwiki-commons-extension-repositories/xwiki-commons-extension-repository-maven-snapshots',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter/xwiki-commons-filter-api',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter/xwiki-commons-filter-xml',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter/xwiki-commons-filter-test',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter/xwiki-commons-filter-events',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter/xwiki-commons-filter-events/xwiki-commons-filter-event-extension',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter/xwiki-commons-filter-streams',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-filter/xwiki-commons-filter-streams/xwiki-commons-filter-stream-xml',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-groovy',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-management',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-websocket',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-netflux',
        '/tmp/v1/xwiki-commons-core/xwiki-commons-velocity',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-archiver',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-extension-plugin',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-spoon/xwiki-commons-tool-spoon-tests',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-webjar-handlers',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-xar',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-xar/xwiki-commons-tool-xar-plugin',
        '/tmp/v1/xwiki-commons-tools/xwiki-commons-tool-xar/xwiki-commons-tool-xar-handlers',
    ]
    
    coverage_per_module_path = {}
    
    for module in modules:
        if not isfile(module + '/target/clover/clover.db') or not os.path.isdir(module + '/src/main/java') or not os.path.isdir(module + '/src/test/java'):
            print('skipping', module)
            continue
        print('running', module)
        mvn_diff_jjoules_coverage(module)
        coverage_per_module_path[module] = read_json(module + '/' + 'clover_coverage.json')

    write_json('/home/benjamin/workspace/diff-jjoules-experiment/coverage_per_module.json', coverage_per_module_path)