import subprocess
from datetime import datetime
from typing import List

import click
from more_itertools import flatten


@click.group()
def main():
    pass


@main.command()
@click.argument('source', required=True)
@click.argument('destination', required=True)
@click.option('-D', '--dedup', is_flag=True, help='Generate a deduplicated stream')
@click.option('-L', '--large-block', is_flag=True, help='Generate a stream which may contain blocks largeth than 128KB')
@click.option('-e', '--embed', is_flag=True, help='Generate a more compact stream by using WRITE_EMBEDDED records for blocks which are stored more compactly on disk by the embedded_data pool feature.')
@click.option('-c', '--compressed', is_flag=True, help='Generate a more compact stream by using compressed WRITE records for blocks which are compressed on disk and in memory')
@click.option('-p', '--props', is_flag=True, help='Include the dataset\'s properties in the stream.')
@click.option('-T', '--to', type=str, help='Destination host.')
def send(source: str, destination: str, dedup: bool, large_block: bool,
         embed: bool, compressed: bool, props: bool, to: str):
    pass



@main.command()
@click.argument('tag', type=str, required=True)
@click.argument('datasets', required=True, nargs=-1)
@click.option('-r', '--recursive', is_flag=True, help='Recursivly snapshot dataset(s)')
@click.option('-o', '--option', multiple=True, help='Snapshot options to add')
@click.option('-n', '--dry-run', is_flag=True, help='Just print the commands that would be run')
def snapshot(tag: str, datasets: List[str], recursive: bool, option: List[str],
             dry_run: bool):
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d-%H%M-%S')
    snapshots = list()
    for dataset in datasets:
        snapshots.append("{dataset}@{timestamp}-{tag}".format(
            dataset=dataset, timestamp=timestamp, tag=tag))
    command = ["zfs", "snapshot"]
    if recursive:
        command.append("-r")
    command.extend(flatten(map(lambda opt: ["-o", opt], option)))
    command.extend(snapshots)
    if dry_run:
        click.echo(" ".join(command))
    else:
        subprocess.call(command)
