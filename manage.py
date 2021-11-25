import sys
import argparse


parser = argparse.ArgumentParser(description="Panda Manager")

if len(sys.argv) == 1:
    print("Missing commands. Use python3 manage.py -h for help")

parser.add_argument("-r", "--run-server", metavar="",
                    help="Start Panda Server", nargs="?", const="")


args = parser.parse_args()

if args.run_server is not None:
    import server
    c = server.Server
    c.run()
