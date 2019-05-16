import typing
from io import StringIO

import ruamel.yaml


def yaml_comments(text: str, stream_mark: bool = False) -> list:
    from ruamel.yaml.error import CommentMark, StreamMark
    from ruamel.yaml.tokens import CommentToken

    if text[-1] == "\n":
        text = text[:-1]

    if stream_mark:
        mark = StreamMark(name="", index=0, line=0, column=0)
    else:
        mark = CommentMark(0)
    return [
        CommentToken(f"# {s}\n" if s else "\n", mark, None) for s in text.split("\n")
    ]


class YAMLGenerator:
    def __init__(self, filename):
        self.config_file = open(filename, "w")
        self.yaml = ruamel.yaml.YAML()
        self.yaml_data = self.yaml.load("{}")
        self.yaml_data._yaml_get_pre_comment()  # Initialize comment areas.
        self.first_comments = ""

    def add(self, key: str, initial: typing.Any, help: typing.Optional[str]):
        existing = bool(self.yaml_data)
        self.yaml_data[key] = initial
        if self.yaml_data.ca.end:
            before = self.yaml_data.ca.end
            self.yaml_data.ca.end = []
        else:
            before = []
        if existing or self.first_comments:
            before.extend(yaml_comments(f"\n{help}" if help else "\n"))
        elif help:
            before.extend(yaml_comments(help))
        bits = self.yaml_data.ca.items.setdefault(key, [None, None, None, None])
        bits[1] = before
        self.save()

    def add_commented(self, key: str, default: typing.Any, help: typing.Optional[str]):
        from easyconf.config import REQUIRED

        if default is REQUIRED:
            return

        comment = StringIO()
        if help:
            comment.write(f"{help}\n")
        self.yaml.dump({key: default}, comment)
        comment = comment.getvalue()

        if not self.yaml_data:
            if self.first_comments:
                comment = f"{self.first_comments}\n{comment}"
            self.yaml_data.ca.comment[1] = yaml_comments(comment)
            self.first_comments = comment
        else:
            self.yaml_data.ca.end.extend(
                yaml_comments(f"\n{comment}", stream_mark=True)
            )

        self.save()

    def save(self):
        self.config_file.seek(0)
        self.yaml.dump(self.yaml_data, self.config_file)
        # Dumping appends the ca.end to the comment map for some reason,
        # so remove it again. Otherwise the second dump will fail
        # miserably.
        self.yaml_data.ca.comment.pop()
        self.config_file.flush()
