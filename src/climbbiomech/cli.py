import typer

def main(fname: str, lname: str = "", formal: bool = False):
	"""
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
	if formal:
		if lname == "":
			print("ERROR: Please input last name")
		else:
			print(f"Hello Mr.{lname}!")
	else:
		print(f"Hello {fname} {lname}!")

if __name__ == "__main__":
    typer.run(main)