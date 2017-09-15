#!/usr/bin/env python3

import builder


class ZeppelinDockerImageBuilder(builder.DockerImageBuilder):

    def _get_version_name(self):
        return "{}".format(self._parsed_args['zeppelin_version'])

    def _get_folder(self):
        return "zeppelin"


if __name__ == '__main__':
    image_builder = ZeppelinDockerImageBuilder('undeadpixel', 'chempack-zeppelin', ['zeppelin_version', 'chempack_spark_version'])
    image_builder.build()

