#!/usr/bin/env python3

import builder

class ChemPackDockerImageBuilder(builder.DockerImageBuilder):

    def _get_version_name(self):
         return "java{}-python{}-r{}-rdkit{}".format(self._parsed_args['java_version'], self._parsed_args['python_version'], self._parsed_args['r_version'], self._parsed_args['rdkit_release'])

    def _get_folder(self):
        return "base"


if __name__ == '__main__':
    image_builder = ChemPackDockerImageBuilder('undeadpixel', 'chempack', ['python_version', 'java_version', 'r_version', 'rdkit_release'])
    image_builder.build()

