#!/usr/bin/python3

import argparse
import subprocess
import os
from pathlib import Path

bwrap_arg_list = []

BREWENV_PREFIX = str(
    Path(os.environ.get('HOME')).joinpath(".brewenv/linuxbrew"))
HIER_NECESSARY_BIND = ["/usr", "/bin", "/lib", "/lib64"]
USER_NECESSARY_BIND = [os.environ.get('HOME')]
BASIC_SANDBOX_BIND = ["/etc/passwd",
                      "/etc/resolv.conf", "/etc/pki/", "/etc/ca-certificates",
                      "/etc/alternatives", "/etc/man_db.conf"]
BWRAP_COMMAND = ["/bin/bash", "-c",
                 "eval \"$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)\"; \
                  export PS1=\"(brewenv)[\\u@\h \W]\$ \" ; \
                  export HOMEBREW_INSTALL_FROM_API=1 ; \
                  export HOMEBREW_NO_ANALYTICS=1 ; "]

for p in HIER_NECESSARY_BIND:
    bwrap_arg_list.append("--ro-bind")
    bwrap_arg_list.append(p)
    bwrap_arg_list.append(p)

if True:
    for p in USER_NECESSARY_BIND:
        bwrap_arg_list.append("--bind")
        bwrap_arg_list.append(p)
        bwrap_arg_list.append(p)


def check_bind_and_append(bind_arg, path_list):
    for p in path_list:
        if os.path.exists(p):
            bwrap_arg_list.append(bind_arg)
            bwrap_arg_list.append(p)
            bwrap_arg_list.append(p)


def add_brew_arg():
    bwrap_arg_list.append("--bind")
    bwrap_arg_list.append(BREWENV_PREFIX)
    bwrap_arg_list.append("/home/linuxbrew/.linuxbrew")


def add_basic_sandbox_arg():
    bwrap_arg_list.extend(
        ["--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-user"])
    check_bind_and_append("--ro-bind", BASIC_SANDBOX_BIND)


def brew_exec(command: list = ["bash"]):
    #basic_sandbox_bind.append(subprocess.run(["tty"], capture_output=True).stdout[:-1])
    add_basic_sandbox_arg()
    add_brew_arg()
    # check_bind_and_append("--ro-bind","/etc")

    #os.environ["PS1"] = "(brewenv)[\\u@\h \W]\$ "
    bwrap_args = ["bwrap"]+bwrap_arg_list+BWRAP_COMMAND
    if command == []:
        command = ["bash"]
    for item in command:
        bwrap_args[-1] = bwrap_args[-1] + " " + item
    if os.environ.get('BREWENV_DEBUG') == '1':
        print(bwrap_args)
    proc = subprocess.Popen(bwrap_args)
    proc.wait(timeout=None)


def subcommand_exec(args):
    brew_exec(args.command)


def subcommand_bash(args):
    brew_exec()


def subcommand_install(args):
    Path(BREWENV_PREFIX).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "https://github.com/Homebrew/brew", BREWENV_PREFIX])
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='brewenv.py', description="A helper program using bwarp for installing and running linuxbrew rootlessly.")
    subparsers = parser.add_subparsers(
        help='sub-command', dest='subparser_name')

    parser_exec = subparsers.add_parser(
        'exec', help='exec command with linuxbrew')
    parser_exec.add_argument(
        metavar='COMMAND', nargs='*', dest="command", type=str, help='the command to execute')
    parser_exec.set_defaults(func=subcommand_exec)

    parser_bash = subparsers.add_parser(
        'bash', help='exec bash with linuxbrew')
    parser_bash.set_defaults(func=subcommand_bash)

    parser_bash = subparsers.add_parser(
        'install', help='exec bash with linuxbrew')
    parser_bash.set_defaults(func=subcommand_install)

    args = parser.parse_args()
    if args.subparser_name:
        args.func(args)
    else:
        args = parser.parse_args(["-h"])

    # subcommand_exec()
    #parser = argparse.ArgumentParser(prog='PROG')
