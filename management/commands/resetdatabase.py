import glob, subprocess
from pathlib import Path
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	help = "Clear the database and all migrations"

	def add_arguments(self, parser):
		res = super(Command, self).add_arguments(parser)
		parser.add_argument(
			"--loaddata", help="Load data from json files in the enterd path"
		)
		parser.add_argument(
			"--run-server", help="Run server on the giving IP:PORT after finishing the command"
		)
		return res

	def handle(self, *args, **options):
		for file_name in glob.glob("*/migrations/[!__init__.py]*", recursive=True):
			Path(file_name).unlink()
			db_path = glob.glob("db.sqlite3", recursive=True)
			if db_path:
				Path(db_path[0]).unlink()
		subprocess.run(["python", "manage.py", "makemigrations"])
		subprocess.run(["python", "manage.py", "migrate"])
		if options.get("loaddata"):
			data_path = options["loaddata"]
			for file_name in glob.glob(f"{data_path}/*", recursive=True):
				file_path = str(Path(file_name))
				subprocess.run(["python", "manage.py", "loaddata", file_path])
		if options.get("run_server"):
			ip_port = options["run_server"]
			try:
				subprocess.run(["python", "manage.py", "runserver", ip_port])
			except KeyboardInterrupt:
				return