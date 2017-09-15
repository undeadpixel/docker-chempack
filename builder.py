
import argparse
import subprocess as sp

# builds and pushes an image for both python 2 and 3 with the args specified

def run(cmd):
    result = sp.run(cmd, shell=True)
    result.check_returncode()

class DockerImageBuilder(object):

    def __init__(self, user, name, args):
        self._user = user
        self._name = name
        self._args = args

        self._create_arg_parser()

        self._folder = "."
        self._parsed_args = {}

    def build(self):
        self._parse_args()
        self._create_image()

    def _create_arg_parser(self):
        self._parser = argparse.ArgumentParser(description="Build one {}/{} image.".format(self._user, self._name))
        for arg in self._args:
            self._parser.add_argument('--{}'.format(arg), required=True)

        self._parser.add_argument('--additional-tags', nargs='*')

    def _parse_args(self):
        self._parsed_args = vars(self._parser.parse_args())
        if not self._parsed_args['additional_tags']:
            self._parsed_args['additional_tags'] = []

    def _get_folder(self):
        return "."

    def _create_image(self):
        version_name = self._get_version_name()
        image_name = self._get_image_name(version_name)

        # docker build
        cmd = "docker build {} -t {}".format(self._get_folder(), image_name)
        for tag in self._parsed_args['additional_tags']:
            cmd += " -t {}".format(self._get_image_name(tag))

        for arg in self._args:
            cmd += " --build-arg {}={}".format(arg.upper(), self._parsed_args[arg])
        self._print_notice("Building")
        status = run(cmd)

        # docker push
        self._print_notice("Pushing")
        run("docker push {}".format(image_name))
        for tag in self._parsed_args['additional_tags']:
            run("docker push {}".format(self._get_image_name(tag)))

    def _get_image_name(self, version):
        return "{}/{}:{}".format(self._user, self._name, version)

    # should override in child classes
    def _get_version_name(self):
        version_items = []
        for arg in self._args:
            val = self._parsed_args[arg]
            version_items.append("{}{}".format(arg, val))
        return "_".join(version_items)

    def _print_notice(self, msg):
        print("-"*len(msg))
        print(msg)
        print("-"*len(msg))

