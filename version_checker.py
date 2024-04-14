from asyncio.subprocess import create_subprocess_shell
from subprocess import PIPE

async def _read_commits() -> dict[str,str]:
	process = await create_subprocess_shell('git log --pretty=oneline',stdout=PIPE)
	commits = reversed((await process.stdout.read()).decode().splitlines())
	return {commit.split(' ',1)[0]:commit.split(' ',1)[1] for commit in commits}

async def _find_start_commit(
	commits:dict[str,str],
	start_commit:str
) -> dict[str,str]:
	if not start_commit: return commits
	for commit in commits.copy():
		if commit == start_commit:
			del commits[commit]
			break
		del commits[commit]
	else:
		raise ValueError('start commit not found')
	return commits

def calculate_version(
	commits:dict[str,str],
	start_version:list[int]
) -> list[int]:
	version = start_version
	for message in commits.values():
		match message.strip().lower()[:6]:
			case 'major;'  : version = [version[0]+1,0,0]
			case 'minor;'  : version = [version[0],version[1]+1,0]
			case 'patch;'|_: version[2] += 1
	return version

async def get_semantic_version(
	start_commit:str=None,
	start_version:list[int]=[0,0,0]
) -> str:
	commits = await _read_commits()
	filtered_commits = await _find_start_commit(commits,start_commit or '')
	version = calculate_version(filtered_commits,start_version)
	return '.'.join([str(v) for v in version])

if __name__ == '__main__':
	from asyncio import run
	print(run(get_semantic_version()))