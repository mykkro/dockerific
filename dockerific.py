import yaml
import os


class Action(object):
    def __init__(self, title=None):
        self.title = title

    def dockerify(self):
        return f"# {self.title}\n" if self.title is not None else ""

class EnvAction(Action):
    def __init__(self, var, value, title=None):
        super().__init__(title=title)
        self.var = var
        self.value = value

    def dockerify(self):
        return super().dockerify() + f"ENV {self.var}={self.value}"

class ArgAction(Action):
    def __init__(self, var, value, title=None):
        super().__init__(title=title)
        self.var = var
        self.value = value

    def dockerify(self):
        return super().dockerify() + f"ARG {self.var}={self.value}"

class CopyAction(Action):
    def __init__(self, src, tgt, title=None):
        super().__init__(title=title)
        self.src = src
        self.target = tgt

    def dockerify(self):
        return super().dockerify() + f"COPY {self.src} {self.target}"

class WorkdirAction(Action):
    def __init__(self, workdir, title=None):
        super().__init__(title=title)
        self.workdir = workdir

    def dockerify(self):
        return super().dockerify() + f"WORKDIR {self.workdir}"

class BashAction(Action):
    def __init__(self, commands=None, title=None):
        super().__init__(title=title)
        self.commands = commands

    def dockerify(self):
        return super().dockerify() + f'CMD ["/bin/bash", "-c" ]'


class CommentAction(Action):
    def __init__(self, title=None):
        super().__init__(title=title)

    def dockerify(self):
        return super().dockerify() + "\n".join([f"# {line}" for line in (self.title or '').split("\n")])
        

class AptAction(Action):
    def __init__(self, pkgs, upgrade=False, title=None):
        super().__init__(title=title)
        self.pkgs = pkgs
        self.upgrade = upgrade

    def dockerify(self):
        out = ["RUN apt-get update &&"]
        if self.upgrade:
            out.append("apt-get upgrade -y &&")
        out.append("apt-get install -y")
        out += self.pkgs

        return super().dockerify() + " \\\n    ".join(out)

class GitAction(Action):
    def __init__(self, url, target, branch=None, depth=None, title=None):
        super().__init__(title=title)
        self.url = url
        self.target = target
        self.branch = branch
        self.depth = depth
        self.title = title

    def dockerify(self):
        out = [f"RUN mkdir -p {self.target} &&", "git clone"]
        if self.branch is not None:
            out.append(f"-b {self.branch}")
        if self.depth is not None:
            out.append(f"--depth {self.depth}")
        out.append(self.url)
        out.append(self.target)

        return super().dockerify() + " \\\n    ".join(out)

class AppendAction(Action):
    def __init__(self, file, items, title=None):
        super().__init__(title=title)
        self.file = file
        self.items = items
        self.title = title

    def dockerify(self):
        out = [f'RUN echo "{it}" >> {self.file}' for it in self.items]
        return super().dockerify() + "\n".join(out)


class RunAction(Action):
    def __init__(self, cmd, title=None):
        super().__init__(title=title)
        self.cmd = cmd

    def dockerify(self):
        return super().dockerify() + f"RUN {self.cmd}"

class PutAction(Action):
    # put a file into local filesystem; path is relative to projectdir
    def __init__(self, path, contents, title=None):
        super().__init__(title=title)
        self.path = path
        self.contents = contents


class Dockerific(object):
    def __init__(self, name, version, base_image, build_actions, project_dir):
        self.name = name
        self.version = version
        self.base_image = base_image
        self.build_actions = build_actions
        self.project_dir = project_dir

    @staticmethod
    def from_dict(d, project_dir):
        type = d["$type"]
        assert(type == "cz.mykkro.dockerific")
        version = d["$version"]
        assert(version == "1.0")
        base_image = d["base"]
        build_actions = [Dockerific.parse_action(b, project_dir) for b in d["build"]]
        return Dockerific(d["name"], d["version"], base_image, build_actions, project_dir)
    
    @staticmethod
    def parse_action(b, project_dir):
        if "bash" in b:
            return BashAction(b["bash"], title=b.get("title"))
        if "put" in b:
            act = PutAction(b["to"], b["contents"], title=b.get("title"))
            path = os.path.join(project_dir, b["to"])
            with open(path, "w", encoding="utf-8") as outfile:
                outfile.write(b["contents"])
            return act
        if "env" in b:
            return EnvAction(b["env"], b["value"], title=b.get("title"))
        if "workdir" in b:
            return WorkdirAction(b["workdir"], title=b.get("title"))
        if "arg" in b:
            return ArgAction(b["arg"], b["value"], title=b.get("title"))
        if "copy" in b:
            return CopyAction(b["src"], b["tgt"], title=b.get("title"))
        if "apt" in b:
            return AptAction(b["pkgs"], upgrade=b.get("upgrade", False), title=b.get("title"))
        if "run" in b:
            return RunAction(b["run"])
        if "git" in b:
            return GitAction(b["git"], b["to"], branch=b.get("branch"), depth=b.get("depth"), title=b.get("title"))
        if "append" in b:
            return AppendAction(b["to"], b["add"], title=b.get("title"))
        assert(False)

    def dockerify(self):
        return f"FROM {self.base_image}\n" + "\n".join([b.dockerify() for b in self.build_actions])
    
    def build_command(self):
        return f"docker build -t \"{self.name}:v{self.version}\" ."


def load_dockerific_project(project_path):

    with open(f"{project_path}/dockerific.yaml", 'r', encoding="utf-8") as infile:
        data = yaml.safe_load(infile)

    return Dockerific.from_dict(data, project_path)
