#!/usr/bin/env python3

import builder


class SparkDockerImageBuilder(builder.DockerImageBuilder):

    def _get_version_name(self):
        return "{}".format(self._parsed_args['spark_version'])

    def _get_folder(self):
        return "spark"


if __name__ == '__main__':
    image_builder = SparkDockerImageBuilder('undeadpixel', 'chempack-spark', ['spark_version', 'chempack_version'])
    image_builder.build()

