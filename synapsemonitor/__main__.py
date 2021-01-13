#!/usr/bin/env python
"""Command line client"""
import argparse

import synapseclient

from . import monitor, update_activity_feed


def monitor_cli(syn, args):
    """Monitor cli"""
    monitor.main(syn, args.projectid,
                 userid=args.userid, email_subject=args.email_subject,
                 days=args.days, update_project=args.update_project)


def update_activity_feed_cli(syn, args):
    """Update activity cli"""
    update_activity_feed.main(syn, args.projectid,
                              delta_time=args.interval,
                              earliest_time=args.earliest_time,
                              wiki=args.wiki)


def build_parser():
    """Set up argument parser and returns"""
    parser = argparse.ArgumentParser(
        description='Checks for new/modified entities in a project.'
    )
    parser.add_argument(
        '-c', '--synapse_config', metavar='file', type=str,
        help='Synapse config file with user credentials '
             '(overrides default ~/.synapseConfig)'
    )

    subparsers = parser.add_subparsers(
        title='commands',
        description='The following commands are available:',
        help='For additional help: "synapsemonitor <COMMAND> -h"'
    )
    parser_monitor = subparsers.add_parser(
        'monitor',
        help='Monitor a Synapse Project'
    )
    parser_monitor.add_argument(
        'projectid', metavar='projectid', type=str,
        help='Synapse ID of project to be monitored.'
    )
    parser_monitor.add_argument(
        '--userid',
        help='User Id of individual to send report, defaults to current user.'
    )
    parser_monitor.add_argument(
        '--email_subject',
        default='New Synapse Files',
        help='Sets the subject heading of the email sent out '
             '(defaults to New Synapse Files)'
    )
    parser_monitor.add_argument(
        '--days', '-d', metavar='days', type=float, default=None,
        help='Find modifications in the last days'
    )
    parser_monitor.add_argument(
        '--update_project', action='store_true',
        help='If set will modify the annotations by setting '
             'lastAuditTimeStamp to the current time on each project.')
    parser_monitor.set_defaults(func=monitor_cli)

    parser_update = subparsers.add_parser(
        'update_activity',
        help='Looks for changes to project in defined time ranges and '
             'updates a wiki'
    )
    parser_update.add_argument(
        'projectid', help='Synapse ID of project to be monitored.'
    )
    parser_update.add_argument(
        '--wiki', '-w', type=str,
        help='Optional sub-wiki id where to store change-log '
             '(defaults to project wiki)'
    )
    parser_update.add_argument(
        '-i', '--interval',
        choices=['week', 'month'], default='week',
        help='divide changesets into either "week" or "month" long intervals '
             '(defaults to week)'
    )
    parser_update.add_argument(
        '--earliest', '-e', metavar='date', dest='earliest_time',
        type=str, default='1-Jan-2014',
        help='The start date for which changes will be searched '
             '(defaults to 1-January-2014)'
    )
    parser_update.set_defaults(func=update_activity_feed_cli)

    return parser


def synapse_login(synapse_config=None):
    if synapse_config is not None:
        syn = synapseclient.Synapse(skip_checks=True,
                                    configPath=synapse_config)
    else:
        syn = synapseclient.Synapse(skip_checks=True)
    syn.login(silent=True)
    return syn


def main():
    args = build_parser().parse_args()
    syn = synapse_login(synapse_config=args.synapse_config)
    args.func(syn, args)


if __name__ == "__main__":
    main()
