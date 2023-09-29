from pathlib import Path

path_strings = [
    "/data/jonathan_ng/elk-reporters/lucid-nightingale",
    "/data/jonathan_ng/elk-reporters/lucid-kalam",
    "/data/jonathan_ng/elk-reporters/distracted-hellman",
    "/data/jonathan_ng/elk-reporters/goofy-tesla",
    "/data/jonathan_ng/elk-reporters/pensive-noether",
    "/data/jonathan_ng/elk-reporters/trusting-hoover"
]

new_folder = Path("./noreps")
new_folder.mkdir(exist_ok=True, parents=True)
for s in path_strings:
    path = Path(s)

    for file in ['eval.csv', 'cfg.yaml']:
        new_path = new_folder / path.stem
        new_path.mkdir(exist_ok=True, parents=True)
        with open(new_path / file, "a+") as f:
            with open(path / file, "r") as f2:
                f.write(f2.read())



